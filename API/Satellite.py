import requests
import json
import os, sys

from HMACSHA256.hmacsha256 import setHeaders

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


def getSatelliteDayTimeList(d, l):
    '''
    서버에 보유하고 있는 위성 데이터의 시간 목록 획득
    :param d: request date
    :param l: 요청 채널(class: Str) ex) lv1 : "1"~"16", lv2: "COT", ...
    :return:
    [
      1583006400000,
      1583006520000,
      1583006640000,
      1583006760000,
      1583006880000,
      1583007000000,
      1583007120000,
      1583007240000,
      1583007360000,
      ...
      1583059320000,
      1583059440000,
      1583059560000,
      1583059680000,
      1583059800000,
      1583059920000,
      1583060040000,
      1583060160000,
      1583060280000
    ]
    '''

    if isinstance(l, int):
        l = str(l)

    data = {
        "parameter1": d,
        "parameter2": l
    }

    data_json = json.dumps(data).encode('utf-8')

    headers = setHeaders()
    response = requests.get(os.getenv('url') + 'v2/satellite/time_list', headers=headers, data=data_json)

    return response.json()


def getSatelliteImage(ts, l):
    '''
    서버에 보유하고 있는 위성 데이터 획득
    :param ts: 요청시간
    :param l: 요청 채널(class: Str) ex) lv1 : "1"~"16", lv2: "COT", ...
    :return:
    {
          "Type": "LE1_01_VI004",
          "Timestamp": 1583007360000,
          "Array": [  // 900x900 이면 [900][900] 배열
            [      20,      20,      20,    .....,    21,      20,      20    ],
            [      20,      20,      20,    .....,    21,      20,      20    ],
            [      20,      20,      20,    .....,    21,      20,      20    ],
            .....
            [      20,      20,      20,    .....,    21,      20,      20    ],
            [      20,      20,      20,    .....,    21,      20,      20    ],
            [      20,      20,      20,    .....,    21,      20,      20    ],
          ],
          "Meta": {
            "Name": "",
            "projection_type": "lambert_conformal_conic",
            "standard_parallel1": 30,
            "standard_parallel2": 60,
            "origin_latitude": 38,
            "central_meridian": 126,
            "false_easting": 0,
            "false_northing": 0,
            "image_width": 1800,
            "image_height": 1800,
            "pixel_size": 1000,
            "upper_left_easting": -899500,
            "upper_left_northing": 899500,
            "upper_right_easting": 899500,
            "upper_right_northing": 899500,
            "lower_left_easting": -899500,
            "lower_left_northing": -899500,
            "lower_right_easting": 899500,
            "lower_right_northing": -899500,
            "_CoordinateTransformType": 0,
            "_CoordinateAxisTypes": 0,
            "file_name": "gk2a_ami_le1b_vi004_ko010lc_202002292016.nc",
            "origianl_sourece_file": "gk2a_ami_le1b_vi004_ela010ge_202002292016.nc",
            "number_of_columns": 1800,
            "number_of_lines": 1800,
            "total_pixel_data_size": 3240000,
            "channel_center_wavelength": "0.47",
            "channel_spatial_resolution": "1.0",
            "data_processing_center": "NMSC",
            "data_processing_mode": "operation",
            "file_format_version": "1.0.0_20181120",
            "instrument_name": "AMI",
            "satellite_name": "GK-2A",
            "DAT:Name": "image_pixel_values",
            "DAT:number_of_total_pixels": 3240000,
            "DAT:average_pixel_value": 19.603371929824561,
            "DAT:channel_name": "VI004",
            "DAT:max_pixel_value": 24,
            "DAT:min_pixel_value": 18,
            "DAT:number_of_total_bits_per_pixel": 16,
            "DAT:number_of_valid_bits_per_pixel": 11
          }
        }
    '''

    if isinstance(l, int):
        l = str(l)

    data = {
        "parameter1": ts,
        "parameter2": l
    }

    data_json = json.dumps(data).encode('utf-8')
    headers = setHeaders()
    response = requests.get(os.getenv('url') + 'v2/satellite/data', headers=headers, data=data_json)

    return response.json()
