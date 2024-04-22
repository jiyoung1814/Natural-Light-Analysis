from .Colorimetry.colorimetry import spd_reshape, spd_to_XYZ, XYZ_to_uv, XYZ_to_xy, uv_to_CCT, uv_to_cd, CCT_to_ref
from .Colorimetry.CRI import CRI
class optical:
    def __init__(self, spd):
        self.spd = spd_reshape(spd)
        self.X,self.Y, self.Z = spd_to_XYZ(self.spd)

        self.x, self.y = XYZ_to_xy(self.X,self.Y, self.Z)
        self.u, self.v = XYZ_to_uv(self.X,self.Y, self.Z)

        self.cct = uv_to_CCT(self.u, self.v)
        self.c, self.d = uv_to_cd(self.u, self.v)

        self.ref_spd = CCT_to_ref(self.cct)
        self.cri = None

    def spd_to_cri(self, ref_spd=None):
        if ref_spd is None:
            self.cri= CRI(self.spd, self.ref_spd)
        else:
            self.cri = CRI(self.spd, ref_spd)
