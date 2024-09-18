# main.py

import random
import pygame
from enums import Keystate
from mammoth import Mammoth
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED, TILE_SIZE
from chunk_manager import ChunkManager
from noise_generator import NoiseGenerator
import spritesheet
from texture_manager import TextureManager
from textures import Textures  # Import the NoiseGenerator class

keystates = {pygame.K_UP: Keystate.UP, pygame.K_DOWN: Keystate.UP, pygame.K_LEFT: Keystate.UP, pygame.K_RIGHT: Keystate.UP}
mammoths = {}
dt = 0

def get_camera_chunk_position(camera_position):
    """Calculate the chunk position based on the camera's pixel position."""
    return camera_position[0] // (32 * TILE_SIZE), camera_position[1] // (32 * TILE_SIZE)

def main():
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

    # Initialize ChunkManager with the noise generator and texture manager
    chunk_manager = ChunkManager(noise_generator, texture_manager)
    # Load chunks in a 3x3 grid centered at (0, 0)
    initial_chunks = [
        (0, 0), (1, 0), (1, -1), (0, -1), (-1, -1),
        (-1, 0), (-1, 1), (0, 1), (1, 1)
    ]
    for chunk_pos in initial_chunks:
        chunk_manager.load_chunk(chunk_pos)

    # Initialize textures
    #sprites = spritesheet.spritesheet('RA_Ground_Tiles.png')
    #textures = Textures(sprites)

    running = True
    camera_position = [0, 0]
    screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Play music
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.queue('music.mp3', 'mp3', -1)
    pygame.mixer.music.play()

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        # Determine the current chunk position of the camera
        camera_chunk_pos = get_camera_chunk_position(camera_position)

        # Update chunks around the camera
        chunk_manager.update_chunks_around_camera(camera_chunk_pos)

        # Clear the screen
        screen.fill((0, 0, 0))

        # Render chunks
        chunk_manager.render(screen, camera_position, screen_center)
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()