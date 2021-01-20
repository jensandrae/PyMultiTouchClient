from objects.handler import Handler


class Square:
    """Simple class to handle a square"""

    # center, width_height as point
    def __init__(self, center, width_height):
        self.center = center
        self.width_height = width_height
        self.handler = Handler()
        self.points = []
        self.calculate_all_points()

    def calculate_all_points(self):
        x_left = self.center - (self.width_height / 2)
        x_right = self.center + (self.width_height / 2)
        y_high = self.center + (self.width_height / 2)
        y_low = self.center - (self.width_height / 2)

        self.points.append((x_left, y_high))  # LH
        self.points.append((x_right, y_high))  # RH
        self.points.append((x_right, y_low))  # RL
        self.points.append((x_left, y_low))  # LL

    def rotate(self, theta):
        self.points = self.handler.rotate_by(self.points, theta)

    def scale(self):
        self.points = self.handler.scale_to_square(self.points)

    def translate(self, point):
        self.points = self.handler.translate_to_point(self.points, point)

    def get_center(self):
        self.center = self.handler.centroid(self.points)
        return self.center
