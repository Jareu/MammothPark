# grass_tile.py

import pygame
from tile import Tile
from settings import TILE_SIZE, COLOR_GRASS

class GrassTile(Tile):
    def __init__(self):
        super().__init__('grass')

    def render(self, surface, x, y):
        pygame.draw.rect(surface, COLOR_GRASS, (x, y, TILE_SIZE, TILE_SIZE))