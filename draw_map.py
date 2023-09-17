import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


def draw_map(robot_map, s, obstacles_coords=None):
    """
    :param list[list[float]] obstacles_coords:
    :param Map robot_map:
    :param float s: cell size
    :return: None
    """
    plt.close()

    side_length = robot_map.n

    fig, ax = plt.subplots()

    square = plt.Rectangle((0, 0), side_length, side_length, fill=False, color='black')
    ax.add_patch(square)

    for obstacle in robot_map.obstacles:
        x0, y0, x1, y1 = obstacle.scale(1)
        rect = Rectangle((x0, y0), x1 - x0, y1 - y0, fill=True, color='blue', zorder=9)
        ax.add_patch(rect)

    if robot_map.robot_positioned():
        robot_x = robot_map.robot_x + 0.5
        robot_y = robot_map.robot_y + 0.5
        if robot_map.n < 100:
            robot = Circle((robot_x, robot_y), 1 / 3, linewidth=1, edgecolor='red', facecolor='red', zorder=10)
            ax.add_patch(robot)
        else:
            plt.scatter(robot_x, robot_y, color='red', marker='o')

        if obstacles_coords is not None:
            for crd in obstacles_coords.values():
                ax.plot([robot_x, crd[0]], [robot_y, crd[1]], 'k--', alpha=0.7)
                plt.scatter(crd[0], crd[1], color='green', marker='o')

    if robot_map.n < 100:
        for i in range(1, robot_map.n):
            ax.axhline(i, color='grey', linewidth=0.3, alpha=0.5)
            ax.axvline(i, color='grey', linewidth=0.3, alpha=0.5)

    ax.set_aspect('equal')
    ax.set_xlim(0, side_length)
    ax.set_ylim(side_length, 0)
    ax.xaxis.tick_top()
    ax.set_xlabel(f"X (cell index: 1 cell = {s} units)")
    ax.set_ylabel(f"Y (cell index)")

    plt.show()
    try:
        plt.savefig("/app/output/map.png")
    except Exception:
        print("Picture isn't saved")
