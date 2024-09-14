# map_chunk.py

from tile_factory import TileFactory
from settings import CHUNK_SIZE, TILE_SIZE

class MapChunk:
    def __init__(self, position, noise_generator):
        self.position = position  # (x, y) coordinates for the chunk
        self.noise_generator = noise_generator
        self.tile_factory = TileFactory(noise_generator)  # Initialize TileFactory with noise generator
        self.tiles = self.generate_tiles()

    def generate_tiles(self):
        # Define noise parameters for this chunk

        noise_parameters = {
            'scale': 10.0,
            'octaves': 2,
            'persistence': 0.3,
            'lacunarity': 5.0
        }

        # Generate tiles for this chunk using the TileFactory
        tiles = []
        for i in range(CHUNK_SIZE):
            row = []
            for j in range(CHUNK_SIZE):
                tile = self.tile_factory.create_tile(self.position, (i, j), noise_parameters)
                row.append(tile)
            tiles.append(row)

        return tiles

    def render(self, surface, camera_position, screen_center):
        # Render all tiles in this chunk
        chunk_x, chunk_y = self.position
        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                # Calculate screen position relative to camera's centered position
                screen_x = (chunk_x * CHUNK_SIZE + i) * TILE_SIZE - camera_position[0] + screen_center[0]
                screen_y = (chunk_y * CHUNK_SIZE + j) * TILE_SIZE - camera_position[1] + screen_center[1]
                self.tiles[i][j].render(surface, screen_x, screen_y)
