# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pythontuio import TuioClient
from threading import Thread
from customListener import CustomListener
import pygame
import math
import copy

display_width = 800
display_height = 800
touch_color = (0, 255, 0)


def test_dispatcher_listener():
    """ starts a client.
    Start the tuio simpleSimulator and send TUIO data to the testclient manualy. if you notice print "detect a new Cursor" all is fine.
    """

    print("Create a new client and start listener.")

    client = TuioClient(("localhost", 3333))
    thread = Thread(target=client.start)
    listener = CustomListener(pygame)
    client.add_listener(listener)
    thread.start()

    print("New client and listener started.")
    return listener, thread


def drawCursors(positions, screen):
    touch_size = 5
    for value in positions.values():
        if len(value) != 2:
            return
        (x, y) = value
        pygame.draw.circle(screen, touch_color, (x * display_width, y * display_height), touch_size)


def init():
    print("Test App TUIO")
    custom_listener_obj, thread = test_dispatcher_listener()
    pygame.init()
    pygame.font.init()
    pygame.fastevent.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((display_width, display_height), 0, 32)

    refresh_event = custom_listener_obj.pygame_refresh_event

    old_cursors = dict()

    done = False
    while not done:

        screen.fill([150, 150, 150])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == refresh_event:
                old_cursors = on_refresh(custom_listener_obj, screen, old_cursors)
        drawCursors(old_cursors, screen)

        pygame.display.update()
        dt = clock.tick(30)

    pygame.quit()


def on_refresh(custom_listener_obj, screen, old_cursors):
    current_cursors = copy.deepcopy(custom_listener_obj.cursors)

    if len(current_cursors) == 2 and len(old_cursors) == 2:
        if set(current_cursors.keys()) == set(old_cursors.keys()):
            (key1, key2) = current_cursors.keys()

            (x, y) = current_cursors.get(key1)
            key1_point_new = (x * display_width, y * display_height)

            (x, y) = old_cursors.get(key1)
            key1_point_old = (x * display_width, y * display_height)

            (x, y) = current_cursors.get(key2)
            key2_point_new = (x * display_width, y * display_height)

            (x, y) = old_cursors.get(key2)
            key2_point_old = (x * display_width, y * display_height)

            distance_new = math.dist(key1_point_new, key2_point_new)
            distance_old = math.dist(key1_point_old, key2_point_old)
            print(key1_point_new, key2_point_new)
            print(key1_point_old, key2_point_old)
            print(distance_old, distance_new)

    return current_cursors


if __name__ == '__main__':
    init()
