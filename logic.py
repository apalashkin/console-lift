import threading
import time


class MoveUpEvent(threading.Event):
    pass


class MoveDownEvent(threading.Event):
    pass

EVENTS = (MoveUpEvent(), MoveDownEvent())


def loop():
    while True:
        for event in EVENTS:
            if isinstance(event, MoveUpEvent):
                event.set()
            time.sleep(0.5)
