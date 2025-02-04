import solarposition
import shade_grid

import math
from shapely.geometry import Polygon as shapely_Polygon
from shapely.validation import make_valid

class system:
    def __init__(self, system_type:str, PV_base_height:float, PV_width:float, PV_length:float, distance_EW:float, distance_NS:float, number_of_panels_EW:int, number_of_panels_NS:int, PV_angle_NS:float = 0, PV_angle_EW:float = 0):
        ''' Instance Variables:
            system_type: This is the type of system which will be simulated, all string inputs are currently possible, but self-shading will only be calculated to the following system types: "optimal", "vertical" and "tracking". In other cases, the self-shaded area will be set to zero if the sun is over the horizon. If the given system type is "tracking", the panel's tilt in the east/west plane (explained later) will be calculated automatically.
            
            PV_base_height: The base height describes the height of the center of the PV panel above ground. Measurement to be given in meters.
            
            PV_width: Describes the width of the PV panel, which is the dimension of the PV panel in east/west direction here. Measurement to be given in meters.
            
            PV_length: Describes the length of the PV panel, which is the dimension of the PV panel in north/south direction here. Measurement to be given in meters.
            
            distance_EW: This is the distance between PV panels along the east/west axis. It describes the distance between the same point on two panels (e.g. center to center). Measurement to be given in meters.
            
            distance_NS: This is the distance between PV panels along the north/south axis. It describes the distance between the same point on two panels (e.g. center to center). Measurement to be given in meters.
            
            number_of_panels_EW: This variable describes the number of PV panels along the east/west axis.
            
            number_of_panels_NS: This variable describes the number of PV panels along the north/south axis.
            
            PV_angle_NS: This is the tilt angle of the PV panel in the north/south plane. Measurements to be given in degrees.
            
            PV_angle_EW: This is the tilt angle of the PV panel in the north/south plane. This parameter does not need to be specified for all systems (with a default value is 0°) because it is automatically calculated for the tracking system. Measurements to be given in degrees.
        '''
        self.system_type = system_type
        self.PV_base_height = PV_base_height
        self.PV_width = PV_width
        self.PV_length = PV_length
        self.distance_EW = distance_EW
        self.distance_NS = distance_NS
        self.number_of_panels_EW = number_of_panels_EW
        self.number_of_panels_NS = number_of_panels_NS
        self.PV_angle_NS = PV_angle_NS
        self.PV_angle_EW = PV_angle_EW
        
        if self.PV_angle_EW < -180 or self.PV_angle_EW > 180 or self.PV_angle_NS < -180 or self.PV_angle_NS > 180:
            print("Only panel angles between -180° and 180° are allowed.")
            exit()

        if self.distance_NS < self.PV_length or self.distance_EW < self.PV_width:
            print("Distance between panels must be larger or equal to the dimension of the panel in that direction.")
            exit()
        
    def get_name(self):
        '''Returns the system type parameter.
        
            Parameters: -
        
            Returns: self.system_type'''
            
        return self.system_type
        
    def tracking_repositioning(self, year, month, day, hour, minute, long, lat):
        '''Readjusts PV panel (tilt angle in E/W plane) depending on the position of the sun (which is calculated via date/time and location).
        
            Parameters: year, month, day, hour, minute, long, lat
        
            Returns: - '''
            
        angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(year, month, day, hour, minute, long, lat)
        angle_in_plane_EW_degrees = (angle_in_plane_EW / math.pi) * 180
        self.PV_angle_EW = 90 - angle_in_plane_EW_degrees

    def backtracking_repositioning(self, year, month, day, hour, minute, long, lat):
        '''Readjusts PV panel (tilt angle in E/W plane) depending on the position of the sun (which is calculated via date/time and location).
        
            Parameters: year, month, day, hour, minute, long, lat
        
            Returns: - '''
            
        angle_in_plane_EW, angle_in_plane_NS = solarposition.calculate_solarposition(year, month, day, hour, minute, long, lat)

        # regular tracking tilt
        angle_in_plane_EW_degrees = (angle_in_plane_EW / math.pi) * 180
        self.PV_angle_EW = 90 - angle_in_plane_EW_degrees

        # calculate shade width in self-shading to check if self-shading occurs
        angle_in_plane_EW_mod = angle_in_plane_EW if angle_in_plane_EW <= (math.pi/2) else math.pi - angle_in_plane_EW # angle above ground - making sun direction (from west or east) irrelevant
        shade_width = self.PV_width - math.sin(angle_in_plane_EW_mod) * self.distance_EW

        # adjust panel tilt in E/W plane so no self-shading occurs
        if shade_width > 0 and angle_in_plane_EW > 0:
            if angle_in_plane_EW < 90:
                alpha = math.radians(angle_in_plane_EW_degrees)
                beta = math.pi - math.asin((self.distance_EW * math.sin(alpha)) / self.PV_width)
                gamma = math.pi - alpha - beta
                self.PV_angle_EW = math.degrees(gamma)
            else:
                alpha = math.radians(180 - angle_in_plane_EW_degrees)
                beta = math.pi - math.asin((self.distance_EW * math.sin(alpha)) / self.PV_width )
                gamma = - (math.pi - alpha - beta)
                self.PV_angle_EW = - math.degrees(gamma)
        
    def calculate_self_shade(self, angle_in_plane_EW, angle_in_plane_NS, PV_angle_EW_rad, PV_angle_NS_rad, azimuth_rad, elevation_rad):
        '''Calculates the total shaded area cast by PV panels onto other PV panels. (Currently only for tracking, optimal and vertical systems, since overhead systems are horizonal (hence no self-shading) at the moment.)
        
            Parameters: 
            - angle_in_plane_EW: angle between ground and an incoming sun beam, projected on the east/west plane
            - angle_in_plane_NS: angle between ground and an incoming sun beam, projected on the north/south plane
            - PV_angle_EW_rad: tilt angle of the PV panel in the east/west plane in radians
            - PV_angle_NS_rad: tilt angle of the PV panel in the north/south plane in radians
            - azimuth_rad: azimuth in radians
            - elevation_rad: elevation in radians
        
            Returns: 
            - shade_total_area: total shaded area on the panels
        '''

        # for tracking/vertical systems
        if self.system_type == "tracking" or self.system_type == "vertical":

            # width of shade on neighbouring panel
            
            # angle above ground - making sun direction (from west or east) irrelevant
            angle_in_plane_EW_mod = angle_in_plane_EW if angle_in_plane_EW <= (math.pi/2) else math.pi - angle_in_plane_EW 
            
            if self.system_type == "tracking":
                shade_width = self.PV_width - math.sin(angle_in_plane_EW_mod) * self.distance_EW
            else:
                shade_width = self.PV_width - math.tan(angle_in_plane_EW_mod) * self.distance_EW

            if shade_width > 0:
                # for later calculation of offset of shade in N/S direction
                # putting sun location in the N/E quadrant to simplify/unify later calculations
                if azimuth_rad <= math.pi/2:
                    angle_off_center = azimuth_rad
                elif math.pi/2 < azimuth_rad  and azimuth_rad <= math.pi:
                    angle_off_center = math.pi - azimuth_rad
                elif math.pi < azimuth_rad and azimuth_rad <= (3/2)*math.pi:
                    angle_off_center = azimuth_rad - math.pi
                elif (3/2)*math.pi < azimuth_rad:
                    angle_off_center = 2*math.pi - azimuth_rad
                    
                # calculate the distance between the top edge of the eluminated panel and the top edge of the panel behind it (from a bird's eye view)
                dist_panel_shade_edge = self.distance_EW - (self.PV_width - shade_width) * math.cos(self.PV_angle_EW)
                
                # calculate shade offset in N/S direction
                shade_offset = math.tan(math.pi/2 - angle_off_center) * dist_panel_shade_edge

                # length (N/S direction) of shade on neighbouring collumn of panels (includes spaces between panels)
                shaded_panel_length = (self.number_of_panels_NS - 1) * self.distance_NS + self.PV_length - shade_offset

                if shaded_panel_length > 0:
                    # calculating number of fully shaded panels so spaces between panels can be excluded (here "fully shaded" means not affected by shade offset in N/S direction)
                    if shaded_panel_length < self.PV_length:
                        nmb_fully_shaded_panels = 0
                    elif shaded_panel_length >= self.PV_length and shaded_panel_length <= self.distance_NS:
                        nmb_fully_shaded_panels = 1 * (self.number_of_panels_EW - 1)
                    else:
                        nmb_fully_shaded_panels = (int((shaded_panel_length - self.PV_length) / self.distance_NS) + 1) * (self.number_of_panels_EW - 1)
    
                    # shade on fully shaded panels
                    shade_area_regular = shade_width * self.PV_length * nmb_fully_shaded_panels
                    
                    # checking if the shade offset "ends" in an area between panels or on a panel, adjusting shade accordingly
                    if shade_offset % self.distance_NS > self.PV_length or nmb_fully_shaded_panels == self.number_of_panels_NS * (self.number_of_panels_EW - 1): # in this case the shade offset ends between panels
                        edge_panel_shade = 0
                    else:
                        # shade on partially shaded panels
                        edge_panel_shade = shade_width * (self.PV_length - (shade_offset % self.distance_NS)) * (self.number_of_panels_EW - 1)
    
                    #total shaded area 
                    shade_total_area = shade_area_regular + edge_panel_shade
    
                    if shade_total_area < 0:
                        shade_total_area = 0
                        
                else:
                    # return 0 if shade length is <= 0
                    return 0 
            else:
                # return 0 if shade width is <= 0
                return 0

        
        elif self.system_type == "standard":

            # return 0% self shading for sun directy overhead and larger angles to avoid unnecessary calculations
            if angle_in_plane_NS >= math.pi/2 and angle_in_plane_NS <= math.pi - math.radians(self.PV_angle_NS):
                return 0
            # return 100% self shading if the sun hits the back of the panels
            elif angle_in_plane_NS > math.pi - math.radians(self.PV_angle_NS):
                return self.number_of_panels_EW * self.number_of_panels_NS * self.PV_width * self.PV_length
                
            # angle between vertical line and sun beam
            alpha = angle_in_plane_NS

            # angle between sun beam and (shaded) panel
            beta = math.pi - (angle_in_plane_NS + abs(PV_angle_NS_rad))

            # angle between shaded panel and vertical line
            gamma = math.pi - alpha - beta

            # distance panel edge to panel edge
            b = self.distance_NS

            # for calculating shade length (N/S dir) (b = distance between top panel edge (first panel) to top panel edge (second panel), a = unshaded part of second panel, c = distance between top edge of first panel and top edge of shade on the second panel)
            a = (b / math.sin(beta)) * math.sin(alpha)
            c = (b / math.sin(beta)) * math.sin(gamma)

            # calculating shade length
            shade_length = self.PV_length - a

            if shade_length > 0:
                # for later calculation of offset of shade in N/S direction
                # putting sun location in the N/E quadrant to simplify/unify later calculations
                if azimuth_rad <= math.pi/2:
                    angle_off_center = azimuth_rad
                elif math.pi/2 < azimuth_rad  and azimuth_rad <= math.pi:
                    angle_off_center = math.pi - azimuth_rad
                elif math.pi < azimuth_rad and azimuth_rad <= (3/2)*math.pi:
                    angle_off_center = azimuth_rad - math.pi
                elif (3/2)*math.pi < azimuth_rad:
                    angle_off_center = 2*math.pi - azimuth_rad

                 # calculate the distance between the top edge of the eluminated panel and the top edge of the panel behind it (from a bird's eye view)
                dist_panel_shade_edge = self.distance_NS - (self.PV_length - shade_length) * math.cos(self.PV_angle_NS)
                
                # calculate shade offset in E/W direction
                shade_offset = math.tan(angle_off_center) * dist_panel_shade_edge

                # length (N/S direction) of shade on neighbouring rows of panels (includes spaces between panels)
                shaded_panel_width = (self.number_of_panels_EW - 1) * self.distance_EW + self.PV_width - shade_offset

               # calculating number of fully shaded panels so spaces between panels can be excluded (here "fully shaded" means not affected by shade offset in E/W direction)
                if shaded_panel_width < self.PV_width:
                    nmb_fully_shaded_panels = 0
                elif shaded_panel_width >= self.PV_width and shaded_panel_width <= self.distance_EW:
                    nmb_fully_shaded_panels = 1 * (self.number_of_panels_NS - 1)
                else:
                    nmb_fully_shaded_panels = (int((shaded_panel_width - self.PV_width) / self.distance_EW) + 1) * (self.number_of_panels_NS - 1)
                    
                # shade on fully shaded panels
                shade_area_regular = shade_length * self.PV_width * nmb_fully_shaded_panels
                
                # checking if the shade offset "ends" in an area between panels or on a panel, adjusting shade accordingly
                if shade_offset % self.distance_EW > self.PV_width or nmb_fully_shaded_panels == self.number_of_panels_EW * (self.number_of_panels_NS - 1): 
                    edge_panel_shade = 0
                else:
                    # shade on partially shaded panels
                    edge_panel_shade = shade_length * (self.PV_width - (shade_offset % self.distance_EW)) * (self.number_of_panels_NS - 1)

                #total shaded area 
                shade_total_area = shade_area_regular + edge_panel_shade

                if shade_total_area < 0:
                    shade_total_area = 0

            else:
                # return 0 if shade length <= 0
                return 0
        
        elif self.system_type == "overhead":

            # return 0% self shading for sun directy overhead and larger angles to avoid unnecessary calculations
            if angle_in_plane_EW >= math.pi/2 and angle_in_plane_EW <= math.pi - math.radians(self.PV_angle_EW):
                return 0
            # return 100% self shading if the sun hits the back of the panels
            elif angle_in_plane_EW > math.pi - math.radians(self.PV_angle_EW):
                return self.number_of_panels_EW * self.number_of_panels_NS * self.PV_width * self.PV_length

            # angle between horizontal line and sun beam
            alpha = angle_in_plane_EW

            # angle between sun beam and (shaded) panel
            beta = math.pi - (angle_in_plane_EW + abs(PV_angle_EW_rad))

            # angle between shaded panel and vertical line
            gamma = math.pi - alpha - beta

            # distance panel edge to panel edge
            b = self.distance_EW

            # for calculating shade length (N/S dir) (b = distance between top panel edge (first panel) to top panel edge (second panel), a = unshaded part of second panel, c = distance between top edge of first panel and top edge of shade on the second panel)
            a = (b / math.sin(beta)) * math.sin(alpha)
            c = (b / math.sin(beta)) * math.sin(gamma)

            # calculating shade length
            shade_length = self.PV_width - a

            if shade_length > 0:
                # for later calculation of offset of shade in N/S direction
                # putting sun location in the N/E quadrant to simplify/unify later calculations
                if azimuth_rad <= math.pi/2:
                    angle_off_center = azimuth_rad
                elif math.pi/2 < azimuth_rad  and azimuth_rad <= math.pi:
                    angle_off_center = math.pi - azimuth_rad
                elif math.pi < azimuth_rad and azimuth_rad <= (3/2)*math.pi:
                    angle_off_center = azimuth_rad - math.pi
                elif (3/2)*math.pi < azimuth_rad:
                    angle_off_center = 2*math.pi - azimuth_rad
                
                # calculate the distance between the top edge of the eluminated panel and the top edge of the panel behind it (from a bird's eye view)
                dist_panel_shade_edge = self.distance_EW - (self.PV_width - shade_length) * math.cos(self.PV_angle_EW)

                # calculate shade offset in E/W direction
                shade_offset = math.tan(math.pi/2 - angle_off_center) * dist_panel_shade_edge

                # width (E/W direction) of shade on neighbouring rows of panels (includes spaces between panels)
                shaded_panel_width = (self.number_of_panels_NS - 1) * self.distance_NS + self.PV_length - shade_offset

                # calculating number of fully shaded panels so spaces between panels can be excluded (here "fully shaded" means not affected by shade offset in E/W direction)
                if shaded_panel_width < self.PV_length:
                    nmb_fully_shaded_panels = 0
                elif shaded_panel_width >= self.PV_length and shaded_panel_width <= self.distance_NS:
                    nmb_fully_shaded_panels = 1 * (self.number_of_panels_EW - 1)
                else:
                    nmb_fully_shaded_panels = (int((shaded_panel_width - self.PV_length) / self.distance_NS) + 1) * (self.number_of_panels_EW - 1)
                    
                # shade on fully shaded panels
                shade_area_regular = shade_length * self.PV_length * nmb_fully_shaded_panels
                
                # checking if the shade offset "ends" in an area between panels or on a panel, adjusting shade accordingly
                if shade_offset % self.distance_NS > self.PV_length or nmb_fully_shaded_panels == self.number_of_panels_NS * (self.number_of_panels_EW - 1):
                    edge_panel_shade = 0
                else:
                    # shade on partially shaded panels
                    edge_panel_shade = shade_length * (self.PV_length - (shade_offset % self.distance_NS)) * (self.number_of_panels_EW - 1)

                #total shaded area 
                shade_total_area = shade_area_regular + edge_panel_shade

                if shade_total_area < 0:
                    shade_total_area = 0

            else:
                # return 0 if shade length <= 0
                return 0
        
        else: 
            shade_total_area = 0

        return shade_total_area
   
    
    def calculate_shade(self, angle_in_plane_EW, angle_in_plane_NS, field_width, field_length, azimuth_rad, grid: shade_grid.shade_grid = None):
        ''' Calculates the position and area of the shade created by PV panels.
        
            Parameters: 
            - angle_in_plane_EW: angle between ground and an incoming sun beam, projected on the east/west plane
            - angle_in_plane_NS: angle between ground and an incoming sun beam, projected on the north/south plane
            - field_width: witdth of the field without buffer
            - field_length: length of the field without buffer
            - azimuth_rad: azimuth in radians
            - grid: grid for percentage shaded calculations
            
            Returns:
            - intersection_percent: shaded area of the field in percent of the total field area
            - self_shade_percentage_of_total_panel_area: shaded area on the panels in percent of the total panel area
        '''
        
        PV_angle_EW_rad = (self.PV_angle_EW / 180)*math.pi       # angle of the PV Panel (in east/west direction) (in rad)
        PV_angle_NS_rad = (self.PV_angle_NS / 180)*math.pi       # angle of the PV Panel (in north/south direction) (in rad)

        # edge height differences
        height_diff_N = math.sin(PV_angle_NS_rad) * self.PV_length / 2
        height_diff_S = - math.sin(PV_angle_NS_rad) * self.PV_length / 2
        height_diff_E = - math.sin(PV_angle_EW_rad) * self.PV_width / 2
        height_diff_W = math.sin(PV_angle_EW_rad) * self.PV_width / 2

        # corner height differences
        PV_height_NE = self.PV_base_height + height_diff_N + height_diff_E
        PV_height_NW = self.PV_base_height + height_diff_N + height_diff_W
        PV_height_SE = self.PV_base_height + height_diff_S + height_diff_E
        PV_height_SW = self.PV_base_height + height_diff_S + height_diff_W

        # shadow position

        # x coordinates of shaded area (for one panel)
        if (self.system_type == "standard"):
            x_PV_shadow_NE = self.PV_width / 2 + abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_NE / math.tan(angle_in_plane_EW)
            x_PV_shadow_NW = self.PV_width / 2 - abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_NW / math.tan(angle_in_plane_EW)
            x_PV_shadow_SE = self.PV_width / 2 + abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_SE / math.tan(angle_in_plane_EW)
            x_PV_shadow_SW = self.PV_width / 2 - abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_SW / math.tan(angle_in_plane_EW)

        else:
            x_PV_shadow_NE = abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_NE / math.tan(angle_in_plane_EW)
            x_PV_shadow_NW = - abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_NW / math.tan(angle_in_plane_EW)
            x_PV_shadow_SE = abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_SE / math.tan(angle_in_plane_EW)
            x_PV_shadow_SW = - abs(math.cos(PV_angle_EW_rad)) * (self.PV_width / 2) - PV_height_SW / math.tan(angle_in_plane_EW)

        # y coordinates of shaded area (for one panel)
        y_PV_shadow_NE = PV_height_NE / math.tan(angle_in_plane_NS) + abs(math.cos(PV_angle_NS_rad)) * self.PV_length
        y_PV_shadow_NW = PV_height_NW / math.tan(angle_in_plane_NS) + abs(math.cos(PV_angle_NS_rad)) * self.PV_length
        y_PV_shadow_SE = PV_height_SE / math.tan(angle_in_plane_NS)
        y_PV_shadow_SW = PV_height_SW / math.tan(angle_in_plane_NS)

        # entire field - individual shadows will be cut out of poly_field, poly_field_complete is later used fo calculate the shaded area
        poly_field = make_valid(shapely_Polygon([(-10, -10), (-10 + (field_width + 20), -10), (-10 + (field_width + 20), -10 + (field_length + 20)), (-10, -10 + (field_length + 20))]))
        poly_field_complete = make_valid(shapely_Polygon([(-10, -10), (-10 + (field_width + 20), -10), (-10 + (field_width + 20), -10 + (field_length + 20)), (-10, -10 + (field_length + 20))]))

        # calculating individual shaddows and cutting them out of field polygon
        for i in range(0, self.number_of_panels_NS):
            for j in range(0, self.number_of_panels_EW):
                # calculating individual shaddows
                poly_new = shapely_Polygon([(x_PV_shadow_SW + j * self.distance_EW, y_PV_shadow_SW + i * self.distance_NS), (x_PV_shadow_SE + j * self.distance_EW, y_PV_shadow_SE + i * self.distance_NS), (x_PV_shadow_NE + j * self.distance_EW, y_PV_shadow_NE + i * self.distance_NS), (x_PV_shadow_NW + j * self.distance_EW, y_PV_shadow_NW + i * self.distance_NS)])
                # cutting them out of field polygon
                poly_field = make_valid(poly_field.difference(poly_new))

        # update for percentage shaded grid
        if grid != None:
            grid.update(make_valid(poly_field_complete.difference(poly_field)))

        # calculating the shaded area (total and in percent)
        intersection_area = poly_field_complete.area - poly_field.area # inverting from unshaded area to shaded area
        intersection_percent = (intersection_area / poly_field_complete.area) * 100 # in %

        self_shade_total = self.calculate_self_shade(angle_in_plane_EW, angle_in_plane_NS, PV_angle_EW_rad, PV_angle_NS_rad, azimuth_rad, elevation_rad)
        self_shade_percentage_of_total_panel_area = (self_shade_total/ (self.number_of_panels_EW * self.number_of_panels_NS * self.PV_width * self.PV_length))*100 # in %

        return intersection_percent, self_shade_percentage_of_total_panel_area
