# map_chunk.py

from tile import Tile
from tile_factory import TileFactory
from settings import CHUNK_SIZE, TILE_SIZE
from textures import Variation

class MapChunk:
    def __init__(self, position, noise_generator, texture_manager):
        self.position = position  # (x, y) coordinates for the chunk
        self.noise_generator = noise_generator
        self.texture_manager = texture_manager
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
                tile_type = self.determine_tile_type((i, j), noise_parameters)
                tile = Tile(tile_type, (i, j), self.texture_manager)
                row.append(tile)
            tiles.append(row)

        return tiles
    
    def determine_tile_type(self, tile_position, noise_parameters):
        noise_value = self.noise_generator.generate_tile_noise(self.position, tile_position, noise_parameters)
        if noise_value > -0.2:
            return 'grass'
        else:
            return 'mud'
        
    def render(self, surface, camera_position, screen_center):
        # Render all tiles in this chunk
        for row in self.tiles:
            for tile in row:
                # Calculate screen position relative to camera's centered position
                tile.render(surface, self.position, camera_position, screen_center)
