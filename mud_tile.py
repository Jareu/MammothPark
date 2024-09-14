# mud_tile.py

import pygame
from tile import Tile
from settings import TILE_SIZE, COLOR_MUD

class MudTile(Tile):
    def __init__(self):
        super().__init__('mud')

    def render(self, surface, x, y):
        pygame.draw.rect(surface, COLOR_MUD, (x, y, TILE_SIZE, TILE_SIZE))
