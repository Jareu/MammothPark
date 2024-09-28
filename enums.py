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

class TileVariation(Enum):
    EMPTY = 0
    CORNER_OUTER_TOP_LEFT = 8
    CORNER_OUTER_BOTTOM_LEFT = 2
    EDGE_TOP = 3
    CORNER_OUTER_TOP_RIGHT = 4
    EDGE_LEFT = 5
    DIAGONAL_TOP_RIGHT_BOTTOM_LEFT = 6
    CORNER_INNER_TOP_LEFT = 7
    CORNER_OUTER_BOTTOM_RIGHT = 1
    DIAGONAL_TOP_LEFT_BOTTOM_RIGHT = 9
    EDGE_RIGHT = 10
    CORNER_INNER_TOP_RIGHT = 11
    EDGE_BOTTOM = 12
    CORNER_INNER_BOTTOM_LEFT = 13
    CORNER_INNER_BOTTOM_RIGHT = 14
    SOLID = 15

class TileType(Enum):
    Dirt = 0
    Grass = 1

class Side(Enum):
    Top = 0
    Right = 1
    Bottom = 2
    Left = 3