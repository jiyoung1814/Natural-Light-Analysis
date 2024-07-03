import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np
from Functions.Converter import TimestampToDatetime


class SatelliteData:
    def __init__(self, data):
        self.type = data['type']
        self.timestamp = data['timestamp']

        try:
            self.array = data['array']
        except:
            self.array = []

        self.meta = SatelliteData_Meta(data['meta'])

        try:
            self.knu_near_image = data['knu_near_image']
        except:
            self.knu_near_image = []

    def setKNUNearImage(self, image):
        self.knu_near_image = image


class SatelliteData_Meta:
    def __init__(self, data):
        self.image_width = data['image_width']
        self.image_height = data['image_height']

        self.upper_left_easting = data['upper_left_easting']
        self.upper_left_northing = data['upper_left_northing']
        self.upper_right_easting = data['upper_right_easting']
        self.upper_right_northing = data['upper_right_northing']
        self.lower_left_easting = data['lower_left_easting']
        self.lower_left_northing = data['lower_left_northing']
        self.lower_right_easting = data['lower_right_easting']
        self.lower_right_northing = data['lower_right_northing']

        self.file_name = data['file_name']
        self.channel_center_wavelength = data['channel_center_wavelength']
        self.channel_spatial_resolution = data['channel_spatial_resolution']
        self.instrument_name = data['instrument_name']
        self.satellite_name = data['satellite_name']


        self.number_of_columns = data['number_of_columns']
        self.number_of_lines = data['number_of_lines']

        try:
            self.DAT_channel_name = data['DAT:channel_name']
        except:
            self.DAT_channel_name = data['DAT_channel_name']
