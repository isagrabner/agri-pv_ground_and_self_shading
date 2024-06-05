import math
import numpy as np
from matplotlib.patches import Polygon
from shapely.geometry import Polygon as shapely_Polygon
from shapely.ops import unary_union

import variables

def calculate_shade(PV_angle_EW, PV_angle_NS, angle_in_plane_EW, angle_in_plane_NS, ax):
    ''' Calculates the position and area of the shade created by PV panels. Adds both to plot.
    
        Parameters: PV_angle_EW, PV_angle_NS, angle_in_plane_EW, angle_in_plane_NS, ax
        
        Returns: - 
        '''
    
    PV_angle_EW_rad = (PV_angle_EW / 180)*math.pi       # angle of the PV Panel (in east/west direction) (in rad)
    PV_angle_NS_rad = (PV_angle_NS / 180)*math.pi       # angle of the PV Panel (in north/south direction) (in rad)

    # edge height differences
    height_diff_N = math.sin(PV_angle_NS_rad) * variables.PV_length / 2
    height_diff_S = - math.sin(PV_angle_NS_rad) * variables.PV_length / 2
    height_diff_E = - math.sin(PV_angle_EW_rad) * variables.PV_width / 2
    height_diff_W = math.sin(PV_angle_EW_rad) * variables.PV_width / 2

    # corner height differences
    PV_height_NE = variables.PV_base_height + height_diff_N + height_diff_E
    PV_height_NW = variables.PV_base_height + height_diff_N + height_diff_W
    PV_height_SE = variables.PV_base_height + height_diff_S + height_diff_E
    PV_height_SW = variables.PV_base_height + height_diff_S + height_diff_W

    # shadow position

    # x coordinates
    x_PV_shadow_NE = abs(math.cos(PV_angle_EW_rad)) * (variables.PV_width / 2) - PV_height_NE / math.tan(angle_in_plane_EW)
    x_PV_shadow_NW = - abs(math.cos(PV_angle_EW_rad)) * (variables.PV_width / 2) - PV_height_NW / math.tan(angle_in_plane_EW)
    x_PV_shadow_SE = abs(math.cos(PV_angle_EW_rad)) * (variables.PV_width / 2) - PV_height_SE / math.tan(angle_in_plane_EW)
    x_PV_shadow_SW = - abs(math.cos(PV_angle_EW_rad)) * (variables.PV_width / 2) - PV_height_SW / math.tan(angle_in_plane_EW)

    # y coordinates
    y_PV_shadow_NE = PV_height_NE / math.tan(angle_in_plane_NS) + abs(math.cos(PV_angle_NS_rad)) * variables.PV_length
    y_PV_shadow_NW = PV_height_NW / math.tan(angle_in_plane_NS) + abs(math.cos(PV_angle_NS_rad)) * variables.PV_length
    y_PV_shadow_SE = PV_height_SE / math.tan(angle_in_plane_NS)
    y_PV_shadow_SW = PV_height_SW / math.tan(angle_in_plane_NS)

    # inital shapely polygon
    poly_sum = shapely_Polygon([(x_PV_shadow_SW, y_PV_shadow_SW), (x_PV_shadow_SE, y_PV_shadow_SE), (x_PV_shadow_NE, y_PV_shadow_NE), (x_PV_shadow_NW, y_PV_shadow_NW)])

    # plotting individual shaddows and adding shaded areas to polygon
    for i in range(0, variables.number_of_panels_NS):
        for j in range(0, variables.number_of_panels_EW):
            # adding shade patch to plot
            y = np.array([[x_PV_shadow_SW + j * variables.distance_EW, y_PV_shadow_SW + i * variables.distance_NS], [x_PV_shadow_SE + j * variables.distance_EW, y_PV_shadow_SE + i * variables.distance_NS], [x_PV_shadow_NE + j * variables.distance_EW, y_PV_shadow_NE + i * variables.distance_NS], [x_PV_shadow_NW + j * variables.distance_EW, y_PV_shadow_NW + i * variables.distance_NS]])
            p = Polygon(y, facecolor = 'k')
            ax.add_patch(p)

            if(i != 0 or j != 0):
                # adding new shade polygon to existing shapely polygon
                poly_new = shapely_Polygon([(x_PV_shadow_SW + j * variables.distance_EW, y_PV_shadow_SW + i * variables.distance_NS), (x_PV_shadow_SE + j * variables.distance_EW, y_PV_shadow_SE + i * variables.distance_NS), (x_PV_shadow_NE + j * variables.distance_EW, y_PV_shadow_NE + i * variables.distance_NS), (x_PV_shadow_NW + j * variables.distance_EW, y_PV_shadow_NW + i * variables.distance_NS)])                
                poly_sum = unary_union([poly_sum, poly_new])

    # calculating the total shaded area
    area = poly_sum.area

    # limit settings for x and y directions in plot
    x_min = min(x_PV_shadow_NW, x_PV_shadow_SW, x_PV_shadow_NE, x_PV_shadow_SE) - 20
    x_max = max(x_PV_shadow_NW, x_PV_shadow_SW, x_PV_shadow_NE, x_PV_shadow_SE) + variables.number_of_panels_EW * variables.distance_EW + 10

    y_min = min(y_PV_shadow_SW, y_PV_shadow_SE, y_PV_shadow_NE, y_PV_shadow_NW) - 20
    y_max = max(y_PV_shadow_SW, y_PV_shadow_SE, y_PV_shadow_NE, y_PV_shadow_NW) + variables.number_of_panels_NS * variables.distance_NS + 10

    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])

    ax.set_aspect('equal', adjustable='box')

    # add area of shaddow into plot
    ax.text(x_PV_shadow_NW , (min(y_PV_shadow_SW, y_PV_shadow_SE)) - 10, 'Shade area ground (in m²) = ' + str(round(area, 3)), color='grey')
