#
# Usage example:
#
# from dollar import Recognizer
#
# r = Recognizer()
# r.addTemplate('square', [(1, 10), (3, 8) ... ])
# r.addTemplate('circle', [(4, 7), (5, 13) ... ])
#
# (name, score) = r.recognize([(5, 6), (7, 12), ... ])
#

import math
import operator

# Contants. Tweak at your peril. :)

numPoints = 64
squareSize = 250.0
halfDiagonal = 0.5 * math.sqrt(250.0 * 250.0 + 250.0 * 250.0)
angleRange = 45.0
anglePrecision = 2.0
phi = 0.5 * (-1.0 + math.sqrt(5.0))  # Golden Ratio


class Recognizer:
    """The $1 gesture recognizer"""

    def __init__(self):
        self.templates = []
        self.distances = []
        self.scores = []

        self.all_names = []
        self.num_templates = dict()

    def recognize(self, points):
        """Determine which gesture template most closely matches the gesture represented by the input points.
        'points' is a list of tuples, eg: [(1, 10), (3, 8) ...]. Returns a tuple of the form (name, score) where name
        is the matching template, and score is a float [0..1] representing the match certainty. """

        points = [Point(point[0], point[1]) for point in points]
        points = _resample(points, numPoints)
        points = _rotate_to_zero(points)
        points = _scale_to_square(points, squareSize)
        points = _translate_to_origin(points)

        best_distance = float("infinity")
        best_template = None
        for i, template in enumerate(self.templates):
            distance = _distance_at_best_angle(points, template, -angleRange, +angleRange, anglePrecision)
            self.distances[i] = distance
            if distance < best_distance:
                best_distance = distance
                best_template = template

        score = 1.0 - (best_distance / halfDiagonal)
        self.scores = [1.0 - (d / halfDiagonal) for d in self.distances]

        return best_template.index, best_template.name, score

    def add_template(self, name, points):
        """Add a new template, and assign it a name. Multiple templates can be given the same name, for more accurate
        matching. Returns an integer representing the number of templates matching this name. """
        self.templates.append(Template(name, points, len(self.templates)))
        self.scores.append(0)
        self.distances.append(0)

        if not name in self.all_names:
            self.all_names.append(name)
            self.all_names.sort()
            self.num_templates[name] = 1
        else:
            self.num_templates[name] += 1

        self.templates.sort(key=operator.attrgetter('name'))

        # Return the number of templates with this name.
        return len([t for t in self.templates if t.name == name])

    def add_templates(self, data_dict):
        for one_type in data_dict.keys():
            if type(data_dict[one_type][0]) == list:
                for one_data in data_dict[one_type]:
                    self.add_template(one_type, one_data)
            else:
                self.add_template(one_type, data_dict[one_type])

    def delete_templates(self, name):
        """Remove all templates matching a given name. Returns an integer representing the new number of templates."""

        self.templates = [t for t in self.templates if t.name != name]
        return len(self.templates)

    def get_template_name(self, remove_duplicate=False):
        gesture_name_dict = dict()

        for i, one_template in enumerate(self.templates):
            if remove_duplicate and one_template.name in gesture_name_dict.values():
                continue
            gesture_name_dict[i] = one_template.name

        return gesture_name_dict

    def get_one_score_by_gesture(self):
        scores = []
        start_index = 0
        for one_key in self.num_templates.keys():
            end_index = start_index + self.num_templates[one_key]
            scores.append(max(self.scores[start_index:end_index]))
            start_index = end_index

        return self.all_names, scores


class Point:
    """Simple representation of a point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    """Simple representation of a rectangle."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Template:
    """A gesture template. Used internally by Recognizer."""

    def __init__(self, name, points, index=-999):
        """'name' is a label identifying this gesture, and 'points' is a list of tuple co-ordinates representing the
        gesture positions. Example: [(1, 10), (3, 8) ...] """
        self.name = name
        self.points = [Point(point[0], point[1]) for point in points]
        self.points = _resample(self.points, numPoints)
        self.points = _rotate_to_zero(self.points)
        self.points = _scale_to_square(self.points, squareSize)
        self.points = _translate_to_origin(self.points)

        self.index = index


def _resample(points, n):
    """Resample a set of points to a roughly equivalent, evenly-spaced set of points."""
    I = _path_length(points) / (n - 1)  # interval length
    D = 0.0
    new_points = [points[0]]
    i = 1
    while i < len(points) - 1:
        d = _distance(points[i - 1], points[i])
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


def _rotate_to_zero(points):
    """Rotate a set of points such that the angle between the first point and the centre point is 0."""
    c = _centroid(points)
    theta = math.atan2(c.y - points[0].y, c.x - points[0].x)
    return _rotate_by(points, -theta)


def _rotate_by(points, theta):
    """Rotate a set of points by a given angle."""
    c = _centroid(points)
    cos = math.cos(theta)
    sin = math.sin(theta)

    new_points = []
    for point in points:
        qx = (point.x - c.x) * cos - (point.y - c.y) * sin + c.x
        qy = (point.x - c.x) * sin + (point.y - c.y) * cos + c.y
        new_points.append(Point(qx, qy))
    return new_points


def _scale_to_square(points, size):
    """Scale a scale of points to fit a given bounding box."""
    B = _bounding_box(points)
    new_points = []
    for point in points:
        qx = point.x * (size / B.width)
        qy = point.y * (size / B.height)
        new_points.append(Point(qx, qy))
    return new_points


def _translate_to_origin(points):
    """Translate a set of points, placing the centre point at the origin."""
    c = _centroid(points)
    new_points = []
    for point in points:
        qx = point.x - c.x
        qy = point.y - c.y
        new_points.append(Point(qx, qy))
    return new_points


def _distance_at_best_angle(points, T, a, b, threshold):
    """Search for the best match between a set of points and a template, using a set of tolerances. Returns a float
    representing this minimum distance. """
    x1 = phi * a + (1.0 - phi) * b
    f1 = _distance_at_angle(points, T, x1)
    x2 = (1.0 - phi) * a + phi * b
    f2 = _distance_at_angle(points, T, x2)

    while abs(b - a) > threshold:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = phi * a + (1.0 - phi) * b
            f1 = _distance_at_angle(points, T, x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = (1.0 - phi) * a + phi * b
            f2 = _distance_at_angle(points, T, x2)
    return min(f1, f2)


def _distance_at_angle(points, T, theta):
    """Returns the distance by which a set of points differs from a template when rotated by theta."""
    new_points = _rotate_by(points, theta)
    return _path_distance(new_points, T.points)


def _centroid(points):
    """Returns the centre of a given set of points."""
    x = 0.0
    y = 0.0
    for point in points:
        x += point.x
        y += point.y
    x /= len(points)
    y /= len(points)
    return Point(x, y)


def _bounding_box(points):
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

    return Rectangle(minX, minY, maxX - minX, maxY - minY)


def _path_distance(pts1, pts2):
    """'Distance' between two paths."""
    d = 0.0
    for index in range(min(len(pts1), len(pts2))):  # assumes pts1.length == pts2.length
        d += _distance(pts1[index], pts2[index])
    return d / len(pts1)


def _path_length(points):
    """Sum of distance between each point, or, length of the path represented by a set of points."""
    d = 0.0
    for index in range(1, len(points)):
        d += _distance(points[index - 1], points[index])
    return d


def _distance(p1, p2):
    """Distance between two points."""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    return math.sqrt(dx * dx + dy * dy)
