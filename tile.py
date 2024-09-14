# tile.py

import pygame
from settings import TILE_SIZE  # Assuming TILE_SIZE is defined in settings.py

class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type
        self.img = None
        
    def render(self, surface, x, y):
        surface.blit(self.img, (x*TILE_SIZE, y*TILE_SIZE))