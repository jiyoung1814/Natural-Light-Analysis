from dotenv import load_dotenv
import numpy as np
from DB.mongoDB import MongoDB
from Functions.Natrual import dataClassifying, getRequiredData, dataFiltering, getDataFromDB,  dataExcluding
from Graph.ScatterPlot import draw_satellite_scatterplot


if __name__ == '__main__':
    load_dotenv()

    # seasons = ['경칩', '추분', '동지', '하지']
    seasons = ['추분']
    # seasons = os.getenv('seasons_names').split(',')
    field_x = 'elevation'
    essential = ['datetime']
    time_slice = ['am', 'pm']

    field_ys = ['lux']

    # filtering percentage
    start_percentage = 2
    end_percentage = 8

    # filter_ys를 기반으로 필터링
    filter_ys = ['gkb01_kc','gkb02_kc','gkb03_kc','gkb04_kc','gkb05_kc','gkb06_kc','gkb07_kc','gkb08_kc','gkb09_kc',
                 'gkb10_kc','gkb11_kc','gkb12_kc','gkb13_kc','gkb14_kc','gkb15_kc','gkb16_kc']

    # satellite filtering percentage
    s_start_percentage = 0
    s_end_percentage = 10

    satellite_threshold = {"gkb01_kc" : 0,"gkb02_kc" : 0,"gkb03_kc" : 40,"gkb04_kc" : 0,"gkb05_kc" : 0,  # 임계 값이 정해져 있음 ex) gkb03_kc >= 40 정상 데이터
                           "gkb06_kc" : 0,"gkb07_kc" : 0,"gkb08_kc" : 0,"gkb09_kc" : 0, "gkb10_kc" : 0,
                           "gkb11_kc" : 0, "gkb12_kc" : 0, "gkb13_kc" : 0, "gkb14_kc" : 0, "gkb15_kc" : 0, "gkb16_kc" : 0}

    exclude_dates = [
        '2020-09-23', '2020-09-24', '2020-09-25', '2020-09-26', '2020-09-27', '2020-09-28', '2020-09-29', '2020-09-30','2022-09-21'
    ]


    # field_y percentage
    f_start_percentage = 0
    f_end_percentage = 100
    f_step_percentage = 10

    # -----DB-----
    # mongoDB 연결
    mongo = MongoDB()
    mongo.connect_DB()


    for season in seasons:
        season_data = getDataFromDB(mongo, f'{season}')

        classified_data = dataClassifying(season_data, timeslice=time_slice)

        classified_time_data = {}
        for time, time_data in classified_data.items():

            data_dict = {}
            required_data = getRequiredData(time_data, [field_x] + field_ys +filter_ys)
            exclude_data = dataExcluding(required_data, exclude_dates)

            filtered_p_data = {}
            for p in range(f_start_percentage, f_end_percentage, f_step_percentage):
                filtered_p_data[p] = dataFiltering(exclude_data, field_x, field_ys[0], start_percentage=p, end_percentage=(p + 10), range_x=1, top=True)

            # draw_satellite_scatterplot(field_x, filter_ys, filtered_p_data)

            draw_satellite_scatterplot(field_x, ['lux', filter_ys[0]], filtered_p_data)

            for i in range(0, len(filter_ys), 2):
                draw_satellite_scatterplot(field_x, [filter_ys[i], filter_ys[i+1]], filtered_p_data)
            break

