import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Functions.Converter import TimestampToDatetime

class DayInfo:
    def __init__(self, daily):
        '''

        :param daily:
        {
          "Date": "2022-02-01",
          "KasiSunRiseTimestamp": 1643700840000,
          "KasiSunNoonTimestamp": 1643719502000,
          "KasiSunSetTimestamp": 1643738160000,
          "CalcSunRiseTimestamp": 1643700841925,
          "CalcSunNoonTimestamp": 1643719491410,
          "CalcSunSetTimestamp": 1643738173858,
          "LwctSunRiseTimestamp": 1643704119000,
          "LwctSunSetTimestamp": 1643735216000,
          "TargetMeasureCount": 622,
          "ActualMeasureCount": 614,
          "DiffRateCCT50": 0.59844054580896688,
          "HighestElevation": 36.048954769368912,
          "NearSeasonTimestamp": 1643953860000,
          "NearSeasonName": "입춘",
          "NearSeasonDiffDay": -3.0766898148148147,
          "Judgment": 5,
          "MemoTimestamp": -62135596800000,
          "MemoUser": "",
          "MemoContants": ""
        }
        '''
        self.date = daily['date']

        self.kasiSunRiseTime = TimestampToDatetime(daily['kasiSunRiseTimestamp'])
        self.kasiSunNoonTime = TimestampToDatetime(daily['kasiSunNoonTimestamp'])
        self.kasiSunSetTime = TimestampToDatetime(daily['kasiSunSetTimestamp'])
        self.calcSunRiseTime = TimestampToDatetime(daily['calcSunRiseTimestamp'])
        self.calcSunNoonTime = TimestampToDatetime(daily['calcSunNoonTimestamp'])
        self.calcSunSetTime = TimestampToDatetime(daily['calcSunSetTimestamp'])
        self.lwctSunRiseTime = TimestampToDatetime(daily['lwctSunRiseTimestamp'])
        self.lwctSunSetTime= TimestampToDatetime(daily['lwctSunSetTimestamp'])

        self.diffRateCCT = daily['diffRateCCT50']
        self.highestEl = daily['highestElevation']
        self.highestLux = daily['highestLux']
        self.nearSeasonName = daily['nearSeasonName']

        self.judgment = daily['judgment']

        self.nearSeasonDiffDay = daily['nearSeasonDiffDay']
        self.nearSeasonTimestamp = daily['nearSeasonTimestamp']
        self.targetMeasureCount = daily['targetMeasureCount']
        self.actualMeasureCount = daily['actualMeasureCount']
        self.memoUser = daily['memoUser']

