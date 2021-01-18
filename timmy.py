#
#
#
import turtle as trtl
import random

# Simply Timmy
TMY = trtl.Turtle()

# Predefined colors
CLRS = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray", "SeaGreen"]

# possible directions
DIRECTIONS = [0, 90, 180, 270]

# Forward in steps
FWRD = 30

# Timmys Speed for doing the step
SPEED = "fastest"

# Size of the Pen
PENSIZE = 15


# Constructor
def __init__(self):
    # Pensize
    TMY.pensize(PENSIZE)
    # Set Speed
    TMY.speed(SPEED)
    # Set Color Random
    TMY.color(random.choice(CLRS))
    # Go forward
    TMY.forward(FWRD)
    # Predefined direction
    TMY.setheading(random.choice(DIRECTIONS))


def showTouches():
    ''' This functions show all touches'''
