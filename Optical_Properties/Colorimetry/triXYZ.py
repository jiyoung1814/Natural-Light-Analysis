import numpy as np
from Optical_Properties.Colorimetry.constant.CMFS import cmfs

def spdToXYZSimple(spd):
    '''
    Convert given spectral distribution to *CIE XYZ* tristimulus values
    :param spd: dict {wavelength: spectral irradiance)
    :return: *CIE XYZ* tristimulus values (class: np.array)
    '''

    X = sum(s * c for s, c in zip(list(spd.values()), cmfs['r'].tolist())) * 683
    Y = sum(s * c for s, c in zip(list(spd.values()), cmfs['g'].tolist())) * 683
    Z = sum(s * c for s, c in zip(list(spd.values()), cmfs['b'].tolist())) * 683

    return X, Y, Z

def spdToXYZ(spd, illuminant):
    '''
    Convert given spectral distribution to *CIE XYZ* tristimulus values
    :param spd: dict {wavelength: spectral irradiance)
    :param illuminant: Reflective spectral distribution
    :return:*CIE XYZ* tristimulus values (class: np.array)
    '''

    d_w = np.diff((np.array(list(spd.keys()))))[0] #step

    k = 100 / sum(s * c_g for s, c_g in zip(list(illuminant.values()), cmfs['g'].tolist())) * d_w

    R_S = {key: spd[key] * illuminant[key] for key in spd}

    X = k * sum(s * c for s, c in zip(list(R_S.values()), cmfs['r'].tolist())) * d_w
    Y = k * sum(s * c for s, c in zip(list(R_S.values()), cmfs['g'].tolist())) * d_w
    Z = k * sum(s * c for s, c in zip(list(R_S.values()), cmfs['b'].tolist())) * d_w

    return X, Y, Z