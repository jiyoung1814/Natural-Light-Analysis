import numpy as np



def reshapeSpd(spd, wl):
    '''

    spd의 스펙트럼 범위를 start ~ end nm로 reshape
    input spd에 없는 wavelength는 근처 wavelength에서 가져옴
    :param spd: input SPD (dict)
    :param start: 시작 wavelength
    :param end: 끝 wavelength
    :param step: 범위 wavelength
    :return: reshaped SPD (dict)
    '''
    input_wl = np.array(list(spd.keys()))

    spd = dict(map(lambda w: (w, spd[input_wl[np.abs(input_wl - w).argmin()]]), wl))
    return spd