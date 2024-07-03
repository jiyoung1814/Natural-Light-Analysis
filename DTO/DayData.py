import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Functions.Converter import TimestampToDatetime


class DayData:
    def __init__(self, data, source='DB'):
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

        self.spdRatio = data['spdRatio']

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

            # 위성 데이터
            self.gkb01_kc = data['gkb01_kc']
            self.gkb02_kc = data['gkb02_kc']
            self.gkb03_kc = data['gkb03_kc']
            self.gkb04_kc = data['gkb04_kc']
            self.gkb05_kc = data['gkb05_kc']
            self.gkb06_kc = data['gkb06_kc']
            self.gkb07_kc = data['gkb07_kc']
            self.gkb08_kc = data['gkb08_kc']
            self.gkb09_kc = data['gkb09_kc']
            self.gkb10_kc = data['gkb10_kc']
            self.gkb11_kc = data['gkb11_kc']
            self.gkb12_kc = data['gkb12_kc']
            self.gkb13_kc = data['gkb13_kc']
            self.gkb14_kc = data['gkb14_kc']
            self.gkb15_kc = data['gkb15_kc']
            self.gkb16_kc = data['gkb16_kc']
            self.gkct = ['gkct']
            self.gkcot_kc = ['gkcot_kc']
            self.gkcer_kc = ['gkcer_kc']

            try:

                # self.gkb01_sl = data['gkb01_sl']
                # self.gkb02_sl = data['gkb02_sl']
                # self.gkb03_sl = data['gkb03_sl']
                # self.gkb04_sl = data['gkb04_sl']
                # self.gkb05_sl = data['gkb05_sl']
                # self.gkb06_sl = data['gkb06_sl']
                # self.gkb07_sl = data['gkb07_sl']
                # self.gkb08_sl = data['gkb08_sl']
                # self.gkb09_sl = data['gkb09_sl']
                # self.gkb10_sl = data['gkb10_sl']
                # self.gkb11_sl = data['gkb11_sl']
                # self.gkb12_sl = data['gkb12_sl']
                # self.gkb13_sl = data['gkb13_sl']
                # self.gkb14_sl = data['gkb14_sl']
                # self.gkb15_sl = data['gkb15_sl']
                # self.gkb16_sl = data['gkb16_sl']

                # self.gkb01_line = data['gkb01_line']
                # self.gkb02_line = data['gkb02_line']
                # self.gkb03_line = data['gkb03_line']
                # self.gkb04_line = data['gkb04_line']
                # self.gkb05_line = data['gkb05_line']
                # self.gkb06_line = data['gkb06_line']
                # self.gkb07_line = data['gkb07_line']
                # self.gkb08_line = data['gkb08_line']
                # self.gkb09_line = data['gkb09_line']
                # self.gkb10_line = data['gkb10_line']
                # self.gkb11_line = data['gkb11_line']
                # self.gkb12_line = data['gkb12_line']
                # self.gkb13_line = data['gkb13_line']
                # self.gkb14_line = data['gkb14_line']
                # self.gkb15_line = data['gkb15_line']
                # self.gkb16_line = data['gkb16_line']
                #
                # self.gkb01_arr = data['gkb01_arr']
                # self.gkb02_arr = data['gkb02_arr']
                # self.gkb03_arr = data['gkb03_arr']
                # self.gkb04_arr = data['gkb04_arr']
                # self.gkb05_arr = data['gkb05_arr']
                # self.gkb06_arr = data['gkb06_arr']
                # self.gkb07_arr = data['gkb07_arr']
                # self.gkb08_arr = data['gkb08_arr']
                # self.gkb09_arr = data['gkb09_arr']
                # self.gkb10_arr = data['gkb10_arr']
                # self.gkb11_arr = data['gkb11_arr']
                # self.gkb12_arr = data['gkb12_arr']
                # self.gkb13_arr = data['gkb13_arr']
                # self.gkb14_arr = data['gkb14_arr']
                # self.gkb15_arr = data['gkb15_arr']
                # self.gkb16_arr = data['gkb16_arr']

                # self.gkb01_line11 = data['gkb01_line11']
                # self.gkb02_line11 = data['gkb02_line11']
                # self.gkb03_line11 = data['gkb03_line11']
                # self.gkb04_line11 = data['gkb04_line11']
                # self.gkb05_line11 = data['gkb05_line11']
                # self.gkb06_line11 = data['gkb06_line11']
                # self.gkb07_line11 = data['gkb07_line11']
                # self.gkb08_line11 = data['gkb08_line11']
                # self.gkb09_line11 = data['gkb09_line11']
                # self.gkb10_line11 = data['gkb10_line11']
                # self.gkb11_line11 = data['gkb11_line11']
                # self.gkb12_line11 = data['gkb12_line11']
                # self.gkb13_line11 = data['gkb13_line11']
                # self.gkb14_line11 = data['gkb14_line11']
                # self.gkb15_line11 = data['gkb15_line11']
                # self.gkb16_line11 = data['gkb16_line11']

                # 지표면 제거 데이터
                self.gkb01_ln = data['gkb01_ln']
                self.gkb02_ln = data['gkb02_ln']
                self.gkb03_ln = data['gkb03_ln']
                self.gkb04_ln = data['gkb04_ln']

                self.gkb01_ln11 = data['gkb01_ln11']
                self.gkb02_ln11 = data['gkb02_ln11']
                self.gkb03_ln11 = data['gkb03_ln11']
                self.gkb04_ln11 = data['gkb04_ln11']

                self.gkb01_lnc11 = data['gkb01_lnc11']
                self.gkb02_lnc11 = data['gkb02_lnc11']
                self.gkb03_lnc11 = data['gkb03_lnc11']
                self.gkb04_lnc11 = data['gkb04_lnc11']

            except Exception as e:
                print()


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
            self.gkct = ['gkCT']
            self.gkcot_kc = ['gkCOT_KC']
            self.gkcer_kc = ['gkCER_KC']

            try:

                # self.gkb01_sl = data['gkB01_SL']
                # self.gkb02_sl = data['gkB02_SL']
                # self.gkb03_sl = data['gkB03_SL']
                # self.gkb04_sl = data['gkB04_SL']
                # self.gkb05_sl = data['gkB05_SL']
                # self.gkb06_sl = data['gkB06_SL']
                # self.gkb07_sl = data['gkB07_SL']
                # self.gkb08_sl = data['gkB08_SL']
                # self.gkb09_sl = data['gkB09_SL']
                # self.gkb10_sl = data['gkB10_SL']
                # self.gkb11_sl = data['gkB11_SL']
                # self.gkb12_sl = data['gkB12_SL']
                # self.gkb13_sl = data['gkB13_SL']
                # self.gkb14_sl = data['gkB14_SL']
                # self.gkb15_sl = data['gkB15_SL']
                # self.gkb16_sl = data['gkB16_SL']

                # self.gkb01_line = data['gkB01_LINE']
                # self.gkb02_line = data['gkB02_LINE']
                # self.gkb03_line = data['gkB03_LINE']
                # self.gkb04_line = data['gkB04_LINE']
                # self.gkb05_line = data['gkB05_LINE']
                # self.gkb06_line = data['gkB06_LINE']
                # self.gkb07_line = data['gkB07_LINE']
                # self.gkb08_line = data['gkB08_LINE']
                # self.gkb09_line = data['gkB09_LINE']
                # self.gkb10_line = data['gkB10_LINE']
                # self.gkb11_line = data['gkB11_LINE']
                # self.gkb12_line = data['gkB12_LINE']
                # self.gkb13_line = data['gkB13_LINE']
                # self.gkb14_line = data['gkB14_LINE']
                # self.gkb15_line = data['gkB15_LINE']
                # self.gkb16_line = data['gkB16_LINE']
                #
                # self.gkb01_arr = data['gkB01_ARR']
                # self.gkb02_arr = data['gkB02_ARR']
                # self.gkb03_arr = data['gkB03_ARR']
                # self.gkb04_arr = data['gkB04_ARR']
                # self.gkb05_arr = data['gkB05_ARR']
                # self.gkb06_arr = data['gkB06_ARR']
                # self.gkb07_arr = data['gkB07_ARR']
                # self.gkb08_arr = data['gkB08_ARR']
                # self.gkb09_arr = data['gkB09_ARR']
                # self.gkb10_arr = data['gkB10_ARR']
                # self.gkb11_arr = data['gkB11_ARR']
                # self.gkb12_arr = data['gkB12_ARR']
                # self.gkb13_arr = data['gkB13_ARR']
                # self.gkb14_arr = data['gkB14_ARR']
                # self.gkb15_arr = data['gkB15_ARR']
                # self.gkb16_arr = data['gkB16_ARR']

                # self.gkb01_line11 = data['gkB01_LINE11']
                # self.gkb02_line11 = data['gkB02_LINE11']
                # self.gkb03_line11 = data['gkB03_LINE11']
                # self.gkb04_line11 = data['gkB04_LINE11']
                # self.gkb05_line11 = data['gkB05_LINE11']
                # self.gkb06_line11 = data['gkB06_LINE11']
                # self.gkb07_line11 = data['gkB07_LINE11']
                # self.gkb08_line11 = data['gkB08_LINE11']
                # self.gkb09_line11 = data['gkB09_LINE11']
                # self.gkb10_line11 = data['gkB10_LINE11']
                # self.gkb11_line11 = data['gkB11_LINE11']
                # self.gkb12_line11 = data['gkB12_LINE11']
                # self.gkb13_line11 = data['gkB13_LINE11']
                # self.gkb14_line11 = data['gkB14_LINE11']
                # self.gkb15_line11 = data['gkB15_LINE11']
                # self.gkb16_line11 = data['gkB16_LINE11']

                # 지표면 제거 데이터
                self.gkb01_ln = data['gkB01_LN']
                self.gkb02_ln = data['gkB02_LN']
                self.gkb03_ln = data['gkB03_LN']
                self.gkb04_ln = data['gkB04_LN']

                self.gkb01_ln11 = data['gkB01_LN11']
                self.gkb02_ln11 = data['gkB02_LN11']
                self.gkb03_ln11 = data['gkB03_LN11']
                self.gkb04_ln11 = data['gkB04_LN11']

                self.gkb01_lnc11 = data['gkB01_LNC11']
                self.gkb02_lnc11 = data['gkB02_LNC11']
                self.gkb03_lnc11 = data['gkB03_LNC11']
                self.gkb04_lnc11 = data['gkB04_LNC11']

            except Exception as e:
                print()
                # print(f"DayData Class Error: {e}")

    def setSPD(self, spds, wavelength=[str(w) for w in range(380, 781)]):
        if type(spds) is dict:
            self.spd = spds
        else:
            self.spd = {wl: spd for wl, spd in zip(wavelength, spds)}

    def setIntgrationTime(self, intgtime):
        self.intgtime = intgtime
