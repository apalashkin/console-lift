import collections
import threading
import time
import types

from asciimatics.effects import Cycle, Print, Sprite
from asciimatics.event import Event
from asciimatics.paths import Path, DynamicPath
from asciimatics.renderers import StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import Screen

PASSANGER = '🚶 '

ROOF = r"""
 /####################\
/                      \
|==========+===========|
"""

FLOOR = r"""
|                      |
|  __            ({:2d})  |
| |  | +               |
|=========     ========|
"""

LIFT = r"""
 _|_
|   |
|___|
"""

Y_BASE = 3


class LiftPath(DynamicPath):
    def process_event(self, event):
        from logic import MoveUpEvent, MoveDownEvent

        if isinstance(event, MoveUpEvent):
            self._y -= 1
            event.clear()
        elif isinstance(event, MoveDownEvent):
            self._y += 1
            event.clear()
        else:
            return event


class Lift(Sprite):
    def __init__(self, screen, path, colour=Screen.COLOUR_WHITE, start_frame=0, stop_frame=0):
        super(Lift, self).__init__(screen, renderer_dict={"default": StaticRenderer(images=[LIFT])},
                                   path=path, colour=colour, start_frame=start_frame, stop_frame=stop_frame)


def modify_roof_for_lift_gaps(roof, lifts):
    replace_map = {
        1: '#' * 12,
        2: ' ' * 12,
        3: '=' * 12,
    }
    return modify_building_for_lift_gaps(roof, lifts, replace_map)


def modify_floor_for_lift_gaps(floor, lifts):
    replace_map = collections.defaultdict(lambda: ' ' * 12)
    replace_map[4] = '=' * 7 + ' ' * 5
    return modify_building_for_lift_gaps(floor, lifts, replace_map)


def modify_building_for_lift_gaps(base_obj, lifts, replace_map):
    if lifts == 1:
        return base_obj

    objs = []
    for i, obj in enumerate(base_obj.split('\n')):
        if not obj:
            continue
        obj = list(obj)
        for _ in range(1, lifts):
            obj.insert(15, replace_map[i])
        objs.append(''.join(obj))
    return '\n'.join(objs)


def build_building(screen, floors, lifts):
    effects = [Print(screen, StaticRenderer([modify_roof_for_lift_gaps(ROOF, lifts)]), Y_BASE - 3)]
    for i in range(floors):
        effects.append(Print(screen, StaticRenderer([modify_floor_for_lift_gaps(FLOOR, lifts).format(floors - i)]), Y_BASE + i * 3))
    return effects


def insert_lifts(screen, effects, floors, lift_count):
    middle_floor = (floors + 1) // 2
    lifts = []
    for i in range(1, lift_count + 1):
        path = LiftPath(screen, effects[middle_floor]._x + 12 * i, effects[middle_floor]._y + 2)
        lifts.append(Lift(screen, path))
    effects.extend(lifts)
    return effects


def open_screen():
    from logic import EVENTS

    def get_lift_events(self):
        for event in EVENTS:
            if event.is_set():
                return event
        return self.__class__.get_event(self)

    screen = Screen.open()
    screen.get_event = types.MethodType(get_lift_events, screen)
    return screen


def make_scenes(effects):
    return [Scene(effects)]
