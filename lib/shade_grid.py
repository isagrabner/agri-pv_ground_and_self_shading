from shapely.geometry import Point as shapely_Point
from shapely.geometry import Polygon as shapely_Polygon

class shade_grid:
    def __init__(self, field_width: float, field_length: float, spacing: float = 1):
        '''Generates a grid with given spacing for the test field (determined by field width and length). 

            Instance variables: 
            - grid_dict: saves the grid points and associates them with a counter which is set to 0 at initialization
            - timestep_count: counter for every time the grid is updated 
            '''
        if (field_width < 0):
            print("Field width cannot be smaller than 0.")
            exit()

        if (field_length < 0):
            print("Field length cannot be smaller than 0.")
            exit()

        # generate grid with 1m spacing for the testing field, set associated count to 0
        self.grid_dict = {}

        for i in range(-10, field_width + 10 + spacing, spacing):
            for j in range(-10, field_length + 10 + spacing, spacing):
                self.grid_dict[shapely_Point(i, j)] = 0

        # initiate timestep count
        self.timestep_count = 0

    def reset(self):
        '''Resets grid_dict so counts for all points are 0, resets timestep_count to 0.
            Parameters: - 
            Returns: -
            '''
        
        # reset all counts to 0
        for point in self.grid_dict:
            self.grid_dict[point] = 0

        # reset timestep count to 0
        self.timestep_count = 0
        

    def update(self, shade_polygon: shapely_Polygon):
        '''Updates grid_dict by checking if a given point is in the shaded area, and adding one to to associated count if it is. Increases timestep_count by 1.
            Parameters: shade_polygon
            Returns: - 
            '''
        
        # add to count if point is in shaded polygon
        for point in self.grid_dict:
            if shade_polygon.contains(point):
                self.grid_dict[point] += 1

        # increase timestep count
        self.timestep_count += 1

    def evaluate(self, interval_count):
        '''Calculated the percentage of points (in the grid_dict) in each percentage category. Percentage categories are determined from the intervall count.
            Parameters: interval_count
            Returns: percentage_steps, percentage_counts_dict
            '''

        # calculate percentage steps between intervalls
        percentage_steps = 1/interval_count

        # generate empty dictionary for later summation of matching points
        percentage_counts_dict = {}
        for i in range(1, interval_count + 1):
            percentage_counts_dict[percentage_steps * i] = 0

        # sort points into matching category depending on the percentage of time they are shaded
        for point in self.grid_dict:
            for percentage in percentage_counts_dict:
                # ternary statement is to include points that are shaded 0% of the time in lowest bin
                if (self.grid_dict[point]/self.timestep_count <= percentage and (self.grid_dict[point]/self.timestep_count > percentage - percentage_steps if percentage - percentage_steps != 0 else self.grid_dict[point]/self.timestep_count >= percentage - percentage_steps)):
                    percentage_counts_dict[percentage] += 1

        # divide category counts by total number of points to get percentage of points in a given category 
        for percentage in percentage_counts_dict:
            percentage_counts_dict[percentage] /= len(self.grid_dict)

        return percentage_steps, percentage_counts_dict