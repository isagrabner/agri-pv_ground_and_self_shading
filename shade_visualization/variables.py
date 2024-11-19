# ---------- variables/setting initial values ----------

# date
year, month, day = 2000, 1, 1
initial_date = '01/01/2000'

# time
hour, minute = 12, 0
initial_time = '12:00'

# longitude value
long = 47.6

# latitude value
lat = 17.2

# base height of the PV panel (in m)
PV_base_height = 8

# dimention of the PV panel in E/W direction (in m)
PV_width = 4

# dimention of the PV panel in N/S direction (in m)
PV_length = 10

# distance between the panels in E/W direction (incl. width of panel, in m)
distance_EW = 6

# distance between the panels in N/S direction (incl. length of panel, in m)
distance_NS = 15

# number of panels in E/W direction
number_of_panels_EW = 5

# number of panels in N/S direction
number_of_panels_NS = 8


# dictionaries for checking format and validity of entered values
valid_date =                {'format':True,
                             'value':True} 

valid_time =                {'format':True,
                             'value':True} 

valid_lat =                 {'format':True,
                             'value':True} 

valid_long =                {'format':True,
                             'value':True}

valid_base_height =         {'format':True,
                             'value':True} 

valid_PV_width =            {'format':True,
                             'value':True}

valid_PV_length =           {'format':True,
                             'value':True}

valid_distance_EW =         {'format':True,
                             'value':True}
                    
valid_distance_NS =         {'format':True,
                             'value':True}

valid_number_of_panels_EW = {'format':True,
                             'value':True}

valid_number_of_panels_NS = {'format':True,
                             'value':True}


angle_NS_slider = False
angle_EW_slider = False
ax_angle_NS_slider = False
ax_angle_EW_slider = False

tracking = False
