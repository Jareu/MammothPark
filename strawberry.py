# strawberry.py

import pygame
from item import Item
from settings import SCREEN_HEIGHT

class Strawberry(Item):
    size = pygame.Vector2(15,18)
    
    def __init__(self, position, sounds, texture):
        self.position = pygame.Vector2(position[0], position[1] - SCREEN_HEIGHT/2)
        self.target = position
        self.speed = 9.81
        self.falling = True
        self.sounds = sounds
        self.texture = texture

        pygame.mixer.Sound.play(self.sounds['falling'])

    def move(self, dt):
        if self.falling == True and self.position.y < self.target.y:      
            self.position.y += self.speed * dt * 50
            if self.position.y >= self.target.y:
                pygame.mixer.Sound.play(self.sounds['small_thud'])
                self.falling = False
    
    def stop(self):
        self.falling = False

    def tick(self, dt):
        self.move(dt)

    def render (self, surface, screen_offset):
        surface.blit(self.texture, (self.position.x + screen_offset[0], self.position.y + screen_offset[1]))