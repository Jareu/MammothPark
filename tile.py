# tile.py

import pygame
from settings import TILE_SIZE  # Assuming TILE_SIZE is defined in settings.py

class Tile:
    def __init__(self, tile_type):
        self.tile_type = tile_type

    def render(self, surface, x, y):
        """Render the tile on the given surface."""
        raise NotImplementedError("Render method must be implemented by subclasses.")
