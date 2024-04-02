import pandas as pd
import numpy as np
import os


def extract_keys(dictionary):
    keys = []
    for key, value in dictionary.items():
        keys.append(key)
        if isinstance(value, dict):
            keys.pop()
            keys.extend(extract_keys(value))
    return keys


def extract_values(dictionary):
    values = []
    for value in dictionary.values():
        if isinstance(value, dict):
            values.extend(extract_values(value))
        else:
            values.append(value)
    return values


def listdict_to_df(data):
    df = pd.DataFrame(columns=extract_keys(data[0]))
    try:
        for idx, row_data in enumerate(data):
            df.loc[idx] = extract_values(row_data)
    except Exception as e:
        print(f'listdict_to_df Error: {e}')
    return df


def saveExcel(data={}, path='', file_name='excel', sheet_name='sheet'):
    try:
        if isinstance(data, list) or isinstance(data, np.ndarray):
            data = listdict_to_df(data)
        elif isinstance(data, dict):
            data = pd.DataFrame.from_dict(data, orient='index')

        if (file_name + '.xlsx') in os.listdir(path):
            with pd.ExcelWriter((path + file_name + '.xlsx'), engine='openpyxl', mode='a') as writer:
                data.to_excel(writer, sheet_name=sheet_name)
            print(f'{path}{file_name}.xlsx => {sheet_name} 저장')
        else:
            print(f'{path}{file_name}.xlsx_생성')
            with pd.ExcelWriter((path + file_name + '.xlsx'), engine='openpyxl') as writer:
                data.to_excel(writer, sheet_name=sheet_name)
            print(f'{path}{file_name}.xlsx => {sheet_name} 저장')

    except Exception as e:
        print(f'saveExcel Error: {e}')


def saveTxt(data, path='', file_name='textfile'):
    try:
        if isinstance(data, list) or isinstance(data, np.ndarray):
            data = listdict_to_df(data)
        elif isinstance(data, dict):
            data = pd.DataFrame.from_dict(data, orient='index').transpose()

        if not os.path.exists(path):
            os.makedirs(path)
            print(f'{path} 폴더 생성')

        df_file_path = os.path.join(path, f"{file_name}.txt")
        data.to_csv(df_file_path, sep='\t')
        print(f'{file_name} 파일 저장')

    except Exception as e:
        print(f'saveTxt Error: {e}')


def readTxtWriteExcel(read_txt_path, write_excel_path, excel_name, sheet_name):
    try:
        df = pd.read_csv(read_txt_path, sep='\t')
        saveExcel(df, write_excel_path, excel_name, sheet_name)

    except Exception as e:
        print(f'readTxt Error: {e}')

