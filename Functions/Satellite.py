import numpy as np
from datetime import datetime

from Functions.Converter import TimestampToDatetime, StrToDatetime, DatetimeToTimestamp, DatetimeToStr, class_to_dict
from Functions.Natrual import classify_24_seasons

from API.Natrual import getDayInfo, getAllDayInfoALL
from API.Satellite import getSatelliteDayTimeList, getSatelliteImage

from DTO.SatelliteData import SatelliteData

import matplotlib.pyplot as plt
import cv2

KNU_NEAR_IMAGE_SIZE_BY_CHANNEL = {
    "LE1_01_VI004": 256,
    "LE1_02_VI005": 256,
    "LE1_03_VI006": 512,
    "LE1_04_VI008": 256,
}

KNU_X_Y_PIXEL_BY_RESOLUTION = {
    "0.5": [2000, 2047],
    "1.0": [1000, 1023],
    "2.0": [500, 511]
}


def getSatelliteImageFromDataPlatform(ts, l):
    """
    자연광 서버로 부터 datetime의 위성 이미지 데이터 요청
    :param ts: 요청 datetime의 ts => dt형태라면 ts로 변환 가능
    :param l: 요청 채널(class: Str) ex) lv1 : "1"~"16", lv2: "COT", ...
    :return: SatelliteData Class
    """

    if isinstance(ts, datetime):
        ts = DatetimeToTimestamp(ts)
    elif isinstance(ts, str):
        ts = DatetimeToTimestamp(StrToDatetime(ts))

    s_i = SatelliteData(getSatelliteImage(ts, l))

    return s_i


def getDaySatelliteImageFromDataPlatform(d, l, sunrise_sunset=True):
    """
    서버에 보유하고 있는 계산 기반의 Day data 중 하루 위성 데이터 반환
    :param d: 요청날짜(class: Str) ex) "2024-01-05"
    :param l: 요청 채널(class: Str) ex) lv1 : "1"~"16", lv2: "COT", ...
    :param source: 요청 위치 ex) Platform, DB
    :param sunrise_sunset: CCT 기준 일출 일몰까지 data load 여부 (True: 일출~일몰, False: 서버 저장 시간)
    :return: class np.array([Satellite Classes])
    """
    days = []

    ts_list = getSatelliteDayTimeList(d, l)

    d_i = getDayInfo(d)  # 요청 날짜 meta data get => 일출 일몰 시각

    i = 0
    for ts in ts_list:
        if sunrise_sunset:  # 일출 일몰 시간만 get
            if d_i.lwctSunRiseTime > TimestampToDatetime(ts) or TimestampToDatetime(ts) > d_i.lwctSunSetTime:
                continue

        # i += 1
        # if i < 200:
        #     continue

        print(f'- {TimestampToDatetime(ts)}')
        s_i = SatelliteData(getSatelliteImage(ts, l))

        # 공주대 근처 픽셀값 추출 ( ex) 256*256 pixels)
        s_i = getKNUNearImage(s_i)
        days.append(s_i)
        # break

        # if i==5:break

    return np.array(days)


def saveDBSatelliteImageFromDataPlatform(db, collection, d, l, sunrise_sunset=True, all_pixels=False):
    '''
    Dataplatform 기반 위성 이미지 데이터 몽고 DB에 저장
    :param db: db Class
    :param collection: db collection
    :param d: 요청날짜(class: Str) ex) "2024-01-05"
    :param l: 요청 채널(class: Str) ex) lv1 : "1"~"16", lv2: "COT", ...
    :param sunrise_sunset: CCT 기준 일출 일몰까지 data load 여부 (True: 일출~일몰, False: 서버 저장 시간)
    :param all_pixels: 모든 픽셀을 저장할껀지 아니면 공주대 근처만 저장할껀지 (True: 모든 픽셀, False: 공주대 근처 픽셀만)
    :return:
    '''

    ts_list = getSatelliteDayTimeList(d, l)

    d_i = getDayInfo(d)  # 요청 날짜 meta data get => 일출 일몰 시각

    i = 0
    for ts in ts_list:

        if sunrise_sunset:  # 일출 일몰 시간만 get
            if d_i.lwctSunRiseTime > TimestampToDatetime(ts) or TimestampToDatetime(ts) > d_i.lwctSunSetTime:
                continue
        if db.check_unique_data(collection, 'timestamp', ts):  # DB에 동일한 값이 있는지 없는지 확인
            print(f'- {TimestampToDatetime(ts)}')
            s_i = getSatelliteImageFromDataPlatform(ts, l)

            if not all_pixels:
                s_i = getKNUNearImage(s_i)  # 공주대 근처 픽셀값 추출 ( ex) 256*256 pixels)

            # db에 저장
            s_i_dict = class_to_dict(s_i)
            if not all_pixels:
                del s_i_dict['array']

            db.save_data(collection, s_i_dict)


def getSeasonDateFromDataPlatform(season):
    """
    자연광 서버에 저장 되어 있는 절기의 날짜 리스트
    :param season: 원하는 절기 입력
    :return: np.array([Str Dates])
    """
    all_days_info = getAllDayInfoALL()
    days_seasons = classify_24_seasons(all_days_info)

    return days_seasons[season]


def getSatelliteImageFromDB(db, collection):
    data = list((db.find_data_all(f'{collection}')))

    days_data = []
    for d in data:
        days_data.append(SatelliteData(d))

    return np.array(days_data)


def getDaysSatelliteImageFromDB(db, collection, start_date, end_date, field):

    if field == "timestamp":
        start_date = DatetimeToTimestamp(start_date)
        end_date = DatetimeToTimestamp(end_date)

    data = list((db.find_data_between_fields(f'{collection}', start_date, end_date, field)))

    days_data = []
    for d in data:
        days_data.append(SatelliteData(d))

    return np.array(days_data)


def getKNUNearImage(data):
    """
    공주대학교 근처 2차원 픽셀 배열 반환
    :param data: SatelliteDataClass
    :return: SatelliteDataClass  Class에 근처 픽셀값이 추가됨 knu_near_image
    """

    image = np.array(data.array)

    image_size = KNU_NEAR_IMAGE_SIZE_BY_CHANNEL[data.type]

    knu_x = KNU_X_Y_PIXEL_BY_RESOLUTION[data.meta.channel_spatial_resolution][0]
    knu_y = KNU_X_Y_PIXEL_BY_RESOLUTION[data.meta.channel_spatial_resolution][1]

    start_x = knu_x - int(image_size / 2)
    end_x = knu_x + int(image_size / 2)
    start_y = knu_y - int(image_size / 2)
    end_y = knu_y + int(image_size / 2)

    data.setKNUNearImage(image[start_y:end_y, start_x:end_x].tolist())

    # plt.imshow(data.knu_near_image, cmap='gray', vmin=0, vmax=1000)
    # # plt.colorbar()
    # plt.plot(int(image_size / 2), int(image_size / 2), 'r+', markersize=5)
    # plt.axis('off')  # Hide axis
    # plt.show()

    return data


# showImage
def ShowImage(image):
    """

    :param image:
    :return:
    """

    image_size = image.shape[0]

    plt.imshow(image, cmap='gray', vmin=0, vmax=500)
    # plt.colorbar()
    if image_size in [128, 256, 512]:
        plt.plot(int(image_size / 2), int(image_size / 2), 'r+', markersize=5)
    plt.axis('off')  # Hide axis
    plt.show()


# preprocessing
def ImageResize(image, desired_size=256, method="Lanczos"):
    """
    위성이미지의 크기가 채널마다 다르기 때문에 원하는 픽셀 수로 이미지 크기 조정
    :param image: np.array([][])
    :param desired_size: 256
    :param method: resizing 방법
    :return: np.array([][])
    """

    image_size = image.shape[1]

    if image_size > desired_size:  # 이미지 축소
        if method == "Lanczos":  # Lanczos 보간법
            resized_image = cv2.resize(image, (desired_size, desired_size), interpolation=cv2.INTER_LANCZOS4)

    elif image_size < desired_size:  # 이미지 확대
        if method == "Bicubic":  # 양삼차 보간법(Bicubic Interpolation) => 확대에 주로 사용
            resized_image = cv2.resize(image, (desired_size, desired_size), interpolation=cv2.INTER_CUBIC)
        # resized_image = image.resize(desired_size, Image.BICUBIC)
    else:
        resized_image = image

    return resized_image


def saveSatelliteImage(db, collection, data, all_pixels=False):
    '''
    Dataplatform 기반 위성 이미지 데이터 몽고 DB에 저장
    :param db: db Class
    :param collection: db collection
    :param data: 하루 SatelliteData Class 배열 => np.array([Satellite Data Class, ...])
    :param all_pixels: 모든 픽셀을 저장할껀지 아니면 공주대 근처만 저장할껀지 (True: 모든 픽셀, False: 공주대 근처 픽셀만)
    :return:
    '''

    db_data = []

    for d in data:
        data_dict = class_to_dict(d)
        if not all_pixels:
            del data_dict['array']

        db_data.append(data_dict)

    db.save_data(collection, np.array(db_data))


#analysis
def getDiffPixelWithNextTimeImage(data):
    """
    위성 이미지 정렬을 위해 다음 시간의 이미지와 픽셀 차이의 평균
    :param data: np.array([SatelliteData , ...])
    :return:
    """
    near_images_by_dt = []
    dt = []

    for i in range(len(data) - 1):
        dt.append(DatetimeToStr(TimestampToDatetime(data[i].timestamp)))
        near_images_by_dt.append(np.mean(np.abs(
            np.array(data[i].knu_near_image) - np.array(data[i + 1].knu_near_image))))

    print(dt)
    print(near_images_by_dt)
    print("-------------------------------------------------")