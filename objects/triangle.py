class Triangle:
    """Simple class to handle a square"""

    # center, width_height as point
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.center = self.calculate_center(a, b, c)

    def calculate_center(self):
        # ToDo: Calculate center correctly
        return self.a
