from enum import Enum
import random
from enums import Direction

class ActionType(Enum):
    IDLE = 0
    WALK_UP = 1
    WALK_DOWN = 2
    WALK_LEFT = 3
    WALK_RIGHT = 4

class Action:
    ACTION_DURATION = 2

    def __init__(self, parent, idle):
        self.duration = self.ACTION_DURATION
        self.parent = parent
        self.time_elapsed = 0
        self.type = ActionType.IDLE

        if not idle:
            rand = random.randrange(0, 5)
            self.set_type(ActionType(rand))

    def set_type(self, action_type):
        self.type = action_type
        if action_type != ActionType.IDLE:
            self.parent.change_direction(Action.direction_from_type(action_type))
            
    def update(self, dt):
        self.time_elapsed += dt
        if self.type != ActionType.IDLE:
            self.parent.move(dt)
        is_finished = self.time_elapsed > self.duration
        return is_finished

    def direction_from_type(type):
        if type == ActionType.WALK_LEFT:
            return Direction.LEFT
        if type == ActionType.WALK_DOWN:
            return Direction.DOWN
        if type == ActionType.WALK_RIGHT:
            return Direction.RIGHT
        if type == ActionType.WALK_UP:
            return Direction.UP