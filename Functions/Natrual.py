import os
import numpy as np
import math

from API.Natrual import getAllDayInfoALL, getDayData, getDayInfo
from DTO.DayData import DayData
from Functions.Converter import DatetimeToStr

# 제외할 날짜
EXCLUDED_24_SEASONS_DATES = {
    "입춘": {'am': [], 'pm': []},
    "우수": {'am': [], 'pm': []},
    "경칩": {'am': ['2023-03-13'], 'pm': ['2023-03-13']},
    "춘분": {'am': ['2023-03-14', '2020-03-19', '2020-03-19'], 'pm': ['2023-03-14', '2020-03-19', '2023-03-26']},
    "청명": {'am': ['2022-04-01', '2021-04-02'], "pm": ['2022-04-01', '2021-04-02']},
    "곡우": {'am': [], 'pm': []},
    "입하": {'am': ['2023-05-03'], 'pm': ['2023-05-03']},
    "소만": {'am': [], 'pm': []},
    "망종": {'am': ['2022-06-06'], 'pm': ['2022-06-06']},
    "하지": {'am': [], 'pm': []},
    "소서": {'am': [], 'pm': []},
    "대서": {'am': ['2021-07-17'], 'pm': ['2021-07-17']},
    "입추": {'am': [], 'pm': []},
    "처서": {'am': ['2021-08-19', '2021-08-17'], 'pm': []},
    "백로": {'am': [], 'pm': []},
    "추분": {'am': ['2022-09-16', '2022-09-18', '2019-09-17', '2022-09-25', '2021-09-26'],
           'pm': ['2022-09-16', '2022-09-18', '2021-09-17', '2022-09-21', '2022-09-19', '2022-09-25', '2022-09-23',
                  '2021-09-26']},
    "한로": {'am': ['2019-10-09', '2022-10-08', '2022-10-14', '2021-10-13', '2021-10-10', '2022-10-05', '2022-10-10',
                  '2021-10-09', '2022-10-04'],
           'pm': ['2022-10-08', '2022-10-14', '2022-10-13', '2021-10-13', '2021-10-10', '2022-10-10']},
    "상강": {'am': ['2022-10-21'], 'pm': ['2022-10-21']},
    "입동": {'am': [], 'pm': []},
    "소설": {'am': [], 'pm': []},
    "대설": {'am': ['2022-12-01'], 'pm': []},
    "동지": {'am': [], 'pm': ['2022-12-25', '2022-12-17']},
    "소한": {'am': ['2022-01-13', '2022-01-11'], 'pm': ['2022-01-13', '2022-01-11']},
    "대한": {'am': [], 'pm': []},
}
# 검증 데이터
VERIFICATION_24_SEASONS_DATES = {
    "입춘": '2023-01-30',
    "우수": '2020-02-23',  # 희망편: '2023-03-02', 절망편: '2023-02-25'
    "경칩": '2024-03-10',  # 희망편: '2023-03-02', '2024-03-09','2024-03-10'  절망편: '2023-03-05',
    "춘분": '2023-03-21',  # 희망편: '2023-03-21', 절망편: '2020-03-18'
    "청명": '2020-04-08',  # 희망편: 2020-04-08(3,4~8%), 2022-03-29(오후는 절망), 절망편: 2022-04-04
    "곡우": '',
    "입하": '',
    "소만": '2023-05-15',
    "망종": '2022-05-31',  # 희망편: '2022-05-31', 절망편: 2019-06-03, '2022-05-13'
    "하지": '2019-06-24',
    "소서": '',
    '대서': '',
    '입추': '',
    '처서': '',
    '백로': '',
    '추분': '2019-09-18',  # 희망편: 2019-09-18, 절망편: '2022-09-30'
    '한로': '2019-10-13',  # 희망편: '2022-10-12','2019-10-13',  절망편:
    '상강': '2022-10-18',
    '입동': '',
    '소설': '2023-11-25',  # 희망편: '2023-11-25'
    '대설': '2021-12-13',  # 희망편: 2023-12-01, 약간의 희망: 2021-12-13, 절망편: 2023-12-03, 2023-12-08, 2021-12-05
    '동지': '2022-12-24',  # '2022-12-24', 절망편'2021-12-22',  '2020-12-19'
    '소한': '2023-01-02',  # 약간의 희망: '2023-01-02'
    '대한': '2022-01-18',  # 희망편: '2022-01-18'(오후 데이터 손 봐야함) , 약간의 희망: '2023-01-25'

}


def getDataFromPlatform(sunrise_sunset=True, visual=True, target_seasons=[]):
    '''
    WITLAB Platform으로 부터 데이터 받아옴
    :param sunrise_sunset: Lwct 일출 일몰 적용, False:KASI 일출 일몰 적용
    :param visual: True => 380-780nm, False => 210_400nm
    :param target_seasons: 원하는 절기만 get
    :return: {'season': np.array[DayData, ...]}
    '''

    '''
    DayInfoAll → Judgment 0인 날짜 목록 획득 (해당 날의 절기 & Judgment 값)
    - 절기 별로 날짜 분류
    '''
    all_days_info = getAllDayInfoALL()

    # 절기별 날짜 분류
    days_seasons = classify_24_seasons(all_days_info)
    '''
    DayDataCalc → 타임스탬프 획득 (SPD 획득에 필요한 타임스탬프)
    SPD Real → 파장 데이터 획득 (input : 타임스탬프)
    '''
    # day_data_seasons = {k: np.array([]) for k in os.getenv('seasons_names').split(",")}
    if len(target_seasons) == 0:
        target_seasons = os.getenv('seasons_names').split(",")

    day_data_seasons = {k: np.array([]) for k in target_seasons}
    for key, dates in days_seasons.items():
        if key in target_seasons:
            for d in dates:
                print(d)
                day_data_seasons[key] = np.append(day_data_seasons[key], getDayData(d, sunrise_sunset, visual))
    return day_data_seasons


def getDataFromDB(db, collection):
    '''
    DB로 부터 데이터 추출
    :param db: db Class
    :param collection: collection Name
    :return: np.array[DayData, ...]
    '''
    data_db = list((db.find_data_all(f'{collection}')))

    data = np.array([])
    for d in data_db:
        data = np.append(data, DayData(data=d, source='DB'))

    return data


def classify_24_seasons(days_info, return_only_dates = True):
    '''
    24절기별로 date를 나눔
    :param days_info: np.array([class: DayInfo])
    :return: {season:np.array([dates(class:str)])} or  return_only_dates: False => {season:np.array([Day_info])}
    '''
    seasons_name = os.getenv('seasons_names').split(',')

    days_by_24_season_dic = {k: np.array([]) for k in seasons_name}

    for d_i in days_info:
        if return_only_dates:
            days_by_24_season_dic[d_i.nearSeasonName] = np.append(days_by_24_season_dic[d_i.nearSeasonName], d_i.date)
        else:
            days_by_24_season_dic[d_i.nearSeasonName] = np.append(days_by_24_season_dic[d_i.nearSeasonName], d_i)
    return days_by_24_season_dic


def dataExcluding(data, exclude_dates=[]):
    '''

    :param data: np.array([DayData dict])
    :param exclude_dates: 해당 날짜 데이터 제거
    :return: np.array([DayData dict])
    '''
    exclude_data = np.array([])

    for d in data:
        if DatetimeToStr(d['datetime'], "%Y-%m-%d") not in exclude_dates:
            exclude_data = np.append(exclude_data, d)

    return exclude_data

def dataClassifying(data, timeslice=[]):
    '''
        시간별로 구역 나누기
        :param data: np.array([DayData,...])
        :param timeslice: ex) [am, pm], [am,noon,pm]
        :return: np.array([DayData,...])
        '''
    classify_time_data = {}

    # 시간으로 구간을 나눠서 회귀식 산출
    if len(timeslice) != 0:
        if len(timeslice) == 2:
            classify_time_data = classify_am_pm(data)
        elif len(timeslice) == 3:
            classify_time_data = classify_am_noon_pm(data)
    else:
        classify_time_data['total'] = data

    return classify_time_data


def classify_am_pm(data):
    '''
    방위각 기준으로 오전 오후 데이터를 나눔
    :param data: np.array([Daydata,...])
    :return: dict{'am':(np.array([Daydata,...])),'pm':(np.array([Daydata,...]))}
    '''
    am = np.array([])
    pm = np.array([])

    over = 10.0

    for d in data:
        try:
            if d.azimuth < float(os.getenv('noon_az')) + over:
                am = np.append(am, d)
            if (float(os.getenv('noon_az')) - over) <= d.azimuth:
                pm = np.append(pm, d)
        except Exception as e:
            print(f'classify_am_pm Error - {d.datetime}: {e}')

    return {'am': am, 'pm': pm}

def classify_am_noon_pm(data):
    '''
    오전 정오 오후 데이터를 나눔
    오전 => el:0~(max_el -5) & az < 180
    오후 => el:0~(max_el -5) & az > 180
    정오 => 나머지
    max_el : 절기의 모든날의 최대 고도 중 가장 낮은 고도
    :param data:
    :return:
    '''

    # 절기의 모든날
    dates = list(set(DatetimeToStr(getattr(d, 'datetime').date(), "%Y-%m-%d") for d in data))

    # 시즌의 모든 날짜의 최고 고도를 구한 후 그 고도들 중 가장 낮은 고도 산출
    max_el = min(getattr(getDayInfo(date), "highestEl") for date in dates)

    am = np.array([])
    pm = np.array([])
    noon = np.array([])

    for d in data:
        try:
            if 0 <= d.elevation:
                if d.elevation < max_el-5.0:
                    if d.azimuth< 180:
                        am = np.append(am, d)
                    else:
                        pm = np.append(pm, d)
                else:
                    noon = np.append(noon, d)
        except Exception as e:
            print(f'classify_am_noon_pm Error - {d.datetime}: {e}')

    return {'am': am, 'noon': noon, 'pm': pm}




def saveDataFromPlatform(db, data, am_pm=True):
    '''
    Natural DayData from Platform 몽고 DB에 저장
    :param db: db Class
    :param data: {'season_name': np.array([DayData, ...])},
    :param am_pm: True: am_pm 나누어 저장, False: 한꺼번에 저장
    :return:
    '''
    for season, value in data.items():
        if am_pm:
            am, pm = classify_am_pm(value)
            try:
                db.save_data(f'{season}_am', am.tolist())
                db.save_data(f'{season}_pm', pm.tolist())

            except Exception as e:
                print(f'saveDataFromPlatform Error - {season} data 저장 : {e}')
        else:
            db.save_data(f'{season}', value)

        print(f'{season} data 저장')


def getRequiredData(data, elements, essential=['datetime']):
    '''
    필요한 요소들로만 DayDaty dict
    :param data: np.array([DayData, ...])
    :param elements: require한 요소들
    :param essential: 기본 요소들 list ex) defalt: ['datetime']
    :return: np.array([DayData Dict])
    '''
    required_datas = []
    for d in data:
        filtered_data = {}
        for ee in essential:
            filtered_data[ee] = getattr(d, ee)

        for e in elements:
            if e.isdigit():
                filtered_data[e] = getattr(d, "spd")[e]
            else:
                filtered_data[e] = getattr(d, e)
        required_datas.append(filtered_data)
    return required_datas


def dataFiltering(data, element_x, element_y, start_percentage=2, end_percentage=8, range_x=1, top=True):
    '''
    x축의 range 내의 상위 p% 데이터 산출 ex) elevation 0~1, 1~2 ... 의 상위 2~8% 데이터 (range_x == 1)
    :param data: np.array([DayData dict,...])
    :param field_x: x축
    :param field_y: y축
    :param start_percentage: 상위 percentage
    :param end_percentage: 하위 percentage
    :param range_x: x축 range
    :param top: True = 상위 or False = 하위
    :return: np.array([DayData dict,...])
    '''

    min_x = int(min(data, key=lambda x: x[element_x])[element_x])
    max_x = int(round(max(data, key=lambda x: x[element_x])[element_x], range_x))

    filtered_data = np.array([])
    for x in range(min_x, max_x, range_x):
        # x축 range 범위 데이터 추출
        filtered_by_x_data = [d for d in data if x <= d[element_x] < x + 1]


        if top is True:
            # y축 상위 p% 데이터 추출
            y_values = [d[element_y] for d in filtered_by_x_data]
            upper_threshold = np.percentile(y_values, 100 - start_percentage)
            lower_threshold = np.percentile(y_values, 100 - end_percentage)
        else:
            y_values = [d[element_y] for d in filtered_by_x_data]
            lower_threshold = np.percentile(y_values, start_percentage)
            upper_threshold = np.percentile(y_values, end_percentage)
        # print(f'{x}:{lower_threshold} {upper_threshold} ~ ')

        extracted_data = [d for d in filtered_by_x_data if lower_threshold <= d[element_y] <= upper_threshold]
        filtered_data = np.append(filtered_data, extracted_data)

    return filtered_data


def getVerificationDate(season):
    return VERIFICATION_24_SEASONS_DATES[season]
