# grass_tile.py

import pygame
from tile import Tile
from settings import TILE_SIZE, COLOR_GRASS

class GrassTile(Tile):
    def __init__(self):
        super().__init__('grass')