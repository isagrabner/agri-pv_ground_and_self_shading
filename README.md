# Agri-PV shade calculation

This program calculates the shaded area created by PV panels on a field in percent of the total area of the given field. It also determines the self-shaded area in percent of the total panel area of a given PV system. Both are done in 15 minute timesteps for one year at a constant longitude and with latitude values between 34° and 72°.

## How to run
After installing the dependencies, the project can be run by simply downloading all project files and running main.py.

Example objects for simulatable system types (standard (current name: optimal), vertical, tracking and overhead systems) can be found at the top of the main.py file. It is possible to choose one of these (currently by uncommenting the chosen system, potential expansion: add possibility for input via terminal), or create your own pv_system object. To do the latter you can copy the syntax used to create the examples (again: potential expansion: add possibility for input via terminal) and change parameters where needed. The available instance variables are described below.

Additionally, the field measurements can be adjusted here. Length and width of the field are set to 80m by default, a 10m buffer is added on each side during shade calculation, resulting in an 100m by 100m (1ha) field.  

### Instance Variables:
- **string system_type**:\
This is the type of system which will be simulated, all string inputs are currently possible, but self-shading will only be calculated to the following system types: "optimal", "vertical" and "tracking". In other cases, the self-shaded area will be set to zero if the sun is over the horizon. If the given system type is "tracking", the panel's tilt in the east/west plane (explained later) will be calculated automatically.

- **float PV_base_height**:\
The base height describes the height of the center of the PV panel above ground. Measurement to be given in meters.

- **float PV_width**:\
Describes the width of the PV panel, which is the dimension of the PV panel in east/west direction here. Measurement to be given in meters.

- **float PV_length**:\
Describes the length of the PV panel, which is the dimension of the PV panel in north/south direction here. Measurement to be given in meters.

- **float distance_EW**:\
This is the distance between PV panels along the east/west axis. It describes the distance between the same point on two panels (e.g. center to center). Measurement to be given in meters.

- **float distance_NS**:\
This is the distance between PV panels along the north/south axis. It describes the distance between the same point on two panels (e.g. center to center). Measurement to be given in meters.

- **int number_of_panels_EW**:\
This variable describes the number of PV panels along the east/west axis.

- **int number_of_panels_NS**:\
This variable describes the number of PV panels along the north/south axis.

- **float PV_angle_NS**:\
This is the tilt angle of the PV panel in the north/south plane. Measurements to be given in degrees.\
A few examples:
  - 0° describes a panel with no tilt, it is horizontal in north/south direction
  - 90° describes a vertical panel facing south
  - -90° describes a vertical panel facing north
  - approx. 35° (with a tilt of 0° in east/west plane) could describe the panel tilt in a standard system.

- **float PV_angle_EW**:\
This is the tilt angle of the PV panel in the north/south plane. This parameter does not need to be specified for all systems (with a default value is 0°) because it is automatically calculated for the tracking system. Measurements to be given in degrees.\
A few examples:
  - 0° describes a panel with no tilt, it is horizontal in east/west direction
  - 90° describes a vertical panel facing east
  - -90° describes a vertical panel facing west
  - a panel with a tilt of either 90° or -90° (and a tilt of 0° in north/south plane) would describe a vertical system

### Output:

After running main.py the output will be a file named "(name_of_your_system_type)_shade_percent_15min.csv". This file includes columns containing latitude, longitude and datetime values (month, day, hour, minute) and the corresponding calculation results. The results columns are:
- **shaded area (in %)**:\
Describes the percentage of the field area which is shaded.

- **self-shaded panel area (in % of total panel area)**:\
Describes the percentage of the total panel area which is shaded by other panels.

- **proximate azimuth of sun**:\
From the actual calculated azimuth an approximate azimuth is determined, which matches with one available in the horizon data file. The azimuths in the horizon data file are evenly spaced in 7.5° steps between -180° and 180°.(e.g. the actual azimuth is -38.1°, the closest available azimuths is -37.5°)

- **apparent elevation of the sun**:\
This describes the apparent elevation of the sun. In combination with the proximate azimuth of the sun this is later used to combine the calculated shading data with horizon data across Europe.

## Requirements
The requirements listed here need to be installed to run this program. They can be installed via the provided shade_calc_env.yml.

- pvlib             0.10.5
- timezonefinder    6.5.0
- pandas            2.2.2
- numpy             1.26.4
- shapely           2.0.4


## Project files

### main.py
Is used to set parameters, call necessary functions and save results.

### pv_system.py
Contains the class system, the instance variables of which are the parameters defining a PV system for this calculation, they include distances between panels, number of panels, measurements etc. The main member functions are used to calculate the shaded/self-shaded area.

### solarposition.py
Contains functions which involve determining the position of the sun at a given timestep.
