import os
from dotenv import load_dotenv

from DB.mongoDB import MongoDB
from Functions.Natrual import getDataFromDB, getRequiredData, dataClassifying, dataFiltering, getVerificationDate

from API.Natrual import getDayData, getDayInfo
from Graph.ScatterPlot import draw_ampm_scatterplot, draw_ampm_predict_scatter, draw_am_noon_pm_scatterplot, draw_am_noon_pm_predict_scatter
from Regression.Linear import polynomial_regression_line_data, best_polynomial_linear_regression_model, predict_regression, evaluation_model

if __name__ == '__main__':
    load_dotenv()
    mongo = MongoDB()
    mongo.connect_DB()

    # # DB에 DataFromPlatform 데이터 저장
    # natural_data = getDataFromPlatform(sunrise_sunset=False)
    # saveDataFromPlatform(db=mongo, data=natural_data, am_pm=True)

    # # 24절기별로 엑셀에 저장
    # 1. mongo에서 데이터
    # 2. 필요 데이터만 추출(필요한 field 만 추출)
    # 3. p% 데이터만 추출
    # 4. 엑셀에 저장

    # seasons_names = os.getenv('seasons_names').split(',')
    # categorize_name = ['am', 'pm']
    #
    # field_x = 'el'
    # fields_y = ['lux', '380', '580', '780']
    # percentage = 5
    # for field_y in fields_y:
    #     for season in seasons_names:
    #         for ampm in categorize_name:
    #
    #             # db에서 데이터 조회
    #             db_data = list(mongo.find_data_all(f'{season}_{ampm}'))
    #
    #             # 필요 데이터만 retrun(datetime, lement_x, element_y)
    #             required_data = getRequiredData(db_data, [field_x, field_y])
    #
    #             # saveExcel(data=required_data, path=os.getenv('save_folder_path'), file_name=f'{field_x}_{field_y}_{percentage}', sheet_name=f'{season}_{ampm}')
    #             filtered_data = getTopPercentageData(required_data, field_x, field_y, percentage=percentage, range_x=1)
    #             saveExcel(data=filtered_data, path=os.getenv('save_folder_path'), file_name= f'filtered_{field_x}_{field_y}_{percentage}', sheet_name=f'{season}_{ampm}')
    #
    #         print(f'{season}_저장 완료')

    field_x = 'elevation'
    field_ys = [str(w) for w in range(380, 781)]
    field_ys = ['lux']
    # seasons = os.getenv('seasons_names').split(",")
    # seasons = ['경칩', '망종', '한로', '동지']
    seasons = ['경칩']
    time_slice = ['am', 'noon', 'pm']

    # filtering percentage
    top_percentage = 2
    end_percentage = 8

    degree = 5  # 차수
    degrees = [3, 4, 5]
    intercept = True  # y절편 유무

    day_info = getDayInfo(getVerificationDate(seasons[0]))
    print(day_info.lwctSunRiseTime)
    print(day_info.lwctSunSetTime)

    # test data
    season_test_data = {}
    for season in seasons:
        day_data = getDayData(getVerificationDate(season), sunrise_sunset=False, visual=True)
        season_test_data[season] = dataClassifying(day_data, timeslice=time_slice)

    season_data = {}
    for season in seasons:
        # season 별 데이터 산출
        db_data = getDataFromDB(mongo, f'{season}')

        # 시간 구간 별로 데이터 나누기
        classified_data = dataClassifying(db_data, timeslice=time_slice)

        field_y_data = {}
        for field_y in field_ys:

            classified_time_data = {}
            for time, time_classified_data in classified_data.items():
                data_dict = {}

                required_data = getRequiredData(time_classified_data, [field_x, field_y])
                data_dict['datetime'] = [d["datetime"] for d in required_data]
                data_dict['x'] = [d[field_x] for d in required_data]
                data_dict['y'] = [d[field_y] for d in required_data]

                # 맑은날 데이터 필터링 => 상위 p1~p2% 데이터 산출
                filtered_data = dataFiltering(required_data, field_x, field_y, top_percentage=top_percentage,
                                              end_percentage=end_percentage, range_x=1)
                data_dict['filtered_x'] = [d[field_x] for d in filtered_data]
                data_dict['filtered_y'] = [d[field_y] for d in filtered_data]

                # 회귀식 산출
                model = best_polynomial_linear_regression_model(data_dict['filtered_x'], data_dict['filtered_y'],
                                                                degrees=degrees, intercept=True)
                # 회귀식 그래프에 나타낼때 필요한 데이터
                data_dict['x_values'], data_dict['y_predict'], data_dict['equation'] = polynomial_regression_line_data(
                    data_dict['filtered_x'], model)
                data_dict['regression'] = model.coef_ + model.intercept_

                # 선정 맑은날 예측
                data_dict['real_datetime'] = [getattr(d, 'datetime') for d in season_test_data[season][time]]
                data_dict['real_x'] = [getattr(d, field_x) for d in season_test_data[season][time]]
                if field_y.isdigit():
                    data_dict['real_y'] = [getattr(d, "spd")[field_y] for d in season_test_data[season][time]]
                else:
                    data_dict['real_y'] = [getattr(d, field_y) for d in season_test_data[season][time]]
                data_dict['predict_y'] = predict_regression(data_dict['real_x'], model)

                print(f"{season}_{field_y}_{time}_MAE: " + str(
                    round(evaluation_model(data_dict['real_y'], data_dict['predict_y'], evaluation_type="MAE"), 2)))

                # 엑셀에 저장
                # saveExcel(data_dict, os.getenv('save_folder_path'), f"_{season}_{field_x}_{top_percentage}_to_{end_percentage}", f'{field_y}_{time}')
                # saveTxt(data_dict, os.getenv('save_folder_path')+field_x+"/"+season+"/", f"{field_y}_{time}")

                classified_time_data[time] = data_dict
            field_y_data[field_y] = classified_time_data
        season_data[season] = field_y_data

    season = seasons[0]
    field_y = 'lux'

    if len(time_slice) == 2:
        draw_ampm_scatterplot(field_x, field_y, season_data[season][field_y]['am'], season_data[season][field_y]['pm'],True)
        draw_ampm_predict_scatter(field_x, field_y, season_data[season][field_y]['am'], season_data[season][field_y]['pm'])
        mae = evaluation_model(season_data[season][field_y]['am']['real_y'] + season_data[season][field_y]['pm']['real_y'],
                               season_data[season][field_y]['am']['predict_y'].tolist() +
                               season_data[season][field_y]['pm']['predict_y'].tolist()
                               , evaluation_type="MAE")
        print(f"{season}_{field_y}_total_MAE: " + str(round(mae, 2)))

    else:
        draw_am_noon_pm_scatterplot(field_x, field_y, season_data[season][field_y]['am'], season_data[season][field_y]['noon'], season_data[season][field_y]['pm'],True)
        draw_am_noon_pm_predict_scatter(field_x, field_y, season_data[season][field_y]['am'], season_data[season][field_y]['noon'], season_data[season][field_y]['pm'])


