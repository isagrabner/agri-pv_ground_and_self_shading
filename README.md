Agri-PV shade visualization


This is a program for visualizing the shade created by a PV system depending on date, time, longitude, latitude and various parameters defining the PV system. Inputs can be changed by the user in a visual interface.


How to run:
After installing the dependencies, the project can be run by simply downloading all project files and running main.py.
Example images of how the inital window should look and one for the system switched to tracking can be found in the Examples folder.


Requirements:
- matplotlib        3.8.2
- numpy             1.26.3
- pandas            2.1.4
- pvlib             0.10.3
- shapely           2.0.2
- timezonefinder    6.4.1


Project files:

main.py
Sets up the inital plot and inputs (by calling the functions in input.py). Calls the functions for input updating (from update.py). It checks for errors in the input and updates the plot.

shade.py
Contains the function calculating the shaded area for the PV system depending on the position of the sun and the PV system parameters.

update.py
Contains the functions for updating the parameters according to the user input. The validity of the input is also checked here.

input.py
Creates textboxes, buttons and sliders for user input. Sets their inital values.

solarposition.py
Contains functions for calculating the solar position (split in angle in E/W and N/S direction) and for checking if the sun is in a valid polition (over the horizon) - currently actual horizon data is not included here, because it's not available yet.

variables.py
Contains the parameters defining the PV system and sun position as well as dictionaries containing their validity. The parameters are set to the inital values and accessed and updated in the other files.


Licence:
Windows95man - No Rules!
