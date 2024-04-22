import numpy as np

from .constant.ROBERTSON1968 import Robertson1968


def uvToCCT(u, v):
    last_dt = last_dv = last_du = 0
    T = 0

    for i in range(1, 31):
        wr_ruvt = Robertson1968.iloc[i]
        wr_ruvt_previous = Robertson1968.iloc[i - 1]

        du = 1
        dv = wr_ruvt['t']

        length = np.hypot(1, dv)

        du /= length
        dv /= length

        uu = u - wr_ruvt['u']
        vv = v - wr_ruvt['v']

        dt = -uu * dv + vv * du

        if dt <= 0 or i == 30:
            if dt > 0:
                dt = 0

            dt = -dt

            f = 0 if i == 1 else dt / (last_dt + dt)

            T = 1.0e6 / (wr_ruvt_previous['r'] * f + wr_ruvt['r'] * (1 - f))

            uu = u - (wr_ruvt_previous['u'] * f + wr_ruvt['u'] * (1 - f))
            vv = v - (wr_ruvt_previous['v'] * f + wr_ruvt['v'] * (1 - f))

            du = du * (1 - f) + last_du * f
            dv = dv * (1 - f) + last_dv * f

            length = np.hypot(du, dv)

            du /= length
            dv /= length

            D_uv = uu * du + vv * dv

            break

        last_dt = dt
        last_du = du
        last_dv = dv

    return T
