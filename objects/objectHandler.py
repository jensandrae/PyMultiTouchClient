import math


class ObjectHandler:

    def __init__(self):
        self.numPoints = 64
        self.squareSize = 250.0
        self.halfDiagonal = 0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)
        self.angleRange = 45.0
        self.anglePrecision = 2.0
        self.phi = 0.5 * (-1.0 + math.sqrt(5.0))  # Golden Ratio

    def scale(self, points, factor):
        """Scales a set of points"""
        # ToDo: IMPORTANT - Implement real scaling !!!

        new_points = []
        for index in points:
            (x, y) = index
            new_points.append((x * factor, y * factor))

        return new_points

    def translate(self, points, point_old, point_new):
        """Translate a set of points"""
        (x_old, y_old) = point_old
        (x_new, y_new) = point_new
        offset_x = x_new - x_old
        offset_y = y_new - y_old

        new_points = []
        for index in points:
            (x, y) = index
            new_points.append(x * offset_x, y * offset_y)

        return new_points

    def calculate_center(self, points):
        """Calculate the center of a set of points"""
        sum_x = 0
        sum_y = 0

        for index in points:
            (x, y) = index
            sum_x += x
            sum_y += y

        x = sum_x / len(points)
        y = sum_y / len(points)
        return x, y

    def path_distance(self, pts1, pts2):
        """Distance' between two paths."""
        d = 0.0
        for index in range(min(len(pts1), len(pts2))):  # assumes pts1.length == pts2.length
            d += self.distance(pts1[index], pts2[index])
        return d / len(pts1)

    def path_length(self, points):
        """Sum of distance between each point, or, length of the path represented by a set of points."""
        d = 0.0
        for index in range(1, len(points)):
            d += self.distance(points[index - 1], points[index])
        return d

    def distance(self, p1, p2):
        """Distance between two points."""
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return math.sqrt(dx * dx + dy * dy)
