import shade_grid
from shapely.geometry import Polygon as shapely_Polygon
import random

def test_init():
    # check if the correct number of points is generated
    field_width, field_length = 10, 10
    grid = shade_grid.shade_grid(field_width, field_length)
    number_of_points = (field_width + 20 + 1) * (field_length + 20 + 1)
    assert len(grid.grid_dict) == number_of_points and grid.timestep_count == 0

def test_update():
    all_pass = True
    field_width, field_length = 10, 10
    polygon = shapely_Polygon([(-11, -11), (-11 + (field_width + 22), -11), (-11 + (field_width + 22), -11 + (field_length/2 + 11.5)), (-11, -11 + (field_length/2 + 11.5))])
    
    # generate field
    grid = shade_grid.shade_grid(field_width, field_length)

    # update field with polygon
    grid.update(polygon)

    # count points in polygon
    count = 0
    for point in grid.grid_dict:
        count += grid.grid_dict[point]

    if not (field_width + 20 + 1) * (field_length/2 + 10 + 1) == count:
        print("First update returns incorrect result.")
        all_pass = False

    grid.update(polygon)
    count = 0
    for point in grid.grid_dict:
        count += grid.grid_dict[point]
    if not (field_width + 20 + 1) * (field_length/2 + 10 + 1) * 2 == count:
        print("Second update returns incorrect result.")
        all_pass = False

    assert all_pass

def test_reset():
    field_width, field_length = 10, 10
    polygon = shapely_Polygon([(-11, -11), (-11 + (field_width + 22), -11), (-11 + (field_width + 22), -11 + (field_length/2 + 11.5)), (-11, -11 + (field_length/2 + 11.5))])
    
    # generate field
    grid = shade_grid.shade_grid(field_width, field_length)

    # update field with polygon
    grid.update(polygon)

    grid.reset()

    # count points in polygon
    count = 0
    for point in grid.grid_dict:
        count += grid.grid_dict[point]

    assert count == 0 and grid.timestep_count == 0

def test_evaluate():
    field_width, field_length = 10, 10
    polygon = shapely_Polygon([(-11, -11), (-11 + (field_width + 22), -11), (-11 + (field_width + 22), -11 + (field_length/2 + 11.5)), (-11, -11 + (field_length/2 + 11.5))])
    
    # generate field
    grid = shade_grid.shade_grid(field_width, field_length)

    # update field with polygon
    grid.update(polygon)

    percentage_steps, percentage_counts_dict = grid.evaluate(2)
    print(percentage_counts_dict)

    theoretical_shaded_percent = ((field_width + 20 + 1) * (field_length/2 + 10 + 1)) / ((field_width + 20 + 1) * (field_length + 20 + 1))

    assert percentage_steps == 0.5 and percentage_counts_dict[0.5] == 1 - theoretical_shaded_percent and percentage_counts_dict[1] == theoretical_shaded_percent

def test_evaluate_percentage_validity():
    field_width, field_length = 10, 10
    
    # generate field
    grid = shade_grid.shade_grid(field_width, field_length)

    # update grid with random polygons
    for i in range(0,10):
        polygon = shapely_Polygon([(-11, -11), (-11 + (random.uniform(0,1) * field_width + 22), -11), (-11 + (random.uniform(0,1) * field_width + 22), -11 + (random.uniform(0,1) * field_length/2 + 22)), (-11, -11 + (random.uniform(0,1) * field_length/2 + 22))])
        grid.update(polygon)

    # evaluate grid
    percentage_steps, percentage_counts_dict = grid.evaluate(5)

    # calculate sum of percentages in bins
    percentage_sum = 0
    for bin in percentage_counts_dict:
        percentage_sum += percentage_counts_dict[bin]

    assert percentage_sum > 1 - 1e-5 and percentage_sum < 1 + 1e-5 and percentage_steps == 0.2
