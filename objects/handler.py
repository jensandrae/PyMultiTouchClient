from objects.point import Point
from objects.triangle import Triangle
from objects.square import Square
from objects.rectangle import Rectangle

import math
import operator


class Handler:

    def __init__(self):
        self.numPoints = 64
        self.squareSize = 250.0
        self.halfDiagonal = 0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)
        self.angleRange = 45.0
        self.anglePrecision = 2.0
        self.phi = 0.5 * (-1.0 + math.sqrt(5.0))  # Golden Ratio

    def resample(self, points, n):
        """Resample a set of points to a roughly equivalent, evenly-spaced set of points."""
        I = self.path_length(points) / (n - 1)  # interval length
        D = 0.0
        new_points = [points[0]]
        i = 1
        while i < len(points) - 1:
            d = self.distance(points[i - 1], points[i])
            if (D + d) >= I:
                qx = points[i - 1].x + ((I - D) / d) * (points[i].x - points[i - 1].x)
                qy = points[i - 1].y + ((I - D) / d) * (points[i].y - points[i - 1].y)
                q = Point(qx, qy)
                new_points.append(q)
                # Insert 'q' at position i in points s.t. 'q' will be the next i
                points.insert(i, q)
                D = 0.0
            else:
                D += d
            i += 1

        # Sometimes we fall a rounding-error short of adding the last point, so add it if so.
        if len(new_points) == n - 1:
            new_points.append(points[-1])
        return new_points

    def rotate_to_zero(self, points):
        """Rotate a set of points such that the angle between the first point and the centre point is 0."""
        c = self.centroid(points)
        theta = math.atan2(c.y - points[0].y, c.x - points[0].x)
        return self.rotate_by(points, -theta)

    def rotate_by(self, points, theta):
        """Rotate a set of points by a given angle."""
        c = self.centroid(points)
        cos = math.cos(theta)
        sin = math.sin(theta)

        new_points = []
        for point in points:
            qx = (point.x - c.x) * cos - (point.y - c.y) * sin + c.x
            qy = (point.x - c.x) * sin + (point.y - c.y) * cos + c.y
            new_points.append(Point(qx, qy))
        return new_points

    def scale_to_square(self, points, size):
        """Scale a scale of points to fit a given bounding box."""
        bounding = self.bounding_box(points)
        new_points = []
        for point in points:
            qx = point.x * (size / bounding.width)
            qy = point.y * (size / bounding.height)
            new_points.append(Point(qx, qy))
        return new_points

    def translate_to_origin(self, points):
        """Translate a set of points, placing the centre point at the origin."""
        c = self.centroid(points)
        new_points = []
        for point in points:
            qx = point.x - c.x
            qy = point.y - c.y
            new_points.append(Point(qx, qy))
        return new_points

    def translate_to_point(self, points, next_center):
        """Translate a set of points, placing the centre point at the origin."""
        new_points = []
        for point in points:  # ToDo: Check this function, of course does not working correct !
            qx = point.x - next_center.x
            qy = point.y - next_center.y
            new_points.append(Point(qx, qy))
        return new_points

    def distance_at_best_angle(self, points, T, a, b, threshold):
        """Search for the best match between a set of points and a template, using a set of tolerances. Returns a
        float representing this minimum distance. """
        x1 = self.phi * a + (1.0 - self.phi) * b
        f1 = self.distance_at_angle(points, T, x1)
        x2 = (1.0 - self.phi) * a + self.phi * b
        f2 = self.distance_at_angle(points, T, x2)

        while abs(b - a) > threshold:
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = self.phi * a + (1.0 - self.phi) * b
                f1 = self.distance_at_angle(points, T, x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = (1.0 - self.phi) * a + self.phi * b
                f2 = self.distance_at_angle(points, T, x2)
        return min(f1, f2)

    def distance_at_angle(self, points, T, theta):
        """Returns the distance by which a set of points differs from a template when rotated by theta."""
        new_points = self.rotate_by(points, theta)
        return self.path_distance(new_points, T.points)

    def centroid(self, points):
        """Returns the centre of a given set of points."""
        x = 0.0
        y = 0.0
        for point in points:
            x += point.x
            y += point.y
        x /= len(points)
        y /= len(points)
        return Point(x, y)

    def bounding_box(self, points):
        """Returns a Rectangle representing the bounding box that contains the given set of points."""
        minX = float("+Infinity")
        maxX = float("-Infinity")
        minY = float("+Infinity")
        maxY = float("-Infinity")

        for point in points:
            if point.x < minX:
                minX = point.x
            if point.x > maxX:
                maxX = point.x
            if point.y < minY:
                minY = point.y
            if point.y > maxY:
                maxY = point.y

        # ToDo -> Übergabeparameter anpassen
        return Rectangle((minX, minY), maxX - minX, maxY - minY)

    def path_distance(self, pts1, pts2):
        """'Distance' between two paths."""
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
