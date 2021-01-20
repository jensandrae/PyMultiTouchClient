from pythontuio import TuioClient
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread

LOG_ACTIVE = False


# Press the green button in the gutter to run the script.
class Listener(TuioListener):

    def __init__(self, pygame):
        self.cursors = dict()
        self.pygame = pygame
        self.pygame_refresh_event = self.pygame.event.custom_type()
        self.pygame_remove_event = self.pygame.event.custom_type()
        self.pygame_add_event = self.pygame.event.custom_type()
        self.pygame_update_event = self.pygame.event.custom_type()
        self.pygame.init()

    def add_tuio_object(self, obj):
        """Abstract function to add a behavior for tuioclient add object event"""
        if LOG_ACTIVE:
            print("add_tuio_object")
            print(obj)

    def update_tuio_object(self, obj):
        """Abstract function to add a behavior for tuioclient update object event"""
        if LOG_ACTIVE:
            print("update_tuio_object")
            print(obj)

    def remove_tuio_object(self, obj):
        """Abstract function to add a behavior for tuioclient remove object event"""
        if LOG_ACTIVE:
            print("remove_tuio_object")

    def add_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuioclient add cursor event"""
        if LOG_ACTIVE:
            print("add_tuio_cursor")
        self.cursors[cur.session_id] = cur.position
        ev = self.pygame.event.Event(self.pygame_add_event)
        self.pygame.fastevent.post(ev)

    def update_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuioclient update cursor event"""
        if LOG_ACTIVE:
            print("update_tuio_cursor")
        self.cursors[cur.session_id] = cur.position
        ev = self.pygame.event.Event(self.pygame_update_event)
        self.pygame.fastevent.post(ev)

    def remove_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuioclient remove cursor event"""
        if LOG_ACTIVE:
            print("remove_tuio_cursor")
        self.cursors.pop(cur.session_id)
        ev = self.pygame.event.Event(self.pygame_remove_event)
        self.pygame.fastevent.post(ev)

    def add_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuioclient add blob event"""
        if LOG_ACTIVE:
            print("add_tuio_blob")
            print(blob)

    def update_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuioclient update blob event"""
        if LOG_ACTIVE:
            print("update_tuio_blob")
            print(blob)

    def remove_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuioclient remove blob event"""
        if LOG_ACTIVE:
            print("remove_tuio_blob")
            print(blob)

    def refresh(self, time):
        """Abstract This callback method is invoked by the TuioClient
        to mark the end of a received TUIO message bundle."""
        if LOG_ACTIVE:
            print("----------------------------------------------")
            for key in self.cursors:
                print(key, 'corresponds to', self.cursors[key])
            print("----------------------------------------------")
        ev = self.pygame.event.Event(self.pygame_refresh_event)
        self.pygame.fastevent.post(ev)
