import re
import datetime
import math

import variables
import solarposition

# functions for updating values with new input

def update_for_tracking():
    '''Updates E/W angle of the PV panel depending on sun position for the tracking system.'''
    if variables.tracking:
        angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(variables.year, variables.month, variables.day, variables.hour, variables.minute, variables.long, variables.lat)
        angle_in_plane_EW_degrees = (angle_in_plane_EW / math.pi) * 180
        variables.angle_EW_slider.set_val(90 - angle_in_plane_EW_degrees)

# ---------- updating values with text input ----------

def update_date(new_date):
    ''' Checks for an input, if the format is correct (dd/mm/yyyy and values can be cast to int) and the value is in the a valid range (checks by attempting daytime conversion). Changes the day, month and year values on submit, if the format is correct.
        
        Parameters: new_date
        
        Returns: - 
        '''

    format_date = re.compile('.{2}/.{2}/.{4}')

    if len(new_date) == 10 and format_date.match(new_date):
        # splitting sting into day, month and year values
        try:
            variables.day = int(new_date[0:2])
            variables.month = int(new_date[3:5])
            variables.year = int(new_date[6:10])

            valid_date_format = True

            # if format is correct, check if values are valid
            try:
                datetime.datetime(year=variables.year,month=variables.month,day=variables.day)
                update_for_tracking()
                valid_date_value = True
            except:
                valid_date_value = False   

        except:
            valid_date_format = False
            valid_date_value = True    

    else:
        valid_date_format = False
        valid_date_value = True 

    # dictionary for checking errors in update function
    variables.valid_date = {'format':valid_date_format,
                            'value':valid_date_value}


def update_time(new_time):
    ''' Checks for an input, if the format is correct (hh:mm and values can be cast to int) and the value is in the a valid range (checks by attempting daytime conversion). Changes the hour and minute values on submit, if the format is correct.
        
        Parameters: new_time
        
        Returns: - 
        '''

    format_time = re.compile('.{2}:.{2}')

    if len(new_time) == 5 and format_time.match(new_time):
        # splitting sting into hour and minute values
        try:
            variables.hour = int(new_time[0:2])
            variables.minute = int(new_time[3:5])

            valid_time_format = True

            # if format is correct, check if values are valid
            try:
                datetime.datetime(year=2000, month=1, day=1, hour=variables.hour, minute=variables.minute)
                update_for_tracking()
                valid_time_value = True
            except:
                valid_time_value = False

        except:
            valid_time_format = False
            valid_time_value = True

    else:
        valid_time_format = False
        valid_time_value = True

    # dictionary for checking errors in update function
    variables.valid_time = {'format':valid_time_format,
                            'value':valid_time_value}   


def update_long(new_long):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (<= 180 and >= -180). Changes the value of the longitude on submit, if the format is correct.
        
        Parameters: new_long
        
        Returns: - 
        '''

    try:
        variables.long = float(new_long)
        valid_long_format = True

        # if format is correct, check if values are valid
        if variables.long <= 180 and variables.long >= -180:
            update_for_tracking()
            valid_long_value = True
        else:
            valid_long_value = False

    except:
        valid_long_format = False
        valid_long_value = True

    # dictionary for checking errors in update function
    variables.valid_long = {'format':valid_long_format,
                            'value':valid_long_value}  


def update_lat(new_lat):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (<= 90 and >= -90). Changes the value of the latitude on submit, if the format is correct.
        
        Parameters: new_lat
        
        Returns: - 
        '''

    try:
        variables.lat = float(new_lat)
        valid_lat_format = True

        if variables.lat <= 90 and variables.lat >= -90:
            update_for_tracking()
            valid_lat_value = True
        else:
            valid_lat_value = False

    except:
        valid_lat_format = False
        valid_lat_value = True

    # dictionary for checking errors in update function
    variables.valid_lat = {'format':valid_lat_format,
                           'value':valid_lat_value}


def update_base_height(new_PV_base_height):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (>= 0 and < 20). Changes the value of the base height on submit, if the format is correct.
        
        Parameters: new_PV_base_height
        
        Returns: - 
        '''

    try:
        variables.PV_base_height = float(new_PV_base_height)
        valid_base_height_format = True

        # if format is correct, check if values are valid (for now not negative and <20m)
        if variables.PV_base_height >= 0 and variables.PV_base_height < 20:
            valid_base_height_value = True
        else:
            valid_base_height_value = False

    except:
        valid_base_height_format = False
        valid_base_height_value = True

    # dictionary for checking errors in the update function
    variables.valid_base_height = {'format': valid_base_height_format,
                                   'value': valid_base_height_value}


def update_width(new_PV_width):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (>= 0 and < 20). Changes the value of the width on submit, if the format is correct.
        
        Parameters: new_PV_width
        
        Returns: - 
        '''

    try:
        variables.PV_width = float(new_PV_width)
        valid_PV_width_format = True

        # if format is correct, check if values are valid (for now not negative and <20m)
        if variables.PV_width >= 0 and variables.PV_width < 20:
            valid_PV_width_value = True
        else:
            valid_PV_width_value = False

    except:
        valid_PV_width_format = False
        valid_PV_width_value = True

    # dictionary for checking errors in the update function
    variables.valid_PV_width = {'format': valid_PV_width_format,
                                'value': valid_PV_width_value}


def update_length(new_PV_length):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (>= 0 and < 20). Changes the value of the length on submit, if the format is correct.
        
        Parameters: new_PV_length
        
        Returns: - 
        '''

    try:
        variables.PV_length = float(new_PV_length)
        valid_PV_length_format = True

        # if format is correct, check if values are valid (for now not negative and <20m)
        if variables.PV_length >= 0 and variables.PV_length < 20:
            valid_PV_length_value = True
        else:
            valid_PV_length_value = False

    except:
        valid_PV_length_format = False
        valid_PV_length_value = True

    # dictionary for checking errors in the update function
    variables.valid_PV_length = {'format': valid_PV_length_format,
                                 'value': valid_PV_length_value}


def update_distance_EW(new_distance_EW):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (>= 0 and < 50). Changes the value of the distance between panels in E/W direction on submit, if the format is correct.
        
        Parameters: new_distance_EW
        
        Returns: - 
        '''

    try:
        variables.distance_EW = float(new_distance_EW)
        valid_distance_EW_format = True

        # if format is correct, check if values are valid (for now not negative and <50m)
        if variables.distance_EW >= 0 and variables.distance_EW < 50:
            valid_distance_EW_value = True
        else:
            valid_distance_EW_value = False

    except:
        valid_distance_EW_format = False
        valid_distance_EW_value = True

    # dictionary for checking errors in the update function
    variables.valid_distance_EW = {'format': valid_distance_EW_format,
                                   'value': valid_distance_EW_value}


def update_distance_NS(new_distance_NS):
    ''' Checks for an input, if the format is correct (can be cast to float) and the value is in the a valid range (>= 0 and < 50). Changes the value of the distance between panels in N/S direction on submit, if the format is correct.
        
        Parameters: new_distance_NS
        
        Returns: - 
        '''

    try:
        variables.distance_NS = float(new_distance_NS)
        valid_distance_NS_format = True

        # if format is correct, check if values are valid (for now not negative and <50m)
        if variables.distance_NS >= 0 and variables.distance_NS < 50:
            valid_distance_NS_value = True
        else:
            valid_distance_NS_value = False

    except:
        valid_distance_NS_format = False
        valid_distance_NS_value = True

    # dictionary for checking errors in the update function
    variables.valid_distance_NS = {'format': valid_distance_NS_format,
                                   'value': valid_distance_NS_value}


def update_number_EW(new_number_of_panels_EW):
    ''' Checks for an input, if the format is correct (can be cast to int) and the value is in the a valid range (>= 1 and <= 100). Changes the number of panels in E/W direction on submit, if the format is correct.
        
        Parameters: new_number_of_panels_EW
        
        Returns: - 
        '''

    try:
        variables.number_of_panels_EW = int(new_number_of_panels_EW)
        valid_number_of_panels_EW_format = True

        # if format is correct, check if values are valid (for now positive and <= 100 panels)
        if variables.number_of_panels_EW >= 1 and variables.number_of_panels_EW <= 100:
            valid_number_of_panels_EW_value = True
        else:
            valid_number_of_panels_EW_value = False
    except:
        valid_number_of_panels_EW_format = False
        valid_number_of_panels_EW_value = True

    # dictionary for checking errors in the update function
    variables.valid_number_of_panels_EW = {'format': valid_number_of_panels_EW_format,
                                           'value': valid_number_of_panels_EW_value}


def update_number_NS(new_number_of_panels_NS):
    ''' Checks for an input, if the format is correct (can be cast to int) and the value is in the a valid range (>= 1 and <= 100). Changes the number of panels in N/S direction on submit, if the format is correct.
        
        Parameters: new_number_of_panels_NS
        
        Returns: - 
        '''

    try:
        variables.number_of_panels_NS = int(new_number_of_panels_NS)
        valid_number_of_panels_NS_format = True

        # if format is correct, check if values are valid (for now positve and <= 100 panels)
        if variables.number_of_panels_NS >= 1 and variables.number_of_panels_NS <= 100:
            valid_number_of_panels_NS_value = True
        else:
            valid_number_of_panels_NS_value = False

    except:
        valid_number_of_panels_NS_format = False
        valid_number_of_panels_NS_value = True

    # dictionary for checking errors in the update function
    variables.valid_number_of_panels_NS = {'format': valid_number_of_panels_NS_format,
                                           'value': valid_number_of_panels_NS_value}


# ------------------ update system ------------------

def update_system(selected_system):
    ''' Updates plot and values (if applicable) according to selected system.
        
        Parameters: selected_system
        
        Returns: - 
        '''

    match selected_system:
        case 'dynamic (two axis)':
            variables.tracking = False
            # both angles freely selectable
            variables.ax_angle_NS_slider.set_visible(True)
            variables.ax_angle_EW_slider.set_visible(True)

        case 'tracking':
            variables.tracking = True
            # angle in N/S direction is set to 0 (perpenticular to ground), angle in E/W direction freely selectable
            variables.angle_NS_slider.set_val(0)
            variables.ax_angle_NS_slider.set_visible(False)
            
            variables.ax_angle_EW_slider.set_visible(True)
            angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(variables.year, variables.month, variables.day, variables.hour, variables.minute, variables.long, variables.lat)
            angle_in_plane_EW_degrees = (angle_in_plane_EW / math.pi) * 180
            variables.angle_EW_slider.set_val(90 - angle_in_plane_EW_degrees)
            #print(90 - angle_in_plane_EW_degrees)

        case 'vertical':
            # both angles are fixed (panels face E/W -> E/W angle = 90, N/S angle = 0)
            variables.tracking = False

            variables.ax_angle_NS_slider.set_visible(False)
            variables.angle_NS_slider.set_val(0)

            variables.ax_angle_EW_slider.set_visible(False)
            variables.angle_EW_slider.set_val(90)

        case 'optimal':
            # both angles are fixed (E/W angle = 0, N/S angle = 45 (stand in) - meant to represent conventional static PV systems)
            variables.tracking = False

            variables.ax_angle_NS_slider.set_visible(False)
            variables.angle_NS_slider.set_val(45) # placeholder

            variables.ax_angle_EW_slider.set_visible(False)
            variables.angle_EW_slider.set_val(0)

        case 'overhead':
            # both angles are freely selectable (for now) - systems vary here (roofshaped or tilted in one direction)
            variables.tracking = False

            variables.ax_angle_NS_slider.set_visible(True)
            variables.angle_NS_slider.set_val(0)
        
            variables.ax_angle_EW_slider.set_visible(True)
            variables.angle_EW_slider.set_val(0)

        case _:
            print('Something is going wrong regarding PV system selection.')

