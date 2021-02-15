import copy
import math
from objects.objectHandler import ObjectHandler


def difference_is_ok(key1, key2):
    # This parameter is the threshold
    # Higher = More different finger moves
    # Lower = More equal finger moves
    sc_new = 0.2
    if (key2 * (1 - sc_new)) < key1 < (key2 * (1 + sc_new)):
        return True
    return False

class GestureHandler:
    """ Detects gestures and process them. """

    def __init__(self, display_width, display_height):
        self.example = "example"
        self.gestures = [
            "None",
            "OneFingerMove",
            "TwoFingerScale",
            "TwoFingerUp",
            "TwoFingerDown",
            "ThreeFingerMove",
            "FourFingerUp",
            "FourFingerDown"]
        self.current_cursors = dict()
        self.old_cursors = dict()
        self.display_width = display_width
        self.display_height = display_height
        self.chosen_object = []
        self.drawn_objects = []
        self.min_scale = 0.015
        self.object_handler = ObjectHandler(display_width, display_height)
        self.scale = 1

    ######################################################
    # Handler...
    def handle(self, drawn_objects, current_cursors, old_cursors):
        """Handler - This function is called with a set of points (drawn object)
        that should be processed with gestures. The drawn object get processed by different
        here defined touch gestures. After processing them a new set of points will be returned. """

        self.current_cursors = current_cursors
        self.old_cursors = old_cursors
        self.drawn_objects = drawn_objects

        # Check if cursors are valid, if note return the processed points
        if self.is_one_finger_move():
            return self.drawn_objects

        elif self.is_two_finger_scaling():
            # ToDo: Check functionality ! Uncomment...
            new_array = []
            for drawn_object in self.drawn_objects:
                self.chosen_object = copy.deepcopy(drawn_object)
                new_array.append(self.process_two_finger_move())
            return new_array
            # return self.points

        elif self.is_three_finger_move():
            new_array = []
            for drawn_object in self.drawn_objects:
                self.chosen_object = copy.deepcopy(drawn_object)
                new_array.append(self.process_three_finger_move())
            return new_array

        elif self.is_four_finger_move():
            new_array = []
            for drawn_object in self.drawn_objects:
                self.chosen_object = copy.deepcopy(drawn_object)
                new_array.append(self.process_four_finger_move())
            return new_array

        return self.drawn_objects

    ######################################################
    # Processing....

    # Process - Two finger move (scale object)
    def process_two_finger_move(self):

        if not self.check_bounding():
            return self.chosen_object

        print("process_two_finger_move()")
        (key1, key2) = self.current_cursors.keys()

        # x y from the newest courser finger 1
        (x, y) = self.current_cursors.get(key1)
        key1_point_new = (x * self.display_width, y * self.display_height)

        # x y from the old courser finger 1
        (x, y) = self.old_cursors.get(key1)
        key1_point_old = (x * self.display_width, y * self.display_height)

        # x y from the newest courser finger 2
        (x, y) = self.current_cursors.get(key2)
        key2_point_new = (x * self.display_width, y * self.display_height)

        # x y from the old courser finger 2
        (x, y) = self.old_cursors.get(key2)
        key2_point_old = (x * self.display_width, y * self.display_height)

        distance_new = math.dist(key1_point_new, key2_point_new)
        distance_old = math.dist(key1_point_old, key2_point_old)

        # Here were scale by factor
        if distance_new < distance_old:
            opt_scale = ((distance_old - distance_new) / (distance_old / 100)) / 100
            if opt_scale > self.min_scale:
                self.scale = 1 - opt_scale
        elif distance_new > distance_old:
            opt_scale = ((distance_new - distance_old) / (distance_old / 100)) / 100
            if opt_scale > self.min_scale:
                self.scale = 1 + opt_scale
        else:
            self.scale = 1

        # ToDo: Check Hitbox !

        return self.object_handler.scale(self.chosen_object, self.scale)

    # Process - Three finger move (move object)
    def process_three_finger_move(self):

        if not self.check_bounding():
            return self.chosen_object

        print("process_three_finger_move()")
        # current_point and old_point are between 0 to 1
        # points are between 0 and display height / width
        current_point = self.current_cursors.get(next(iter(self.current_cursors)))
        old_point = self.old_cursors.get(next(iter(self.old_cursors)))
        return self.object_handler.translate(self.chosen_object, old_point, current_point)

    # Process - Four finger move (rotate object)
    def process_four_finger_move(self):

        if not self.check_bounding():
            return self.chosen_object

        print("process_four_finger_move()")
        # ToDo: Do a real implementation
        angle = 0.05

        print("Angle for rotation: ", angle)

        return self.object_handler.rotate(self.chosen_object, angle)

    # Check if a gesture is chosen by cursor
    def check_bounding(self):
        offset = 20
        center = self.object_handler.calculate_center(self.chosen_object)
        for point_object in self.chosen_object:
            (po_x, po_y) = point_object
            (cu_x, cu_y) = self.current_cursors.get(next(iter(self.current_cursors)))

            new_point = (cu_x * self.display_width, cu_y * self.display_height)

            distance = self.object_handler.distance(point_object, new_point)
            distance_center = self.object_handler.distance(new_point, center)

            if distance < offset or distance_center < (offset * 2):
                return True

        return False

    ######################################################
    # Checking....

    # ONE FINGER MOVE
    def is_one_finger_move(self):
        if self.check_finger(1):
            return True
        return False

    # Check - If is a two finger move
    def is_two_finger_scaling(self):
        if self.check_finger(2):
            if set(self.current_cursors.keys()) == set(self.old_cursors.keys()):
                return True
        return False

    # Check - If is a synced three finger move
    def is_three_finger_move(self):
        # Value for accuracy between the fingers, if true it is a correct 3 finger translation
        is_three_finger_move = False

        if self.check_finger(3):
            # Get the Keys (UTIO IDs) from each cursor
            (key1, key2, key3) = self.current_cursors.keys()

            # Calculate all positions from the last frame an the actual for each finger
            (x, y) = self.current_cursors.get(key1)
            key1_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key1)
            key1_point_old = (x * self.display_width, y * self.display_height)

            (x, y) = self.current_cursors.get(key2)
            key2_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key2)
            key2_point_old = (x * self.display_width, y * self.display_height)

            (x, y) = self.current_cursors.get(key3)
            key3_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key3)
            key3_point_old = (x * self.display_width, y * self.display_height)

            # Get the distances between the last and the actual frame for each finger
            dkey1 = math.dist(key1_point_old, key1_point_new)
            dkey2 = math.dist(key2_point_old, key2_point_new)
            dkey3 = math.dist(key3_point_old, key3_point_new)

            # Compare all distances, if all three are nearly the same, then its a 3 finger move
            # Works great, seems there is no need for other indicators like a rectangle ore something else
            if difference_is_ok(dkey1, dkey2) and difference_is_ok(dkey2, dkey3) and difference_is_ok(dkey1, dkey3):
                if difference_is_ok(dkey2, dkey1) and difference_is_ok(dkey3, dkey2) and difference_is_ok(dkey3, dkey1):
                    is_three_finger_move = True

            ## Other possible Indicators...
            ## Vergleiche alle Winkel, sofern alle drei nur wenige prozent voneinander abweichen ok
            ## Vergleiche alle Richtungen, sofern alle drei nur wenige prozent voneinander abweichen ok

        return is_three_finger_move

    # Check - If is a synced four finger move
    def is_four_finger_move(self):
        # ToDo: Important - Break this function down to a simple logik, use it here and same with 3 finger
        # Value for accuracy between the fingers, if true it is a correct 3 finger translation
        is_four_finger_move = False

        if self.check_finger(4):
            # Get the Keys (UTIO IDs) from each cursor
            (key1, key2, key3, key4) = self.current_cursors.keys()

            # Calculate all positions from the last frame an the actual for each finger
            (x, y) = self.current_cursors.get(key1)
            key1_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key1)
            key1_point_old = (x * self.display_width, y * self.display_height)

            (x, y) = self.current_cursors.get(key2)
            key2_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key2)
            key2_point_old = (x * self.display_width, y * self.display_height)

            (x, y) = self.current_cursors.get(key3)
            key3_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key3)
            key3_point_old = (x * self.display_width, y * self.display_height)

            (x, y) = self.current_cursors.get(key4)
            key4_point_new = (x * self.display_width, y * self.display_height)

            (x, y) = self.old_cursors.get(key4)
            key4_point_old = (x * self.display_width, y * self.display_height)

            # Get the distances between the last and the actual frame for each finger
            dkey1 = math.dist(key1_point_old, key1_point_new)
            dkey2 = math.dist(key2_point_old, key2_point_new)
            dkey3 = math.dist(key3_point_old, key3_point_new)
            dkey4 = math.dist(key4_point_old, key4_point_new)

            keySet1 = [dkey1, dkey2, dkey3, dkey4]
            keySet2 = [dkey1, dkey2, dkey3, dkey4]

            # Check all distances between last and actual finger
            for k1 in keySet1:
                for k2 in keySet2:
                    if not difference_is_ok(k1, k2):
                        is_four_finger_move = True
                    else:
                        return False

            ## Other possible Indicators...
            ## Vergleiche alle Winkel, sofern alle drei nur wenige prozent voneinander abweichen ok
            ## Vergleiche alle Richtungen, sofern alle drei nur wenige prozent voneinander abweichen ok

        return is_four_finger_move

    # Check - The amount of fingers between two frames
    def check_finger(self, fingers):
        if len(self.current_cursors) == fingers and len(self.old_cursors) == fingers:
            if set(self.current_cursors.keys()) == set(self.old_cursors.keys()):
                return True  # Yes there are still the same fingers
        return False
