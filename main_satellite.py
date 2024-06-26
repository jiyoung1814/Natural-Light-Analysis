from dotenv import load_dotenv
import os
from DB.mongoDB import MongoDB
from Functions.Natrual import getDayData, getDataFromPlatform, dataClassifying, getRequiredData, dataFiltering, getDataFromDB, saveDataFromPlatform, getVerificationDate, dataExcluding
from Functions.File import saveExcel, saveTxt
from Regression.Linear import best_polynomial_linear_regression_model, predict_regression, polynomial_regression_line_data
from Graph.ScatterPlot import draw_ampm_scatterplot,draw_ampm_predict_scatter

from API.Natrual import get_satellite

if __name__ == '__main__':
    load_dotenv()

    # datetime = ['202002282110']
    # get_satellite(datetime)

    seasons = ['경칩', '추분', '동지', '하지']
    # seasons = os.getenv('seasons_names').split(',')
    field_x = 'elevation'
    essential = ['datetime']
    time_slice = ['am', 'pm']

    field_ys = ['640']
    # field_ys = [str(w) for w in range(380, 781)]

    # filtering percentage
    start_percentage = 2
    end_percentage = 8

    filter_ys = ['le03']  # filter_ys를 기반으로 필터링
    # satellite filtering percentage
    s_start_percentage = 0
    s_end_percentage = 10

    exclude_dates = ['2021-03-13', '2021-03-10', '2022-03-09', '2021-03-05', '2022-03-08', '2021-03-08']

    # -----학습-----
    # 다항 회귀
    degrees = [3, 4, 5]
    intercept = True  # y절편 유무
    # test data
    season_test_data = {}
    # for season in seasons:
    #     day_data = getDayData(getVerificationDate(season), sunrise_sunset=True, visual=True)
    #     season_test_data[season] = dataClassifying(day_data, timeslice=time_slice)


    mode = 'save_DB' # 그래프 그리거나(graph) 데이터 저장하거나(save_filtering or save_regression or save_raw), API에서 데이터 받아서 DB에 저장(save_DB)


    # -----DB-----
    # mongoDB 연결
    mongo = MongoDB()
    mongo.connect_DB()

    if mode =='save_DB': # # DB에 데이터 저장
        data = getDataFromPlatform(sunrise_sunset=False, visual=True, target_seasons = seasons)
        saveDataFromPlatform(db=mongo, data=data, am_pm=False)

    else:

        for season in seasons:
            season_data = getDataFromDB(mongo, f'{season}')

            classified_data = dataClassifying(season_data, timeslice=time_slice)

            for filter_y in filter_ys:

                classified_time_data={}
                for time, time_data in classified_data.items():
                    data_dict = {}
                    required_data = getRequiredData(time_data, [field_x, filter_y]+field_ys)
                    if mode == 'save_raw': # raw Data 저장
                        data_dict['datetime'] = [d["datetime"] for d in required_data]
                        data_dict[field_x] = [d[field_x] for d in required_data]
                        data_dict[filter_y] = [d[filter_y] for d in required_data]
                        for field_y in field_ys:
                            data_dict[field_y] = [d[field_y] for d in required_data]
                        saveExcel(data_dict, os.getenv('save_folder_path')+f'satellite/',f"satellite_{season}_{field_x}_{filter_y}_raw_", f'{filter_y}_{field_y}_{time}')
                        data_dict={}
                        continue

                    # filtering
                    satellite_cols = ["le", "ct"]
                    if any(col in filter_y for col in satellite_cols):  # satellite data => 하위 0~8%

                        if satellite_cols[0] in filter_y: # 맑은날이 40부터?
                            preprocessed_data = [d for d in required_data if d[filter_y] >= 40]
                        filtered_data = dataFiltering(preprocessed_data, field_x, filter_y, start_percentage=s_start_percentage, end_percentage=s_end_percentage, range_x=1, top=False)

                    else:  # natural data => 상위 2~8%
                        filtered_data = dataFiltering(required_data, field_x, filter_y, start_percentage=start_percentage, end_percentage=end_percentage, range_x=1, top=True)

                    exclude_data = dataExcluding(filtered_data, exclude_dates)

                    for e in essential:
                        data_dict[f'filtered_{e}'] = [d[e] for d in exclude_data]

                    data_dict[f'filtered_{filter_y}'] = [d[filter_y] for d in exclude_data]

                    for field_y in field_ys:
                        if mode == 'graph':
                            # 그래프 그릴 때만 사용하기 => raw값임
                            data_dict[field_x] = [d[field_x] for d in required_data]
                            data_dict[field_y] = [d[field_y] for d in required_data]
                            # --------------------------------

                        data_dict[f'filtered_{field_x}'] = [d[field_x] for d in exclude_data]
                        data_dict[f'filtered_{field_y}'] = [d[field_y] for d in exclude_data]

                        if mode == 'save_filtering':
                            saveExcel(data_dict, os.getenv('save_folder_path')+'/satellite/', f'{season}_{field_x}_filtered_{filter_y}_{s_start_percentage}_to_{s_end_percentage}.xlsx', f'{field_y}_{time}', orient='columns')
                            continue

                        # 회귀식 산출
                        model = best_polynomial_linear_regression_model(data_dict[f'filtered_{field_x}'], data_dict[f'filtered_{field_y}'], degrees=degrees,intercept=True)
                        data_dict[f'regression_{field_x}'], data_dict[f'regression_{field_y}'], equation = polynomial_regression_line_data(data_dict[f'filtered_{field_x}'], model)
                        # print(equation)
                        data_dict['regression'] = model.coef_ + model.intercept_

                        # 선정 맑은날 예측
                        data_dict['real_datetime'] = [getattr(d, 'datetime') for d in season_test_data[season][time]]
                        data_dict[f'real_{field_x}'] = [getattr(d, field_x) for d in season_test_data[season][time]]

                        if mode == 'graph': # 그래프 그리기
                            if field_y.isdigit():
                                data_dict[f'real_{field_y}']= [getattr(d, "spd")[field_y] for d in season_test_data[season][time]]
                            else:
                                data_dict[f'real_{field_y}'] = [getattr(d, field_y) for d in season_test_data[season][time]]
                            data_dict[f'predict_{field_y}'] = predict_regression( data_dict[f'real_{field_x}'], model)

                            classified_time_data[time] = data_dict
                        elif mode == 'save_regression': # 회귀식저장하기
                            if field_y.isdigit():
                                data_dict[f'real_y'] = [getattr(d, "spd")[field_y] for d in
                                                                season_test_data[season][time]]
                            else:
                                data_dict[f'real_y'] = [getattr(d, field_y) for d in season_test_data[season][time]]
                            data_dict[f'predict_y'] = predict_regression(data_dict[f'real_{field_x}'], model)

                            wanted_cols = ['regression', 'real_datetime',f'real_y', f'predict_y']
                            data_dict = {k:v for k, v in data_dict.items() if k in wanted_cols}
                            saveTxt(data_dict, os.getenv('save_folder_path') + f'satellite/{field_x}/{str(s_start_percentage)}_{str(s_end_percentage)}/{season}/{getVerificationDate(season)}/', f"{field_y}_{time}")

                if mode == 'graph': # 그래프 그리기
                    draw_ampm_scatterplot(field_x, field_ys[0], classified_time_data['am'],classified_time_data['pm'], True)
                    draw_ampm_predict_scatter(field_x, field_ys[0], classified_time_data['am'],classified_time_data['pm'])
