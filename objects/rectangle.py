from objects.handler import Handler


class Rectangle:
    """Simple representation of a rectangle."""

    def __init__(self, center, width, height):
        # center as (x, y)
        self.center = center
        self.width = width
        self.height = height
        self.handler = Handler()
