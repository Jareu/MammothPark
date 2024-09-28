# map_chunk.py

from settings import CHUNK_SIZE, TILE_SIZE, DEBUG
from tile import Tile
from enums import TileVariation
from enums import TileType
from enums import Side
import pygame

class MapChunk:
    def __init__(self, position, noise_generator, texture_manager, chunk_manager):
        self.position = position
        self.pixel_position = (self.position[0] * CHUNK_SIZE * TILE_SIZE, self.position[1] * CHUNK_SIZE * TILE_SIZE)
        self.noise_generator = noise_generator
        self.texture_manager = texture_manager
        self.chunk_manager = chunk_manager  # Reference to ChunkManager to access neighbouring chunks
        self.tiles = self.generate_tiles()
        self.display_tiles = self.generate_display_tiles()

        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.text = self.font.render('[' + str(position[0]) + ',' + str(position[1]) + ']', True, (255,255,0))
        self.text_rect = self.text.get_rect()

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
    
    def regenerate_edges(self):
        for i in range(CHUNK_SIZE):
            for j in [0, CHUNK_SIZE-1]:
                # Top and Bottom
                tile = self.tiles[i][j]
                display_tile = self.determine_display_tile(tile.tile_type, i, j)
                self.display_tiles[i][j] = display_tile

                # Left and Right
                if(i > 0 and i < CHUNK_SIZE-1): # (skipping top and bottom tiles)
                    tile = self.tiles[j][i]
                    display_tile = self.determine_display_tile(tile.tile_type, j, i)
                    self.display_tiles[j][i] = display_tile

    def determine_display_tile(self, type, i, j):
        # Get the types of neighbouring tiles
        display_tile = 0b1000 * (type == TileType.Grass)

        directions = {
            0b0001: (i - 1, j - 1), # Top Left
            0b0010: (i, j - 1), # Top Right
            0b0100: (i - 1, j), # Bottom Left
        }

        for direction, (x, y) in directions.items():
            neighbour_tile_type = self.get_neighbour_tile_type(x, y)
            display_tile += direction * (neighbour_tile_type == TileType.Grass)

        return display_tile
    
    def get_neighbour_tile_type(self, x, y):
        # Check if the neighbour is within the current chunk
        if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE:
            return self.tiles[x][y].tile_type
        else:
            # Neighbour is in another chunk
            neighbour_chunk_pos, local_pos = self.get_neighbour_chunk_and_local_pos(x, y)
            neighbour_chunk = self.chunk_manager.get_chunk(neighbour_chunk_pos)

            if neighbour_chunk:
                neighbour_tile = neighbour_chunk.tiles[local_pos[0]][local_pos[1]]
                return neighbour_tile.tile_type
            else:
                # print('Neightbour chunk ' + str(neighbour_chunk_pos[0]) +  ', ' + str(neighbour_chunk_pos[1]) + ' doesn\'t exist for chunk ' + str (self.position))
                # Default to a tile type (e.g., Grass or Dirt)
                return TileType.Grass  # Adjust as needed    

    def get_neighbour_chunk_and_local_pos(self, x, y):
        # Calculate chunk position and local position for out-of-bounds coordinates
        chunk_offset = (x // CHUNK_SIZE, y // CHUNK_SIZE)
        local_x = x % CHUNK_SIZE
        local_y = y % CHUNK_SIZE
        neighbour_chunk_pos = (self.position[0] + chunk_offset[0] , self.position[1] + chunk_offset[1])
        return neighbour_chunk_pos, (local_x, local_y)

    def render(self, surface, camera_position, screen_center):
        # Render all tiles in this chunk
        screen_offset_x = self.pixel_position[0] - camera_position[0] + screen_center[0]
        screen_offset_y = self.pixel_position[1] - camera_position[1] + screen_center[1]

        for i in range(CHUNK_SIZE):
            for j in range(CHUNK_SIZE):
                # Calculate screen position relative to camera's centered position
                # render dirt layer
                # use display_tiles to render grass layer somehow
                # render tile graphics on top
                
                world_tile = self.tiles[i][j]
                display_tile = self.display_tiles[i][j]

                if world_tile.tile_type == TileType.Dirt:
                    world_tile.render(surface, (screen_offset_x, screen_offset_y))

                if display_tile == 0:
                    continue

                world_x = self.pixel_position[0] + (i - 0.5) * TILE_SIZE
                world_y = self.pixel_position[1] + (j - 0.5) * TILE_SIZE
            
                # Calculate the screen position
                screen_x = world_x - camera_position[0] + screen_center[0]
                screen_y = world_y - camera_position[1] + screen_center[1]
                texture = self.texture_manager.get_texture(TileType.Grass, TileVariation(display_tile))
                surface.blit(texture, (screen_x, screen_y))

        if (DEBUG == True):
            chunk_length = CHUNK_SIZE * TILE_SIZE
            x1 = self.position[0] * chunk_length - camera_position[0] + screen_center[0]
            x2 = (self.position[0]+1) * chunk_length - camera_position[0] + screen_center[0]
            y1 = self.position[1] * chunk_length - camera_position[1] + screen_center[1]
            y2 = (self.position[1]+1) * chunk_length - camera_position[1] + screen_center[1]

            chunk_lines = [(x2, y1), (x1, y1), (x1, y2)]

            pygame.draw.aalines(surface, (255, 255, 0), False, chunk_lines)
            self.text_rect.x = x1 + TILE_SIZE / 2
            self.text_rect.y = y1 + TILE_SIZE / 2
            surface.blit(self.text, self.text_rect)