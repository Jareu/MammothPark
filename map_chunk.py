# map_chunk.py

from tile import Tile
from settings import CHUNK_SIZE, TILE_SIZE

class MapChunk:
    def __init__(self, position, noise_generator, texture_manager):
        self.position = position
        self.noise_generator = noise_generator
        self.texture_manager = texture_manager
        self.tiles = self.generate_tiles()

    def generate_tiles(self):
        noise_parameters = {
            'scale': 10.0,
            'octaves': 2,
            'persistence': 0.3,
            'lacunarity': 5.0
        }

        # Generate noise for the entire chunk
        noise_array = self.noise_generator.generate_chunk_noise(self.position, noise_parameters)

        tiles = []
        for i in range(CHUNK_SIZE):
            row = []
            for j in range(CHUNK_SIZE):
                noise_value = noise_array[i, j]
                tile_type = self.determine_tile_type(noise_value)
                tile = Tile(tile_type, (i, j), self.texture_manager)
                row.append(tile)
            tiles.append(row)

        return tiles
    
    def determine_tile_type(self, noise_value):
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
