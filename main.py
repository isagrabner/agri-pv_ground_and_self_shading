import matplotlib.pyplot as plt

import update
import variables
import shade
import solarposition
import input

# Program to display the area shaded by a dynamic PV system and calculate the shaded area, includes an interactive graph where the angle of the incoming sunbeams can be changed (angle in N/S direction -> alpha, angle in E/W direction -> beta).

# ------------------------ error checks ------------------------

def check_for_errors():
    '''Checks if date is correctly formated and valid.
    
       Parameters:
       errors (string): list of errors

       Returns:
       valid_date (bool): describes if the date is valid;
       errors (string): list of errors'''

    # string for errors to be printed if shade cannot be plotted
    errors = ''
    # number of errors
    number_of_errors = 0

    # arrays of error types and dictionaries containing errors to be accessed in for loop
    error_dicts = [variables.valid_date, variables.valid_time, variables.valid_lat, variables.valid_long, variables.valid_base_height, variables.valid_PV_width, variables.valid_PV_length, variables.valid_distance_EW, variables.valid_distance_NS, variables.valid_number_of_panels_EW, variables.valid_number_of_panels_NS]
    error_types = ['date', 'time', 'latitude', 'longitude', 'base height', 'PV panel width', 'PV panel length', 'distance in E/W direction', 'distance in N/S direction', 'number of panels in E/W direction', 'number of panels in N/S direction']

    # loop checking if errors regarding format or value occured during setting of new values, adds error messsages to errors and counts errors 
    for i in range(0, len(error_dicts)):
        if error_dicts[i]['format'] == False:
            errors = errors + ('' if len(errors) == 0 else '\n') + 'Given ' + error_types[i] + ' is formated incorrectly.'
            number_of_errors += 1
        elif error_dicts[i]['value'] == False:
            errors = errors + ('' if len(errors) == 0 else '\n') + 'Given ' + error_types[i] + ' is invalid.'
            number_of_errors += 1
    
    return errors, number_of_errors


# ------------------------- update plot ------------------------

def update_plot(val):
    '''Checks for errors in inputs and - if no errors occur - updates the plot of shaded areas after the update button is clicked.'''

    ax.clear()

    errors, number_of_errors = check_for_errors()

    # calculating sun position and checking for invalid values
    if number_of_errors == 0:
        angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(variables.year, variables.month, variables.day, variables.hour, variables.minute, variables.long, variables.lat)
        errors, number_of_errors = solarposition.check_solarposition(angle_in_plane_EW, angle_in_plane_NS, errors, number_of_errors)
    
    # if all values are valid plot shaddows, print the errors otherwise
    if number_of_errors == 0:
        shade.calculate_shade(angle_EW_slider.val, angle_NS_slider.val, angle_in_plane_EW, angle_in_plane_NS, ax)
    else:
        ax.text(0.5, 0.5, 'Errors:\n' + errors, fontsize=12, color='red', ha='center', va='center')


# ---------------------------- main ----------------------------
# setting plot area for graphic
fig,ax = plt.subplots()
fig.subplots_adjust(right=0.6, left=0.06, bottom=0.25)

update.update_date(variables.initial_date)
update.update_time(variables.initial_time)


# ----------------- create textboxes for input -----------------

date_box = input.textbox_date(fig)
time_box = input.textbox_time(fig)
long_box = input.textbox_long(fig)
lat_box = input.textbox_lat(fig)
base_height_box = input.textbox_base_height(fig)
width_box = input.textbox_width(fig)
length_box = input.textbox_length(fig)
distance_EW_box = input.textbox_distance_EW(fig)
distance_NS_box = input.textbox_distance_NS(fig)
number_EW_box = input.textbox_number_EW(fig)
number_NS_box = input.textbox_number_NS(fig)


# --------- update values with textbox input on submit ---------

date_box.on_submit(update.update_date)
time_box.on_submit(update.update_time)
long_box.on_submit(update.update_long)
lat_box.on_submit(update.update_lat)
base_height_box.on_submit(update.update_base_height)
width_box.on_submit(update.update_width)
length_box.on_submit(update.update_length)
distance_EW_box.on_submit(update.update_distance_EW)
distance_NS_box.on_submit(update.update_distance_NS)
number_EW_box.on_submit(update.update_number_EW)
number_NS_box.on_submit(update.update_number_NS)


# --------------------- other user inputs ----------------------

# PV system selection
systems_radiobuttons = input.buttons_system(fig)
systems_radiobuttons.on_clicked(update.update_system)

# button for updating plot
update_button = input.button_update(fig)
update_button.on_clicked(update_plot)

# sliders for PV panel angle
angle_EW_slider = input.slider_angle_EW(fig)
angle_EW_slider.on_changed(update_plot)

angle_NS_slider = input.slider_angle_NS(fig)
angle_NS_slider.on_changed(update_plot)


# ---------------------------- plot ----------------------------

# show plot (maximized)
figManager = plt.get_current_fig_manager()
try:
    figManager.resize(*figManager.window.maxsize())
except:
    figManager.window.showMaximized()
plt.show()