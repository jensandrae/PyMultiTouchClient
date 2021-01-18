# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pythontuio import TuioClient
from threading import Thread
from customListener import CustomListener
import pygame


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
    for value in positions.cursors.values():
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
    screen = pygame.display.set_mode((display_width, display_height))

    refresh_event = custom_listener_obj.pygame_refresh_event

    done = False
    while not done:
        screen.fill([150, 150, 150])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == refresh_event:
                drawCursors(custom_listener_obj, screen)

        pygame.display.update()
        dt = clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    init()
