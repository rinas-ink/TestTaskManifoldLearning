import bisect
from abc import ABC, abstractmethod

"""
Coordinates in this file reflect map's cell number (starting 0) and don't depend on cell size s.
Top-left corner cell of map has coordinate (0, 0) and bottom right cell has (n-1, n-1).
"""


class Rectangle:
    def __init__(self, x0, y0, x1, y1):
        """
        Function receives 2 non-negative integer coordinates of
        2 diagonal corners of a rectangle.
        """
        if x0 < 0 or y0 < 0 or x1 < 0 or y1 < 0:
            raise ValueError("Corners of rectangle must have non-negative coordinates.")
        if x0 == x1 or y0 == y1:
            raise ValueError("Rectangle must have square > 0.")
        self.x = tuple(sorted([x0, x1]))
        self.y = tuple(sorted([y0, y1]))

    def intersects_x_col(self, x):
        return self.x[0] <= x < self.x[1]

    def intersects_y_row(self, y):
        return self.y[0] <= y < self.y[1]

    def is_cell_in_rectangle(self, x, y):
        return self.intersects_x_col(x) and self.intersects_y_row(y)

    def inside_map(self, map_size):
        return self.x[0] >= 0 and self.x[1] <= map_size and \
            self.y[0] >= 0 and self.y[1] <= map_size

    def square(self):
        return (self.x[1] - self.x[0]) * (self.y[1] - self.y[0])

    def scale(self, mult):
        """
        Scale all coordinates by mult and return them as array [x0, y0, x1, y1]
        :param float mult:
        :return: list[float]
        """
        return [self.x[0] * mult, self.y[0] * mult, self.x[1] * mult, self.y[1] * mult]


class Map(ABC):
    """
    Class that's responsible for keeping information about the map, updating it
    and responding on user queries.

    Coordinates in all function's parameters reflect map's cell number (starting 0) and don't depend on cell size s.
    Top-left corner cell of map has coordinate (0, 0) and bottom right cell has (n-1, n-1).
    """

    def __init__(self, n, obstacles):
        """
        Creates empty map with specified n and s.
        :param int n: Grid size
        :param list[Rectangle]: Obstacles, assumed that all are inside the map.
        """
        self.n = n
        self.obstacles = obstacles
        self.robot_x = -1
        self.robot_y = -1

    def robot_positioned(self):
        return self.robot_x >= 0 and self.robot_y >= 0

    @abstractmethod
    def cell_obstructed(self, x, y):
        """
        Tells if there is any obstacle (not robot) in cell (x, y)
        :param int x:
        :param int y:
        :return: bool
        """
        pass

    def position_robot(self, x, y):
        """
        Positions or repositions(if robot already was there) robot on the (x, y) cell of the map.
        :param int x:
        :param int y:
        :return: None
        """
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            raise ValueError("Robot is out of the map.")
        if self.cell_obstructed(x, y):
            raise ValueError("Can't put robot in the obstructed cell.")
        self.robot_x = x
        self.robot_y = y

    @abstractmethod
    def get_obstacles_positions(self):
        if not self.robot_positioned():
            raise ValueError("Robot isn't positioned. Position robot first.")


class Map1(Map):
    """
    In this realisation:
    Getting information about obstacles near robot works in O(obstacle_amount).
    Initializing of map works in O(obstacle_amount) < O(N^2).
    Map consumes O(obstacle_amount) < O(N^2) memory.
    """

    def cell_obstructed(self, x, y):
        for obstacle in self.obstacles:
            if obstacle.is_cell_in_rectangle(x, y):
                return True
        return False

    def get_obstacles_positions(self):
        super().get_obstacles_positions()
        grid_crds = {"up": [self.robot_x, -1],
                     "left": [-1, self.robot_y],
                     "down": [self.robot_x, self.n],
                     "right": [self.n, self.robot_y]}
        for obstacle in self.obstacles:
            if obstacle.intersects_x_col(self.robot_x):
                if obstacle.y[1] < self.robot_y:
                    grid_crds["up"][1] = max(grid_crds["up"][1], obstacle.y[1] - 1)
                if obstacle.y[0] > self.robot_y:
                    grid_crds["down"][1] = min(grid_crds["down"][1], obstacle.y[0])
            elif obstacle.intersects_y_row(self.robot_y):
                if obstacle.x[1] < self.robot_x:
                    grid_crds["left"][0] = max(obstacle.x[1] - 1, grid_crds["left"][0])
                if obstacle.x[0] > self.robot_x:
                    grid_crds["right"][0] = min(obstacle.x[0], grid_crds["right"][0])
        return grid_crds


class Map2(Map):
    """
    In this realisation:
    Getting information about obstacles near robot works in O(log N).
    Initializing of map works in O(sum_of_obstacles_squares) < O(N^2).
    Map consumes O(sum_of_obstacles_squares) < O(N^2) memory.
    Might be useful in online version, when
    sum_obst_squares + amount_of_updates * log2(n) < amount_of_updates * obstacles_amount
    """

    def __init__(self, n, obstacles):
        super().__init__(n, obstacles)
        self.obstructed_y_to_x = dict()
        self.obstructed_x_to_y = dict()
        for obstacle in obstacles:
            for i in range(obstacle.y[0], obstacle.y[1]):
                for j in range(obstacle.x[0], obstacle.x[1]):
                    if i not in self.obstructed_y_to_x:
                        self.obstructed_y_to_x[i] = []
                    self.obstructed_y_to_x[i].append(j)
                    if j not in self.obstructed_x_to_y:
                        self.obstructed_x_to_y[j] = []
                    self.obstructed_x_to_y[j].append(i)
        for key, value in self.obstructed_x_to_y.items():
            self.obstructed_x_to_y[key] = sorted(set(value))
        for key, value in self.obstructed_y_to_x.items():
            self.obstructed_y_to_x[key] = sorted(set(value))

    def cell_obstructed(self, x, y):
        if x in self.obstructed_x_to_y:
            ind = bisect.bisect_left(self.obstructed_x_to_y[x], y)
            if ind < len(self.obstructed_x_to_y[x]) and self.obstructed_x_to_y[x][ind] == y:
                return True
        return False

    def get_obstacles_positions(self):
        super().get_obstacles_positions()
        grid_crds = {"up": [self.robot_x, -1],
                     "left": [-1, self.robot_y],
                     "down": [self.robot_x, self.n],
                     "right": [self.n, self.robot_y]}
        if self.robot_x in self.obstructed_x_to_y:
            current_x_col = self.obstructed_x_to_y[self.robot_x]
            y_index = bisect.bisect_left(current_x_col, self.robot_y)
            if y_index > 0:
                up_y = current_x_col[y_index - 1]
                grid_crds["up"][1] = up_y

            if y_index < len(current_x_col):
                down_y = current_x_col[y_index]
                grid_crds["down"][1] = down_y

        if self.robot_y in self.obstructed_y_to_x:
            current_y_row = self.obstructed_y_to_x[self.robot_y]
            x_index = bisect.bisect_left(current_y_row, self.robot_x)
            if x_index > 0:
                left_x = current_y_row[x_index - 1]
                grid_crds["left"][0] = left_x

            if x_index < len(current_y_row):
                right_x = current_y_row[x_index]
                grid_crds["right"][0] = right_x

        return grid_crds
