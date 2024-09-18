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
        self.noise = OpenSimplex(seed)
        self.default_parameters =  {'scale': 100.0, 'octaves': 1, 'persistence': 0.5, 'lacunarity': 2.0}

    def generate_chunk_noise(self, chunk_position, noise_parameters = None):
        chunk_x, chunk_y = chunk_position
        if noise_parameters is None:
            noise_parameters = self.default_parameters

        # Create grid of coordinates
        x_indices = np.arange(CHUNK_SIZE)
        y_indices = np.arange(CHUNK_SIZE)
        x_grid, y_grid = np.meshgrid(x_indices, y_indices, indexing='ij')

        # Convert to world coordinates
        world_x = (chunk_x * CHUNK_SIZE + x_grid) / noise_parameters['scale']
        world_y = (chunk_y * CHUNK_SIZE + y_grid) / noise_parameters['scale']

        # Generate noise for the entire chunk
        noise_values = self._generate_octave_noise(world_x, world_y, noise_parameters)
        return noise_values
    
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
        noise_value = np.zeros_like(x)
        frequency = 1.0
        amplitude = 1.0
        max_value = 0.0

        for _ in range(parameters['octaves']):
            nx = x * frequency
            ny = y * frequency
            noise_value += self.vectorized_noise2d(nx, ny) * amplitude
            max_value += amplitude
            amplitude *= parameters['persistence']
            frequency *= parameters['lacunarity']

        return noise_value / max_value
    
    def vectorized_noise2d(self, x, y):
        # Vectorized noise function using NumPy arrays
        flat_x = x.flatten()
        flat_y = y.flatten()
        noise_values = np.array([self.noise.noise2(ix, iy) for ix, iy in zip(flat_x, flat_y)])
        return noise_values.reshape(x.shape)