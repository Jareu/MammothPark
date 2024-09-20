# map_chunk.py

from settings import CHUNK_SIZE, TILE_SIZE
from tile import Tile
from tile_variation import TileVariation
from tile_type import TileType


class MapChunk:
    def __init__(self, position, noise_generator, texture_manager, chunk_manager):
        self.position = position
        self.noise_generator = noise_generator
        self.texture_manager = texture_manager
        self.chunk_manager = chunk_manager  # Reference to ChunkManager to access neighboring chunks
        self.tiles = self.generate_tiles()
        self.display_tiles = self.generate_display_tiles()
    
    def generate_tiles(self):
        # Generate noise and create tiles as before
        noise_array = self.noise_generator.generate_chunk_noise(self.position)
        tiles = []
        for i in range(CHUNK_SIZE):
            row = []
            for j in range(CHUNK_SIZE):
                noise_value = noise_array[i, j]
                tile_type = self.determine_tile_type(noise_value)
                tile_position = (i, j)
                tile = Tile(tile_type, tile_position, self.texture_manager)
                row.append(tile)
            tiles.append(row)
        return tiles
    
    def determine_tile_type(self, noise_value):
        # Define your thresholds
        if noise_value > -0.2:
            return TileType.Grass
        else:
            return TileType.Dirt
    
    def generate_display_tiles(self):
        display_tiles = []

        for i in range(CHUNK_SIZE):
            row = []
            for j in range(CHUNK_SIZE):
                tile = self.tiles[i][j]
                display_tile = self.determine_display_tile(tile.tile_type, i, j)
                row.append(display_tile)
            display_tiles.append(row)
        return display_tiles
    
    def determine_display_tile(self, type, i, j):
        # Get the types of neighboring tiles
        display_tile = 0b1000 * (type == TileType.Grass)

        directions = {
            0b0001: (i - 1, j - 1), # Top Left
            0b0010: (i, j - 1), # Top Right
            0b0100: (i - 1, j), # Bottom Left
        }

        for direction, (x, y) in directions.items():
            neighbor_tile_type = self.get_neighbor_tile_type(x, y)
            display_tile += direction * (neighbor_tile_type == TileType.Grass)

        return display_tile
    
    def get_neighbor_tile_type(self, x, y):
        # Check if the neighbor is within the current chunk
        if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE:
            return self.tiles[x][y].tile_type
        else:
            # Neighbor is in another chunk
            neighbor_chunk_pos, local_pos = self.get_neighbor_chunk_and_local_pos(x, y)
            neighbor_chunk = self.chunk_manager.get_chunk(neighbor_chunk_pos)

            if neighbor_chunk:
                neighbor_tile = neighbor_chunk.tiles[local_pos[0]][local_pos[1]]
                return neighbor_tile.tile_type
            else:
                # Default to a tile type (e.g., Grass or Dirt)
                return TileType.Grass  # Adjust as needed    

    def get_neighbor_chunk_and_local_pos(self, x, y):
        # Calculate chunk position and local position for out-of-bounds coordinates
        chunk_offset_x = x // CHUNK_SIZE
        chunk_offset_y = y // CHUNK_SIZE
        local_x = x % CHUNK_SIZE
        local_y = y % CHUNK_SIZE
        neighbor_chunk_pos = (self.position[0] + chunk_offset_x, self.position[1] + chunk_offset_y)
        return neighbor_chunk_pos, (local_x, local_y)

    def render(self, surface, camera_position, screen_center):
        # Render all tiles in this chunk

        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                # Calculate screen position relative to camera's centered position
                # render dirt layer
                # use display_tiles to render grass layer somehow
                # render tile graphics on top
                
                world_tile = self.tiles[i][j]
                display_tile = self.display_tiles[i][j]

                if world_tile.tile_type == TileType.Dirt:
                    world_tile.render(surface, self.position, camera_position, screen_center)

                if display_tile == 0:
                    continue

                world_x = (self.position[0] * CHUNK_SIZE + i) * TILE_SIZE - TILE_SIZE * 0.5
                world_y = (self.position[1] * CHUNK_SIZE + j) * TILE_SIZE - TILE_SIZE * 0.5
            
                # Calculate the screen position
                screen_x = world_x - camera_position[0] + screen_center[0]
                screen_y = world_y - camera_position[1] + screen_center[1]
                texture = self.texture_manager.get_texture(TileType.Grass, TileVariation(display_tile))
                surface.blit(texture, (screen_x, screen_y))