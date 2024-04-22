import pandas as pd
import numpy as np
import math
from .colorimetry import XYZ_to_uv, spd_to_XYZ, XYZ_to_uv, uv_to_cd
from .constant.TCS import TCS

class CRI:
    def __init__(self, spd_t, spd_r):
        cri_r = spd_to_cri(spd_t, spd_r)

        self.ra = np.mean(np.array(list(cri_r.values()))[:8])
        self.r1 = cri_r['TCS01']
        self.r2 = cri_r['TCS02']
        self.r3 = cri_r['TCS03']
        self.r4 = cri_r['TCS04']
        self.r5 = cri_r['TCS05']
        self.r6 = cri_r['TCS06']
        self.r7 = cri_r['TCS07']
        self.r8 = cri_r['TCS08']
        self.r9 = cri_r['TCS09']
        self.r10 = cri_r['TCS10']
        self.r11 = cri_r['TCS11']
        self.r12 = cri_r['TCS12']
        self.r13 = cri_r['TCS13']
        self.r14 = cri_r['TCS14']




def spd_to_cri(spd_t, spd_r):
    test_tcs_colorimetry_data = tcs_colorimetry_data(spd_t, spd_r, True)
    reference_tcs_colorimetry_data = tcs_colorimetry_data(spd_r, spd_r)

    CRI_r ={}
    diff = reference_tcs_colorimetry_data - test_tcs_colorimetry_data

    for i, d in diff.iterrows():
        euclidean_d = math.sqrt(sum([x**2 for x in d]))
        CRI_r[i] = 100 - 4.6 * euclidean_d

    return CRI_r

def tcs_colorimetry_data(spd_t, spd_r, chromatic_adaptation = False):
    X_t, Y_t, Z_t = spd_to_XYZ(spd_t)
    u_t, v_t = XYZ_to_uv(X_t, Y_t, Z_t)

    X_r, Y_r, Z_r = spd_to_XYZ(spd_r)
    u_r, v_r = XYZ_to_uv(X_r, Y_r, Z_r)

    tcs_data = pd.DataFrame({}, columns=['W', 'U', 'V'])

    for i in TCS.columns:
        spd_tcs = TCS[i].to_dict()
        X_tcs, Y_tcs, Z_tcs = spd_to_XYZ(spd_tcs, spd_t)
        u_tcs, v_tcs = XYZ_to_uv(X_tcs, Y_tcs, Z_tcs)

        if chromatic_adaptation:
            c_t, d_t = uv_to_cd(u_t, v_t)
            c_r, d_r = uv_to_cd(u_r, v_r)
            tcs_c, tcs_d = uv_to_cd(u_tcs, v_tcs)

            c_r_c_t = c_r / c_t
            d_r_d_t = d_r / d_t

            u_tcs = ( 10.872 + 0.404 * c_r_c_t * tcs_c - 4 * d_r_d_t * tcs_d) / (16.518 + 1.481 * c_r_c_t * tcs_c - d_r_d_t * tcs_d)
            v_tcs = 5.52 / (16.518 + 1.481 * c_r_c_t * tcs_c - d_r_d_t * tcs_d)

        W_tcs = 25 * (np.sign(Y_tcs) * Y_tcs ** (1 / 3)) - 17
        U_tcs = 13 * W_tcs * (u_tcs - u_r)
        V_tcs = 13 * W_tcs * (v_tcs - v_r)

        tcs_data.loc[i] = [W_tcs, U_tcs, V_tcs]

    return tcs_data