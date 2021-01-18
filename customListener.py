from pythontuio import TuioClient
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread


# Press the green button in the gutter to run the script.
class CustomListener(TuioListener):

    def __init__(self, pygame):
        self.cursors = dict()
        self.pygame = pygame
        self.pygame_refresh_event = self.pygame.event.custom_type()
        self.pygame.init()
        # Init stuff here

    def add_tuio_object(self, obj):
        """Abstract function to add a behavior for tuio add object event"""
        print("add_tuio_object")
        print(obj)

    def update_tuio_object(self, obj):
        """Abstract function to add a behavior for tuio update object event"""
        print("update_tuio_object")
        print(obj)

    def remove_tuio_object(self, obj):
        """Abstract function to add a behavior for tuio remove object event"""
        print("remove_tuio_object")

    def add_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuio add cursor event"""
        self.cursors[cur.session_id] = cur.position

    def update_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuio update cursor event"""
        print("update_tuio_cursor")
        self.cursors[cur.session_id] = cur.position

    def remove_tuio_cursor(self, cur):
        """Abstract function to add a behavior for tuio remove cursor event"""
        print("remove_tuio_cursor")
        self.cursors.pop(cur.session_id)

    def add_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuio add blob event"""
        print("add_tuio_blob")
        print(blob)

    def update_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuio update blob event"""
        print("update_tuio_blob")
        print(blob)

    def remove_tuio_blob(self, blob):
        """Abstract function to add a behavior for tuio remove blob event"""
        print("remove_tuio_blob")
        print(blob)

    def refresh(self, time):
        """Abstract This callback method is invoked by the TuioClient
        to mark the end of a received TUIO message bundle."""
        print("----------------------------------------------")
        for key in self.cursors:
            print(key, 'corresponds to', self.cursors[key])
        print("----------------------------------------------")
        ev = self.pygame.event.Event(self.pygame_refresh_event)
        self.pygame.fastevent.post(ev)

# ToDo(1) ● Implementierung der TuioClient API # (DONE)
# ToDo(2) ● Auswerten der TUIO Events # (DONE)
# ToDo(3) ● Erstellen einer eigenen Gesten-Alogrhytmik zur Interaktion mit 2-Dimensionalen Objekten (translate, rotate, scale) (Praktikum 4+5)
# ToDo(4) ● Erweiterte Gestenerkennungen (Praktikum 4+5) -> Diskrete Gesten sind gemeint !

#### Zwischen ToDo's für 2D Interaktion
# ToDo(3.1) ● getCourserId()
# ToDo(3.2) ● getSessionId()
# ToDo(3.3) ● getX()
# ToDo(3.4) ● getY()
# ToDo(3.5) ● translate() -> Kont. Gesten
# ToDo(3.6) ● rotate() -> Kont. Gesten
# ToDo(3.7) ● scale() -> Kont. Gesten
# ToDo(3.8) ● Erweiterte Gestenerkennung (MUSS ?) -> Nicht Kontin. Gesten -> Sehr relevant für Benotung -> Keine False Positives idealerweise
# ToDo(3.9) ● Normalisierung der Geste + Reduktion auf 32 Punkte einer unrealistischen Geste


# 1. Kein Objekt
# 2. Wenn per wer. GEsten etwas erkannt wird dann zeichen allgemein, nicht so wie user (Das gilt immer auch wenn schon was da ist)
# 3. Kont. Gesten anwenden

# Objekte -> Dreieck, Rechteck, Kreis

## Objekte aus Geste Erkennen -> Erstellen -> Löschen ->
## Es reicht simple impl. sauberes erkennen von Gesten !!! -> Klare erkennung von Geste ist relevant, was damit gesteuert wird nicht, es muss nur eindeutig sein !!!

## Letzer Termin als Arbeitstermin -> Wenn nicht fertig, dann seperater Termin zur Abgabe (ca. 14 Tage danach) !! -> Abgabe ist aber trotzdem möglich !!

#### FRAGE AN PROF
# Müssen verschiedene Objekte vorhanden sein die seperat gesteuert werden können sollten ?
#


##### UNITY -> Erscheinen lassen von Objekten und diese seperat Steuern ?!
