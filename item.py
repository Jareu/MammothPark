# item.py

import pygame
from settings import TILE_SIZE, CHUNK_SIZE, SCREEN_HEIGHT

class Item:    
    def __init__(self, position, sounds, texture):
        self.position = pygame.Vector2(position[0], position[1] - SCREEN_HEIGHT/2)
        self.target = position
        self.sounds = sounds
        self.texture = texture
        self.size = pygame.Vector2(1,1) # min size of 1x1

    def tick(self, dt):
        """Placeholder for tick"""
        pass

    def render (self, surface, screen_offset):
        surface.blit(self.texture, (self.position.x + screen_offset[0], self.position.y + screen_offset[1]))