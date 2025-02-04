import csv
import datetime
import math
import pandas as pd

import pv_system
import solarposition
import shade_grid

# current system specifications (rows/collums of panels are approximated as one large panel where possible)

#system = pv_system.system("standard", 1.5, 80, 2, 80, 10, 1, 9, 35, 0)
#system = pv_system.system("vertical", 1.4, 1.2, 80, 10, 80, 9, 1, 0, 90)
#system = pv_system.system("overhead", 1, 1, 80, 10, 80, 9, 1, 0, 10)
system = pv_system.system("tracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0) 
#system = pv_system.system("backtracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0)

# longitude value
long = 0

# field dimensions (10m buffer on every side added in shade calculation - total 1 ha)

# field dimension in E/W direction (in m)
field_width = 80 

# field dimension in N/S direction (in m)
field_length = 80

# import lat dependent tilts for standard system
lat_depentent_tilts = pd.read_csv("tilt_by_lat.csv")

# specifications for results file
columns=['lat', 'long', 'month', 'day', 'hour', 'minute', 'shaded area (in %)', 'self-shaded panel area (in ' + '%' + ' of total panel area)', 'proximate azimuth of sun', 'apparent elevation of sun']
filename = str(system.get_name()) + '_shade_percent_15min.csv'
with open(filename, 'a') as f_object:
    writer_object = csv.writer(f_object)
    writer_object.writerow(columns)
    f_object.close()

# specifications for percentage of time shaded file - no horizons considered for this (just for comparing systems)
columns=['lat', 'long', 'month', 'day']
percentage_intervals = 5

for i in range(1, percentage_intervals + 1):
    new_column = str(round((i/percentage_intervals - 1/percentage_intervals) * 100, 1)) + " - " + str(round((i/percentage_intervals) * 100, 1)) + " %"
    columns.append(new_column)

filename_percent_of_time_shaded = str(system.get_name()) + '_percent_of_time_shaded.csv'

with open(filename_percent_of_time_shaded, 'a') as f_object:
    writer_object = csv.writer(f_object)
    writer_object.writerow(columns)
    f_object.close()

for lat in range(34, 72):
    # change panel tilt in optimal system depending on lat
    if system.system_type == "standard":
        system.PV_angle_NS = lat_depentent_tilts["tilt (europe)"].where(lat_depentent_tilts["lat"] == int(lat)).dropna().values[0]
        
    for year in range(2000, 2001):
        for month in range(1, 13):
            for day in range(1, 32):

                try:
                    datetime.datetime(year=year, month=month, day=day)
                    grid = shade_grid.shade_grid(field_width, field_length)

                    for hour in range(0,24):

                        for minute in range(0,60,15):
                            
                            azimuth_rad, elevation_rad = solarposition.calculate_azimuth_and_elevation_rad(year, month, day, hour, minute, long, lat)
                            
                            if azimuth_rad < 0 or azimuth_rad > 2*math.pi:
                                raise invalid_azimuth
                            
                            # position of pv panel needs to be readjusted with each time step for tracking systems
                            if system.system_type == 'tracking':
                                system.tracking_repositioning(year, month, day, hour, minute, long, lat)
                            
                            if system.system_type == 'backtracking':
                                system.backtracking_repositioning(year, month, day, hour, minute, long, lat)
                                
                            angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(year, month, day, hour, minute, long, lat)

                            proximate_azimuth, apparent_elevation = solarposition.correct_solarposition(year, month, day, hour, minute, long, lat)
                            
                            # check if sun is over or under horizon in any case (< 0°), shade calculation is skipped in that case (shaded area and self-shade area are both set to 100%)
                            if apparent_elevation >= 0:
                                intersection_percent, self_shade_percentage_of_total_panel_area = system.calculate_shade(angle_in_plane_EW, angle_in_plane_NS, field_width, field_length, azimuth_rad, elevation_rad, grid)
                            else:
                                intersection_percent = 100
                                self_shade_percentage_of_total_panel_area = 100

                            # adding line with results to file
                            new_line = [lat, long, round(month), round(day), round(hour), round(minute), intersection_percent, self_shade_percentage_of_total_panel_area, proximate_azimuth, apparent_elevation] #angle_in_plane_NS, angle_in_plane_EW]
                            
                            with open(filename, 'a') as f_object:
                                writer_object = csv.writer(f_object)
                                writer_object.writerow(new_line)
                                f_object.close()

                    percentage_steps, percentage_counts_dict = grid.evaluate(percentage_intervals)
                    
                    # adding line to percentage of time shaded file
                    new_line = [lat, long, round(month), round(day)]
                    
                    for bin in percentage_counts_dict:
                        new_line.append(percentage_counts_dict[bin])

                    with open(filename_percent_of_time_shaded, 'a') as f_object:
                                writer_object = csv.writer(f_object)
                                writer_object.writerow(new_line)
                                f_object.close()

                    grid.reset()
                        
                except ValueError:
                    print("Error at lat=", lat, ", year=", year, ", month=", month, "day=", day)
                    pass
                except Exception as invalid_azimuth:
                    print("Invalid azimuth calculated at lat=", lat, ", year=", year, ", month=", month, "day=", day)
                    pass
