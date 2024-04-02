import os

from dotenv import load_dotenv

from DB.mongoDB import MongoDB
from Functions.Natrual import getDataFromDB, getRequiredData, dataClassifying, dataFiltering, getVerificationDate
from Functions.Excel import saveExcel, saveTxt

from API.Natrual import getDayData
from Regression.Linear import best_polynomial_linear_regression_model, predict_regression


if __name__ == '__main__':
    load_dotenv()
    mongo = MongoDB()
    mongo.connect_DB()

    field_x = 'elevation'
    field_ys = [str(w) for w in range(380, 781)]
    # field_ys = ['lux']
    # seasons = os.getenv('seasons_names').split(",")
    # seasons = ['경칩', '망종', '한로', '동지']
    seasons = ['경칩']
    time_slice = ['am', 'noon', 'pm']

    # filtering percentage
    top_percentage = 2
    end_percentage = 8

    degree = 5 # 차수
    degrees = [3,4,5]
    intercept = True # y절편 유무

    #test data 구하기
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
