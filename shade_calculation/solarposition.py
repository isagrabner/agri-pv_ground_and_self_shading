from pvlib import solarposition
from timezonefinder import TimezoneFinder
import pandas as pd
import math
import numpy as np

def find_nearest(array, value):
    '''Finds nearest value in array to given value.
    
        Parameters: array, value
        
        Returns: array[idx]'''
        
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def calculate_azimuth_rad(year=2019, month=6, day=1, hour=12, minute=0, long=47.6, lat=17.2):
    ''' Calculates azimuth in rad based on date/time and location.
    
        Parameters: year, month, day, hour, minute, long, lat
        
        Returns: azimuth_rad'''

    # create datetime with timezone based on longitude and latitude
    obj = TimezoneFinder() 
    date_time = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, tz = obj.timezone_at(lng=long, lat=lat))

    # calculate solar position
    solar_position = solarposition.get_solarposition(date_time, long, lat)
    azimuth = float(solar_position.at[date_time,'azimuth'])

    # converting elevation and azimuth to rad
    azimuth_rad = (azimuth / 180) * math.pi

    return azimuth_rad


def calculate_solarposition(year=2019, month=6, day=1, hour=12, minute=0, long=47.6, lat=17.2):
    ''' Calculates the solar position depending on date/time and longitude/latitude. Converts solarposition to angles in the vertical planes in E/W and N/S direction.
    
        Parameters: year, month, day, hour, minute, long, lat
        
        Returns: angle_in_plane_EW, angle_in_plane_NS'''
        
    # solar position

    # create datetime with timezone based on longitude and latitude
    obj = TimezoneFinder() 
    date_time = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, tz = obj.timezone_at(lng=long, lat=lat))

    # calculate solar position
    solar_position = solarposition.get_solarposition(date_time, long, lat)
    apparent_elevation = float(solar_position.at[date_time,'apparent_elevation'])
    azimuth = float(solar_position.at[date_time,'azimuth'])

    # converting elevation and azimuth to rad
    apparent_elevation_rad = (apparent_elevation / 180) * math.pi
    azimuth_rad = (azimuth / 180) * math.pi

    height = math.sin(apparent_elevation_rad)

    if height >= 0:
        distance_NS = - math.cos(azimuth_rad) #offset_distance
        distance_EW = math.sin(azimuth_rad) #offset_distance

        angle_in_plane_NS = math.pi/2 - math.atan(distance_NS/height) 
        angle_in_plane_EW = math.pi/2 - math.atan(distance_EW/height)

    else:
        angle_in_plane_NS, angle_in_plane_EW = -1, -1 # sun under horizon
    
    return angle_in_plane_EW, angle_in_plane_NS


def correct_solarposition(year, month, day, hour, minute, long, lat):#, horizon_data):
    '''Calculates sun elevation and proximate azimuth (nearest azimuth available in horizon data). Data is saved so validity of sun position (i.e. if the sun is below the horizon) can be checked later. 
    
       Parameters: year, month, day, hour, minute, long, lat

       Returns: proximate_azimuth, apparent_elevation'''

    # create datetime with timezone based on longitude and latitude
    obj = TimezoneFinder() 
    date_time = pd.Timestamp(year=year, month=month, day=day, hour=hour, minute=minute, tz = obj.timezone_at(lng=long, lat=lat))

    # calculate solar position
    solar_position = solarposition.get_solarposition(date_time, long, lat)
    apparent_elevation = float(solar_position.at[date_time,'apparent_elevation'])
    azimuth = float(solar_position.at[date_time,'azimuth'])

    # convert azimuth to azimuth used in horizon data (0° - 360° to -180° - 180°)
    azimuth_converted = azimuth - 180

    # array of possible azimuth values (same as in horizon data)
    azimuth_array = np.linspace(-180, 180, num=49)
    
    # find nearest azimuth to current solar position
    proximate_azimuth = find_nearest(azimuth_array, azimuth_converted)
    
    return proximate_azimuth, apparent_elevation