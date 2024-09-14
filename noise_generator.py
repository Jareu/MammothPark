# noise_generator.py

from settings import CHUNK_SIZE
from opensimplex import OpenSimplex
import numpy as np

class NoiseGenerator:
    def __init__(self, seed=0):
        """
        Initialize the NoiseGenerator with parameters for generating terrain noise.

        :param seed: Seed for the noise function to ensure reproducibility.
        :param scale: Scale of the noise, affecting the frequency of features.
        :param octaves: Number of layers of noise to combine for complexity.
        :param persistence: Controls the amplitude of each octave.
        :param lacunarity: Controls the frequency of each octave.
        """
        self.seed = seed
        self.default_parameters =  {'scale': 100.0, 'octaves': 1, 'persistence': 0.5, 'lacunarity': 2.0}
        self.noise = OpenSimplex(seed=self.seed)

    def generate_chunk_noise(self, chunk_position, noise_parameters = None):
        """
        Generate a 2D array of noise values for a specific chunk.

        :param chunk_position: (x, y) tuple indicating the chunk's world position.
        :return: 2D numpy array of noise values representing terrain heights.
        """
        chunk_x, chunk_y = chunk_position
        noise_array = np.zeros((CHUNK_SIZE, CHUNK_SIZE))

        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                # Convert local chunk coordinates to world coordinates
                world_x = (chunk_x * CHUNK_SIZE + i) / noise_parameters['scale']
                world_y = (chunk_y * CHUNK_SIZE + j) / noise_parameters['scale']

                # Generate OpenSimplex noise value for the current world coordinate
                noise_value = self._generate_octave_noise(world_x, world_y, self.default_parameters if noise_parameters is None else noise_parameters)
                
                # Store the noise value in the array
                noise_array[i][j] = noise_value

        return noise_array
    
    def generate_tile_noise(self, chunk_position, tile_position, noise_parameters = None):
        """
        Generate a 2D array of noise values for a specific chunk.

        :param chunk_position: (x, y) tuple indicating the chunk's world position.
        :return: 2D numpy array of noise values representing terrain heights.
        """
        chunk_x, chunk_y = chunk_position
        tile_x, tile_y = tile_position

        # Convert local chunk coordinates to world coordinates
        world_x = (chunk_x * CHUNK_SIZE + tile_x) / noise_parameters['scale']
        world_y = (chunk_y * CHUNK_SIZE + tile_y) / noise_parameters['scale']

        # Generate OpenSimplex noise value for the current world coordinate
        noise_value = self._generate_octave_noise(world_x, world_y, self.default_parameters if noise_parameters is None else noise_parameters)
        
        return noise_value
    
    def _generate_octave_noise(self, x, y, parameters):
        """
        Generate noise value using multiple octaves for more complex terrain.

        :param x: X coordinate in world space.
        :param y: Y coordinate in world space.
        :return: Noise value with octaves applied.
        """
        noise_value = 0
        frequency = 1
        amplitude = 1
        max_value = 0  # Used for normalizing the result to the range [-1, 1]

        for _ in range(parameters['octaves']):
            noise_value += self.noise.noise2(x * frequency, y * frequency) * amplitude
            max_value += amplitude
            amplitude *= parameters['persistence']
            frequency *= parameters['lacunarity']

        return noise_value / max_value
