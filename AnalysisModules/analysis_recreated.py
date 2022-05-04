from HyperGuiModules.utility import *
import logging
import numpy as np
from scipy.ndimage.filters import gaussian_filter, median_filter
import cv2
from scipy.ndimage import gaussian_filter1d
np.set_printoptions(threshold=sys.maxsize)


class RecreatedAnalysis:
    # performs analyses necessary for recreated image
    def __init__(self, path, data_cube, wavelength, params, listener, mask=None):

        self.listener = listener

        # inputs
        self.path = path
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = wavelength
        self.absorbance = False
        self.normal = False
        self.negative = False

        # params
        self.R1 = params[0]
        self.R2 = params[1]
        self.S1 = params[2]
        self.S2 = params[3]
        self.T1 = params[4]
        self.T2 = params[5]
        self.U1 = params[6]
        self.U2 = params[7]

        # calculated generally
        self.x1 = None
        self.x2 = None
        self.x_absorbance = None
        self.x_reflectance = None
        self.x_absorbance_w = None
        self.x_reflectance_w = None
        self.x_absorbance_masked = None
        self.x_absorbance_masked_w = None
        self.x_reflectance_masked = None
        self.x_reflectance_masked_w = None

        # specific to module
        self.rgb = None
        self.sto2 = None
        self.sto2_masked = None
        self.nir = None
        self.nir_masked = None
        self.thi = None
        self.thi_masked = None
        self.twi = None
        self.twi_masked = None
        self.tli = None
        self.tli_masked = None
        self.ohi = None
        self.ohi_masked = None

        self._x_absorbance_gradient = None
        self._x_absorbance_gradient_min_1 = None
        self._x_absorbance_gradient_min_2 = None
        self._x_absorbance_min_570_590 = None
        self._x_absorbance_min_740_780 = None
        self._x_absorbance_mean_825_925 = None
        self._x_absorbance_mean_655_735 = None
        self._x_absorbance_mean_530_590 = None
        self._x_absorbance_mean_785_825 = None
        self._x_absorbance_mean_880_900 = None
        self._x_absorbance_mean_955_980 = None

        self._x_reflectance_gradient = None
        self._x_reflectance_gradient_min_1 = None
        self._x_reflectance_gradient_min_2 = None
        self._x_reflectance_min_570_590 = None
        self._x_reflectance_min_740_780 = None
        self._x_reflectance_mean_825_925 = None
        self._x_reflectance_mean_655_735 = None
        self._x_reflectance_mean_530_590 = None
        self._x_reflectance_mean_785_825 = None
        self._x_reflectance_mean_880_900 = None
        self._x_reflectance_mean_955_980 = None
        self.analysis()
        
    def get_rgb(self):
        return self.rgb
    def get_sto2(self):
        return self.sto2
    def get_nir(self):
        return self.nir
    def get_thi(self):
        return self.thi
    def get_ohi(self):
        return self.ohi
    def get_tli(self):
        return self.tli
    def get_twi(self):
        return self.twi

    def analysis(self):
        self.__setup()
        self._calc_general()
        self._calc_sto2()
        self._calc_nir()
        self._calc_thi()
        self._calc_twi()
        self._calc_tli()
        self._calc_ohi()
        self._calc_rgb()
        self._detect_background()

    # --------------------------------------------------- UPDATERS ----------------------------------------------------

    def update_mask(self, new_mask):
        self.mask = new_mask
        self.analysis()

    def update_wavelength(self, new_wavelength):
        self.wavelength = new_wavelength
        self.analysis()

    def update_normal(self, new_normal):
        self.normal = new_normal
        self.analysis()

    def update_absorbance(self, new_absorbance):
        self.absorbance = new_absorbance
        self.analysis()

    # ------------------------------------------------- CALCULATORS --------------------------------------------------
        
    def _calc_rgb(self, LUT_gamma=0, minWL=500, maxWL=995, WLsteps=5, cube_index=None, RGB_image=None, scanning='horizontal'):
        blue_range_start = int((530 - minWL) / WLsteps)
        blue_range_end = int((560 - minWL) / WLsteps)
        green_range_start = int((540 - minWL) / WLsteps)
        green_range_end = int((590 - minWL) / WLsteps)
        red_range_start = int((585 - minWL) / WLsteps)
        red_range_end = int((725 - minWL) / WLsteps)
        factor = 1.02 * 255 * 1.5  # like in RGB-Image 1.5.vi
        if cube_index is None:
            RGB_image = np.zeros((self.data_cube.shape[0], self.data_cube.shape[1], 3), dtype=np.float)
            # for blue pixel take the 530-560nm
            RGB_image[:, :, 2] = self.data_cube[:, :, blue_range_start:blue_range_end].mean(axis=2)
            # for the green pixel take 540-590nm
            RGB_image[:, :, 1] = self.data_cube[:, :, green_range_start:green_range_end].mean(axis=2)
            # for the red pixel take 585-725nm
            RGB_image[:, :, 0] = self.data_cube[:, :, red_range_start:red_range_end].mean(axis=2)
            # scale to 255
            RGB_image = np.clip((RGB_image * factor), 0, 255).astype(np.uint8)
            #cv2.LUT(RGB_image, LUT_gamma, dst=RGB_image)  # apply gamma correction
            #RGB_image = np.rot90(RGB_image, k=1, axes=(0, 1))
            self.rgb = np.rot90(np.rot90(np.rot90(RGB_image)))
        else:
            RGB_line = np.zeros((cube.shape[0], 3), dtype=np.float)
            # for blue pixel take the 530-560nm
            RGB_line[:, 2] = self.data_cube[:, blue_range_start:blue_range_end].mean(axis=1)
            # for the green pixel take 540-590nm
            RGB_line[:, 1] = self.data_cube[:, green_range_start:green_range_end].mean(axis=1)
            # for the red pixel take 585-725nm
            RGB_line[:, 0] = self.data_cube[:, red_range_start:red_range_end].mean(axis=1)
            # scale to 255
            RGB_line = np.clip((RGB_line * factor), 0, 255).astype(np.uint8)
            #cv2.LUT(RGB_line, LUT_gamma, dst=RGB_line)  # apply gamma correction
            if scanning == 'horizontal':    # horizontal scanning (left2right)
                RGB_image[:, cube_index, :] = RGB_line[::-1]
            else:   # vertical scanning (bottom2top)
                RGB_image[cube_index, :, :] = RGB_line[::-1]
            self.rgb = np.rot90(np.rot90(np.rot90(RGB_image)))

    def _calc_sto2(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None):
        # gaussian window for smoothing
        sigma = 2.66  # to be definded
        first_range_start = int(round((573 - minWL) / WLsteps))
        first_range_end = int(round((587 - minWL) / WLsteps))
        second_range_start = int(round((740 - minWL) / WLsteps))
        second_range_end = int(round((780 - minWL) / WLsteps)) + 1  # !!! should be changed for diff WL steps
        if cube_index is None:
            smoothed_cube = gaussian_filter1d(self.data_cube, sigma, axis=2)
            # cube = convolve1d(cube, gaussFkt, axis=2, origin=0)
            first_derivative = np.gradient(smoothed_cube, axis=2)
            second_derivative = np.gradient(first_derivative, axis=2)
            # calculate min of 2nd derivative between 573 and 587 nm
            min_value = second_derivative[:, :, first_range_start:first_range_end].min(axis=2)
            # calculate diff of mean and max of 2nd derivative between 740 and 780 nm
            max_value = second_derivative[:, :, second_range_start:second_range_end].max(axis=2)
            mean_value = second_derivative[:, :, second_range_start:second_range_end].mean(axis=2)
            # calculate parameter from range subresults
            sub1 = (min_value / 0.2)
            sub2 = ((mean_value - max_value) / (-0.03)) + sub1
            sub3 = ((sub1 / sub2) * 0.6) + 0.4
            sto2_image = np.exp(sub3) - 1.48
            # spatial smoothing with median kernel
            cv2.medianBlur(sto2_image, 5, dst=sto2_image)
            sto2_image = np.rot90(sto2_image, k=1, axes=(0, 1))
        else:
            smoothed_cube = gaussian_filter1d(self.data_cube, sigma, axis=1)
            # cube = convolve1d(cube, gaussFkt, axis=2, origin=0)
            first_derivative = np.gradient(smoothed_cube, axis=1)
            second_derivative = np.gradient(first_derivative, axis=1)
            # calculate min of 2nd derivative between 573 and 587 nm
            min_value = second_derivative[:, first_range_start:first_range_end].min(axis=1)
            # calculate diff of mean and max of 2nd derivative between 740 and 780 nm
            max_value = second_derivative[:, second_range_start:second_range_end].max(axis=1)
            mean_value = second_derivative[:, second_range_start:second_range_end].mean(axis=1)
    
            # calculate parameter from range subresults
            sub1 = (min_value / 0.2)
            sub2 = ((mean_value - max_value) / (-0.03)) + sub1
            sub3 = ((sub1 / sub2) * 0.6) + 0.4
            sto2_image = sto2_image = np.exp(sub3) - 1.48
        np.clip(sto2_image, 0.000001, 1, out=sto2_image)
        self.sto2 = np.rot90(np.rot90(np.rot90(sto2_image)))
        if self.mask is not None:
            self.sto2_masked = np.ma.array(self.sto2[:, :], mask=[self.mask])
            logging.debug("Masked Sto2 Mean: " + str(self.sto2_masked.mean()))


    def _calc_nir(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None):
        a = -0.46
        b = 0.45
        first_range_start = int((825 - minWL) / WLsteps)
        first_range_end = int((925 - minWL) / WLsteps)
        second_range_start = int((655 - minWL) / WLsteps)
        second_range_end = int((735 - minWL) / WLsteps)
        if cube_index is None:
            # calculate mean between 825 and 925 nm
            mean_value1 = self.data_cube[:, :, first_range_start:first_range_end].mean(axis=2)
            # calculate mean between 655 and 735 nm
            mean_value2 = self.data_cube[:, :, second_range_start:second_range_end].mean(axis=2)
            # calculate parameter from range subresults
            sub1 = (-np.log(mean_value1 / mean_value2) - a) / (b - a)
            nir_image = (np.log(sub1 + 2.51) / np.log(1.3)) - 3.8  # y = log1.3 (x + 2.51) - 3.8
            nir_image = np.rot90(nir_image, k=1, axes=(0, 1))
        else:
            # calculate mean between 825 and 925 nm
            mean_value1 = self.data_cube[:, first_range_start:first_range_end].mean(axis=1)
            # calculate mean between 655 and 735 nm
            mean_value2 = self.data_cube[:, second_range_start:second_range_end].mean(axis=1)
            # calculate parameter from range subresults
            sub1 = (-np.log(mean_value1 / mean_value2) - a) / (b - a)
            nir_image = (np.log(sub1 + 2.51) / np.log(1.3)) - 3.8  # y = log1.3 (x + 2.51) - 3.8
        # clip values outside range
        np.clip(nir_image, 0.000001, 1, out=nir_image)
        self.nir = np.rot90(np.rot90(np.rot90(nir_image)))
        if self.mask is not None:
            self.nir_masked = np.ma.array(self.nir[:, :], mask=[self.mask])
            logging.debug("Masked NIR Mean: " + str(self.nir_masked.mean()))

    def _calc_thi(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None):
        a = 0.4
        b = 1.55
        first_range_start = int((530 - minWL) / WLsteps)
        first_range_end = int((590 - minWL) / WLsteps)
        second_range_start = int((785 - minWL) / WLsteps)
        second_range_end = int((825 - minWL) / WLsteps)
        if cube_index is None:
            # calculate mean between 530 and 590 nm
            mean_value1 = self.data_cube[:, :, first_range_start:first_range_end].mean(axis=2)
            # calculate mean between 785 and 825 nm
            mean_value2 = self.data_cube[:, :, second_range_start:second_range_end].mean(axis=2)
            # calculate parameter from range subresults
            ohi_image = (-np.log(mean_value1 / mean_value2) - a) / (b - a) / 2
            ohi_image = np.rot90(ohi_image, k=1, axes=(0, 1))
        else:
            # calculate mean between 530 and 590 nm
            mean_value1 = self.data_cube[:, first_range_start:first_range_end].mean(axis=1)
            # calculate mean between 785 and 825 nm
            mean_value2 = self.data_cube[:, second_range_start:second_range_end].mean(axis=1)
            # calculate parameter from range subresults
            ohi_image = (-np.log(mean_value1 / mean_value2) - a) / (b - a) / 2
        # clip values outside range
        np.clip(ohi_image, 0.000001, 1, out=ohi_image)
        self.thi = (np.rot90(np.rot90(np.rot90(ohi_image))))*2
        if self.mask is not None:
            self.thi_masked = np.ma.array(self.thi[:, :], mask=[self.mask])
            logging.debug("Masked THI Mean: " + str(self.thi_masked.mean()))


    def _calc_twi(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None):
        a = 0.1
        b = -0.5
        first_range_start = int((875 - minWL) / WLsteps)
        first_range_end = int((895 - minWL) / WLsteps)
        second_range_start = int((950 - minWL) / WLsteps)
        second_range_end = int((975 - minWL) / WLsteps)
        if cube_index is None:
            # calculate mean between 875 and 895 nm
            mean_value1 = self.data_cube[:, :, first_range_start:first_range_end].mean(axis=2)
            # calculate mean between 950 and 975 nm
            mean_value2 = self.data_cube[:, :, second_range_start:second_range_end].mean(axis=2)
            # calculate parameter from range subresults
            twi_image = (-np.log(mean_value1 / mean_value2) - a) / (b - a)
            twi_image = np.rot90(twi_image, k=1, axes=(0, 1))
        else:
            # calculate mean between 875 and 895 nm
            mean_value1 = self.data_cube[:, first_range_start:first_range_end].mean(axis=1)
            # calculate mean between 950 and 975 nm
            mean_value2 = self.data_cube[:, second_range_start:second_range_end].mean(axis=1)
            # calculate parameter from range subresults
            twi_image = (-np.log(mean_value1 / mean_value2) - a) / (b - a)
        # clip values outside range
        np.clip(twi_image, 0.000001, 1, out=twi_image)
        self.twi = np.rot90(np.rot90(np.rot90(twi_image)))
        if self.mask is not None:
            self.twi_masked = np.ma.array(self.twi[:, :], mask=[self.mask])
            logging.debug("Masked TWI Mean: " + str(self.twi_masked.mean()))
 
    def _calc_tli(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None):
        sigma = 2.66 * 1.67  # to be definded
        range_start = int(round((925 - minWL) / WLsteps))
        range_end = int(round((935 - minWL) / WLsteps))
        if cube_index is None:
            log_cube = -np.log(self.data_cube)
            smooth_log_cube = gaussian_filter1d(log_cube, sigma, axis=2)
            first_derivative = np.gradient(smooth_log_cube, axis=2)
            second_derivative = np.gradient(first_derivative, axis=2)
            # calculate mean between 925 and 935 nm
            mean_value = second_derivative[:, :, range_start:range_end].mean(axis=2)
            # normalize parameter
            tli_image = mean_value / (-0.006)
            # spatial smoothing with median kernel
            cv2.medianBlur(tli_image, 5, dst=tli_image)
            tli_image = np.rot90(tli_image, k=1, axes=(0, 1))
        else:
            log_cube = -np.log(self.data_cube)
            smooth_log_cube = gaussian_filter1d(log_cube, sigma, axis=1)
            first_derivative = np.gradient(smooth_log_cube, axis=1)
            second_derivative = np.gradient(first_derivative, axis=1)
            # calculate mean between 925 and 935 nm
            mean_value = second_derivative[:, range_start:range_end].mean(axis=1)
            # normalize parameter
            tli_image = mean_value / (-0.006)
        # clip values outside range
        np.clip(tli_image, 0.000001, 1, out=tli_image)
        self.tli = np.rot90(np.rot90(np.rot90(tli_image)))
        if self.mask is not None:
            self.tli_masked = np.ma.array(self.tli[:, :], mask=[self.mask])
            logging.debug("Masked TLI Mean: " + str(self.tli_masked.mean()))
            
    def _calc_ohi(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None):
        a = 0.4
        b = 1.55
        first_range_start = int((530 - minWL) / WLsteps)
        first_range_end = int((590 - minWL) / WLsteps)
        second_range_start = int((785 - minWL) / WLsteps)
        second_range_end = int((825 - minWL) / WLsteps)
        if cube_index is None:
            # calculate mean between 530 and 590 nm
            mean_value1 = self.data_cube[:, :, first_range_start:first_range_end].mean(axis=2)
            # calculate mean between 785 and 825 nm
            mean_value2 = self.data_cube[:, :, second_range_start:second_range_end].mean(axis=2)
            # calculate parameter from range subresults
            ohi_image = (-np.log(mean_value1 / mean_value2) - a) / (b - a) / 2
            ohi_image = np.rot90(ohi_image, k=1, axes=(0, 1))
        else:
            # calculate mean between 530 and 590 nm
            mean_value1 = self.data_cube[:, first_range_start:first_range_end].mean(axis=1)
            # calculate mean between 785 and 825 nm
            mean_value2 = self.data_cube[:, second_range_start:second_range_end].mean(axis=1)
            # calculate parameter from range subresults
            ohi_image = (-np.log(mean_value1 / mean_value2) - a) / (b - a) / 2
        # clip values outside range
        np.clip(ohi_image, 0.000001, 1, out=ohi_image)
        self.ohi = np.rot90(np.rot90(np.rot90(ohi_image)))
        if self.mask is not None:
            self.ohi_masked = np.ma.array(self.ohi[:, :], mask=[self.mask])
            logging.debug("Masked OHI Mean: " + str(self.ohi_masked.mean()))
        
    def _detect_background(self, minWL=500, maxWL=995, WLsteps=5, cube_index=None, scanning='horizontal'):
        a = -0.1
        b = 1.6
        first_range_start = int((510 - minWL) / WLsteps)
        first_range_end = int((570 - minWL) / WLsteps)
        second_range_start = int((650 - minWL) / WLsteps)
        second_range_end = int((710 - minWL) / WLsteps)
        if cube_index is None:
            # calculate mean between 510 and 570 nm
            mean_value1 = self.data_cube[:, :, first_range_start:first_range_end].mean(axis=2)
            # calculate mean between 650 and 710 nm
            mean_value2 = self.data_cube[:, :, second_range_start:second_range_end].mean(axis=2)
            # calculate parameter from range subresults
            sub1 = (-np.log(mean_value1 / mean_value2) - a) / b
            # calculate mean between 500 and 1000 nm
            mean_value3 = self.data_cube[:, :, :].mean(axis=2)
            mean_value1[mean_value1 > 0.7] = 0
            sub1[sub1 < 0] = 0
            mean_value3[mean_value3 < 0.1] = 0
            bg_mask = mean_value1 * sub1 * mean_value3
            bg_mask[bg_mask != 0] = 1
            bg_mask = np.rot90(bg_mask, k=1, axes=(0, 1))
        else:
            # calculate mean between 510 and 570 nm
            mean_value1 = self.data_cube[:, first_range_start:first_range_end].mean(axis=1)
            # calculate mean between 650 and 710 nm
            mean_value2 = self.data_cube[:, second_range_start:second_range_end].mean(axis=1)
            # calculate parameter from range subresults
            sub1 = (-np.log(mean_value1 / mean_value2) - a) / b
            # calculate mean between 500 and 1000 nm
            mean_value3 = self.data_cube[:, :].mean(axis=1)
            mean_value1[mean_value1 > 0.7] = 0
            sub1[sub1 < 0] = 0
            mean_value3[mean_value3 < 0.1] = 0
            bg_mask_line = mean_value1 * sub1 * mean_value3
            bg_mask_line[bg_mask_line != 0] = 1
            if scanning == 'horizontal':    # scanning left2right
                bg_mask[:, cube_index] = bg_mask_line[::-1]
            else:   # scanning bottom2top
                bg_mask[cube_index, :] = bg_mask_line[::-1]
        self.bg_mask = np.rot90(np.rot90(np.rot90(bg_mask)))
        self.ohi = self.ohi*self.bg_mask
        self.twi = self.twi*self.bg_mask
        self.nir = self.nir*self.bg_mask
        self.tli = self.tli*self.bg_mask
        self.thi = self.thi*self.bg_mask
        self.sto2 = self.sto2*self.bg_mask
            


    # --------------------------------------------- GENERAL CALCULATORS ----------------------------------------------

    def _calc_general(self):
        self.__calc_x1()
        self.__calc_x_reflectance()
        self.__calc_x2()
        self.__calc_x_absorbance()

    def __calc_x1(self):
        neg = 0
        # normalise
        if self.normal and not self.absorbance:
            data = self.data_cube
            if np.ma.min(self.data_cube) < 0:
                neg = np.abs(np.ma.min(data))
                data = data + np.abs(np.ma.min(data))
            if np.ma.min(self.data_cube) > 0:
                data = data - np.abs(np.ma.min(data))
            neg = neg / np.ma.max(data)
            self.x1 = data / np.ma.max(data)
        else:
            self.x1 = self.data_cube
        # mask negatives
        if self.negative:
            self.x1 = np.ma.array(self.x1, mask=self.x1 < neg)

    def __calc_x_reflectance(self):
        self.x_reflectance = self.x1

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_reflectance_w = np.mean(self.x_reflectance[:, :, wav_lower:wav_upper+1], axis=2)
        else:
            self.x_reflectance_w = self.x_reflectance[:, :, self.wavelength[0]]

        if self.mask is not None:
            mask = np.array([self.mask.T] * 100).T
            self.x_reflectance_masked = np.ma.array(self.x_reflectance[:, :, :], mask=mask)
            # self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(max(0, min(self.wavelength)), 0))
                wav_upper = int(round(min(max(self.wavelength), 99), 0))
                self.x_reflectance_masked_w = np.ma.array(np.mean(self.x_reflectance[:, :, wav_lower:wav_upper+1],
                                                                  axis=2), mask=self.mask)
            else:
                self.x_reflectance_masked_w = np.ma.array(self.x_reflectance[:, :, self.wavelength[0]], mask=self.mask)

    def __calc_x2(self):
        self.x2 = -np.ma.log(self.x1)
        self.x2 = np.ma.array(self.x2, mask=~np.isfinite(self.x2))
        neg = 0
        # normalise
        if self.normal and self.absorbance:
            data = self.x2
            if np.ma.min(self.x2) < 0:
                neg = np.abs(np.ma.min(data))
                data = data + np.abs(np.ma.min(data))
            if np.ma.min(self.x2) > 0:
                data = data - np.abs(np.ma.min(data))
            neg = neg / np.ma.max(data)
            self.x2 = data / np.ma.max(data)
        # mask negatives
        if self.negative:
            self.x2 = np.ma.array(self.x2, mask=self.x2 < neg)

    def __calc_x_absorbance(self):
        self.x_absorbance = self.x2

        if self.wavelength[0] != self.wavelength[1]:
            wav_lower = int(round(max(0, min(self.wavelength)), 0))
            wav_upper = int(round(min(max(self.wavelength), 99), 0))
            self.x_absorbance_w = np.mean(self.x_absorbance[:, :, wav_lower:wav_upper+1], axis=2)
        else:
            self.x_absorbance_w = self.x_absorbance[:, :, self.wavelength[0]]

        if self.mask is not None:
            # self.x_absorbance_masked = self.__apply_2DMask_on_3DArray(self.mask, self.x_absorbance)
            mask = np.array([self.mask.T] * 100).T
            self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=mask)
            # self.x_absorbance_masked = np.ma.array(self.x_absorbance[:, :, :], mask=np.array([self.mask] * 100))
            if self.wavelength[0] != self.wavelength[1]:
                wav_lower = int(round(min(0, min(self.wavelength)), 0))
                wav_upper = int(round(max(max(self.wavelength), 99), 0))
                self.x_absorbance_masked_w = np.ma.array(np.mean(self.x_absorbance[:, :, wav_lower:wav_upper+1],
                                                                 axis=2), mask=self.mask)
            else:
                self.x_absorbance_masked_w = np.ma.array(self.x_absorbance[:, :, self.wavelength[0]], mask=self.mask)
                
    def __setup(self):
        self.wavelengths = np.arange(500, 1000, 5)
        self.limits_list = [570, 590, 740, 780, 825, 925, 655, 735, 530, 785, 880, 900, 955, 980]
        self.limits = {}
        
        for limit in self.limits_list:
            self.limits[str(limit)] = self.__idx_from_wavelength(limit)
        self.filtered_img = gaussian_filter(self.data_cube, sigma=[0, 0, 6])
        self.second_deriv_img = np.gradient(np.gradient(self.filtered_img, axis=-1), axis=-1)
        
    def __idx_from_wavelength(self, limit_wavelength):
        idx = list(self.wavelengths).index(limit_wavelength)
        return idx
    

