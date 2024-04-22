import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Functions.Converter import TimestampToDatetime


class DayData:
    def __init__(self, data, source = 'DB'):
        self.datetime = TimestampToDatetime(data['timestamp'])
        self.timestamp = data['timestamp']
        self.azimuth = data['azimuth']
        self.elevation = data['elevation']
        self.lux = data['lux']
        self.cct = data['cct']
        self.swR100 = data['swR100']
        self.mwR100 = data['mwR100']
        self.lwR100 = data['lwR100']
        self.x1931 = data['x1931']
        self.y1931 = data['y1931']
        self.u1960 = data['u1960']
        self.v1960 = data['v1960']
        self.u1976 = data['u1976']
        self.v1976 = data['v1976']
        self.deltaUV = data['deltaUV']

        # 위성 데이터
        self.gkb01_kc = data['gkB01_KC']
        self.gkb02_kc = data['gkB02_KC']
        self.gkb03_kc = data['gkB03_KC']
        self.gkb04_kc = data['gkB04_KC']
        self.gkb05_kc = data['gkB05_KC']
        self.gkb06_kc = data['gkB06_KC']
        self.gkb07_kc = data['gkB07_KC']
        self.gkb08_kc = data['gkB08_KC']
        self.gkb09_kc = data['gkB09_KC']
        self.gkb10_kc = data['gkB10_KC']
        self.gkb11_kc = data['gkB11_KC']
        self.gkb12_kc = data['gkB12_KC']
        self.gkb13_kc = data['gkB13_KC']
        self.gkb14_kc = data['gkB14_KC']
        self.gkb15_kc = data['gkB15_KC']
        self.gkb16_kc = data['gkB16_KC']

        if source == 'DB':
            # self.azimuth = data['az']
            # self.elevation = data['el']

            self.cri = data['cri']
            self.r1 = data['r1']
            self.r2 = data['r2']
            self.r3 = data['r3']
            self.r4 = data['r4']
            self.r5 = data['r5']
            self.r6 = data['r6']
            self.r7 = data['r7']
            self.r8 = data['r8']
            self.r9 = data['r9']
            self.r10 = data['r10']
            self.r11 = data['r11']
            self.r12 = data['r12']
            self.r13 = data['r13']
            self.r14 = data['r14']
            self.spd = data['spd']
            self.intgtime = data['intgtime']

        elif source == 'Platform':

            self.cri = data['crI_Ra']
            self.r1 = data['crI_R'][0]
            self.r2 = data['crI_R'][1]
            self.r3 = data['crI_R'][2]
            self.r4 = data['crI_R'][3]
            self.r5 = data['crI_R'][4]
            self.r6 = data['crI_R'][5]
            self.r7 = data['crI_R'][6]
            self.r8 = data['crI_R'][7]
            self.r9 = data['crI_R'][8]
            self.r10 = data['crI_R'][9]
            self.r11 = data['crI_R'][10]
            self.r12 = data['crI_R'][11]
            self.r13 = data['crI_R'][12]
            self.r14 = data['crI_R'][13]

            self.spd = {}
            self.intgtime = 0




    def setSPD(self, spds, wavelength=[str(w) for w in range(380, 781)]):
        if type(spds) is dict:
            self.spd = spds
        else:
            self.spd = {wl: spd for wl, spd in zip(wavelength, spds)}

    def setIntgrationTime(self, intgtime):
        self.intgtime = intgtime
