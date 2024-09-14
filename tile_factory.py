# tile_factory.py

from grass_tile import GrassTile
from mud_tile import MudTile
from noise_generator import NoiseGenerator

class TileFactory:
    grass_threshold = -0.2

    def __init__(self, noise_generator):
        self.noise_generator = noise_generator

    def create_tile(self, chunk_position, tile_position, noise_parameters):
        """
        Create a tile based on the noise value at the given position.

        :param chunk_position: (x, y) tuple indicating the chunk's world position.
        :param tile_x: X coordinate of the tile within the chunk.
        :param tile_y: Y coordinate of the tile within the chunk.
        :param noise_parameters: Parameters for the noise generator.
        :return: A tile instance (e.g., GrassTile, MudTile).
        """

        # Generate noise value for the tile's position
        noise_value = self.noise_generator.generate_tile_noise(chunk_position, tile_position, noise_parameters)

        # Determine the type of tile based on noise value
        if noise_value > self.grass_threshold:
            return GrassTile()
        else:
            return MudTile()
