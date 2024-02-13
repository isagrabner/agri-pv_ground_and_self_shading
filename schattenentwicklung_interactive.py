import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.widgets import Slider
from shapely.geometry import Polygon as shapely_Polygon
from shapely.ops import unary_union

# Program to display the area shaded by a dynamic PV system and calculate the shaded area, includes an interactive graph where the angle of the incoming sunbeams can be changed (angle in N/S direction -> alpha, angle in E/W direction -> beta).

def schatten(alpha, beta):
    # input parameters
    h = 2                                   # height (of posts) of the PV panel (in m)
    b = 4                                   # width of the PV panel (in m)
    l = 10                                  # length of the PV panel (in m)
    alpha_rad = (alpha / 180)*math.pi       # angle between sunbeam and ground/ angle of the PV Panel (in east/west direction; optimal Position) (in rad)
    beta_rad = (beta / 180)*math.pi         # angle between sunbeam and ground/ angle of the PV Panel (in north/south direction) (in rad)

    nmb_ns = 5                              # number of panels in north/south direction
    nmb_ew = 10                             # number of panels in east/west direction
    distance_ns = 15                        # distance between the panels in north/south direction (incl. lenght of panel)
    distance_ew = 6                         # distance between the panels in east/west direction (incl. width of panel)

    # shaddow position (first panel with southern post at (0,0))
    K_east = - math.tan(math.pi/2 - alpha_rad) * h + (b / (2 * math.sin(alpha_rad)))    # position of the east corner of the shaddow (x-val)
    K_west = - math.tan(math.pi/2 - alpha_rad) * h - (b / (2 * math.sin(alpha_rad)))    # position of the west corner of the shaddow (x-val)

    P_south_east = (h - math.cos(alpha_rad) * b/2) / math.tan(beta_rad)        # position of the south east point of the shaddow (y-val)
    P_south_west = (h + math.cos(alpha_rad) * b/2) / math.tan(beta_rad)        # position of the south west point of the shaddow (y-val)

    P_north_east = (h - math.cos(alpha_rad) * b/2) / math.tan(beta_rad) + l    # position of the north east point of the shaddow (y-val)
    P_north_west = (h + math.cos(alpha_rad) * b/2) / math.tan(beta_rad) + l    # position of the north west point of the shaddow (y-val)

    poly_sum = shapely_Polygon([(K_west, P_south_west), (K_east, P_south_east), (K_east, P_north_east), (K_west, P_north_west)])

    # plotting all individual shaddows
    for i in range(0, nmb_ns):
        for j in range(0, nmb_ew):
            y = np.array([[K_west + j*distance_ew, P_south_west + i*distance_ns], [K_east + j*distance_ew, P_south_east + i*distance_ns], [K_east + j*distance_ew, P_north_east + i*distance_ns], [K_west + j*distance_ew, P_north_west + i*distance_ns]])
            p = Polygon(y, facecolor = 'k')
            ax.add_patch(p)

            if(i != 0 or j != 0):
                poly_new = shapely_Polygon([(K_west + j*distance_ew, P_south_west + i*distance_ns), (K_east + j*distance_ew, P_south_east + i*distance_ns), (K_east + j*distance_ew, P_north_east + i*distance_ns), (K_west + j*distance_ew, P_north_west + i*distance_ns)])                
                poly_sum = unary_union([poly_sum, poly_new])

    area = poly_sum.area

    # limit settings for x and y directions in graph
    ax.set_xlim([K_west - 20, K_east + nmb_ew*distance_ew + 20])
    ax.set_ylim([(P_south_east if P_south_east < P_north_west else P_south_west) - 20, (P_south_east if P_south_east > P_north_west else P_south_west) + nmb_ns*distance_ns +20])

    ax.set_aspect('equal', adjustable='box')

    # add area of shaddow into graph
    ax.text(K_west , (P_south_east if P_south_east < P_north_west else P_south_west)-10, 'Shade area ground (in m²) = ' + str(round(area, 3)), color='grey')

def update(val):
    ax.clear()
    schatten(alpha_slider.val, beta_slider.val)

#main
fig,ax = plt.subplots()
fig.subplots_adjust(right=0.875, left=0.125, bottom=0.25)

# sliders for alpha and beta
axalpha = fig.add_axes([0.175, 0.1, 0.65, 0.03])
alpha_slider = Slider(
    ax=axalpha,
    label="$\\alpha$",
    valmin=1,
    valmax=179,
    valinit=90,
    orientation="horizontal"
)

axbeta = fig.add_axes([0.175, 0.05, 0.65, 0.03])
beta_slider = Slider(
    ax=axbeta,
    label="$\\beta$",
    valmin=1,
    valmax=90,
    valinit=90,
    orientation="horizontal"
)

alpha_slider.on_changed(update)
beta_slider.on_changed(update)

plt.show()