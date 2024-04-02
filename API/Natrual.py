import os, sys
import requests
import json
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from HMACSHA256.hmacsha256 import setHeaders
from DTO.DayInfo import DayInfo
from DTO.DayData import DayData


def getAllDayInfoALL(judgment=True):
    '''
    서버에 보유하고 있는 모든 Day Info 정보 요청.
    :param judgment: Judgment 0인 날짜 목록만 추출 여부(True: 0인 날짜만, False: 모든 날짜)
    :return: (class: np.array[DayInfo Classes])
    '''

    headers = setHeaders()
    response = requests.get(os.getenv('url') + 'v2/natural/day_info_all', headers=headers).json()

    days = []
    for d in response:

        d_i = DayInfo(d)

        try:
            if judgment:
                if d_i.judgment == 0:
                    days.append(d_i)
            else:
                days.append(d_i)

        except Exception as e:
            print(f'getAllDayInfoALL Error: '+e)

    return np.array(days)


def getDayInfo(date):
    '''
    서버에 보유하고 있는 계산 기반의 Day Data 중 하루 정보 요청
    :param date: 요청날짜(class: Str) ex) "2024-01-05"
    :param sunrise_sunset: Lwct 일출 일몰 적용 여부, false면 KASI 일출 일몰 적용
    :return:
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
    data = {'parameter1': date}
    data_json = json.dumps(data).encode('utf-8')

    headers = setHeaders()
    response = requests.get(os.getenv('url') + 'v2/natural/day_info', headers=headers, data=data_json)

    dayInfo = DayInfo(response.json())

    return dayInfo

def getDayData(date, sunrise_sunset=True, visual = True):
    '''

    :param date:
    :param sunrise_sunset:True: Lwct 일출 일몰 적용, False:KASI 일출 일몰 적용
    :param visual:
    :return:
    '''

    # 타임스탬프 획득 (SPD 획득에 필요한 타임스탬프)
    day_data = getDayDataCalc(date, sunrise_sunset)
    for data in day_data:
        spd, intgtime = getSPD(data.timestamp, visual)
        data.setSPD(spd)
        data.setIntgrationTime(intgtime)
    return day_data


def getDayDataCalc(date, sunrise_sunset=True):
    '''
    서버에 보유하고 있는 계산 기반의 Day Data 중 하루 정보 요청.
    :param date:
    :param sunrise_sunset: True: Lwct 일출 일몰 적용, False:KASI 일출 일몰 적용
    :return: np.array([DayData, ...])
    '''

    data = {'parameter1': date,
            "parameter2": sunrise_sunset
            }

    response = requests.get(os.getenv('url') + 'v2/natural/day_calc', headers=setHeaders(), data=json.dumps(data).encode('utf-8'))

    dayData_arr = np.array([])
    for time_data in response.json():
        dayData = DayData(time_data, source='Platform')
        dayData_arr = np.append(dayData_arr, dayData)
    return dayData_arr


def getSPD(ts, visual= True):

    '''
    서버에 과거 측정된 SPD 데이터를 요청

    :param ts:
    :param visual: 받은 파장 범위(True: "spD_380_780":, False: spD_210_400)
    :return: {wavelenght: spd}, intgtime

    res = >
    {
        "timestamp":1704408287000,
        "dt":"2024-01-05T07:44:47",
        "integrationTime":1000,
        "spD_210_400":
        [
            2.1221184239519514E-05,  // 210nm
            4.9341748760902506E-06,  // 211nm
            2.1763743798734427E-07,  // 212nm
            1.4822960501520758E-05,  // 213nm
            -4.841132557843429E-06,  // 214nm
            3.577957744918843E-06,   // 215nm
            ...
            0.00032525693772177686,  // 398nm
            0.00038515641588522664,  // 399nm
            0.00043088212385203095   // 400nm
        ],
        "spD_380_780":
        [
            0.00028457581890880293,  // 380nm
            0.00027179975896975166,  // 381nm
            0.00024010871549444836,  // 382nm
            0.00020953043273801652,  // 383nm
            0.0002204233913431461,   // 384nm
            0.000249117910523435,    // 385nm
            ...
            0.00030907749727656736,  // 778nm
            0.0003076529392071561,   // 779nm
            0.0003107191248866715    // 780nm
        ]
    }
    '''


    data = {'parameter1': ts}

    response = requests.get(os.getenv('url') + 'v2/natural/spd_real', headers=setHeaders(), data=json.dumps(data).encode('utf-8'))

    if visual is True:
        spd ={str(w): s for w, s in zip(range(380, 781), response.json()['spD_380_780'])}
    else:
        spd = {str(w): s for w, s in zip(range(210, 400), response.json()['spD_210_400'])}

    intgtime = response.json()['integrationTime']

    return spd, intgtime
