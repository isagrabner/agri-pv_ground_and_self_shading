from pvlib import solarposition
from timezonefinder import TimezoneFinder
import pandas as pd
import math

def calculate_solarposition(year=2019, month=6, day=1, hour=12, minute=0, long=47.6, lat=17.2):
    ''' Calculates the solar position depending on date/time and longitude/latitude. Converts solarposition to angles in the vertical planes in E/W and N/S direction.
    
        Parameters: year, month, day, hour, long, lat
        
        Returns: angle_in_plane_EW, angle_in_plane_NS
        '''
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
    offset_distance = math.cos(apparent_elevation_rad)

    if height >= 0:
        distance_NS = offset_distance * (- math.cos(azimuth_rad))
        distance_EW = offset_distance * math.sin(azimuth_rad)

        angle_in_plane_NS = math.atan(height / abs(distance_NS)) if azimuth > 90 and azimuth < 270 else math.pi - math.atan(height / abs(distance_NS)) #if distance_NS > 0 else math.pi - math.atan(height / abs(distance_NS))
        angle_in_plane_EW = math.atan(height / abs(distance_EW)) if azimuth < 180 else math.pi - math.atan(height / abs(distance_EW)) #if distance_EW > 0 else math.pi - math.atan(height / abs(distance_EW))

        #angle_in_plane_NS = math.atan(height / abs(distance_NS)) if distance_NS > 0 else math.pi - math.atan(height / abs(distance_NS))
        #angle_in_plane_EW = math.atan(height / abs(distance_EW)) if distance_EW > 0 else math.pi - math.atan(height / abs(distance_EW))

    else:
        angle_in_plane_NS, angle_in_plane_EW = -1, -1

    '''
    # calculating angles in planes E/W and N/S
    height = math.tan(apparent_elevation_rad)
    section_EW = abs(math.sin(azimuth_rad))
    #section_EW = math.sin(azimuth_rad)
    section_NS = abs(math.cos(azimuth_rad))
    #section_NS = - math.cos(azimuth_rad)

    angle_in_plane_EW = math.atan(height / section_EW) + (0 if azimuth > 180 else math.pi/2)
    angle_in_plane_NS = math.atan(height / section_NS) + (0 if azimuth < 90 or azimuth > 210 else math.pi/2)'''

    return angle_in_plane_EW, angle_in_plane_NS


def check_solarposition(angle_in_plane_EW, angle_in_plane_NS, errors, number_of_errors):
    '''Checks if solar position is valid, i.e. if the sun is below the horizon. 
    
       Parameters: angle_in_plane_EW, angle_in_plane_NS, errors, number_of_errors

       Returns: errors, number_of_errors
       '''

    if angle_in_plane_EW < 0 or angle_in_plane_NS < 0: # horizon values to be included here
        errors = errors + ('' if len(errors) == 0 else '\n') + 'Sun is under the horizon for the given values.'
        number_of_errors += 1

    return errors, number_of_errors