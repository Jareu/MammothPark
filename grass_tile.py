# grass_tile.py

import pygame
from tile import Tile
from tile_type import TileType
from settings import TILE_SIZE, COLOR_GRASS

class GrassTile(Tile):
    def __init__(self):
        super().__init__(TileType.Grass)