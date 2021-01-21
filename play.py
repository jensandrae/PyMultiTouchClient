import pygame
import copy

from tuioclient.Listener import Listener
from objects.colorGenerator import ColorGenerator
from gestures.gestureHandler import GestureHandler
from dollar import Dollar
from pythontuio import TuioClient
from threading import Thread


class Play:
    PEN_SIZE = 3
    MIN_N_POINTS = 10

    def __init__(self):

        # State Machine
        self.first_draw_after_reset_done = False
        self.reset_gesture = 'check'
        self.none_state = 'None'
        self.actual_state = self.none_state
        self.drawn_points = []

        # Main Stuff
        self.display_height = 600
        self.display_width = 900
        self.old_point = (None, None)
        self.points = []
        self.dollar = Dollar()
        self.pygame = pygame
        self.pygame.init()
        self.pygame.font.init()
        self.pygame.fastevent.init()
        self.clock = self.pygame.time.Clock()
        self.screen = self.pygame.display.set_mode((self.display_width, self.display_height))
        self.done = False
        self.actual_gesture = self.reset_gesture

        # Display setting
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

        # Gesture Handler
        self.gesture_handler = GestureHandler(self.display_width, self.display_height)
        self.old_cursors = []
        self.actual_cursor = []

        # Starts the main loop
        self.run()

    # Move of a or multiple cursors, adds points to dollar algorithm
    def move(self, actual_cursor):
        if len(actual_cursor) > 0:
            # set here the new point
            point = next(iter(actual_cursor.values()))
            # point = (event.x, event.y)
            # if self.old_point != (None, None):
            # self.canvas.create_line(self.old_point, point, width=self.PEN_SIZE)
            # else:
            # self.canvas.delete('all')
            self.points.append(point)
            self.old_point = point

    # Event Up, check if a gesture was drawn (Mouse Up)
    def reset(self):
        self.old_point = (None, None)
        self.points = []

    # Display Cursor in Pygame
    def draw_cursors(self, cursors):
        touch_size = 5

        for value in cursors.values():
            if len(value) != 2:
                print("No value")
                return
            (x, y) = value
            # print(value)
            self.pygame.draw.circle(
                self.screen,
                self.color_cursor,
                (x * self.display_width, y * self.display_height), touch_size)

    # Display some additional info in the pygame windows
    def display_info(self):
        self.screen.blit(self.font.render("Froemmer - Multitouch Gesture App", True, self.color_info), (10, 10))
        self.screen.blit(self.font.render(self.all_types_string, True, self.color_info), (20, 30))
        self.screen.blit(self.font.render("Last drawn gesture: %s" % self.actual_gesture, True, self.color_info),
                         (20, 60))

    # Get the gesture (object) as string from the dollar algorithm
    def get_gesture_from_dollar_algo(self):
        if len(self.points) == 0:
            return
        else:
            # ##########################################################################
            # Important, here is the only direct shint point with the dollar algorithm #
            # ##########################################################################
            # We give our actual set of pints an get the gesture for these points      #
            # ##########################################################################
            self.actual_gesture = self.dollar.get_object_by_gesture(self.points)

    # State machine to update the state by actual gesture and other things
    def update_state(self):

        # If actual gesture is equal to the reset gesture (of course delete)
        if self.actual_gesture == self.reset_gesture:
            self.actual_state = self.none_state
            self.first_draw_after_reset_done = False

        # ElseIf actual gesture is not the reset gesture (of course delete)
        elif self.actual_gesture != self.reset_gesture:

            if not self.first_draw_after_reset_done:
                # Now we can draw a new gesture
                self.actual_state = self.actual_gesture
                self.first_draw_after_reset_done = True
                new_points = copy.deepcopy(self.points)
                self.drawn_points = []
                scale = 1.0
                for pnt in new_points:
                    (x, y) = pnt
                    x *= self.display_width * x * scale
                    y *= self.display_width * y * scale
                    self.drawn_points.append([x, y])

    # Acts depending on the state of the state machine
    def handle_state(self):

        if self.actual_state == self.none_state:
            # reset everything and show nothing
            pass
        elif self.actual_state != self.none_state:
            if len(self.drawn_points) > 2:
                # pygame.draw.lines(self.screen, (0, 255, 0), False, self.drawn_points, 5)
                self.drawn_points = self.gesture_handler.handle(self.drawn_points, self.actual_cursor, self.old_cursors)
                pygame.draw.lines(self.screen, (0, 255, 0), False, self.drawn_points, 5)
                # pygame.draw.circle(self.screen, self.color_cursor, (200, 200), 200)
                # display the drawn figure
                pass
        pass

    def run(self):

        # Main Looooop....
        while not self.done:

            # Set actual_cursor as a copy, (self.listener.cursors)
            # can change while a single poll is running
            self.old_cursors = copy.deepcopy(self.actual_cursor)
            self.actual_cursor = copy.deepcopy(self.listener.cursors)

            # PyGame set Background
            self.screen.fill([255, 255, 255])

            # Check all pygame Events...
            for event in self.pygame.event.get():

                # Quit (close windows), quit by user
                if event.type == self.pygame.QUIT:
                    self.done = True

                # Quit (klick escape), quit by user
                elif event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_ESCAPE:
                        self.done = True

                # TUIO Event, new cursor
                elif event.type == self.event_down:
                    pass

                # TUIO Event, cursor move (one or more)
                elif event.type == self.event_move:
                    self.move(self.actual_cursor)

                # TUIO Event, cursor up
                elif event.type == self.event_up:
                    self.get_gesture_from_dollar_algo()
                    self.update_state()
                    self.reset()

                # TUIO Event, if tuio server sends new data
                elif event.type == self.event_refresh:
                    pass

            self.handle_state()
            self.display_info()
            self.draw_cursors(self.actual_cursor)
            self.pygame.display.flip()
            self.clock.tick(30)

        self.pygame.quit()


if __name__ == "__main__":
    multi_touch = Play()
