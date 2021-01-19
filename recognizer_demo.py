from pythontuio import TuioClient
from threading import Thread
from customListener import CustomListener
from dollar import Recognizer

import math
import copy
import random
import pygame
import pickle

LEFT = 1
RIGHT = 3

display_width = 800
display_height = 800
touch_color = (0, 255, 0)

scale = 1
trans_x = 0
trans_y = 0

# Raw points for the three example gestures.
circlePoints = [(269, 84), (263, 86), (257, 92), (253, 98), (249, 104), (245, 114), (243, 122), (239, 132), (237, 142),
                (235, 152), (235, 162), (235, 172), (235, 180), (239, 190), (245, 198), (251, 206), (259, 212),
                (267, 216), (275, 218), (281, 222), (287, 224), (295, 224), (301, 226), (311, 226), (319, 226),
                (329, 226), (339, 226), (349, 226), (352, 226), (360, 226), (362, 225), (366, 219), (367, 217),
                (367, 209), (367, 206), (367, 198), (367, 190), (367, 182), (367, 174), (365, 166), (363, 158),
                (359, 152), (355, 146), (353, 138), (349, 134), (345, 130), (341, 124), (340, 122), (338, 121),
                (337, 119), (336, 117), (334, 116), (332, 115), (331, 114), (327, 110), (325, 109), (323, 109),
                (321, 108), (320, 108), (318, 107), (316, 107), (315, 107), (314, 107), (313, 107), (312, 107),
                (311, 107), (310, 107), (309, 106), (308, 106), (307, 105), (306, 105), (305, 105), (304, 105),
                (303, 104), (302, 104), (301, 104), (300, 104), (299, 103), (298, 103), (296, 102), (295, 101),
                (293, 101), (292, 100), (291, 100), (290, 100), (289, 100), (288, 100), (288, 99), (287, 99), (287, 99)]
squarePoints = [(193, 123), (193, 131), (193, 139), (195, 151), (197, 161), (199, 175), (201, 187), (205, 201),
                (207, 213), (209, 225), (213, 235), (213, 243), (215, 251), (215, 254), (217, 262), (217, 264),
                (217, 266), (217, 267), (218, 267), (219, 267), (221, 267), (224, 267), (227, 267), (237, 267),
                (247, 265), (259, 263), (273, 261), (287, 261), (303, 259), (317, 257), (331, 255), (347, 255),
                (361, 253), (375, 253), (385, 253), (395, 251), (403, 249), (406, 249), (408, 249), (408, 248),
                (409, 248), (409, 246), (409, 245), (409, 242), (409, 234), (409, 226), (409, 216), (407, 204),
                (407, 194), (405, 182), (403, 172), (403, 160), (401, 150), (399, 140), (399, 130), (397, 122),
                (397, 119), (397, 116), (396, 114), (396, 112), (396, 111), (396, 110), (396, 109), (396, 108),
                (396, 107), (396, 106), (396, 105), (394, 105), (392, 105), (384, 105), (376, 105), (364, 105),
                (350, 107), (334, 109), (318, 111), (306, 113), (294, 115), (286, 117), (278, 117), (272, 119),
                (269, 119), (263, 121), (260, 121), (254, 123), (251, 123), (245, 125), (243, 125), (242, 125),
                (241, 126), (240, 126), (238, 127), (236, 127), (232, 128), (231, 128), (231, 129), (230, 129),
                (228, 129), (227, 129), (226, 129), (225, 129), (224, 129), (223, 129), (222, 129), (221, 130),
                (221, 130)]
trianglePoints = [(282, 83), (281, 85), (277, 91), (273, 97), (267, 105), (261, 113), (253, 123), (243, 133),
                  (235, 141), (229, 149), (221, 153), (217, 159), (216, 160), (215, 161), (214, 162), (216, 162),
                  (218, 162), (221, 162), (227, 164), (233, 166), (241, 166), (249, 166), (259, 166), (271, 166),
                  (283, 166), (297, 166), (309, 164), (323, 164), (335, 162), (345, 162), (353, 162), (361, 160),
                  (363, 159), (365, 159), (366, 158), (367, 158), (368, 157), (369, 157), (370, 156), (371, 156),
                  (371, 155), (372, 155), (372, 153), (372, 152), (372, 151), (372, 149), (372, 147), (371, 145),
                  (367, 141), (363, 137), (359, 133), (353, 129), (349, 125), (343, 121), (337, 119), (333, 115),
                  (327, 111), (325, 110), (324, 109), (320, 105), (318, 104), (314, 100), (312, 99), (310, 98),
                  (306, 94), (305, 93), (303, 92), (301, 91), (300, 90), (298, 89), (297, 88), (296, 88), (295, 87),
                  (294, 87), (293, 87), (293, 87)]


class RecognizerDemo():
    def __init__(self, screen):
        self.screen = screen
        self.background = (200, 200, 200, 255)
        self.font = pygame.font.SysFont('hack', 15)
        self.fontBig = pygame.font.SysFont('hack', 25)
        self.mouseDown = False
        self.mouseButton = False
        self.positions = []

        self.all_types_string = None
        self.recognizer = Recognizer()

        self.extra_trainingPoints = []

        self.all_types_string = "Gestures: circle, square, triangle"
        self.recognizer.addTemplate('circle', circlePoints)
        self.recognizer.addTemplate('square', squarePoints)
        self.recognizer.addTemplate('triangle', trianglePoints)

        self.last_name = None
        self.last_index = -1
        self.last_accuracy = 0.0

        self.client = TuioClient(("localhost", 3333))
        self.thread = Thread(target=self.client.start)
        self.listener = CustomListener(pygame)
        self.client.add_listener(self.listener)
        self.thread.start()

        # Event that triggers based on TUIO Cursor Event
        self.event_refresh = self.listener.pygame_refresh_event
        self.event_down = self.listener.pygame_add_event
        self.event_move = self.listener.pygame_update_event
        self.event_up = self.listener.pygame_remove_event

    def useCustomTemplate(self, file_name):
        self.recognizer = Recognizer()
        with open(file_name, 'rb') as handle:
            custom_training = pickle.load(handle)
        for one_type in custom_training.keys():
            if type(custom_training[one_type][0]) == list:
                for one_data in custom_training[one_type]:
                    self.recognizer.addTemplate(one_type, one_data)
            else:
                self.recognizer.addTemplate(one_type, custom_training[one_type])

            if self.all_types_string == None:
                self.all_types_string = "Gestures: " + one_type
            else:
                self.all_types_string += "," + one_type
        print(self.all_types_string)

    def OnPaint(self, event):
        #        self.screen.fill(self.background)

        if not event == None:
            self.mouseButton = event

        if self.positions == []:
            return
        (x, y, event_type) = self.positions[-1]

        if event_type == "stop":
            points = [(p[0], p[1]) for p in self.positions]
            if len(points) > 10:
                (index, name, score) = self.recognizer.recognize(points)
                if score > 0.8:  ## ToDo Test only if better than 90%
                    self.last_index = index
                    self.last_name = name
                    self.last_accuracy = score
                    # if self.mouseButton == RIGHT:
                    #    self.extra_trainingPoints.append(points)
                    #    print("training points saved ", len(points))
                    #    self.mouseButton = None

            else:
                self.last_index = -1
                self.last_name = '(Not enough points - try again!)'
                self.last_accuracy = 0.0

    def draw(self):
        # if self.mouseButton == LEFT:
        #     dot_color = (255, 255, 255)
        # elif self.mouseButton == RIGHT:
        #     dot_color = (255, 100, 100)
        # else:
        dot_color = (0, 0, 0)  # ToDo: Bissel mehr Farbe rein bringen

        for position in self.positions:
            (x, y, event_type) = position
            if event_type == "start":
                r = 10
            elif event_type == "stop":
                r = 1
            else:
                r = 3
            pygame.draw.circle(self.screen, dot_color, (x, y), r)

        self.screen.blit(self.font.render("Froemmer - Multitouch Gesture App", True, (0, 255, 255)), (10, 10))
        self.screen.blit(self.font.render(self.all_types_string, True, (0, 255, 255)), (20, 30))

        self.screen.blit(self.font.render("Last drawn gesture: %s" % self.last_name, True, (0, 255, 255)), (20, 60))
        self.screen.blit(
            self.font.render("Gesture accuracy: %2.2f%%" % (self.last_accuracy * 100), True, (0, 255, 255)),
            (20, 80))


def draw_cursors(positions, screen):
    touch_size = 5
    for value in positions.values():
        if len(value) != 2:
            return
        (x, y) = value
        pygame.draw.circle(screen, touch_color, (x * display_width, y * display_height), touch_size)


def on_refresh(listener, old_cursors):
    current_cursors = copy.deepcopy(listener.cursors)

    print("XXX ", current_cursors)
    print("XXX ", old_cursors)

    ####################################################################################################################
    # Multi Touch Gesture - SCALING with 2 fingers
    if len(current_cursors) == 2 and len(old_cursors) == 2:
        if set(current_cursors.keys()) == set(old_cursors.keys()):
            print("SCALING ACTIVE")
            (key1, key2) = current_cursors.keys()

            # x y from the newest courser finger 1
            (x, y) = current_cursors.get(key1)
            key1_point_new = (x * display_width, y * display_height)

            # x y from the old courser finger 1
            (x, y) = old_cursors.get(key1)
            key1_point_old = (x * display_width, y * display_height)

            # x y from the newest courser finger 2
            (x, y) = current_cursors.get(key2)
            key2_point_new = (x * display_width, y * display_height)

            # x y from the old courser finger 2
            (x, y) = old_cursors.get(key2)
            key2_point_old = (x * display_width, y * display_height)

            distance_new = math.dist(key1_point_new, key2_point_new)
            distance_old = math.dist(key1_point_old, key2_point_old)

            # print(key1_point_new, key2_point_new)
            # print(key1_point_old, key2_point_old)
            # print(distance_old, distance_new)

            # Use global value scale local
            global scale
            # Minimum scale before the scale gets displayed, looks smoother
            min_scale = 0.015

            # Here were scale by factor
            if distance_new < distance_old:
                opt_scale = ((distance_old - distance_new) / (distance_old / 100)) / 100
                if opt_scale > min_scale:
                    scale = 1 - opt_scale
            elif distance_new > distance_old:
                opt_scale = ((distance_new - distance_old) / (distance_old / 100)) / 100
                if opt_scale > min_scale:
                    scale = 1 + opt_scale
            else:
                scale = 1


    ####################################################################################################################
    # Multi Touch Gesture - TRANSLATING with 3 fingers
    if len(current_cursors) == 3 and len(old_cursors) == 3:
        if set(current_cursors.keys()) == set(old_cursors.keys()):
            print("TRANSLATING ACTIVE")
            # Value for accuracy between the fingers, if true it is a correct 3 finger translation
            difference_in_distance_ok = False

            # Get the Keys (UTIO IDs) from each cursor
            (key1, key2, key3) = current_cursors.keys()

            # Calculate all positions from the last frame an the actual for each finger
            (x, y) = current_cursors.get(key1)
            key1_point_new = (x * display_width, y * display_height)

            (x, y) = old_cursors.get(key1)
            key1_point_old = (x * display_width, y * display_height)

            (x, y) = current_cursors.get(key2)
            key2_point_new = (x * display_width, y * display_height)

            (x, y) = old_cursors.get(key2)
            key2_point_old = (x * display_width, y * display_height)

            (x, y) = current_cursors.get(key3)
            key3_point_new = (x * display_width, y * display_height)

            (x, y) = old_cursors.get(key3)
            key3_point_old = (x * display_width, y * display_height)

            # Get the distances between the last and the actual frame for each finger
            dkey1 = math.dist(key1_point_old, key1_point_new)
            dkey2 = math.dist(key2_point_old, key2_point_new)
            dkey3 = math.dist(key3_point_old, key3_point_new)

            # Compare all distances, if all three are nearly the same, then its a 3 finger move
            # Works great, seems there is no need for other indicators like a rectangle ore something else
            if difference_is_ok(dkey1, dkey2) and difference_is_ok(dkey2, dkey3) and difference_is_ok(dkey1, dkey3):
                if difference_is_ok(dkey2, dkey1) and difference_is_ok(dkey3, dkey2) and difference_is_ok(dkey3, dkey1):
                    difference_in_distance_ok = True

            ## Other possible Indicators...
            ## Vergleiche alle Winkel, sofern alle drei nur wenige prozent voneinander abweichen ok
            ## Vergleiche alle Richtungen, sofern alle drei nur wenige prozent voneinander abweichen ok

            ## Dann nimm eine x_neu - x_alt, sowie y_neu - y_alt, dies kannst du als translation auf die alten koordinaten rechnen
            if difference_in_distance_ok:
                global trans_x
                global trans_y
                x_new, y_new = current_cursors.get(key1)
                x_old, y_old = old_cursors.get(key1)
                trans_x = (x_new - x_old) * 1000
                trans_y = (y_new - y_old) * 1000

    return current_cursors


def difference_is_ok(key1, key2):
    # This parameter is the threshold
    # Higher = More different finger moves
    # Lower = More equal finger moves
    sc_new = 0.2
    if (key2 * (1 - sc_new)) < key1 < (key2 * (1 + sc_new)):
        return True
    return False


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    pygame.fastevent.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 800))
    done = False

    # Random colors for the visualized objects
    colours = ["CornflowerBlue", "DarkOrchid", "IndianRed", "DeepSkyBlue", "LightSeaGreen", "wheat", "SlateGray",
               "SeaGreen"]
    colours_rand = (random.choice(colours), random.choice(colours), random.choice(colours), random.choice(colours))

    demo = RecognizerDemo(screen)
    demo.OnPaint(None)

    rect_width = 500
    rect_height = 500
    circle_radius = 200
    rect_x = 150
    rect_y = 150
    ci_x = 300
    ci_y = 300

    # [100, 700], [500, 200], [900, 700]
    a_x = 100
    a_y = 700
    b_x = 500
    b_y = 200
    c_x = 900
    c_y = 700

    last_key = dict()
    old_cursors = dict()
    current_cursors = dict()

    current_state = None
    last_state = None

    while not done:
        screen.fill([255, 255, 255])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

            elif event.type == demo.event_refresh:
                old_cursors = on_refresh(demo.listener, old_cursors)
                current_state = demo.last_name

            elif event.type == demo.event_down:
                print("event_down 1")
                if len(demo.listener.cursors) == 1:
                    print("event_down 2")
                    if last_key != demo.listener.cursors.keys():  # len(last_key) == 0 or
                        print("event_down FINAL")
                        demo.mouseDown = True
                        (x, y) = next(iter(demo.listener.cursors.values()))
                        demo.positions = [(x, y, 'start')]
                        demo.OnPaint(demo.event_down)  # ToDo was passiert hier ?!
                        pos = next(iter(demo.listener.cursors.values()))
                        last_key = next(iter(demo.listener.cursors))
                        # Needed for event.type == demo.event_up:
                        current_cursors = copy.deepcopy(demo.listener.cursors)

            elif event.type == demo.event_move:
                print("event_move 1")
                if len(demo.listener.cursors) == 1:
                    print("event_move 2")
                    if len(demo.listener.cursors) == 1 and last_key == next(iter(demo.listener.cursors)):  # ÄNDERUNG
                        print("event_move FINAL")
                        if demo.mouseDown:
                            (x, y) = next(iter(demo.listener.cursors.values()))
                            demo.positions.append((x, y, 'move'))
                            demo.OnPaint(None)
                            # Needed for event.type == demo.event_up:
                            current_cursors = copy.deepcopy(demo.listener.cursors)

            elif event.type == demo.event_up:
                print("event_up 1")
                if len(demo.listener.cursors) == 0 and len(current_cursors) == 1:  # and len(last_key) != 0
                    print("event_up FINAL")
                    demo.mouseDown = False
                    (x, y) = next(iter(current_cursors.values()))
                    demo.positions.append((x, y, 'stop'))
                    demo.OnPaint(None)  # demo.OnPaint(event.button)

        demo.OnPaint(None)
        demo.draw()

        # scaling
        rect_width *= scale
        rect_height *= scale
        circle_radius *= scale
        # translating
        rect_x += trans_x
        rect_y += trans_y
        ci_x += trans_x
        ci_y += trans_y
        a_x += trans_x
        a_y += trans_y
        b_x += trans_x
        b_y += trans_y
        c_x += trans_x
        c_y += trans_y

        if last_state != current_state:
            rect_width = 500
            rect_height = 500
            circle_radius = 200
            rect_x = 150
            rect_y = 150
            ci_x = 300
            ci_y = 300
            a_x = 100
            a_y = 700
            b_x = 500
            b_y = 200
            c_x = 900
            c_y = 700

        if current_state == None:
            print("No figure detected")
        elif current_state == "circle":
            last_state = current_state
            pygame.draw.circle(screen, colours_rand[2], [ci_x, ci_y], circle_radius, 10)
        elif current_state == "square":
            last_state = current_state
            pygame.draw.rect(screen, colours_rand[0], [rect_x, rect_y, rect_width, rect_height], 10)
        elif current_state == "triangle":
            last_state = current_state
            pygame.draw.polygon(screen, colours_rand[3], [[a_x, a_y], [b_x, b_y], [c_x, c_y]], 10)

        scale = 1
        trans_x = 0
        trans_y = 0

        draw_cursors(demo.listener.cursors, screen)
        pygame.display.flip()
        dt = clock.tick(100)

    pygame.quit()

    if len(demo.extra_trainingPoints) > 0:
        print("=======Copy below print to put as input=======", end="\n")
        for i, one_template in enumerate(demo.extra_trainingPoints):
            print("input_{} = ".format(i), end="")
            print(one_template)
