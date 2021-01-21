import math


class ObjectHandler:

    def __init__(self, display_width, display_height):
        self.numPoints = 64
        self.squareSize = 250.0
        self.halfDiagonal = 0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)
        self.angleRange = 45.0
        self.anglePrecision = 2.0
        self.phi = 0.5 * (-1.0 + math.sqrt(5.0))  # Golden Ratio
        self.display_height = display_height
        self.display_width = display_width

    def scale(self, points, factor):
        """Scales a set of points"""
        # ToDo: IMPORTANT - Implement real scaling !!!

        new_points = []
        for index in points:
            (x, y) = index
            new_points.append((x * factor, y * factor))

        return new_points

    def translate(self, points, old_point, current_point):
        """Translate a set of points"""
        (x_old, y_old) = old_point
        (x_current, y_current) = current_point
        offset_x = x_current - x_old
        offset_y = y_current - y_old

        new_points = []
        for index in points:
            (x, y) = index
            new_points.append((x + offset_x * self.display_width, y + offset_y * self.display_height))

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
