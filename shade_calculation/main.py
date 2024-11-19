import csv
import datetime

import pv_system
import solarposition

# current system specifications (rows/collums of panels are approximated as one large panel where possible)

#system = pv_system.system("optimal", 1.5, 80, 2, 2, 10, 1, 9, 35, 0)
#system = pv_system.system("vertical", 1.4, 1.2, 80, 10, 80, 9, 1, 0, 90)
#system = pv_system.system("overhead", 1.5, 1, 2, 2, 3, 41, 41, 0, 0) # should be altered to line up panel edges so eighter rows or collums can be approximated as one panel each
system = pv_system.system("tracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0) 

# longitude value
long = 0

# field dimensions (10m buffer on every side added in shade calculation - total 1 ha)

# field dimension in E/W direction (in m)
field_width = 80 

# field dimension in N/S direction (in m)
field_length = 80

# specifications for results file
columns=['lat', 'long', 'month', 'day', 'hour', 'minute', 'shaded area (in %)', 'self-shaded panel area (in ' + '%' + ' of total panel area)', 'proximate azimuth of sun', 'apparent elevation of sun']
filename = str(system.get_name()) + '_shade_percent_15min.csv'
with open(filename, 'a') as f_object:
    writer_object = csv.writer(f_object)
    writer_object.writerow(columns)
    f_object.close()

for lat in range(34, 72):
    for year in range(2000, 2001):
        for month in range(1, 13):
            for day in range(1, 32):

                try:
                    datetime.datetime(year=year, month=month, day=day)

                    for hour in range(0,24):

                        for minute in range(0,60,15):
                            
                            azimuth_rad = solarposition.calculate_azimuth_rad(year, month, day, hour, minute, long, lat)

                            # position of pv panel needs to be readjusted with each time step for tracking systems
                            if system.system_type == 'tracking':
                                system.tracking_repositioning(year, month, day, hour, minute, long, lat)

                            angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(year, month, day, hour, minute, long, lat)

                            proximate_azimuth, apparent_elevation = solarposition.correct_solarposition(year, month, day, hour, minute, long, lat)
                            
                            # check if sun is over or under horizon in any case (< 0°), shade calculation is skipped in that case (shaded area and self-shade area are both set to 100%)
                            if apparent_elevation >= 0:
                                intersection_percent, self_shade_percentage_of_total_panel_area = system.calculate_shade(angle_in_plane_EW, angle_in_plane_NS, field_width, field_length, azimuth_rad)
                            else:
                                intersection_percent = 100
                                self_shade_percentage_of_total_panel_area = 100

                            # adding line with results to file
                            new_line = [lat, long, round(month), round(day), round(hour), round(minute), intersection_percent, self_shade_percentage_of_total_panel_area, proximate_azimuth, apparent_elevation] #angle_in_plane_NS, angle_in_plane_EW]
                            
                            with open(filename, 'a') as f_object:
                                writer_object = csv.writer(f_object)
                                writer_object.writerow(new_line)
                                f_object.close()
                        
                except:
                    print("Error at lat=", lat, ", year=", year, ", month=", month, "day=", day)
                    pass