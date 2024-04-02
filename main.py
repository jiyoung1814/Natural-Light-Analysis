import os

from dotenv import load_dotenv

from DB.mongoDB import MongoDB
from Functions.Natrual import getDataFromDB, getRequiredData, dataClassifying, dataFiltering, getVerificationDate
from Functions.Excel import saveExcel, saveTxt

from API.Natrual import getDayData
from Graph.ScatterPlot import draw_ampm_scatterplot, draw_ampm_predict_scatter
from Regression.Linear import polynomial_regression_line_data, best_polynomial_linear_regression_model, predict_regression

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
    # field_ys = ['lux']
    # seasons = os.getenv('seasons_names').split(",")
    # seasons = ['경칩', '망종', '한로', '동지']
    seasons = ['상강']
    time_slice = ['am', 'pm']

    # filtering percentage
    top_percentage = 2
    end_percentage = 8

    degree = 5 # 차수
    degrees = [3,4,5]
    intercept = True # y절편 유무

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

                # 맑은날 데이터 필터링 => 상위 p1~p2% 데이터 산출
                filtered_data = dataFiltering(required_data, field_x, field_y, top_percentage=top_percentage,end_percentage=end_percentage, range_x=1)
                filtered_x = [d[field_x] for d in filtered_data]
                filtered_y = [d[field_y] for d in filtered_data]

                # 회귀식 산출
                model = best_polynomial_linear_regression_model(filtered_x, filtered_y, degrees=degrees, intercept=True)

                data_dict['regression'] = model.coef_ + model.intercept_

                # 선정 맑은날 예측
                data_dict['real_datetime'] = [getattr(d, 'datetime') for d in season_test_data[season][time]]
                real_x = [getattr(d, field_x) for d in season_test_data[season][time]]

                if field_y.isdigit():
                    data_dict['real_y'] = [getattr(d, "spd")[field_y]for d in season_test_data[season][time]]
                else:
                    data_dict['real_y'] = [getattr(d, field_y) for d in season_test_data[season][time]]
                data_dict['predict_y'] = predict_regression(real_x, model)

                # # 엑셀에 저장
                # saveExcel(data_dict, os.getenv('save_folder_path'), f"_{season}_{field_x}_{top_percentage}_to_{end_percentage}", f'{field_y}_{time}')

                # text file 저장
                saveTxt(data_dict, os.getenv('save_folder_path') + field_x + "/" +str(top_percentage)+"_"+str(end_percentage) + "/"+ season + "/", f"{field_y}_{time}")


    # # 원하는 절기의 맑은날 광특성 예측
    # data_regression = {}
    #
    # for ampm in categorize_name:
    #     data_dict ={}
    #
    #     # DB로 부터 데이터 추출
    #     db_data = list(mongo.find_data_all(f'{season}_{ampm}'))
    #     required_data = getRequiredData(db_data, [field_x, field_y])
    #     data_dict['x1'] = [d[field_x] for d in required_data]
    #     data_dict['y1'] = [d[field_y] for d in required_data]
    #
    #     # # 이상한 날짜(excluded_24_seasons_dates) 데이터 제거
    #     # excluded_dates = excluded_24_seasons_dates[season][ampm]
    #     # excluded_data = [d for d in required_data if d['datetime'].date() not in [StrToDate(date) for date in excluded_dates]]
    #
    #     # 상위 p% 데이터 산출
    #     filtered_data = getTopPercentageData(required_data, field_x, field_y, top_percentage=top_percentage, end_percentage = end_percentage, range_x=1)
    #     data_dict['x2'] = [d[field_x] for d in filtered_data]
    #     data_dict['y2'] = [d[field_y] for d in filtered_data]
    #
    #     # 회귀식 생성
    #     data_dict['model'] = polynomial_linear_regression(data_dict['x2'], data_dict['y2'], degree, intercept=intercept)
    #     data_dict['x_values'], data_dict['y_predict'], data_dict['equation'] = polynomial_regression_line_data(data_dict['x2'], data_dict['model'])
    #     print(ampm+"_"+field_y+' => '+ data_dict['equation'])
    #
    #     data_regression[ampm] = data_dict
    #
    # draw_ampm_scatterplot(field_x, field_y, data_regression['am'], data_regression['pm'], True)
    #
    # # 원하는 날짜의 데이터 가져오기
    # day_data = getDayData(verification_24_season_dates[season], sunrise_sunset=False)
    #
    # day_info = getDayInfo(verification_24_season_dates[season])
    # print("LwctSunRise: " + DatetimeToStr(day_info.lwctSunRiseTime))
    # print("LwctSunSet: " + DatetimeToStr(day_info.lwctSunSetTime))
    #
    # # ampm으로 나누기
    # day_am_pm_data = {}
    # day_am_pm_data['am'], day_am_pm_data['pm'] = classify_am_pm(day_data)
    #
    # data_verification = {}
    # for ampm in categorize_name:
    #     data_dict = {}
    #     required_data = getRequiredData(day_am_pm_data[ampm], [field_x, field_y])
    #     data_dict['datetime'] = [d['datetime'] for d in required_data]
    #     data_dict['x1'] = [d[field_x] for d in required_data]
    #     data_dict['y1'] = [d[field_y] for d in required_data]
    #
    #     data_dict['x2'] = [d[field_x] for d in required_data]
    #     data_dict['y2'] = predict_regression(data_dict['x1'], data_regression[ampm]['model'])
    #
    #     data_verification[ampm] = data_dict
    #
    #
    # draw_ampm_scatterplot(field_x, field_y, data_verification['am'], data_verification['pm'], False)
    #
    # # for ampm, ampm_data in data_verification.items():
    # #     result = [{'datetime': dt, 'az': az, 'lux': lux, 'predict_lux': predict_lux} for dt, az, lux, predict_lux in
    # #               zip(ampm_data['datetime'], ampm_data['x1'], ampm_data['y1'],ampm_data['y2'])]
    # #
    # #     saveExcel(result, os.getenv('save_folder_path'), f'verification_{season}_{percentage}_{degree}', sheet_name=f'{season}_{ampm}')
    #
    #
    # # # 원하는 절기의 spd 예측
    # # field_ys = [str(w) for w in range(380, 781)]
    # #
    # # # data_regression = {}
    # # # for ampm in categorize_name:
    # # #     data_dict = {}
    # # #
    # # #     # DB로 부터 데이터 추출
    # # #     db_data = list(mongo.find_data_all(f'{season}_{ampm}'))
    # # #
    # # #     data_dict_by_y = {}
    # # #     for field_y in field_ys:
    # # #         required_data = getRequiredData(db_data, [field_x, field_y])
    # # #
    # # #         # 이상한 날짜(excluded_24_seasons_dates) 데이터 제거
    # # #         excluded_dates = excluded_24_seasons_dates[season][ampm]
    # # #         excluded_data = [d for d in required_data if d['datetime'].date() not in [StrToDate(date) for date in excluded_dates]]
    # # #
    # # #         # 상위 p% 데이터 산출
    # # #         filtered_data = getTopPercentageData(excluded_data, field_x, field_y, percentage=percentage, range_x=1)
    # # #         x = [d[field_x] for d in filtered_data]
    # # #         y = [d[field_y] for d in filtered_data]
    # # #
    # # #         # 회귀식 생성
    # # #         data_dict_by_y['model'] = polynomial_linear_regression(x, y, degree, intercept=intercept)
    # # #         print(field_y+'_회귀식 생성: '+polynomial_equation(data_dict_by_y['model']))
    # # #
    # # #         data_dict[field_y] = data_dict_by_y
    # # #
    # # #     data_regression[ampm] = data_dict
    # #
    # #
    # # # 검증 데이터
    # # verification_24_season_dates = {
    # #     "입춘": '2023-01-30',
    # #     "우수": '2020-02-23',  # '2023-03-02' 희망편 '2023-02-25' 절망편
    # #     "경칩": '2023-03-02',  # '2023-03-02' 희망편 '2023-03-05' 절망편
    # #     "소만": '2023-05-15'
    # # }
    # # el = 46
    # #
    # # # 원하는 날짜의 데이터 가져오기
    # # day_data = getDayData(verification_24_season_dates[season], sunrise_sunset=False)
    # #
    # # # ampm으로 나누기
    # # day_am_pm_data = {}
    # # day_am_pm_data['am'], day_am_pm_data['pm'] = classify_am_pm(day_data)
    # #
    # # data_verification = {}
    # # for ampm in categorize_name:
    # #
    # #     # 그 날의 시간별 고도 추출
    # #     el = [d[field_x] for d in day_am_pm_data[ampm]]
    # #
    # #     # 고도 별 spd 추출
    # #     data_dict = {}
    # #     for e in el:
    # #         data = [[day_am_pm_data['spd'][key] for key in field_ys] for d in day_am_pm_data if d[e] == 3]
