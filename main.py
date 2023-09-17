import map as mp
from math import log2
from draw_map import *


def convert_coords_to_rectangle(coordinates, map_size):
    rectangle = mp.Rectangle(*coordinates)
    if not rectangle.inside_map(map_size):
        raise ValueError("Rectangle must be completely inside the map.")
    return rectangle


def format_obstacles_positions(obst_crds):
    obst_crds["up"][0] += 0.5
    obst_crds["up"][1] += 1

    obst_crds["left"][0] += 1
    obst_crds["left"][1] += 0.5

    obst_crds["down"][0] += 0.5

    obst_crds["right"][1] += 0.5


if __name__ == '__main__':
    while True:
        try:
            n = int(input("Please, enter map size N. It should be integer positive number: "))
            s = float(input("Please, enter cell size S. May be floating: "))
            if n <= 0 or s <= 0:
                raise ValueError("N and S should be integer positive numbers.")
        except ValueError as e:
            print(e)
            continue
        print("\nPlease, enter obstacles' coordinates.\n"
              "Obstacle is Rectangle with non-empty square.\n"
              "Each rectangle should be inside the map, rectangles may intersect.\n"
              "Coordinates are counted from top left corner (0, 0) and increase to the right and bottom.\n"
              "Coordinates don't depend on cell size s, but only on grid lines.\n"
              "For example, coordinates of bottom right corner of a map are (n, n).\n"
              "For example, rectangle with coordinates `0 0 1 1` is just one cell at the top left corner.\n"
              "You need to enter coordinates of 2 diagonal corners (x0, y0) and (x1, y1) of each rectangle.\n"
              "Each rectangle should go on new line in format: `x0 y0 x1 y1`.\n"
              "When you are finished press Enter one more time.\n"
              )
        obstacles = []
        sum_obst_squares = 0  # to choose which algorithm to use
        while True:
            coords = input().split()
            if len(coords) == 0:
                break
            elif len(coords) == 4:
                try:
                    coords = [int(c) for c in coords]
                    obstacles.append(convert_coords_to_rectangle(coords, n))
                    sum_obst_squares += obstacles[-1].square()
                except ValueError as e:
                    print(e)
            else:
                print("You should enter either 4 coordinates of rectangles' corners or press enter to finish.")

        rp = 1  # Approximate number of positions that robot will pass
        try:
            rp = int(
                input("Please, enter approximate amount of positions that your robot to change or just press Enter: "))
        except ValueError:
            pass

        robot_map = mp.Map2(n, obstacles)
        if sum_obst_squares + rp * log2(n) < rp * len(obstacles):
            robot_map = mp.Map1(n, obstacles)

        while True:
            try:
                robot_x, robot_y = [int(i) for i in
                                    input("Please enter 2 robot coordinates x, y divided by space: ").split()]
                robot_map.position_robot(robot_x, robot_y)
            except ValueError as e:
                print(e)
                continue
            except IndexError:
                print("Robot must have only 2 coordinates x and y.")
                continue

            try:
                obstacles_coords = robot_map.get_obstacles_positions()
                format_obstacles_positions(obstacles_coords)
                print("Obstacles coordinates in grid coordinates (independent on cell size): ")
                for key, value in obstacles_coords.items():
                    print(f"({key}: {value[0]}, {value[1]})")

                print("Obstacles coordinates dependent on cell size: ")
                for key, value in obstacles_coords.items():
                    print(f"({key}: {value[0] * s}, {value[1] * s})")
                draw_map(robot_map, s, obstacles_coords)
            except ValueError as e:
                print(e)
