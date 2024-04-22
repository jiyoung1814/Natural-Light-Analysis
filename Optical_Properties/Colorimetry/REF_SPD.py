import numpy as np
from .constant.CIE_D_Serise import CIE_D_SERIES

condition = [-1, 0, 1, 2]


def blackbody_spd(cct, wl):
    c1 = 3.741771E-16
    c2 = 0.014388
    n = 1

    wl = np.array(wl)

    l = wl * 1e-9
    d = np.expm1(c2 / (n * l * cct)) ** -1
    p = ((c1 * n ** -2 * l ** -5) / np.pi) * d

    return {key: value for key, value in zip(wl, p * 1e-9)}


def CCT_to_xy_CIE_D(CCT):
    CCT_3 = CCT ** 3
    CCT_2 = CCT ** 2

    if CCT <= 7000:
        x_D = -4.607 * 10 ** 9 / CCT_3 + 2.9678 * 10 ** 6 / CCT_2 + 0.09911 * 10 ** 3 / CCT + 0.24406
    else:
        x_D = -2.0064 * 10 ** 9 / CCT_3 + 1.9018 * 10 ** 6 / CCT_2 + 0.24748 * 10 ** 3 / CCT + 0.23704

    y_D = -3.000 * x_D ** 2 + 2.870 * x_D - 0.275

    return x_D, y_D


def Interpolate_Distribution(spd, wl):
    '''

    :param spd: 보간할 SPD (class: pd.Series)
    :param wl: interpolated 할 wavelength (class: np.array)
    :return: interpolated SPD (class: dict)
    '''
    b_w = np.array(spd.keys())
    interpolated_spd = {key: 0 for key in wl}

    for w in wl:
        ld = []
        s = []
        for c in condition:
            lambda_w = b_w[np.abs(b_w - w).argmin() + c]
            ld.append(lambda_w)

            s.append(spd[lambda_w])

        for i in range(4):
            numerator = 1
            denominator = 1
            for j in range(4):
                if i != j:
                    numerator *= (w - ld[j])
                    denominator *= ld[i] - ld[j]
            interpolated_spd[w] += (numerator / denominator) * s[i]

    return interpolated_spd


def CIE_illuminant_D_series_spd(cct, wl):
    '''
    입력 색온도의 CIE D Series 광원 SPD 추출출
    :param cct: 입력 색온도
    :param wl: interpolated 할 wavelength (class: np.array)
    :return: interpolated CIE D Series SPD (class: dict)
    '''
    x_D, y_D = CCT_to_xy_CIE_D(cct)

    M = 0.0241 + 0.2562 * x_D - 0.7341 * y_D
    M1 = np.around((-1.3515 - 1.7703 * x_D + 5.9114 * y_D) / M, 3)
    M2 = np.around((0.0300 - 31.4424 * x_D + 30.0717 * y_D) / M, 3)

    distribution = CIE_D_SERIES['S0'] + M1 * CIE_D_SERIES['S1'] + M2 * CIE_D_SERIES['S2']
    # 보간
    return Interpolate_Distribution(distribution, wl)
