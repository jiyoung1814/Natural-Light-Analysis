from dotenv import load_dotenv
from DB.mongoDB import MongoDB
import numpy as np

from Functions.Satellite import getSeasonDateFromDataPlatform, saveDBSatelliteImageFromDataPlatform
from Functions.Satellite import getSatelliteImageFromDataPlatform, getKNUNearImage, getDaySatelliteImageFromDataPlatform, saveSatelliteImage\
                                , ShowImage, ImageResize, getDaySatelliteImageFromDataPlatform\
                                ,getSatelliteImageFromDB, getDaysSatelliteImageFromDB, getDiffPixelWithNextTimeImage

from Functions.Converter import TimestampToDatetime

if __name__ == '__main__':
    load_dotenv()

    mongo = MongoDB()
    mongo.connect_DB('Satellite')

    channels = [4]

    seasons = ['경칩']

    mode = 'save_DB'
    source = "DB" #DB, DataPlatform

    if mode == 'save_DB':
        for season in seasons:
            dates = getSeasonDateFromDataPlatform(season)
            for ch in channels:
                print(f'--------------ch{ch}--------------')
                for d in dates:
                    print(d)
                    saveDBSatelliteImageFromDataPlatform(mongo, f"{season}_{ch}", d, ch)

    elif mode =='test':
        dates = ['2024-03-03', '2024-03-04', '2024-03-05', '2024-03-06', '2024-03-07','2024-03-08', '2024-03-09', '2024-03-10']
        datetimes = ['2024-03-10 10:46:00', '2024-03-10 10:48:00', '2024-03-10 10:50:00', '2024-03-10 10:52:00']
        datetimes = ['2024-03-10 10:46:00', '2024-03-10 10:48:00', '2024-03-10 10:50:00', '2024-03-10 10:52:00']


        # for ch in channels:
        #     near_images_by_dt = []
        #     for dt in datetimes:
        #         image = getSatelliteImageFromDataPlatform(dt, ch)
        #         image = getKNUNearImage(image)
        #
        #         near_images_by_dt.append(np.array(image.knu_near_image))
        #
        #         # # image resize
        #         # img = np.array(image.knu_near_image)
        #         # ShowImage(img)
        #         # img = ImageResize(np.array(image.knu_near_image).astype(np.uint16), 256, method="Bicubic")
        #         # ShowImage(img)
        #
        #     diff_near_images_by_dt = []
        #     for i, dt in enumerate(datetimes[:len(datetimes)-1]):
        #         print(f"{np.mean(np.abs(near_images_by_dt[i] - near_images_by_dt[i+1]))}")



        for ch in channels:
            for date in dates:
                day_satellite_image = None
                if source == "DB":
                    print(date)
                    day_satellite_image = getDaysSatelliteImageFromDB(mongo, f"{seasons[0]}_{ch}", f"{date} 00:00:00", f"{date} 23:59:59", "timestamp")
                elif source == "DataPlatform":
                    day_satellite_image = getDaySatelliteImageFromDataPlatform(date, ch, sunrise_sunset=True)

                # 위성 이미지 정렬을 위해 다음 시간의 이미지와 픽셀 차이의 평균
                getDiffPixelWithNextTimeImage(day_satellite_image)





    # for season in seasons:
    #     # dates = getSeasonDateFromDataPlatform(season)
    #     for ch in channels:
    #         print(f'--------------ch{ch}--------------')
    #         for d in dates:
    #             print(d)
    #             day_satellite_image = getDaySatelliteImageFromDataPlatform(d, ch, sunrise_sunset=True)
    #             # saveSatelliteImage(mongo, season, day_satellite_image, True)
