'''
    자연광 하루 데이터를 획득

    date // 날짜
    timestamp // 날짜의 타임스탬프
    sunrise // 일출 타임스탬프
    sunset // 일몰 타임스탬프
    startLwstCct // 색온도 저점 일출 타임스탬프
    endLwstCct // 색온도 저점 일몰 타임스탬프
    totalCount // 데이터 총 개수
    validCount // 데이터 유효 개수
    judgment // 데이터 유효 여부
    nearSeasonName // 근처 24절기 이름
    nearSeasonDiffDay // 근처 24절기와의 차이일
    diffRateCCT50_All // 색온도 차분
    diffRateCCT50_Part1 // 색온도 차분 Part1
    diffRateCCT50_Part2 // 색온도 차분 Part2
    diffRateCCT50_Part3 // 색온도 차분 Part3
    startLwstData // 색온도 저점 일출의 자연광 데이터
    endLwstData // 색온도 저점 일몰의 자연광 데이터
    dataList // 일출부터 일몰까지의 자연광 데이터 리스트

    lux // 조도
    cct // 색온도
    cri, r9, r12  // 연색성
    triX, triY, triZ // 삼자극치
    uva, uvb, uvi // 자외선
    swr, mwr, narr // 파장 비율 (380-480, 480-560, 446-477)
    minuteFromSunrise // 생체박명, 일출로부터 걸린 Minute
    minuteFromSunset // 생체박명, 일몰까지 남은 Minute
    sun_azimuth, sun_elevation // 태양 방위각, 고도
    time_ratio // 색온도 일출, 일몰 기준의 하루 시간을 0~1로 표현한 상대 시간

'''
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Functions.Converter import TimestampToStrDatetime

daily_properties = ['sunrise', 'sunset', 'nearSeasonName', 'startLwstCct', 'endLwstCct', 'diffRateCCT50_All']
optical_properties = ['lux', 'cct', 'cri', 'r9', 'r12', 'triX', 'triY', 'triZ', 'uvi', 'uva', 'uvb', 'swr', 'mwr',
                      'narr', 'sun_azimuth', 'sun_elevation']


class DayNaturalLight:

    def __init__(self, res):

        self.date = res['date']
        self.sunrise = TimestampToStrDatetime(res['sunrise'])
        self.sunset = TimestampToStrDatetime(res['sunset'])
        self.nearSeasonName = res['nearSeasonName']
        self.dataList = res['dataList']
        self.startLwstCct = TimestampToStrDatetime(res['startLwstCct'])
        self.endLwstCct = TimestampToStrDatetime(res['endLwstCct'])
        self.diffRateCCT50_All = res['diffRateCCT50_All']

        self.timeData = pd.DataFrame({}, columns=['time']+optical_properties)
        self.sortDataList()

    def sortDataList(self):
        '''
        아래 두개의 방법중 하나 고르기
        1. 일출 ~ 일몰
        2. 일출 최저점 ~ 일몰 최저점
        :return: DataFrame {index = time, columns = optical_properties}
        '''

        # # 1. 일출 ~ 일몰
        # for t in self.dataList:
        #     self.timeData.loc[t['datetime']] = [t[op] for op in optical_properties]

        # 2. 일출 최저점 ~ 일몰 최저점
        for t in self.dataList:
            if self.startLwstCct <= t["datetime"] <= self.endLwstCct:
                self.timeData.loc[t['datetime']] = ([t['datetime'].split()[1]] + [t[op] for op in optical_properties])



    def getDailyAPIByList(self):
        return [self.sunrise.split(" ")[1], self.sunset.split(" ")[1], self.nearSeasonName, self.startLwstCct.split(" ")[1], self.endLwstCct.split(" ")[1],
                self.diffRateCCT50_All]



# class Optical_Properties:
#     def __init__(self, timeData):
#         self.lux = timeData['lux']
#         self.cct = timeData['cct']
#         self.cri = timeData['cri']
#         self.r9 = timeData['r9']
#         self.r12 = timeData['r12']
#         self.triX = timeData['triX']
#         self.triY = timeData['triY']
#         self.triZ = timeData['triZ']
#         self.uvi = timeData['uvi']
#         self.uva = timeData['uva']
#         self.uvb = timeData['uvb']
#         self.swr = timeData['swr']
#         self.mwr = timeData['mwr']
#         self.narr = timeData['narr']
#         self.sun_azimuth = timeData['sun_azimuth']
#         self.sun_elevation = timeData['sun_elevation']
