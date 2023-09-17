import unittest
import map as mp


class TestRectangle(unittest.TestCase):
    def test_rectangle(self):
        r1 = mp.Rectangle(0, 0, 1, 1)
        self.assertEqual(r1.intersects_x_col(0), True)
        self.assertEqual(r1.intersects_x_col(1), False)
        self.assertEqual(r1.intersects_y_row(0), True)
        self.assertEqual(r1.intersects_y_row(1), False)
        self.assertEqual(r1.inside_map(1), True)
        self.assertEqual(r1.inside_map(2), True)
        self.assertEqual(r1.is_cell_in_rectangle(0, 0), True)
        self.assertEqual(r1.is_cell_in_rectangle(-1, 0), False)
        self.assertEqual(r1.is_cell_in_rectangle(1, 0), False)
        self.assertEqual(r1.square(), 1)
        self.assertEqual(r1.scale(1.5), [0, 0, 1.5, 1.5])

        with self.assertRaises(ValueError):
            r2 = mp.Rectangle(-3, 0, 1, 2)

        with self.assertRaises(ValueError):
            r2 = mp.Rectangle(1, 2, 1, 2)

        with self.assertRaises(ValueError):
            r2 = mp.Rectangle(4, 4, 4, 4)

        r1 = mp.Rectangle(7, 5, 1, 2)
        self.assertEqual(r1.intersects_x_col(1), True)
        self.assertEqual(r1.intersects_x_col(6), True)
        self.assertEqual(r1.intersects_x_col(0), False)
        self.assertEqual(r1.intersects_x_col(7), False)
        self.assertEqual(r1.intersects_y_row(2), True)
        self.assertEqual(r1.intersects_y_row(4), True)
        self.assertEqual(r1.intersects_y_row(1), False)
        self.assertEqual(r1.intersects_y_row(5), False)
        self.assertEqual(r1.inside_map(2), False)
        self.assertEqual(r1.inside_map(6), False)
        self.assertEqual(r1.inside_map(7), True)
        self.assertEqual(r1.inside_map(9), True)
        self.assertEqual(r1.is_cell_in_rectangle(0, 0), False)
        self.assertEqual(r1.is_cell_in_rectangle(6, 1), False)
        self.assertEqual(r1.is_cell_in_rectangle(3, 2), True)
        self.assertEqual(r1.is_cell_in_rectangle(4, 4), True)
        self.assertEqual(r1.is_cell_in_rectangle(4, 5), False)
        self.assertEqual(r1.square(), 18)
        self.assertEqual(r1.scale(2), [2, 4, 14, 10])


class MapTest(unittest.TestCase):

    def test_map1_check_obstructed(self):
        self.check_obstructed(mp.Map1)

    def test_map2_check_obstructed(self):
        self.check_obstructed(mp.Map2)

    def test_map1_regular_situation(self):
        self.regular_situation(mp.Map1)

    def test_map2_regular_situation(self):
        self.regular_situation(mp.Map2)

    def check_obstructed(self, map_constructor):
        n = 5
        rectangles = [mp.Rectangle(0, 0, 5, 2),
                      mp.Rectangle(0, 5, 2, 0),
                      mp.Rectangle(5, 5, 4, 4)]
        m = map_constructor(n, rectangles)
        self.assertEqual(m.cell_obstructed(0, 0), True)
        self.assertEqual(m.cell_obstructed(0, 1), True)
        self.assertEqual(m.cell_obstructed(3, 1), True)
        self.assertEqual(m.cell_obstructed(4, 4), True)

        self.assertEqual(m.cell_obstructed(2, 2), False)
        self.assertEqual(m.cell_obstructed(2, 3), False)
        self.assertEqual(m.cell_obstructed(2, 4), False)
        self.assertEqual(m.cell_obstructed(3, 2), False)
        self.assertEqual(m.cell_obstructed(3, 3), False)
        self.assertEqual(m.cell_obstructed(3, 4), False)
        self.assertEqual(m.cell_obstructed(4, 3), False)

    def regular_situation(self, map_constructor):
        n = 5
        rectangles = [mp.Rectangle(0, 0, 5, 2),
                      mp.Rectangle(0, 5, 2, 0),
                      mp.Rectangle(5, 5, 4, 4)]
        m = map_constructor(n, rectangles)
        self.assertEqual(m.robot_positioned(), False)
        m.position_robot(3, 4)
        obstacle_pos = m.get_obstacles_positions()
        self.assertEqual(obstacle_pos, [[4, 1], [1, 3], [4, 4], [5, 3]])

        # with self.assertRaises(ValueError):
        #     m1.position_robot(1, 1)
        for i in range(2):
            obstacle_pos = m.get_obstacles_positions()
            self.assertEqual(obstacle_pos, [[4, 1], [1, 3], [4, 4], [5, 3]])

    def test_maps_errors(self):
        pass

    def create_map(self, n, rectangles):
        pass


if __name__ == '__main__':
    unittest.main()
