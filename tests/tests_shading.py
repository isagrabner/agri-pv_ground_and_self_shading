import pv_system

import pytest
import math

# functions for calculating tracking/backtracking tilt angles directly from sun beam angle
def tracking_repositioning_for_testing(sys, angle_in_plane_EW):
    '''Readjusts PV panel (tilt angle in E/W plane) in tracking systems based directly on the angle of incoming sunbeams in the E/W plane. Meant for testing.

        Parameters: system, angle_in_plane_EW

        Returns: -'''
    
    angle_in_plane_EW_degrees = (angle_in_plane_EW / math.pi) * 180
    sys.PV_angle_EW = 90 - angle_in_plane_EW_degrees

def backtracking_repositioning_for_testing(sys, angle_in_plane_EW):
    '''Readjusts PV panel (tilt angle in E/W plane) in backtracking systems based directly on the angle of incoming sunbeams in the E/W plane. Meant for testing.

        Parameters: system, angle_in_plane_EW

        Returns: -'''
    
    # regular tracking tilt
    angle_in_plane_EW_degrees = (angle_in_plane_EW / math.pi) * 180
    sys.PV_angle_EW = 90 - angle_in_plane_EW_degrees

    # calculate shade width in self-shading to check if self-shading occurs
    angle_in_plane_EW_mod = angle_in_plane_EW if angle_in_plane_EW <= (math.pi/2) else math.pi - angle_in_plane_EW
    shade_width = sys.PV_width - math.sin(angle_in_plane_EW_mod) * sys.distance_EW

    # adjust panel tilt in E/W plane so no self-shading occurs
    if shade_width > 0 and angle_in_plane_EW > 0:
            if angle_in_plane_EW < 90:
                alpha = math.radians(angle_in_plane_EW_degrees)
                beta = math.pi - math.asin((sys.distance_EW * math.sin(alpha)) / sys.PV_width)
                #print(beta)
                gamma = math.pi - alpha - beta
                sys.PV_angle_EW = math.degrees(gamma)
            else:
                alpha = math.radians(180 - angle_in_plane_EW_degrees)
                beta = math.pi - math.asin((sys.distance_EW * math.sin(alpha)) / sys.PV_width)
                gamma = - (math.pi - alpha - beta)
                sys.PV_angle_EW = - math.degrees(gamma)

# function for calculating sunbeam angles in N/S and E/W plane directly from azimuth and elevation
def calculate_angle_EW_and_NS(elevation_rad, azimuth_rad):
    '''Converts solarposition (elevation and azimuth) to angles in the vertical planes in E/W and N/S direction. Parameters are in radiants, return values in degrees. Meant for testing.
    
        Parameters: elevation_rad, azimuth_rad
        
        Returns: angle_in_plane_EW, angle_in_plane_NS'''
    
    distance_NS = - math.cos(azimuth_rad) * math.cos(elevation_rad) #offset_distance
    distance_EW = math.sin(azimuth_rad) * math.cos(elevation_rad) #offset_distance

    height = math.sin(elevation_rad)

    angle_in_plane_NS = math.pi/2 - math.atan(distance_NS/height) 
    angle_in_plane_EW = math.pi/2 - math.atan(distance_EW/height)

    return angle_in_plane_EW, angle_in_plane_NS


# ------------ defining systems ------------
@pytest.fixture()
def sys_tracking():
    # system used for simulations
    return pv_system.system("tracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0)

    # alternate systems

    # system with even number of separate panels without gaps
    #return pv_system.system("tracking", 1.4, 1.2, 20, 10, 20, 9, 4, 0)

    # system with odd number of separate panels without gaps
    #return pv_system.system("tracking", 1.4, 1.2, 16, 10, 16, 9, 5, 0)

    # system with gaps between panels
    #return pv_system.system("tracking", 1.4, 1.2, 10, 10, 14, 9, 6, 0)

@pytest.fixture()
def sys_vertical():
    # system used for simulations
    return pv_system.system("vertical", 1.4, 1.2, 80, 10, 80, 9, 1, 0, 90)

    # alternate systems

    # system with even number of separate panels without gaps
    #return pv_system.system("vertical", 1.4, 1.2, 20, 10, 20, 9, 4, 0, 90)

    # system with odd number of separate panels without gaps
    #return pv_system.system("vertical", 1.4, 1.2, 16, 10, 16, 9, 5, 0, 90)

    # system with gaps between panels
    #return pv_system.system("vertical", 1.4, 1.2, 10, 10, 14, 9, 6, 0, 90)

@pytest.fixture()
def sys_standard():
    # system used for simulations
    return pv_system.system("standard", 1.5, 80, 2, 80, 10, 1, 9, 35, 0)

    # alternate systems

    # system with even number of separate panels without gaps
    #return pv_system.system("standard", 1.5, 20, 2, 20, 10, 4, 9, 35, 0)

    # system with odd number of separate panels without gaps
    #return pv_system.system("standard", 1.5, 16, 2, 16, 10, 5, 9, 35, 0)

    # system with gaps between panels
    #return pv_system.system("standard", 1.5, 10, 2, 14, 10, 6, 9, 35, 0)

@pytest.fixture()
def sys_overhead():
    # system used for simulations
    return pv_system.system("overhead", 1, 1, 80, 10, 80, 9, 1, 0, 10)

    # alternate systems

    # system with even number of separate panels without gaps
    #return pv_system.system("overhead", 1, 1, 20, 10, 20, 9, 4, 0, 10)

    # system with odd number of separate panels without gaps
    #return pv_system.system("overhead", 1, 1, 16, 10, 16, 9, 5, 0, 10)

    # system with gaps between panels
    #return pv_system.system("overhead", 1, 1, 10, 10, 14, 9, 6, 0, 10)

@pytest.fixture()
def sys_backtracking():
    # system used for simulations
    return pv_system.system("backtracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0)

    # alternate systems

    # system with even number of separate panels without gaps
    #return pv_system.system("backtracking", 1.4, 1.2, 20, 3, 20, 9, 4, 0)

    # system with odd number of separate panels without gaps
    #return pv_system.system("backtracking", 1.4, 1.2, 16, 3, 16, 9, 5, 0)

    # system with gaps between panels
    #return pv_system.system("backtracking", 1.4, 1.2, 10, 3, 14, 9, 6, 0)


# ------------ other parameters ------------
# delta
@pytest.fixture()
def delta():
    return 1e-4

# field width
@pytest.fixture()
def field_width():
    return 80

# field length
@pytest.fixture()
def field_length():
    return 80

# field area
@pytest.fixture()
def total_field_area():
    field_width = 80
    field_length = 80
    return (field_width + 20) * (field_length + 20)


# ------------------ tests ------------------

# --------------- sun overhead ---------------
def test_sun_overhead_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2

    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])

    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area (= expected shade)
    total_panel_area = sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width

    # Test 1: Check if ground shading for tracking system is correctly calculated (sun directly overhead)
    if not ((total_panel_area / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area / total_field_area)*100 - delta < intersection_percent_overhead):
        print("Test 1 failed. Shaded ground area does not match panel area for tracking system with the sun in an overhead position.\nGround shading area (in %) = ", intersection_percent_overhead, "\nPanel area as portion of field area (in %) = ", (total_panel_area / total_field_area)*100)
        
    assert (total_panel_area / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area / total_field_area)*100 - delta < intersection_percent_overhead

def test_sun_overhead_sys_tracking_self_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, math.radians(90))

    # Test 2: Check if self shading for tracking system is correctly calculated (sun directly overhead)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead):
        print("Test 2 failed. Self-shaded area does not match theoretical value (0%) for tracking system with the sun in an overhead position.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_overhead, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead

def test_sun_overhead_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 3: Check if ground shading for vertical system is correctly calculated (sun directly overhead)
    if not (0 + delta > intersection_percent_overhead and 0 - delta < intersection_percent_overhead):
        print("Test 3 failed. Shaded ground area does not match expected value for vertical system with the sun in an overhead position.\nGround shading area (in %) = ", intersection_percent_overhead, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_overhead and 0 - delta < intersection_percent_overhead
            
def test_sun_overhead_sys_vertical_self_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
       
    # Test 4: Check if self shading for vertical system is correctly calculated (sun directly overhead)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead):
        print("Test 4 failed. Self-shaded area does not match theoretical value (0%) for vertical system with the sun in an overhead position.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_overhead, "\nExpected self-shaded area (in %) = ", 0)

    assert (0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead)

def test_sun_overhead_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # panel area projected on ground      
    total_panel_area_projected_on_ground = math.cos(math.radians(sys_standard.PV_angle_NS)) * sys_standard.PV_length * sys_standard.PV_width * sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS
            
    # Test 5: Check if ground shading for standard system is correctly calculated (sun directly overhead)
    if not ((total_panel_area_projected_on_ground / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area_projected_on_ground / total_field_area)*100 - delta < intersection_percent_overhead):
        print("Test 5 failed. Shaded ground area does not match projected panel area for standard system with the sun in an overhead position.\nGround shading area (in %) = ", intersection_percent_overhead, "\nPanel area as portion of field area (in %) = ", (total_panel_area_projected_on_ground / total_field_area)*100)

    assert (total_panel_area_projected_on_ground / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area_projected_on_ground / total_field_area)*100 - delta < intersection_percent_overhead

def test_sun_overhead_sys_standard_self_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 6: Check if self shading for standard system is correctly calculated (sun directly overhead)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead): 
        print("Test 6 failed. Self-shaded area does not match theoretical value (0%) for standard system with the sun in an overhead position.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_overhead, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead

def test_sun_overhead_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # panel area projected on ground
    total_panel_area_projected_on_ground = math.cos(math.radians(sys_overhead.PV_angle_EW)) * sys_overhead.PV_length * sys_overhead.PV_width * sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS
            
    # Test 7: Check if ground shading for overhead system is correctly calculated (sun directly overhead)
    if not ((total_panel_area_projected_on_ground / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area_projected_on_ground / total_field_area)*100 - delta < intersection_percent_overhead):
        print("Test 7 failed. Shaded ground area does not match projected panel area for overhead system with the sun in an overhead position.\nGround shading area (in %) = ", intersection_percent_overhead, "\nPanel area as portion of field area (in %) = ", (total_panel_area_projected_on_ground / total_field_area)*100)

    assert (total_panel_area_projected_on_ground / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area_projected_on_ground / total_field_area)*100 - delta < intersection_percent_overhead
            
def test_sun_overhead_sys_overhead_self_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int): 
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
   
    # Test 8: Check if self shading for overhead system is correctly calculated (sun directly overhead)
    if (0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead):
        print("Test 8 failed. Self-shaded area does not match theoretical value (0%) for overhead system with the sun in an overhead position.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_overhead, "\nExpected self-shaded area (in %) = ", 0)
    
    assert 0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead

def test_sun_overhead_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_backtracking.number_of_panels_EW * sys_backtracking.number_of_panels_NS * sys_backtracking.PV_length * sys_backtracking.PV_width

    # Test 9: Check if ground shading for backtracking system is correctly calculated (sun directly overhead)
    if not ((total_panel_area / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area / total_field_area)*100 - delta < intersection_percent_overhead):
        print("Test 9 failed. Shaded ground area does not match panel area for backtracking system with the sun in an overhead position.\nGround shading area (in %) = ", intersection_percent_overhead, "\nPanel area as portion of field area (in %) = ", (total_panel_area / total_field_area)*100)

    assert (total_panel_area / total_field_area)*100 + delta > intersection_percent_overhead and (total_panel_area / total_field_area)*100 - delta < intersection_percent_overhead
            
def test_sun_overhead_sys_backtracking_self_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.pi/2
    azimuth_rad = math.pi/2
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_overhead, self_shade_percentage_of_total_panel_area_overhead = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
         
    # Test 10: Check if self shading for backtracking system is correctly calculated (sun directly overhead)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead):
        print("Test 10 failed. Self-shaded area does not match theoretical value (0%) for backtracking system with the sun in an overhead position.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_overhead, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_overhead and 0 - delta <= self_shade_percentage_of_total_panel_area_overhead


# ------------ sun at horizon (E) ------------
def test_sun_horizon_E_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 11: Check if ground shading for tracking system is correctly calculated (sun at horizon in the east)
    if not (0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east):
        print("Test 11 failed. Shaded ground area does not match the theoretical value (0%) for tracking system with the sun at the horizon in the east.\nGround shading area (in %) = ", intersection_percent_at_horizon_east, "\nExpected ground shading (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east

def test_sun_horizon_E_sys_tracking_self_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area 
    total_panel_area = sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width
    
    # calculate total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less = (sys_tracking.number_of_panels_EW - 1) * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width 
   
    # Test 12: Check if self shading for tracking system is correctly calculated (sun at horizon in the east) - expected: all rows except for the first one are fully shaded
    if not ((total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east):
        print("Test 12 failed. Self-shaded area does not match theoretical value for tracking system with the sun at the horizon in the east.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_east, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east

def test_sun_horizon_E_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 13: Check if ground shading for vertical system is correctly calculated (sun at horizon in the east)
    if not (0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east):
        print("Test 13 failed. Shaded ground area does not match expected value for vertical system with the sun at the horizon in the east.\nGround shading area (in %) = ", intersection_percent_at_horizon_east, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east

def test_sun_horizon_E_sys_vertical_self_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_vertical.number_of_panels_EW * sys_vertical.number_of_panels_NS * sys_vertical.PV_length * sys_vertical.PV_width

    #calculate total panel area minus 1 row (= expected self-shading)      
    total_panel_area_with_1_row_less = (sys_vertical.number_of_panels_EW - 1) * sys_vertical.number_of_panels_NS * sys_vertical.PV_length * sys_vertical.PV_width

    # Test 14: Check if self shading for vertical system is correctly calculated (sun at horizon in the east)
    if not ((total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east):
        print("Test 14 failed. Self-shaded area does not match theoretical value for vertical system with the sun at the horizon in the east.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_east, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east

def test_sun_horizon_E_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 15: Check if ground shading for standard system is correctly calculated (sun at horizon in the east)
    if not (0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east):
        print("Test 15 failed. Shaded ground area does not match the theoretical value for standard system with the sun at the horizon in the east.\nGround shading area (in %) = ", intersection_percent_at_horizon_east, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east
            
def test_sun_horizon_E_sys_standard_self_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 16: Check if self shading for standard system is correctly calculated (sun at horizon in the east)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east):
        print("Test 16 failed. Self-shaded area does not match the theoretical value (0%) for standard system with the sun at the horizon in the east.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_east, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east

def test_sun_horizon_E_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
    
    # Test 17: Check if ground shading for overhead system is correctly calculated (sun at horizon in the east)
    if not (0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east):
        print("Test 17 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at the horizon in the east.\nGround shading area (in %) = ", intersection_percent_at_horizon_east, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east

def test_sun_horizon_E_sys_overhead_self_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area 
    total_panel_area = sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS * sys_overhead.PV_length * sys_overhead.PV_width

    #calculate total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less = (sys_overhead.number_of_panels_EW - 1) * sys_overhead.number_of_panels_NS * sys_overhead.PV_length * sys_overhead.PV_width
     
    # Test 18: Check if self shading for overhead system is correctly calculated (sun at horizon in the east)
    if not ((total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east):
        print("Test 18 failed. Self-shaded area does not match theoretical value for overhead system with the sun at the horizon in the east.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_east, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east

def test_sun_horizon_E_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 19: Check if ground shading for backtracking system is correctly calculated (sun at the horizon in the east)
    if not (0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east):
        print("Test 19 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at the horizon in the east.\nGround shading area (in %) = ", intersection_percent_at_horizon_east, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_east and 0 - delta < intersection_percent_at_horizon_east

def test_sun_horizon_E_sys_backtracking_self_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_east, self_shade_percentage_of_total_panel_area_at_horizon_east = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 20: Check if self shading for backtracking system is correctly calculated (sun at the horizon in the east)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east):
        print("Test 20 failed. Self-shaded area does not match the theoretical value (0%) for backtracking system with the sun at the horizon in the east.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_east, "\nExpected self-shaded area (in %) = ", 0)
    
    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_east and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_east

# ------------ sun at horizon (S) ------------
def test_sun_horizon_S_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 21: Check if ground shading for tracking system is correctly calculated (sun at horizon in the south)
    if not (0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south):
        print("Test 21 failed. Shaded ground area does not match the theoretical value (0%) for tracking system with the sun at the horizon in the south.\nGround shading area (in %) = ", intersection_percent_at_horizon_south, "\nExpected ground shading (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south

def test_sun_horizon_S_sys_tracking_self_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 22: Check if self shading for tracking system is correctly calculated (sun at horizon in the south)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south):
        print("Test 22 failed. Self-shaded area does not match theoretical value for tracking system with the sun at the horizon in the south.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_south, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south

def test_sun_horizon_S_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 23: Check if ground shading for vertical system is correctly calculated (sun at horizon in the south)
    if not (0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south):
        print("Test 23 failed. Shaded ground area does not match expected value for vertical system with the sun at the horizon in the south.\nGround shading area (in %) = ", intersection_percent_at_horizon_south, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south

def test_sun_horizon_S_sys_vertical_self_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 24: Check if self shading for vertical system is correctly calculated (sun at horizon in the south)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south):
        print("Test 24 failed. Self-shaded area does not match theoretical value for vertical system with the sun at the horizon in the south.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_south, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south

def test_sun_horizon_S_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
        
    # Test 25: Check if ground shading for standard system is correctly calculated (sun at horizon in the south)
    if not (0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south):
        print("Test 25 failed. Shaded ground area does not match the theoretical value for standard system with the sun at the horizon in the south.\nGround shading area (in %) = ", intersection_percent_at_horizon_south, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south

def test_sun_horizon_S_sys_standard_self_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS * sys_standard.PV_length * sys_standard.PV_width
    
    # calculate total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less = sys_standard.number_of_panels_EW * (sys_standard.number_of_panels_NS - 1) * sys_standard.PV_length * sys_standard.PV_width
        
    # Test 26: Check if self shading for standard system is correctly calculated (sun at horizon in the south)
    if not ((total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south):
        print("Test 26 failed. Self-shaded area does not match the theoretical value for standard system with the sun at the horizon in the south.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_south, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south

def test_sun_horizon_S_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 27: Check if ground shading for overhead system is correctly calculated (sun at horizon in the south)
    if not (0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south):
        print("Test 27 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at the horizon in the south.\nGround shading area (in %) = ", intersection_percent_at_horizon_south, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south

def test_sun_horizon_S_sys_overhead_self_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 28: Check if self shading for overhead system is correctly calculated (sun at horizon in the south)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south):
        print("Test 28 failed. Self-shaded area does not match theoretical value for overhead system with the sun at the horizon in the south.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_south, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south

def test_sun_horizon_S_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 29: Check if ground shading for backtracking system is correctly calculated (sun at the horizon in the south)
    if not (0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south):
        print("Test 29 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at the horizon in the south.\nGround shading area (in %) = ", intersection_percent_at_horizon_south, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_south and 0 - delta < intersection_percent_at_horizon_south

def test_sun_horizon_S_sys_backtracking_self_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_south, self_shade_percentage_of_total_panel_area_at_horizon_south = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 30: Check if self shading for backtracking system is correctly calculated (sun at the horizon in the south)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south):
        print("Test 30 failed. Self-shaded area does not match the theoretical value (0%) for backtracking system with the sun at the horizon in the south.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_south, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_south and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_south

# ------------ sun at horizon (W) ------------
def test_sun_horizon_W_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 31: Check if ground shading for tracking system is correctly calculated (sun at horizon in the west)
    if not (0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west):
        print("Test 31 failed. Shaded ground area does not match the theoretical value (0%) for tracking system with the sun at the horizon in the west.\nGround shading area (in %) = ", intersection_percent_at_horizon_west, "\nExpected ground shading (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west

def test_sun_horizon_W_sys_tracking_self_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width

    # calculate total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less = (sys_tracking.number_of_panels_EW - 1) * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width 

    # Test 32: Check if self shading for tracking system is correctly calculated (sun at horizon in the west) - expected: all rows except for the first one are fully shaded
    if not ((total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west):
        print("Test 32 failed. Self-shaded area does not match theoretical value for tracking system with the sun at the horizon in the west.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_west, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west

def test_sun_horizon_W_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 33: Check if ground shading for vertical system is correctly calculated (sun at horizon in the west)
    if not (0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west):
        print("Test 33 failed. Shaded ground area does not match expected value for vertical system with the sun at the horizon in the west.\nGround shading area (in %) = ", intersection_percent_at_horizon_west, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west

def test_sun_horizon_W_sys_vertical_self_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_vertical.number_of_panels_EW * sys_vertical.number_of_panels_NS * sys_vertical.PV_length * sys_vertical.PV_width
    
    # calculate total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less = (sys_vertical.number_of_panels_EW - 1) * sys_vertical.number_of_panels_NS * sys_vertical.PV_length * sys_vertical.PV_width

    # Test 34: Check if self shading for vertical system is correctly calculated (sun at horizon in the west)
    if not ((total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west):
        print("Test 34 failed. Self-shaded area does not match theoretical value for vertical system with the sun at the horizon in the west.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_west, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less / total_panel_area) * 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and (total_panel_area_with_1_row_less / total_panel_area) * 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west

def test_sun_horizon_W_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 35: Check if ground shading for standard system is correctly calculated (sun at horizon in the west)
    if not (0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west):
        print("Test 35 failed. Shaded ground area does not match the theoretical value for standard system with the sun at the horizon in the west.\nGround shading area (in %) = ", intersection_percent_at_horizon_west, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west

def test_sun_horizon_W_sys_standard_self_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 36: Check if self shading for standard system is correctly calculated (sun at horizon in the west)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west):
        print("Test 36 failed. Self-shaded area does not match the theoretical value (0%) for standard system with the sun at the horizon in the west.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_west, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west

def test_sun_horizon_W_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 37: Check if ground shading for overhead system is correctly calculated (sun at horizon in the west)
    if not (0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west):
        print("Test 37 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at the horizon in the west.\nGround shading area (in %) = ", intersection_percent_at_horizon_west, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west

def test_sun_horizon_W_sys_overhead_self_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 38: Check if self shading for overhead system is correctly calculated (sun at horizon in the west)
    if not (100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west):
        print("Test 38 failed. Self-shaded area does not match theoretical value for overhead system with the sun at the horizon in the west.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_west, "\nExpected self-shaded area (in %) = ", 0)

    assert 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west

def test_sun_horizon_W_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])

    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 39: Check if ground shading for backtracking system is correctly calculated (sun at the horizon in the west)
    if not (0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west):
        print("Test 39 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at the horizon in the west.\nGround shading area (in %) = ", intersection_percent_at_horizon_west, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_west and 0 - delta < intersection_percent_at_horizon_west

def test_sun_horizon_W_sys_backtracking_self_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi * (3/2)
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])

    # calculate shade percentages
    intersection_percent_at_horizon_west, self_shade_percentage_of_total_panel_area_at_horizon_west = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 40: Check if self shading for backtracking system is correctly calculated (sun at the horizon in the west)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west):
        print("Test 40 failed. Self-shaded area does not match the theoretical value (0%) for backtracking system with the sun at the horizon in the west.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_west, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_west and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_west

# ------------ sun at horizon (N) ------------
def test_sun_horizon_N_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 41: Check if ground shading for tracking system is correctly calculated (sun at horizon in the north)
    if not (0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north):
        print("Test 41 failed. Shaded ground area does not match the theoretical value (0%) for tracking system with the sun at the horizon in the north.\nGround shading area (in %) = ", intersection_percent_at_horizon_north, "\nExpected ground shading (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north

def test_sun_horizon_N_sys_tracking_self_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 42: Check if self shading for tracking system is correctly calculated (sun at horizon in the north) - expected: all rows except for the first one are fully shaded
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north):
        print("Test 42 failed. Self-shaded area does not match theoretical value for tracking system with the sun at the horizon in the north.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_north, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north

def test_sun_horizon_N_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 43: Check if ground shading for vertical system is correctly calculated (sun at horizon in the north)
    if not (0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north):
        print("Test 43 failed. Shaded ground area does not match expected value for vertical system with the sun at the horizon in the north.\nGround shading area (in %) = ", intersection_percent_at_horizon_north, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north

def test_sun_horizon_N_sys_vertical_self_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 44: Check if self shading for vertical system is correctly calculated (sun at horizon in the north)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north):
        print("Test 44 failed. Self-shaded area does not match theoretical value for vertical system with the sun at the horizon in the north.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_north, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north

def test_sun_horizon_N_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 45: Check if ground shading for standard system is correctly calculated (sun at horizon in the north)
    if not (0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north):
        print("Test 45 failed. Shaded ground area does not match the theoretical value for standard system with the sun at the horizon in the north.\nGround shading area (in %) = ", intersection_percent_at_horizon_north, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north

def test_sun_horizon_N_sys_standard_self_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 46: Check if self shading for standard system is correctly calculated (sun at horizon in the north)
    if not (100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north):
        print("Test 46 failed. Self-shaded area does not match the theoretical value for standard system with the sun at the horizon in the north.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_north, "\nExpected self-shaded area (in %) = ", 0)

    assert 100 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 100 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north

def test_sun_horizon_N_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # Test 47: Check if ground shading for overhead system is correctly calculated (sun at horizon in the north)
    if not (0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north):
        print("Test 47 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at the horizon in the north.\nGround shading area (in %) = ", intersection_percent_at_horizon_north, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north

def test_sun_horizon_N_sys_overhead_self_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
    
    # Test 48: Check if self shading for overhead system is correctly calculated (sun at horizon in the north)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north):
        print("Test 48 failed. Self-shaded area does not match theoretical value for overhead system with the sun at the horizon in the north.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_north, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north

def test_sun_horizon_N_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
    
    # Test 49: Check if ground shading for backtracking system is correctly calculated (sun at the horizon in the north)
    if not (0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north):
        print("Test 49 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at the horizon in the north.\nGround shading area (in %) = ", intersection_percent_at_horizon_north, "\nExpected ground shading area (in %) = ", 0)

    assert 0 + delta > intersection_percent_at_horizon_north and 0 - delta < intersection_percent_at_horizon_north

def test_sun_horizon_N_sys_backtracking_self_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = 0

    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent_at_horizon_north, self_shade_percentage_of_total_panel_area_at_horizon_north = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)
    
    # Test 50: Check if self shading for backtracking system is correctly calculated (sun at the horizon in the north)
    if not (0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north):
        print("Test 50 failed. Self-shaded area does not match the theoretical value (0%) for backtracking system with the sun at the horizon in the north.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area_at_horizon_north, "\nExpected self-shaded area (in %) = ", 0)

    assert 0 + delta >= self_shade_percentage_of_total_panel_area_at_horizon_north and 0 - delta <= self_shade_percentage_of_total_panel_area_at_horizon_north

# ----------- half self-shade width -----------
def test_half_self_shade_width_sys_tracking(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    azimuth_rad = math.pi/2
    # find sun angle at which self-shading should be half on panel rows behind the first one
    elevation_rad = math.asin((sys_tracking.PV_width * 0.5)/sys_tracking.distance_EW)

    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_tracking.number_of_panels_NS * (sys_tracking.number_of_panels_EW - 1) * sys_tracking.PV_length * sys_tracking.PV_width)/2
     
    # Test 51: Check if self-shading is half on panel rows behind the first one for chosen sun angle in tracking system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 51 failed. Self-shaded area does not match the theoretical value for tracking system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

def test_half_self_shade_width_sys_vertical(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    azimuth_rad = math.pi/2
    # find sun angle at which self-shading should be half on panel rows behind the first one
    elevation_rad = math.atan((sys_vertical.PV_width * 0.5)/sys_vertical.distance_EW)

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_vertical.number_of_panels_EW * sys_vertical.number_of_panels_NS * sys_vertical.PV_length * sys_vertical.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_vertical.number_of_panels_NS * (sys_vertical.number_of_panels_EW - 1) * sys_vertical.PV_length * sys_vertical.PV_width)/2

    # Test 52: Check if self-shading is half on panel rows behind the first one for chosen sun angle in vertical system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 52 failed. Self-shaded area does not match the theoretical value for vertical system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

def test_half_self_shade_width_sys_standard(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    azimuth_rad = math.pi
    # find sun angle at which self-shading should be half on panel rows behind the first one   
    c = math.sqrt((sys_standard.PV_length/2)**2 + sys_standard.distance_NS**2 - 2 * (sys_standard.PV_length/2) * sys_standard.distance_NS * math.cos(math.radians(sys_standard.PV_angle_NS)))
    elevation_rad = math.acos((c**2 - (sys_standard.PV_length/2)**2 + sys_standard.distance_NS**2) / (2 * c * sys_standard.distance_NS))

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS * sys_standard.PV_length * sys_standard.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_standard.number_of_panels_EW * (sys_standard.number_of_panels_NS - 1) * sys_standard.PV_length * sys_standard.PV_width)/2

    # Test 53: Check if self-shading is half on panel rows behind the first one for chosen sun angle in standard system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 53 failed. Self-shaded area does not match the theoretical value for standard system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

def test_half_self_shade_width_sys_overhead(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    azimuth_rad = math.pi/2
    # find sun angle at which self-shading should be half on panel rows behind the first one   
    c = math.sqrt((sys_overhead.PV_width/2)**2 + sys_overhead.distance_EW**2 - 2 * (sys_overhead.PV_width/2) * sys_overhead.distance_EW * math.cos(math.radians(sys_overhead.PV_angle_EW)))
    elevation_rad = math.acos((c**2 - (sys_overhead.PV_width/2)**2 + sys_overhead.distance_EW**2) / (2 * c * sys_overhead.distance_EW))

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS * sys_overhead.PV_length * sys_overhead.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_overhead.number_of_panels_NS * (sys_overhead.number_of_panels_EW - 1) * sys_overhead.PV_length * sys_overhead.PV_width)/2

    # Test 54: Check if self-shading is half on panel rows behind the first one for chosen sun angle in overhead system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 54 failed. Self-shaded area does not match the theoretical value for overhead system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

# ----------- half self-shade length -----------
def test_half_self_shade_length_sys_tracking(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2 + math.atan((field_length/2)/sys_tracking.distance_EW)

    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS * sys_tracking.PV_length * sys_tracking.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_tracking.number_of_panels_NS * (sys_tracking.number_of_panels_EW - 1) * sys_tracking.PV_length * sys_tracking.PV_width)/2
    
    # Test 55: Check if self-shading is half on panel rows behind the first one for chosen sun angle in tracking system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 55 failed. Self-shaded area does not match the theoretical value for tracking system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

def test_half_self_shade_length_sys_vertical(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2 + math.atan((field_length/2)/sys_vertical.distance_EW)

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_vertical.number_of_panels_EW * sys_vertical.number_of_panels_NS * sys_vertical.PV_length * sys_vertical.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_vertical.number_of_panels_NS * (sys_vertical.number_of_panels_EW - 1) * sys_vertical.PV_length * sys_vertical.PV_width)/2
    
    # Test 56: Check if self-shading is half on panel rows behind the first one for chosen sun angle in vertical system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 56 failed. Self-shaded area does not match the theoretical value for vertical system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

def test_half_self_shade_length_sys_standard(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2 + math.atan(sys_standard.distance_NS/(field_length/2))

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS * sys_standard.PV_length * sys_standard.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_standard.number_of_panels_EW * (sys_standard.number_of_panels_NS - 1) * sys_standard.PV_length * sys_standard.PV_width)/2
    
    # Test 57: Check if self-shading is half on panel rows behind the first one for chosen sun angle in standard system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 57 failed. Self-shaded area does not match the theoretical value for standard system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

def test_half_self_shade_length_sys_overhead(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = 1e-10
    azimuth_rad = math.pi/2 + math.atan((field_length/2)/sys_overhead.distance_EW)

    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    # calculate total panel area
    total_panel_area = sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS * sys_overhead.PV_length * sys_overhead.PV_width
    
    # calculate half of total panel area minus 1 row (= expected self-shading)
    total_panel_area_with_1_row_less_half = (sys_overhead.number_of_panels_NS * (sys_overhead.number_of_panels_EW - 1) * sys_overhead.PV_length * sys_overhead.PV_width)/2
    
    # Test 58: Check if self-shading is half on panel rows behind the first one for chosen sun angle in standard system
    if not ((total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area):
        print("Test 58 failed. Self-shaded area does not match the theoretical value for overhead system.\nSelf-shaded area (in %) = ", self_shade_percentage_of_total_panel_area, "\nExpected self-shaded area (in %) = ", (total_panel_area_with_1_row_less_half / total_panel_area) * 100)

    assert (total_panel_area_with_1_row_less_half / total_panel_area) * 100 + delta > self_shade_percentage_of_total_panel_area and (total_panel_area_with_1_row_less_half / total_panel_area) * 100 - delta < self_shade_percentage_of_total_panel_area

# ------ test ground shading 80° elevation -----
# tracking system
def test_sun_80_deg_E_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi/2

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_tracking.PV_length * (sys_tracking.PV_width / math.sin(sun_angle_EW)) * sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS)) / total_field_area
    
    # Test 59: Check if ground shading for tracking system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 59 failed. Shaded ground area does not match the theoretical value for tracking system with the sun at the 80° elevation in the east.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_W_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi * (3/2)

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_tracking.PV_length * (sys_tracking.PV_width / math.sin(sun_angle_EW)) * sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS)) / total_field_area
    
    # Test 60: Check if ground shading for tracking system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 60 failed. Shaded ground area does not match the theoretical value for tracking system with the sun at 80° elevation in the west.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_S_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (sys_tracking.PV_width * sys_tracking.PV_length * sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS) / total_field_area
    
    # Test 61: Check if ground shading for tracking system is correctly calculated 
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 61 failed. Shaded ground area does not match the theoretical value for tracking system with the sun at 80° elevation in the south.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_N_sys_tracking_ground_shading(sys_tracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = 0
    
    # reposition PV panel according to sun position
    tracking_repositioning_for_testing(sys_tracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_tracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (sys_tracking.PV_width * sys_tracking.PV_length * sys_tracking.number_of_panels_EW * sys_tracking.number_of_panels_NS) / total_field_area
    
    # Test 62: Check if ground shading for tracking system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 62 failed. Shaded ground area does not match the theoretical value for tracking system with the sun at 80° elevation in the north.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

# vertical system
def test_sun_80_deg_E_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi/2

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_vertical.PV_length * (sys_vertical.PV_width / math.tan(sun_angle_EW)) * sys_vertical.number_of_panels_EW * sys_vertical.number_of_panels_NS)) / total_field_area
    
    # Test 63: Check if ground shading for vertical system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 63 failed. Shaded ground area does not match the theoretical value for vertical system with the sun at the 80° elevation in the east.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_W_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi * (3/2)

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_vertical.PV_length * (sys_vertical.PV_width / abs(math.tan(sun_angle_EW))) * sys_vertical.number_of_panels_EW * sys_vertical.number_of_panels_NS)) / total_field_area
    
    # Test 64: Check if ground shading for vertical system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 64 failed. Shaded ground area does not match the theoretical value for vertical system with the sun at 80° elevation in the west.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_S_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = 0
    # Test 65: Check if ground shading for vertical system is correctly calculated 
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 65 failed. Shaded ground area does not match the theoretical value for vertical system with the sun at 80° elevation in the south.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_N_sys_vertical_ground_shading(sys_vertical: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = 0
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_vertical.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = 0
    # Test 66: Check if ground shading for vertical system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 66 failed. Shaded ground area does not match the theoretical value for vertical system with the sun at 80° elevation in the north.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

# standard system
def test_sun_80_deg_E_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi/2
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (math.cos(math.radians(sys_standard.PV_angle_NS)) * sys_standard.PV_length * sys_standard.PV_width * sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS) / total_field_area
    
    # Test 67: Check if ground shading for standard system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 67 failed. Shaded ground area does not match the theoretical value for standard system with the sun at the 80° elevation in the east.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_W_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi * (3/2)
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (math.cos(math.radians(sys_standard.PV_angle_NS)) * sys_standard.PV_length * sys_standard.PV_width * sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS) / total_field_area
    
    # Test 68: Check if ground shading for standard system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 68 failed. Shaded ground area does not match the theoretical value for standard system with the sun at 80° elevation in the west.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_S_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_standard.PV_length * math.sin(math.pi - sun_angle_NS - math.radians(sys_standard.PV_angle_NS)) / math.sin(sun_angle_NS)) * sys_standard.PV_width * sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS) / total_field_area
    
    # Test 69: Check if ground shading for standard system is correctly calculated 
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 69 failed. Shaded ground area does not match the theoretical value for standard system with the sun at 80° elevation in the south.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_N_sys_standard_ground_shading(sys_standard: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = 0

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_standard.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_standard.PV_length * math.sin(math.pi - sun_angle_NS - math.radians(sys_standard.PV_angle_NS)) / math.sin(sun_angle_NS)) * sys_standard.PV_width * sys_standard.number_of_panels_EW * sys_standard.number_of_panels_NS) / total_field_area
    
    # Test 70: Check if ground shading for standard system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 70 failed. Shaded ground area does not match the theoretical value for standard system with the sun at 80° elevation in the north.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

# overhead system
def test_sun_80_deg_E_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi/2

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_overhead.PV_width * math.sin(math.pi - sun_angle_EW - math.radians(sys_overhead.PV_angle_EW)) / math.sin(sun_angle_EW)) * sys_overhead.PV_length * sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS) / total_field_area
    
    # Test 71: Check if ground shading for overhead system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 71 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at the 80° elevation in the east.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_W_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi * (3/2)

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_overhead.PV_width * math.sin(math.pi - sun_angle_EW - math.radians(sys_overhead.PV_angle_EW)) / math.sin(sun_angle_EW)) * sys_overhead.PV_length * sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS) / total_field_area
    
    # Test 72: Check if ground shading for overhead system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 72 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at 80° elevation in the west.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_S_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (math.cos(math.radians(sys_overhead.PV_angle_EW)) * sys_overhead.PV_length * sys_overhead.PV_width * sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS) / total_field_area
    
    # Test 73: Check if ground shading for tracking system is correctly calculated 
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 73 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at 80° elevation in the south.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_N_sys_overhead_ground_shading(sys_overhead: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = 0
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_overhead.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (math.cos(math.radians(sys_overhead.PV_angle_EW)) * sys_overhead.PV_length * sys_overhead.PV_width * sys_overhead.number_of_panels_EW * sys_overhead.number_of_panels_NS) / total_field_area
    
    # Test 74: Check if ground shading for overhead system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 74 failed. Shaded ground area does not match the theoretical value for overhead system with the sun at 80° elevation in the north.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

# backtracking system
def test_sun_80_deg_E_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi/2

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_backtracking.PV_length * (sys_backtracking.PV_width / math.sin(sun_angle_EW)) * sys_backtracking.number_of_panels_EW * sys_backtracking.number_of_panels_NS)) / total_field_area
    
    # Test 75: Check if ground shading for backtracking system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 75 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at the 80° elevation in the east.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_W_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi * (3/2)

    # calculate sun angles in N/S and E/W plane
    sun_angle_EW = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0]
    sun_angle_NS = calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1]
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = ((sys_backtracking.PV_length * (sys_backtracking.PV_width / math.sin(sun_angle_EW)) * sys_backtracking.number_of_panels_EW * sys_backtracking.number_of_panels_NS)) / total_field_area
    
    # Test 76: Check if ground shading for backtracking system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 76 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at 80° elevation in the west.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_S_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = math.pi
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (sys_backtracking.PV_width * sys_backtracking.PV_length * sys_backtracking.number_of_panels_EW * sys_backtracking.number_of_panels_NS) / total_field_area
    
    # Test 77: Check if ground shading for backtracking system is correctly calculated 
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 77 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at 80° elevation in the south.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)

def test_sun_80_deg_N_sys_backtracking_ground_shading(sys_backtracking: pv_system.system, delta: float, field_width: int, field_length: int, total_field_area: int):
    # setting elevation and azimuth
    elevation_rad = math.radians(80)
    azimuth_rad = 0
    
    # reposition PV panel according to sun position
    backtracking_repositioning_for_testing(sys_backtracking, calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0])
    
    # calculate shade percentages
    intersection_percent, self_shade_percentage_of_total_panel_area = sys_backtracking.calculate_shade(calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[0], calculate_angle_EW_and_NS(elevation_rad, azimuth_rad)[1], field_width, field_length, azimuth_rad, elevation_rad)

    expected_ground_shading = (sys_backtracking.PV_width * sys_backtracking.PV_length * sys_backtracking.number_of_panels_EW * sys_backtracking.number_of_panels_NS) / total_field_area
    
    # Test 78: Check if ground shading for backtracking system is correctly calculated
    if not (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent):
        print("Test 78 failed. Shaded ground area does not match the theoretical value for backtracking system with the sun at 80° elevation in the north.\nGround shading area (in %) = ", intersection_percent, "\nExpected ground shading (in %) = ", expected_ground_shading * 100)

    assert (expected_ground_shading * 100 + delta > intersection_percent and expected_ground_shading * 100 - delta < intersection_percent)
