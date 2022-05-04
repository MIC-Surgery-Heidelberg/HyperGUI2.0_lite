def get_index_16(x):
    import numpy as np
    from scipy.ndimage import gaussian_filter1d
    import cv2
    sigma = 2.66
    minWL = 500
    WLsteps = 5
    first_range_start = int(round((573 - minWL) / WLsteps))
    first_range_end = int(round((587 - minWL) / WLsteps))
    second_range_start = int(round((740 - minWL) / WLsteps))
    second_range_end = int(round((780 - minWL) / WLsteps)) + 1
        
    smoothed_cube = gaussian_filter1d(x, sigma, axis=2)
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
    np.clip(sto2_image, 0.000001, 1, out=sto2_image)
    index = sto2_image
    return index

