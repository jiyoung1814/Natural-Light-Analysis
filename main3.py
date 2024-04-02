import os
from dotenv import load_dotenv

from Functions.Excel import readTxtWriteExcel

if __name__ == '__main__':
    load_dotenv()

    field_x = 'elevation'
    field_ys = [str(w) for w in range(380, 781)]
    # field_ys = ['lux', '380', '580', '780']
    # seasons = os.getenv('seasons_names').split(",")
    # seasons = ['경칩', '망종', '한로', '동지']
    seasons = ['상강', '대설']
    time_slice = ['am', 'pm']


    # filtering percentage
    top_percentage = 2
    end_percentage = 8

    degree = 5  # 차수
    degrees = [3, 4, 5]
    intercept = True  # y절편 유무

    write_excel_path =os.getenv('save_folder_path')+f'{field_x}/excel/'
    for season in seasons:
        for time in time_slice:
            exel_name = f'{season}_{time}'
            for field_y in field_ys:
                read_file_path = os.getenv('save_folder_path')+f"{field_x}/{top_percentage}_{end_percentage}/{season}/{field_y}_{time}.txt"
                sheet_name = f'{field_y}'

                readTxtWriteExcel(read_file_path, write_excel_path, exel_name, sheet_name)