# texture_manager.py

import pygame

class TextureManager:
    def __init__(self):
        self.textures = {}
        self.load_textures()

    def load_textures(self):
        # Load textures for each tile type
        self.textures['grass'] = pygame.image.load('textures/grass.png').convert_alpha()
        self.textures['mud'] = pygame.image.load('textures/mud.png').convert_alpha()
        # Add more textures here as you introduce new tile types

    def get_texture(self, tile_type):
        # Return the texture for the given tile type
        return self.textures.get(tile_type)
