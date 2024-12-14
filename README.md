Agri-PV shade calculation

This program calculates the shaded area created by PV panels on a field in percent of the total area of the given field. It also determines the self-shaded area in percent of the total panel area of a given PV system. Both is done in 15 minute timesteps for one year at a constant longitude and with latitude values between 34° and 72°.

How to run:
After installing the dependencies, the project can be run by simply downloading all project files and running main.py.


Requirements:
- pvlib             0.10.5
- timezonefinder    6.5.0
- pandas            2.2.2
- numpy             1.26.4
- shapely           2.0.4


Project files:

main.py
Is used to set parameters, call necessary functions and save results.

pv_system.py
Contains the class system, the instance variables of which are the parameters defining a PV system for this calculation, they include distances between panels, number of panels, measurements etc. The main member functions are used to calculate the shaded/self-shaded area.

solarposition.py
Contains functions which involve determining the position of the sun at a given timestep.
