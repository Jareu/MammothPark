from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Keystate(Enum):
    DOWN = 1
    DOWN_FROM_UP = 2
    UP_FROM_DOWN = 3
    UP = 4