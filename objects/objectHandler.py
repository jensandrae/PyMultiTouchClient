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
        #  This can only be done by using "calculate_center()".
        #  Have to use scaling from or to the center of the object for each point.

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

    def rotate(self, points, angle):
        """ Rotate a set of points counterclockwise by a given angle around a calculated origin.
        Minimum are three different points. The angle should be given in radians. """

        origin = self.calculate_center(points)
        print("Calculated origin: ", origin)
        rotated_points = []

        for single_point in points:
            rotated_points.append(self.rotate_single_point(origin, single_point, angle))

        return rotated_points

    def rotate_single_point(self, point_origin, point_rotate, angle):
        """ Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians. """
        ox, oy = point_origin
        px, py = point_rotate

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy

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

        (x_old, y_old) = p1
        (x_current, y_current) = p2

        dx = x_current - x_old
        dy = y_current - y_old
        return math.sqrt(dx * dx + dy * dy)
