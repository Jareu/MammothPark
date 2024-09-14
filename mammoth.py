import pygame
import spritesheet
import random
from enums import Direction
from action import Action, ActionType

ANIMATION_FPS = 6
ANIMATION_SPEED = 1/ANIMATION_FPS
NUM_FRAMES = 4
CASUAL_SPEED = 100
PLAYER_SPEED = 200
        
class Mammoth:
    size = pygame.Vector2(156,159)
    
    def __init__(self, position, controlled):
        self.controlled = controlled
        self.moving = False
        self.direction_vector = pygame.Vector2()
        self.animation_timer = 0
        self.frame_index = 0
        self.speed = PLAYER_SPEED
        self.position = position
        self.direction = Direction.RIGHT

        if not controlled:
            self.speed = CASUAL_SPEED
            idle = True if random.random() > 0.5 else False
            self.current_action = Action(self, idle)
            self.current_action.time_elapsed += random.random() * Action.ACTION_DURATION
        
        self.spritesheet = spritesheet.spritesheet('mammoth.png')
        self.img_down = self.spritesheet.images_at([
            (self.size.x, 0, self.size.x, self.size.y),
            (self.size.x*2, 0, self.size.x, self.size.y),
            (self.size.x, 0, self.size.x, self.size.y),
            (0, 0, self.size.x, self.size.y)
        ], (0,0,0))

        self.img_left = self.spritesheet.images_at([
            (self.size.x, self.size.y, self.size.x, self.size.y),
            (self.size.x*2, self.size.y, self.size.x, self.size.y),
            (self.size.x, self.size.y, self.size.x, self.size.y),
            (0, self.size.y, self.size.x, self.size.y)
        ], (0,0,0))

        self.img_right = self.spritesheet.images_at([
            (self.size.x, self.size.y*2, self.size.x, self.size.y),
            (self.size.x*2, self.size.y*2, self.size.x, self.size.y),
            (self.size.x, self.size.y*2, self.size.x, self.size.y),
            (0, self.size.y*2, self.size.x, self.size.y)
        ], (0,0,0))

        self.img_up = self.spritesheet.images_at([
            (self.size.x, self.size.y*3, self.size.x, self.size.y),
            (self.size.x*2, self.size.y*3, self.size.x, self.size.y),
            (self.size.x, self.size.y*3, self.size.x, self.size.y),
            (0, self.size.y*3, self.size.x, self.size.y)
        ], (0,0,0))
    
    def move(self, dt):        
        self.position.x += dt * self.direction_vector.x * self.speed
        self.position.y += dt * self.direction_vector.y * self.speed
        self.moving = True
    
    def change_direction(self, new_direction):
        self.direction = new_direction

        if new_direction == Direction.LEFT:
            self.direction_vector.x = -1
            self.direction_vector.y = 0
            return
        if new_direction == Direction.RIGHT:
            self.direction_vector.x = 1
            self.direction_vector.y = 0
            return
        if new_direction == Direction.DOWN:
            self.direction_vector.x = 0
            self.direction_vector.y = 1
            return
        if new_direction == Direction.UP:
            self.direction_vector.x = 0
            self.direction_vector.y = -1
    
    def stop(self):
        self.moving = False
        self.animation_timer = 0
        self.frame_index = 0

    def get_image(self):
        match self.direction:
            case Direction.DOWN:
                return self.img_down[self.frame_index]
            case Direction.LEFT:
                return self.img_left[self.frame_index]
            case Direction.RIGHT:
                return self.img_right[self.frame_index]
            case Direction.UP:
                return self.img_up[self.frame_index]
    
    def handle_animations(self, dt):
        if not self.moving:
            return
        
        new_anim_timer = (self.animation_timer + dt) % ANIMATION_SPEED

        if new_anim_timer < self.animation_timer:
            self.frame_index = (self.frame_index + 1) if self.frame_index < NUM_FRAMES-1 else 0

        self.animation_timer = new_anim_timer

    def tick(self, dt):
        self.handle_animations(dt)
        if not self.controlled:
            self.do_behaviour(dt)

    def do_behaviour(self, dt):
        is_finished = self.current_action.update(dt)
        if is_finished:
            self.stop()
            self.current_action = Action(self, self.current_action.type != ActionType.IDLE)
