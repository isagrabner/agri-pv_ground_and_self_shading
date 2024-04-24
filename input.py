from matplotlib.widgets import TextBox
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Slider
from matplotlib.widgets import Button

import variables

# functions for creating widgets for user input

# --------------------------- text input ---------------------------

# input text box date
def textbox_date(fig):
    '''Creates a text box for date with initial value.'''
    ax_date = fig.add_axes([0.65, 0.85, 0.11, 0.04])
    date_box = TextBox(ax_date, "Date: ", textalignment="center", initial=variables.initial_date)
    return date_box

# input text box time
def textbox_time(fig):
    '''Creates a text box for time with initial value.'''
    ax_time = fig.add_axes([0.65, 0.75, 0.11, 0.04])
    time_box = TextBox(ax_time, "Time: ", textalignment="center", initial=variables.initial_time)
    return time_box

# input text box longitude
def textbox_long(fig):
    '''Creates a text box for longitude with initial value.'''
    ax_long = fig.add_axes([0.65, 0.65, 0.11, 0.04])
    long_box = TextBox(ax_long, "Longitude: ", textalignment="center", initial=variables.long)
    return long_box

# input text box latitude
def textbox_lat(fig):
    '''Creates a text box for latitude with initial value.'''
    ax_lat = fig.add_axes([0.65, 0.55, 0.11, 0.04])
    lat_box = TextBox(ax_lat, "Latitude: ", textalignment="center", initial=variables.lat)
    return lat_box

# input text box PV panel base height
def textbox_base_height(fig):
    '''Creates a text box for base height (of the PV panel) with initial value.'''
    ax_base_height = fig.add_axes([0.875, 0.85, 0.11, 0.04])
    base_height_box = TextBox(ax_base_height, "Base height (in m): ", textalignment="center", initial=variables.PV_base_height)
    return base_height_box

# input text box for PV panel width (dimension in E/W direction)
def textbox_width(fig):
    '''Creates a text box for width (of the PV panel) with initial value.'''
    ax_width = fig.add_axes([0.875, 0.75, 0.11, 0.04])
    width_box = TextBox(ax_width, "Panel width (E/W) (in m): ", textalignment="center", initial=variables.PV_width)
    return width_box

# input text box for PV panel length (dimension in N/S direction)
def textbox_length(fig):
    '''Creates a text box for length (of the PV panel) with initial value.'''
    ax_length = fig.add_axes([0.875, 0.65, 0.11, 0.04])
    length_box = TextBox(ax_length, "Panel length (N/S) (in m): ", textalignment="center", initial=variables.PV_length)
    return length_box

# input text box for PV panel distance in E/W direction
def textbox_distance_EW(fig):
    '''Creates a text box for the distance between PV panels in E/W direction with initial value.'''
    ax_distance_EW = fig.add_axes([0.875, 0.55, 0.11, 0.04])
    distance_EW_box = TextBox(ax_distance_EW, "Panel distance (E/W) (in m): ", textalignment="center", initial=variables.distance_EW)
    return distance_EW_box

# input text box for PV panel distance in N/S direction
def textbox_distance_NS(fig):
    '''Creates a text box for the distance between PV panels in N/S direction with initial value.'''
    ax_distance_NS = fig.add_axes([0.875, 0.45, 0.11, 0.04])
    distance_NS_box = TextBox(ax_distance_NS, "Panel distance (N/S) (in m): ", textalignment="center", initial=variables.distance_NS)
    return distance_NS_box

# input text box for number of panels in E/W direction
def textbox_number_EW(fig):
    '''Creates a text box for the number of PV panels in E/W direction with initial value.'''
    ax_number_EW = fig.add_axes([0.875, 0.35, 0.11, 0.04])
    number_EW_box = TextBox(ax_number_EW, "Number of PV panels E/W: ", textalignment="center", initial=variables.number_of_panels_EW)
    return number_EW_box

# input text box for number of panels in N/S direction
def textbox_number_NS(fig):
    '''Creates a text box for the number of PV panels in N/S direction with initial value.'''
    ax_number_NS = fig.add_axes([0.875, 0.25, 0.11, 0.04])
    number_NS_box = TextBox(ax_number_NS, "Number of PV panels N/S: ", textalignment="center", initial=variables.number_of_panels_NS)
    return number_NS_box


# ---------------- sliders for angles of PV panel -----------------

def slider_angle_EW(fig):
    '''Creates a slider for the angle of the PV panels in E/W direction with initial value.'''
    variables.ax_angle_EW_slider = fig.add_axes([0.1, 0.1, 0.49, 0.03])
    variables.angle_EW_slider = Slider(
        ax=variables.ax_angle_EW_slider,
        label="PV angle E/W",
        valmin=-90,
        valmax=90,
        valinit=0,
        orientation="horizontal")

    return variables.angle_EW_slider

def slider_angle_NS(fig):
    '''Creates a slider for the angle of the PV panels in N/S direction with initial value.'''
    variables.ax_angle_NS_slider = fig.add_axes([0.1, 0.05, 0.49, 0.03])
    variables.angle_NS_slider = Slider(
        ax=variables.ax_angle_NS_slider,
        label="PV angle N/S",
        valmin=-90,
        valmax=90,
        valinit=0,
        orientation="horizontal")

    return variables.angle_NS_slider


# ----------------------- other user inputs -----------------------

# PV system selection
def buttons_system(fig):
    '''Creates a buttons for PV system selection.'''
    axsystems = fig.add_axes([0.65, 0.25, 0.11, 0.24])
    systems_radiobuttons = RadioButtons(axsystems, ('dynamic (two axis)', 'tracking', 'vertical', 'optimal', 'overhead'), active=0, activecolor='black')
    return systems_radiobuttons

# Update button
def button_update(fig):
    '''Creates update button.'''
    axbutton = fig.add_axes([0.65, 0.125, 0.335, 0.04])
    update = Button(axbutton, 'Update')
    return update