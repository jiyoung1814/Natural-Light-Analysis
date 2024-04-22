import os

import pandas as pd
from dotenv import load_dotenv

from Functions.Natrual import getVerificationDate
from Functions.File import readTxtWriteExcel, readTxtToDict, saveExcel
from Functions.Converter import StrToDatetime
from API.Natrual import getDayInfo

from Optical_Properties.optical import optical

if __name__ == '__main__':
    load_dotenv()

    field_x = 'elevation'
    field_ys = [str(w) for w in range(380, 781)]
    # field_ys = ['lux', '380', '580', '780']
    # seasons = os.getenv('seasons_names').split(",")
    # seasons = ['경칩', '망종', '한로', '동지']
    seasons = ['경칩']
    time_slice = ['am', 'pm']

    # filtering percentage
    top_percentage = 0
    end_percentage = 10

    degree = 5  # 차수
    degrees = [3, 4, 5]
    intercept = True  # y절편 유무

    # # txt 파일 읽어서 절기별 선정한 날짜 모든 시간의 field_y 실측값과 예측값 엑셀에 저장 -> 엑셀에 시간 입력하면 그 시간의 광특성 확인 가능
    # write_excel_path = os.getenv('save_folder_path') + f'satellite/{field_x}/excel/'
    # for season in seasons:
    #     for time in time_slice:
    #         exel_name = f'{season}_{getVerificationDate(season)}_{time}'
    #         for field_y in field_ys:
    #             read_file_path = os.getenv('save_folder_path') + f"satellite/{field_x}/{top_percentage}_{end_percentage}/{season}/{getVerificationDate(season)}/{field_y}_{time}.txt"
    #             sheet_name = f'{field_y}'
    #
    #             readTxtWriteExcel(read_file_path, write_excel_path, exel_name, sheet_name)

    # txt 파일 읽어서 절기 별 선정한 날짜의 하루 field_y 실측값과 예측값 및 광특성 비교
    dt_field = 'real_datetime'
    add_fields = [f'real_y', f'predict_y']
    fields = [dt_field] + add_fields  # fields의 첫번째 요소는 무조건 datetime

    time_interval = [7,8,9,10,11,12,13,14,15,16,17,18]

    season_data = {}
    for season in seasons:
        read_txt_path = os.getenv('save_folder_path') + f"satellite/{field_x}/{top_percentage}_{end_percentage}/{season}/{getVerificationDate(season)}/"

        # 데이터 읽기
        data = {}
        for field_y in field_ys:
            for time in time_slice:
                read_data = readTxtToDict(read_txt_path+f'{field_y}_{time}.txt', fields=fields)

                # dict{field:[]} to dict{datetime: {field_y: {field: value, field2: value}, field_y: {field: value, field2: value} , ...}} ex) datetime:{380:{real_y: 10, predict_y = 11}, 381: {},,,}
                for dt, *field in zip(read_data[dt_field], *[read_data[key] for key in add_fields]):
                    time_data = {add_fields[i]: values for i, values in enumerate(field)}

                    # 하루 중 중복 datetime은 평균값으로
                    if dt in data.keys():
                        data[dt][field_y] = time_data
                        if field_y in data[dt].keys():
                            data[dt][field_y] = {key: (data[dt][field_y].get(key, 0) + time_data.get(key, 0)) / 2 for key in data[dt][field_y].keys()}
                    else:
                        data[dt] = {field_y: time_data}

        # 읽어온 날의 CCT 기반 일출 일몰 시간 구하기
        read_date = list(data.keys())[0].split()[0]
        read_date_info = getDayInfo(read_date)
        sun_rise = read_date_info.lwctSunRiseTime
        sun_set = read_date_info.lwctSunSetTime

        # time_interval로 데이터 나누기
        time_interval_data ={key: {} for key in time_interval}

        for dt, dt_value in data.items():
            dt = StrToDatetime(dt)
            if sun_rise <= dt <= sun_set: # 일출 일몰 시간 사이의 데이터만 추출
                if dt.hour in time_interval:
                    spd = {key: {int(w): d[key] for w,d in dt_value.items()} for key in add_fields}
                    optical_properties = {}

                    spd_mae = sum(abs(spd[add_fields[0]][wl] - spd[add_fields[1]][wl]) for wl in spd[add_fields[0]])/ len(spd[add_fields[0]])

                    for y, s in spd.items():
                        spd_optical = optical(s)
                        swr = sum([s[w] for w in range(380, 431)])/ sum(s.values()) * 100
                        spd_optical.spd_to_cri()
                        optical_properties[y] = {'CCT': getattr(spd_optical, 'cct'), "ILLUM": getattr(spd_optical, 'Y'), "CRI": getattr(getattr(spd_optical, 'cri'),'ra'), 'SWR': swr, 'spd_mae':spd_mae}

                    time_interval_data[dt.hour].update({dt.time(): optical_properties})



        write_excel_path =os.getenv('save_folder_path')+f'satellite/{field_x}/excel_optical/{season}/{getVerificationDate(season)}/'
        if not os.path.exists(write_excel_path):
            os.makedirs(write_excel_path)
            print(f'{write_excel_path} 폴더 생성')

        for i_time, i_time_data in time_interval_data.items(): # interval
            flatten_time_data = {}
            if isinstance(i_time_data, dict):
                for dt, dt_data in i_time_data.items(): # dt
                    flattened_value = {}
                    if isinstance(dt_data, dict):
                        for add_field, add_field_data in dt_data.items(): # add_fields
                            if isinstance(add_field_data, dict):
                                for y, y_data in add_field_data.items(): # field_y
                                    new_key = f"{add_field}_{y}"
                                    flattened_value[new_key] = y_data
                            else:
                                flattened_value[add_field] = add_field_data
                    else:
                        flattened_value = dt_data

                    flatten_time_data[dt] = flattened_value
                saveExcel(flatten_time_data, write_excel_path, f'{season}_{read_date}_optical', f'{i_time}', orient='index')

