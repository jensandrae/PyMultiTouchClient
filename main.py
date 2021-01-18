# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from pythontuio import TuioClient, TuioServer
from pythontuio import Cursor
from pythontuio import TuioListener
from threading import Thread

from customListener import CustomListener


def test_dispatcher_listener():
    """ starts a client.
    Start the tuio simpleSimulator and send TUIO data to the testclient manualy. if you notice print "detect a new Cursor" all is fine.
    """

    print("Create a new client and start listener.")

    client = TuioClient(("localhost", 3333))
    t = Thread(target=client.start)
    listener = CustomListener()
    client.add_listener(listener)
    t.start()

    print("New client and listener started.")


if __name__ == '__main__':
    print("Test App TUIO")
    test_dispatcher_listener()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
