# main.py

import random
import pygame
from enums import Keystate
from mammoth import Mammoth
from strawberry import Strawberry
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED, TILE_SIZE
from chunk_manager import ChunkManager
from noise_generator import NoiseGenerator
from texture_manager import TextureManager

keystates = {pygame.K_UP: Keystate.UP, pygame.K_DOWN: Keystate.UP, pygame.K_LEFT: Keystate.UP, pygame.K_RIGHT: Keystate.UP}
mammoths = {}
strawberry_texture = None
strawberries = []
sounds = {}

dt = 0

def populate_mammoths(n):
    for i in range(n):
        position = pygame.Vector2 (random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT)
        new_mammoth = Mammoth(position, False)
        mammoths[i+1] = new_mammoth

def handle_actors():
    for mammoth in mammoths.values():
        mammoth.tick(dt)
        
    for strawberry in strawberries:
        strawberry.tick(dt)

def sort_mammoths():
    mammoth_ys = {}

    for mammoth_id, mammoth in mammoths.items():
        mammoth_ys[mammoth_id] = mammoth.position.y
    sorted_mammoths = sorted(mammoth_ys.items(), key=lambda x:x[1])
    mammoth_ids = list(zip(*sorted_mammoths))[0]
    return mammoth_ids

def drop_strawberry(position):
    global strawberries
    strawberry = Strawberry(position, sounds, strawberry_texture)
    strawberries.append(strawberry)

def main():
    global dt, sounds, strawberry_texture
    # Initialize Pygame
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mammoth Park")
    clock = pygame.time.Clock()

    # Initialize TextureManager
    texture_manager = TextureManager()

    # Initialize NoiseGenerator 
    noise_generator = NoiseGenerator(seed=42)
    noise_generator.default_parameters = {
        'scale': 10.0,
        'octaves': 2,
        'persistence': 0.3,
        'lacunarity': 5.0
    }
    
    # Initialize ChunkManager with the noise generator and texture manager
    chunk_manager = ChunkManager(noise_generator, texture_manager)

    running = True
    camera_position = [0, 0]
    screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    chunk_manager.update_chunks_around_camera(camera_position)

    # Initialize sounds effects

    sounds['falling'] = pygame.mixer.Sound("audio/falling.mp3")
    sounds['small_thud'] = pygame.mixer.Sound("audio/small-thud.mp3")
    strawberry_texture = pygame.image.load("textures/strawberry.png")

    # Play music
    pygame.mixer.music.load('audio/music.mp3')
    pygame.mixer.music.queue('audio/music.mp3', 'mp3', -1)
    pygame.mixer.music.play()

    populate_mammoths(20)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor_pos_x, cursor_pos_y = pygame.mouse.get_pos()
                cursor_pos_x += camera_position[0] - screen_center[0]
                cursor_pos_y += camera_position[1] - screen_center[1]
                cursor_pos = pygame.Vector2(cursor_pos_x, cursor_pos_y)
                drop_strawberry(cursor_pos)

        # Handle keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            camera_position[0] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            camera_position[0] += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            camera_position[1] -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            camera_position[1] += PLAYER_SPEED

        # Update chunks around the camera
        chunk_manager.update_chunks_around_camera(camera_position)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render chunks
        chunk_manager.render(screen, camera_position, screen_center)
        
        sorted_mammoths = sort_mammoths()

        for mammoth_id in sorted_mammoths:
            screen.blit(mammoths[mammoth_id].get_image(), mammoths[mammoth_id].position + mammoths[mammoth_id].size/2 - camera_position)

        handle_actors()

        for strawberry in strawberries:
            screen_offset_x =- camera_position[0] + screen_center[0]
            screen_offset_y =- camera_position[1] + screen_center[1]
            strawberry.render(screen, (screen_offset_x, screen_offset_y))

        # Update display
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()