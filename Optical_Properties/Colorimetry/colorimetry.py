from .ReshapeSPD import reshapeSpd
from .triXYZ import spdToXYZSimple, spdToXYZ
from .CCT import uvToCCT
from .REF_SPD import blackbody_spd, CIE_illuminant_D_series_spd

start = 360
end = 780
step = 1
wl = [x for x in range(start, end + 1, step)]


def spd_reshape(spd):
    return reshapeSpd(spd, wl)


def spd_to_XYZ(spd, illuminant=None):
    if illuminant is None:
        return spdToXYZSimple(spd)
    else:
        return spdToXYZ(spd, illuminant)


def XYZ_to_xy(X, Y, Z):
    return X / (X + Y + Z), Y / (X + Y + Z)


def XYZ_to_uv(X, Y, Z):
    return (4 * X) / (X + 15 * Y + 3 * Z), (6 * Y) / (X + 15 * Y + 3 * Z)


def uv_to_CCT(u, v):
    return uvToCCT(u, v)


def uv_to_cd(u, v):
    return (4 - u - 10 * v) / v, (1.708 * v + 0.404 - 1.481 * u) / v


def CCT_to_ref(cct):
    if cct < 5000:
        return blackbody_spd(cct, wl)
    else:
        return CIE_illuminant_D_series_spd(cct, wl)
