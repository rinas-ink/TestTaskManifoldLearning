from sortedcontainers import SortedSet
import bisect


class Rectangle:
    def __init__(self, x0, y0, x1, y1):
        """
        Function receives 2 non-negative integer coordinates of
        2 diagonal cells of a rectangle.
        """
        if x0 < 0 or y0 < 0 or x1 < 0 or y1 < 0:
            raise ValueError("Corners of rectangle must have non-negative coordinates")
        if x0 == x1 or y0 == y1:
            raise ValueError("Rectangle must have square > 0")
        self.x = tuple(sorted([x0, x1]))
        self.y = tuple(sorted([y0, y1]))


class Map1:
    """
    Class that's responsible for keeping information about the map, updating it
    and responding on user queries.

    Coordinates in all function's parameters reflect map's cell number (starting 0) and don't depend on cell size s.
    Top-left corner cell of map has coordinate (0, 0) and bottom right cell has (n-1, n-1).

    Adding obstacles and getting information about obstacles near robot works in O(log N).
    Class is better to use if log N << amount of obstacles
    """

    def __init__(self, n, s):
        """
        Creates empty map with specified n and s.
        :param int n: Grid size
        :param int s: Cell size
        """
        self.n = n
        self.s = s
        self.rectangle_cnt = 0
        self.robot_x = -1
        self.robot_y = -1
        self.obstacles = dict()
        """
        Hash map from rectangle id to its coordinates
        """
        self.obstructed_y_to_x = dict()
        self.obstructed_x_to_y = dict()

    def is_cell_obstructed(self, x, y):
        """
        Tells if there is any obstacle (not robot) in cell (x, y)
        :param int x:
        :param int y:
        :return: bool
        """
        return x in self.obstructed_y_to_x and y in self.obstructed_y_to_x[x]

    def add_obstacle(self, rectangle):
        """
        Adds given rectangle to the map
        :param rectangle:
        :return: None
        """
        if rectangle.x[1] >= self.n:
            raise ValueError("Obstacle is out of the map")
        for i in range(rectangle.y[0], rectangle.y[1]):  # TODO: copypaste
            for j in range(rectangle.x[0], rectangle.x[1]):
                if self.is_cell_obstructed(i, j):
                    raise ValueError("Obstacles shouldn't cover each other")

        self.obstacles[self.rectangle_cnt] = rectangle
        self.rectangle_cnt += 1
        for i in range(rectangle.y[0], rectangle.y[1]):  # TODO: copypaste
            for j in range(rectangle.x[0], rectangle.x[1]):
                if i not in self.obstructed_y_to_x:
                    self.obstructed_y_to_x[i] = SortedSet([j])
                else:
                    self.obstructed_y_to_x[i].add(j)
                if j not in self.obstructed_x_to_y:
                    self.obstructed_y_to_x[j] = SortedSet([i])
                else:
                    self.obstructed_y_to_x[j].add(i)

    def position_robot(self, x, y):
        """
        Positions or repositions(if robot already was there) robot on the (x, y) cell of the map.
        :param int x:
        :param int y:
        :return: None
        """
        if x < 0 or x >= self.n or y < 0 or y >= self.n:
            raise ValueError("Robot is out of the map")
        if self.is_cell_obstructed(x, y):
            raise ValueError("Can't put robot in the obstructed cell")
        self.robot_x = x
        self.robot_y = y

    def remove_obstacle(self, obstacle_id):
        if obstacle_id not in self.obstacles:
            raise ValueError("No such obstacle")
        rectangle = self.obstacles[obstacle_id]
        for i in range(rectangle.y[0], rectangle.y[1]):  # TODO: copypaste
            for j in range(rectangle.x[0], rectangle.x[1]):
                self.obstructed_y_to_x[i].remove(j)
                self.obstructed_x_to_y[j].remove(i)

    def get_obstacles_positions(self):
        if self.robot_x < 0 or self.robot_y < 0:
            raise ValueError("Robot isn't positioned. Position robot first")
        grid_crds = [(self.robot_x, -1),  # up = 0
                     (-1, self.robot_y),  # left = 90
                     (self.robot_x, self.n),  # down = 180
                     (self.n, self.robot_y)]  # right = 270
        if self.robot_x in self.obstructed_x_to_y:
            current_x_col = self.obstructed_y_to_x[self.robot_y]
            lower_bound_y_index = bisect.bisect_left(current_x_col, self.robot_x)
            up_y = current_x_col[lower_bound_y_index]
            if up_y < self.robot_x:
                grid_crds[0] = (self.robot_x, up_y)

            if lower_bound_y_index < len(current_x_col) - 1:
                upper_bound_y_index = lower_bound_y_index + 1
                down_y = current_x_col[upper_bound_y_index]
                grid_crds[2] = (self.robot_x, down_y)

        if self.robot_y in self.obstructed_y_to_x:
            current_y_row = self.obstructed_y_to_x[self.robot_y]
            lower_bound_x_index = bisect.bisect_left(current_y_row, self.robot_x)
            left_x = current_y_row[lower_bound_x_index]
            if left_x < self.robot_x:
                grid_crds[1] = (left_x, self.robot_y)

            if lower_bound_x_index < len(current_y_row) - 1:
                upper_bound_x_index = lower_bound_x_index + 1
                right_x = current_y_row[upper_bound_x_index]
                grid_crds[3] = (right_x, self.robot_y)

        return [(grid_crds[0][0] + 0.5, grid_crds[0][1] + 1),  # up
                (grid_crds[1][0] + 1, grid_crds[1][1] + 0.5),  # left
                (grid_crds[2][0] + 0.5, grid_crds[2][1]),  # down
                (grid_crds[3][0], grid_crds[3][1] + 0.5)  # right
                ]




