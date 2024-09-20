# dirt_tile.py

import pygame
from tile import Tile
from tile_type import TileType
from settings import TILE_SIZE, COLOR_DIRT

class DirtTile(Tile):
    def __init__(self):
        super().__init__(TileType.Dirt)

