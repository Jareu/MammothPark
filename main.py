# main.py

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PLAYER_SPEED, TILE_SIZE
from chunk_manager import ChunkManager
from noise_generator import NoiseGenerator  # Import the NoiseGenerator class

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

def get_camera_chunk_position(camera_position):
    """Calculate the chunk position based on the camera's pixel position."""
    return camera_position[0] // (32 * TILE_SIZE), camera_position[1] // (32 * TILE_SIZE)

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

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
