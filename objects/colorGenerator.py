import random


class ColorGenerator:

    def __init__(self):
        # Random colors for the visualized objects
        self.colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat",
                        "SlateGray",
                        "SeaGreen"]

    def get_new_color_preset(self):
        return random.choice(self.colours)

    def get_new_colors_preset(self, amount):
        colours_rand = []
        for i in range(0, amount):
            colours_rand.append(random.choice(self.colours))
        return colours_rand
