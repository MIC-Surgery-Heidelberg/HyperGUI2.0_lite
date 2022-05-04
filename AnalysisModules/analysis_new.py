from AnalysisModules.Indices import Index
from HyperGuiModules.utility import *
import logging
import os
np.set_printoptions(threshold=sys.maxsize)

RGB_FILE = "_RGB-Image.png"
STO2_FILE = "_Oxygenation.png"
NIR_FILE = "_NIR-Perfusion.png"
THI_FILE = "_THI.png"
TWI_FILE = "_TWI.png"
OHI_FILE = "_OHI.png"
TLI_FILE = "_TLI.png"

RGB_FILE_SEGM = "_RGB-Image_segm.png"
STO2_FILE_SEGM = "_Oxygenation_segm.png"
NIR_FILE_SEGM = "_NIR-Perfusion_segm.png"
THI_FILE_SEGM = "_THI_segm.png"
TWI_FILE_SEGM = "_TWI_segm.png"
OHI_FILE_SEGM = "_OHI_segm.png"
TLI_FILE_SEGM = "_TLI_segm.png"


class NewAnalysis:
    # performs analyses necessary for new image
    def __init__(self, path, data_cube, wavelength, index_number, listener, mask=None):

        self.listener = listener
        self.segm = False

        # inputs
        self.path = path
        self.data_cube = data_cube
        self.mask = mask
        self.wavelength = wavelength
        self.absorbance = False
        self.normal = False
        self.negative = False

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
        self.rgb_og = None
        self.sto2_og = None
        self.nir_og = None
        self.thi_og = None
        self.twi_og = None
        self.tli_og = None
        self.index_number = index_number
        self.index = None
        self.index_masked = None

        self.analysis()

    def analysis(self):
        self._calc_general()
        self._calc_index(self.index_number)

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

    def update_index(self, new_index_number):
        self.index_number = new_index_number
        self.analysis()

    # --------------------------------------------------- GETTERS ----------------------------------------------------

    def get_rgb_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + RGB_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + RGB_FILE 
        if os.path.exists(filename):
            self.rgb_og = image_to_array(filename)
            if self.rgb_og.shape[0] == 550:
                chopped = self.rgb_og[50:530, 20:660, :3]
            else:
                chopped = self.rgb_og[30:510, 3:643, :3]
            reshaped = self.ensure_shape(chopped)
        else:
            reshaped = np.zeros((480, 640,3))
        return reshaped

    def get_sto2_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + STO2_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + STO2_FILE 
        if os.path.exists(filename):
            self.sto2_og = image_to_array(filename)
            if self.sto2_og.shape[0] == 550:
                chopped = self.sto2_og[50:530, 50:690, :3]
            else:
                chopped = self.sto2_og[26:506, 4:644, :3]
        else:
            chopped = np.zeros((480, 640,3))
        return chopped

    def get_nir_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + NIR_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + NIR_FILE 
        if os.path.exists(filename):
            self.nir_og = image_to_array(filename)
            if self.nir_og.shape[0] == 550:
                chopped = self.nir_og[50:530, 50:690, :3]
            else:
                chopped = self.nir_og[26:506, 4:644, :3]
        else:
            chopped = np.zeros((480, 640,3))
        return chopped

    def get_thi_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + THI_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + THI_FILE 
        if os.path.exists(filename):
            self.thi_og = image_to_array(filename)
            if self.thi_og.shape[0] == 550:
                chopped = self.thi_og[50:530, 50:690, :3]
            else:
                chopped = self.thi_og[26:506, 4:644, :3]
        else:
            chopped = np.zeros((480, 640,3))
        return chopped

    def get_twi_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + TWI_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + TWI_FILE 
        if os.path.exists(filename):
            self.twi_og = image_to_array(filename)
            if self.twi_og.shape[0] == 550:
                chopped = self.twi_og[50:530, 50:690, :3]
            else:
                chopped = self.twi_og[26:506, 4:644, :3]
        else:
            chopped = np.zeros((480, 640,3))
        return chopped
    
    def get_tli_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + TLI_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + TLI_FILE 
        if os.path.exists(filename):
            self.tli_og = image_to_array(filename)
            if self.tli_og.shape[0] == 550:
                chopped = self.tli_og[50:530, 50:690, :3]
            else:
                chopped = self.tli_og[26:506, 4:644, :3]
        else:
            chopped = np.zeros((480, 640,3))
        return chopped
    
    def get_ohi_og(self, segm = None):
        if segm is None:
            segm = self.segm
        if segm:
            self.segm = True
            filename = str(self.path[:-13]) + OHI_FILE_SEGM 
        else:
            self.segm = False
            filename = str(self.path[:-13]) + OHI_FILE 
        if os.path.exists(filename):
            self.ohi_og = image_to_array(filename)
            if self.ohi_og.shape[0] == 550:
                chopped = self.ohi_og[50:530, 50:690, :3]
            else:
                chopped = self.ohi_og[26:506, 4:644, :3]
        else:
            chopped = np.zeros((480, 640,3))
        return chopped
    
    def get_wl_data(self):
        if self.absorbance:
            new_data = self.x_absorbance_w
        else:
            new_data = self.x_reflectance_w
        return new_data

    def get_wl_data_masked(self):
        if self.absorbance:
            new_data = self.x_absorbance_masked_w
        else:
            new_data = self.x_reflectance_masked_w
        return new_data
    
    def ensure_shape(self, data):
        arr = np.asarray(data.shape)
        g = arr.copy()
        arr.sort()
        i1 = np.where(g == arr[1])[0][0]
        i2 = np.where(g == arr[2])[0][0]
        i3 = np.where(g == arr[0])[0][0]
        return np.moveaxis(data, [i1, i2, i3], [0, 1, 2])

    # ------------------------------------------------- CALCULATORS --------------------------------------------------

    def _calc_index(self, index_number):
        logging.debug("CALCULATING: INDEX...")
        if self.absorbance:
            index_module = Index(index_number, self.x_absorbance, wavelength=self.wavelength, listener=self.listener)
            self.index = index_module.get_index()
            if self.mask is not None:
                self.index_masked = np.ma.array(index_module.get_index(), mask=self.mask)
        else:
            index_module = Index(index_number, self.x1, wavelength=self.wavelength, listener=self.listener)
            self.index = index_module.index
            if self.mask is not None:
                self.index_masked = np.ma.array(index_module.get_index(), mask=self.mask)

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
