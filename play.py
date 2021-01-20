import random
import pygame
import copy

from dollar import Dollar
from tuioclient.Listener import Listener
from objects.colorGenerator import ColorGenerator
from pythontuio import TuioClient
from threading import Thread


class Play:
    PEN_SIZE = 3
    MIN_N_POINTS = 10

    def __init__(self):

        # Main Stuff
        self.old_point = (None, None)
        self.points = []
        self.recognizer = Dollar()
        self.pygame = pygame
        self.pygame.init()
        self.pygame.font.init()
        self.pygame.fastevent.init()
        self.clock = self.pygame.time.Clock()
        self.screen = self.pygame.display.set_mode((800, 800))
        self.done = False
        self.last_gesture = ''

        # Display setting
        self.display_width = 800
        self.display_height = 800
        self.background = (200, 200, 200, 255)
        self.font = pygame.font.SysFont('hack', 40)
        self.fontBig = pygame.font.SysFont('hack', 40)
        self.all_types_string = None

        # Colors
        self.color_generator = ColorGenerator()
        self.color_cursor = self.color_generator.get_new_color_preset()
        self.color_info = self.color_generator.get_new_color_preset()

        # TUIO Client & Listener
        self.client = TuioClient(("localhost", 3333))
        self.thread = Thread(target=self.client.start)
        self.listener = Listener(pygame)

        # Event that triggers based on TUIO Cursor Event
        self.event_refresh = self.listener.pygame_refresh_event
        self.event_down = self.listener.pygame_add_event
        self.event_move = self.listener.pygame_update_event
        self.event_up = self.listener.pygame_remove_event
        self.client.add_listener(self.listener)
        self.thread.start()

        # Starts the main loop
        self.run()

    def move(self, actual_cursor):  ## EVENT MOVE
        if len(actual_cursor) > 0:
            point = next(iter(actual_cursor.values()))  # set here the new point
            # point = (event.x, event.y)
            # if self.old_point != (None, None):
            # self.canvas.create_line(self.old_point, point, width=self.PEN_SIZE)
            # else:
            # self.canvas.delete('all')
            self.points.append(point)
            self.old_point = point

    def reset(self):  ## EVENT UP
        self.old_point = (None, None)
        self.points = []

    def draw_cursors(self, cursors):
        touch_size = 5

        for value in cursors.values():
            if len(value) != 2:
                print("No value")
                return
            (x, y) = value
            print(value)
            self.pygame.draw.circle(
                self.screen,
                self.color_cursor,
                (x * self.display_width, y * self.display_height), touch_size)

    def display_info(self):
        self.screen.blit(self.font.render("Froemmer - Multitouch Gesture App", True, self.color_info), (10, 10))
        self.screen.blit(self.font.render(self.all_types_string, True, self.color_info), (20, 30))
        self.screen.blit(self.font.render("Last drawn gesture: %s" % self.last_gesture, True, self.color_info),
                         (20, 60))

    def display_last_object(self):
        if len(self.points) == 0:
            return
        else:
            self.last_gesture = self.recognizer.get_gesture(self.points)

    def run(self):

        while not self.done:

            actual_cursor = copy.deepcopy(self.listener.cursors)
            self.screen.fill([255, 255, 255])

            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.done = True

                elif event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_ESCAPE:
                        self.done = True

                elif event.type == self.event_down:
                    print()

                elif event.type == self.event_move:
                    self.move(actual_cursor)

                elif event.type == self.event_up:
                    self.display_last_object()
                    self.reset()

                elif event.type == self.event_refresh:
                    print()

            self.display_info()
            self.draw_cursors(actual_cursor)
            self.pygame.display.flip()
            dt = self.clock.tick(30)

        self.pygame.quit()


if __name__ == "__main__":
    multi_touch = Play()
