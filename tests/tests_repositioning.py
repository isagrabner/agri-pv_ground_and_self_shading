import pv_system
import solarposition

import pytest
import math

@pytest.fixture()
def sys_tracking():
    return pv_system.system("tracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0)

@pytest.fixture()
def sys_backtracking():
    return pv_system.system("backtracking", 1.4, 1.2, 80, 10, 80, 9, 1, 0)

@pytest.fixture()
def delta():
    return 1e-4

def test_tracking_repositioning(sys_tracking: pv_system.system, delta: float):
    year, month, day, minute = 2000, 7, 1, 0
    long, lat = 0, 45

    pass_for_all = True

    for hour in [5, 6, 7, 8, 9, 10]:
        angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(year, month, day, hour, minute, long, lat)
        sys_tracking.tracking_repositioning(year, month, day, hour, minute, long, lat)

        if not (sys_tracking.PV_angle_EW < 90 - math.degrees(angle_in_plane_EW) + delta and sys_tracking.PV_angle_EW > 90 - math.degrees(angle_in_plane_EW) - delta):
            print("Calculated value for the panel tilt in E/W direction: ", sys_tracking.PV_angle_EW)
            print("Expected value: ", 90 - math.degrees(angle_in_plane_EW))
            pass_for_all = False
            break
    
    assert pass_for_all

def test_backtracking_repositioning(sys_backtracking: pv_system.system, delta: float):
    year, month, day = 2000, 7, 1
    long, lat = 0, 45

    pass_for_all = True

    for hour in [5]:
        for minute in range(0, 10, 1):
            angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(year, month, day, hour, minute, long, lat)
            sys_backtracking.backtracking_repositioning(year, month, day, hour, minute, long, lat)

            print("\nsun angle in plane: ", math.degrees(angle_in_plane_EW))

            if (sys_backtracking.PV_width - math.sin(angle_in_plane_EW) * sys_backtracking.distance_EW) > 0:
                theoretical_tilt_angle =  math.pi - (math.pi - math.asin((sys_backtracking.distance_EW * math.sin(angle_in_plane_EW))/ sys_backtracking.PV_width)) - angle_in_plane_EW

                print("tilt angle: ", sys_backtracking.PV_angle_EW)
                if not (sys_backtracking.PV_angle_EW < math.degrees(theoretical_tilt_angle) + delta and sys_backtracking.PV_angle_EW > math.degrees(theoretical_tilt_angle) - delta):
                    print("Calculated value for the panel tilt in E/W direction: ", sys_backtracking.PV_angle_EW)
                    print("Expected value: ", math.degrees(theoretical_tilt_angle))
                    pass_for_all = False
                    break
            else:
                print("tilt angle: ", sys_backtracking.PV_angle_EW)
                if not (sys_backtracking.PV_angle_EW < 90 - math.degrees(angle_in_plane_EW) + delta and sys_backtracking.PV_angle_EW > 90 - math.degrees(angle_in_plane_EW) - delta):
                    print("Calculated value for the panel tilt in E/W direction: ", sys_backtracking.PV_angle_EW)
                    print("Expected value: ", 90 - math.degrees(angle_in_plane_EW))
                    pass_for_all = False
                    break
    
    assert pass_for_all