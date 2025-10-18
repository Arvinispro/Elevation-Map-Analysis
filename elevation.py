"""Assignment 2 functions."""

from copy import deepcopy


# Examples to use in doctests:
THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]

# Used to compare floats in doctests:
# If the difference between the expected return value and the actual return
# value is less than EPSILON, we will consider the test passed.
EPSILON = 0.005


# We provide a full docstring for this function as an example.
def compare_elevations_within_row(elevation_map: list[list[int]], map_row: int,
                                  level: int) -> list[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """
    count_l = 0
    count_e = 0
    count_g = 0
    for item in elevation_map[map_row]:
        if item < level:
            count_l += 1
        elif item == level:
            count_e += 1
        else:
            count_g += 1
    return [count_l, count_e, count_g]
# We provide a partial doctest in this function as an example of
# testing a function that modifies its input. Note the use of deepcopy
# to create a copy of the nested list to use in the function call. We
# do this to make sure that different doctests do not affect each
# other.


def update_elevation(elevation_map: list[list[int]], start: list[int],
                     stop: list[int], delta: int) -> None:
    """Modify each cell between start and stop in the given elevation_map by
    the value of delta
    >>> THREE_BY_THREE_COPY = deepcopy(THREE_BY_THREE)
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = deepcopy(FOUR_BY_FOUR)
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]
    """
    if start[0] == stop[0]:
        for i in range(start[1], stop[1] + 1):
            elevation_map[start[0]][i] = elevation_map[stop[0]][i] + delta
    if start[1] == stop[1]:
        for i in range(start[0], stop[0] + 1):
            elevation_map[i][start[1]] = elevation_map[i][stop[1]] + delta
# We provide a partial doctest in this function as an example of
# testing a function that returns a float. Note the use of abs and
# EPSILON to check if two floats are "close enough". We do this to
# deal with inevitable errors that arise in floating point arithmetic.


def get_average_elevation(elevation_map: list[list[int]]) -> float:
    """return the average elevation across all the cells in the elevation_map.
    >>> abs(get_average_elevation(UNIQUE_3X3) - 5.0) < EPSILON
    True
    >>> abs(get_average_elevation(FOUR_BY_FOUR) - 3.8125) < EPSILON
    True
    """
    total = 0
    for my_variable in elevation_map:
        for element in my_variable:
            total = total + element
    return total / pow(len(elevation_map), 2)


def find_peak(elevation_map: list[list[int]]) -> list[int]:
    """Return the cell which contains the highest elevation point in the
    elevation_map.
    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(FOUR_BY_FOUR)
    [2, 1]
    """
    start = [0, 0]
    for i in range(len(elevation_map)):
        for j in range(len(elevation_map)):
            if elevation_map[start[0]][start[1]] <= elevation_map[i][j]:
                start = [i, j]
    return start


def is_sink(elevation_map: list[list[int]], cell: list[int]) -> bool:
    """Return True if and only if the cell is a sink in the elevation_map.
    >>> is_sink(THREE_BY_THREE, [0, 0])
    True
    >>> is_sink(THREE_BY_THREE, [99, -89])
    False
    >>> is_sink(FOUR_BY_FOUR, [1, 1])
    False
    """
    map_e = elevation_map
    row = cell[0]
    column = cell[1]
    if not is_valid_cell(cell, len(map_e)):
        return False
    for i in range(row - 1, row + 2):
        for j in range(column - 1, column + 2):
            if is_valid_cell([i, j], len(map_e)):
                if map_e[row][column] > map_e[i][j]:
                    return False
    return True


def find_local_sink(elevation_map: list[list[int]],
                    cell: list[int]) -> list[int]:
    """Return the local sink for the given cell in the elevation_map.
    A local sink is the cell to which the water from this cell will flow.
    >>> find_local_sink(UNIQUE_3X3, [1, 1])
    [0, 0]
    >>> find_local_sink(UNIQUE_4X4, [0, 0])
    [0, 1]
    >>> find_local_sink(UNIQUE_3X3, [0, 0])
    [0, 0]
    >>> find_local_sink(UNIQUE_4X4, [2, 3])
    [2, 2]
    """
    result = cell
    adjacent_cells = get_adjacent_cells(cell, len(elevation_map))
    for cells in adjacent_cells:
        if is_valid_cell(cells, len(elevation_map)):
            if is_cell_lower(elevation_map, cells, result):
                result = cells
    return result


def can_hike_to(elevation_map: list[list[int]], start: list[int],
                dest: list[int], supplies: int) -> bool:
    """Return True if and only if the hiker can travel from start to dest
    in the elevation_map without running out of supplies
    >>> e_map = [[1, 6, 5, 6],[2, 5, 6, 8],[7, 2, 8, 1],[4, 4, 7, 3]]
    >>> can_hike_to(e_map, [3, 3], [2, 3], 10)
    True
    >>> can_hike_to(e_map, [3, 3], [2, 2], 8)
    False
    >>> can_hike_to(e_map, [3, 3], [3, 0], 7)
    True
    >>> can_hike_to(e_map, [3, 3], [3, 0], 6)
    False
    >>> can_hike_to(e_map, [3, 3], [0, 0], 18)
    True
    >>> can_hike_to(e_map, [3, 3], [0, 0], 17)
    False
    """
    map_e = elevation_map
    s_t = start
    while start != dest:
        north_compare = map_e[s_t[0] - 1][s_t[1]] - map_e[s_t[0]][s_t[1]]
        west_compare = map_e[s_t[0]][s_t[1] - 1] - map_e[s_t[0]][s_t[1]]
        if s_t[0] > dest[0] and s_t[1] > dest[1]:
            if abs(north_compare) <= abs(west_compare):
                supplies = supplies - abs(north_compare)
                start[0] = start[0] - 1
            else:
                supplies = supplies - abs(west_compare)
                start[1] = start[1] - 1
        elif start[0] == dest[0]:
            supplies = supplies - abs(west_compare)
            start[1] = start[1] - 1
        elif start[1] == dest[1]:
            supplies = supplies - abs(north_compare)
            start[0] = start[0] - 1
    return supplies >= 0


def get_lower_resolution(elevation_map: list[list[int]]) -> list[list[int]]:
    """Return a new elevation map, which is constructed from the values of
    the elevation_map by taking the average of the four original points.
    >>> map = [[1, 6, 5, 6],[2, 5, 6, 8],[7, 2, 8, 1],[4, 4, 7, 3]]
    >>> get_lower_resolution(map)
    [[3, 6], [4, 4]]
    >>> map1 = [[7, 9, 1],[4, 2, 1],[3, 2, 3]]
    >>> get_lower_resolution(map1)
    [[5, 1], [2, 3]]
    """
    map_e = elevation_map
    result = []
    dimension = len(elevation_map)
    for i in range(0, dimension, 2):
        row = []
        for j in range(0, dimension, 2):
            total = 0
            count = 0
            if is_valid_cell([i, j], dimension):
                count += 1
                total += elevation_map[i][j]
            if is_valid_cell([i, j + 1], dimension):
                count += 1
                total += elevation_map[i][j + 1]
            if is_valid_cell([i + 1, j], dimension):
                count += 1
                total += elevation_map[i + 1][j]
            if is_valid_cell([i + 1, j + 1], dimension):
                count += 1
                total += map_e[i + 1][j + 1]
            row.append(total // count)
        result.append(row)
    return result
# These functions are not required in the assignment. However, we believe it is
# a great idea to define these functions and use them as helpers in the
# required functions.


def is_valid_cell(cell: list[int], dimension: int) -> bool:
    """Return True if and only if cell is a valid cell in an elevation map
    of dimensions dimension x dimension.

    Precondition: cell is a list of length 2.

    >>> is_valid_cell([1, 1], 2)
    True
    >>> is_valid_cell([0, 2], 2)
    False
    >>> is_valid_cell([-3, 2], 3)
    False
    """
    for item in cell:
        if item >= dimension or item < 0:
            return False
    return True


def is_cell_lower(elevation_map: list[list[int]], cell_1: list[int],
                  cell_2: list[int]) -> bool:
    """Return True iff cell_1 has a lower elevation than cell_2.

    Precondition: elevation_map is a valid elevation map
                  cell_1 and cell_2 are valid cells in elevation_map

    >>> map = [[0, 1], [2, 3]]
    >>> is_cell_lower(map, [0, 0], [1, 1])
    True
    >>> is_cell_lower(map, [1, 1], [0, 0])
    False

    """
    c_1 = cell_1
    c_2 = cell_2
    return elevation_map[c_1[0]][c_1[1]] < elevation_map[c_2[0]][c_2[1]]


def get_adjacent_cells(cell: list[int], dimension: int) -> list[list[int]]:
    """Return a list of cells adjacent to cell in an elevation map with
    dimensions dimension x dimension.

    Precondition: cell is a valid cell for an elevation map with
                  dimensions dimension x dimension.

    >>> adjacent_cells = get_adjacent_cells([1, 1], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
    >>> adjacent_cells = get_adjacent_cells([1, 0], 3)
    >>> adjacent_cells.sort()
    >>> adjacent_cells
    [[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]]

    """
    result = []
    for i in range(cell[0] - 1, cell[0] + 2):
        for j in range(cell[1] - 1, cell[1] + 2):
            if [i, j] != cell and is_valid_cell([i, j], dimension):
                result.append([i, j])
    return result


if __name__ == '__main__':
    import doctest
    doctest.testmod()
