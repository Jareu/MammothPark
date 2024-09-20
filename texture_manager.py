# texture_manager.py

import pygame
from settings import TILE_SIZE
from spritesheet import SpriteSheet
from tile_variation import TileVariation
from tile_type import TileType

class TextureManager:
    texture_offsets = {
        TileVariation.EMPTY: (0, 0),
        TileVariation.CORNER_INNER_BOTTOM_LEFT: (48, 144),
        TileVariation.CORNER_INNER_BOTTOM_RIGHT: (96, 144),
        TileVariation.CORNER_INNER_TOP_LEFT: (144, 48),
        TileVariation.CORNER_INNER_TOP_RIGHT: (144, 96),
        TileVariation.CORNER_OUTER_BOTTOM_LEFT: (96, 0),
        TileVariation.CORNER_OUTER_BOTTOM_RIGHT: (48, 0),
        TileVariation.CORNER_OUTER_TOP_LEFT: (0, 96),
        TileVariation.CORNER_OUTER_TOP_RIGHT: (0, 48),
        TileVariation.DIAGONAL_TOP_LEFT_BOTTOM_RIGHT: (48, 96),
        TileVariation.DIAGONAL_TOP_RIGHT_BOTTOM_LEFT: (96, 48),
        TileVariation.EDGE_LEFT: (48, 48),
        TileVariation.EDGE_TOP: (144, 0),
        TileVariation.EDGE_RIGHT: (96, 96),
        TileVariation.EDGE_BOTTOM: (0, 144),
        TileVariation.SOLID: (144, 144),
    }
        
    def __init__(self):
        self.textures = {}
        self.load_textures()

    def load_textures(self):
        # Load textures for each tile type
        self.textures[TileType.Grass] = {}
        self.textures[TileType.Dirt] = {}

        self.textures[TileType.Dirt][TileVariation.SOLID] = pygame.image.load('textures/dirt.png').convert_alpha()

        grass_sprite = SpriteSheet('textures/grass_sprite.png')

        # Load textures for each variation
        for variation in TileVariation:
            self.textures[TileType.Grass][variation] = grass_sprite.image_at(
                (self.texture_offsets[variation][0], self.texture_offsets[variation][1], TILE_SIZE, TILE_SIZE),
                (0, 0, 0)
            )

    def get_texture(self, tile_type, variation=None):
        # Return the texture for the given tile type
        if variation is None:
            return self.textures[tile_type][TileVariation.SOLID]
        return self.textures[tile_type][variation]
