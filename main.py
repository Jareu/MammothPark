# main.py

import random
import pygame
from enums import Keystate
from mammoth import Mammoth
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED, TILE_SIZE
from chunk_manager import ChunkManager
from noise_generator import NoiseGenerator  # Import the NoiseGenerator class

keystates = {pygame.K_UP: Keystate.UP, pygame.K_DOWN: Keystate.UP, pygame.K_LEFT: Keystate.UP, pygame.K_RIGHT: Keystate.UP}
mammoths = {}
dt = 0

def get_camera_chunk_position(camera_position):
    """Calculate the chunk position based on the camera's pixel position."""
    return camera_position[0] // (32 * TILE_SIZE), camera_position[1] // (32 * TILE_SIZE)

def populate_mammoths(n):
    for i in range(n):
        position = pygame.Vector2 (random.random() * SCREEN_WIDTH, random.random() * SCREEN_HEIGHT)
        new_mammoth = Mammoth(position, False)
        mammoths[i+1] = new_mammoth

def handle_actors():
    for mammoth in mammoths.values():
        mammoth.tick(dt)

def sort_mammoths():
    mammoth_ys = {}

    for mammoth_id, mammoth in mammoths.items():
        mammoth_ys[mammoth_id] = mammoth.position.y
    sorted_mammoths = sorted(mammoth_ys.items(), key=lambda x:x[1])
    mammoth_ids = list(zip(*sorted_mammoths))[0]
    return mammoth_ids

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Map Game")

# Initialize NoiseGenerator
noise_generator = NoiseGenerator(seed=42)

# Initialize ChunkManager with the noise generator
chunk_manager = ChunkManager(noise_generator)

# Load chunks in a 3x3 grid centered at (0, 0)
initial_chunks = [
    (0, 0), (1, 0), (1, -1), (0, -1), (-1, -1),
    (-1, 0), (-1, 1), (0, 1), (1, 1)
]
for chunk_pos in initial_chunks:
    chunk_manager.load_chunk(chunk_pos)

# Camera position (center of screen)
camera_position = [0, 0]  # This represents the world coordinates at the center of the screen

screen_centre = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
mammoths[0] = Mammoth(screen_centre, True)
populate_mammoths(20)

# Main game loop
running = True
clock = pygame.time.Clock()

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
    chunk_manager.render(screen, camera_position, screen_center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    
    sorted_mammoths = sort_mammoths()
    for mammoth_id in sorted_mammoths:
        screen.blit(mammoths[mammoth_id].get_image(), mammoths[mammoth_id].position + mammoths[mammoth_id].size/2 - camera_position)

    handle_actors()

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    dt = clock.tick(FPS) / 1000

# Quit Pygame
pygame.quit()
