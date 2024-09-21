# map_chunk.py

from settings import CHUNK_SIZE, TILE_SIZE
from tile import Tile
from tile_variation import TileVariation
from tile_type import TileType
from side import Side
import pygame

class MapChunk:
    def __init__(self, position, noise_generator, texture_manager, chunk_manager):
        self.position = position
        self.noise_generator = noise_generator
        self.texture_manager = texture_manager
        self.chunk_manager = chunk_manager  # Reference to ChunkManager to access neighbouring chunks
        self.get_neighbouring_chunks()
        self.tiles = self.generate_tiles()
        self.display_tiles = self.generate_display_tiles()
        self.regen_neighbours()
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.text = self.font.render('[' + str(position[0]) + ',' + str(position[1]) + ']', True, (255,255,0))
        self.text_rect = self.text.get_rect()

    def regen_neighbours(self):
        for neighbour in self.neighbours:
            if neighbour is None:
                print('Chunk ' + str(neighbour[0]) + ', ' + str(neighbour[1]) + 'is null')

        for side, neighbour in neighbours_pos.items():
            with self.chunk_lock:
                if neighbour in self.loaded_chunks:
                    self.loaded_chunks[neighbour].regenerate_edge_display_tiles(side)
                else:
                    print('neighbour ' + str(neighbour) + ' not found in ' + str(list(self.loaded_chunks.keys())))

    def get_neighbouring_chunks(self):
        self.neighbours = {}
        self.neighbours[(-1, 0)] = self.chunk_manager.get_chunk(self.position + (-1, 0)) # Left
        self.neighbours[(-1, -1)]= self.chunk_manager.get_chunk(self.position + (-1, -1)) # Top Left
        self.neighbours[(0, -1)] = self.chunk_manager.get_chunk(self.position + (0, -1)) # Top

        for neighbour in self.neighbours:
            neighbour.regenerate_edge_display_tiles(side)

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

    def regenerate_edge_display_tiles(self, side):
        self.get_neighbouring_chunks()
        last_tile = CHUNK_SIZE-1

        if side == (0,-1):
            #print('Regenerating top side')
            for x in range(CHUNK_SIZE):
                tile = self.tiles[x][0]
                self.display_tiles[x][0] = self.determine_display_tile(tile.tile_type, x, 0)

        elif side == Side.Bottom:
            #print('Regenerating bottom side')
            for x in range(CHUNK_SIZE):
                tile = self.tiles[x][last_tile]
                self.display_tiles[x][last_tile] = self.determine_display_tile(tile.tile_type, x, last_tile)

        elif side == Side.Left:
            #print('Regenerating left side')
            for y in range(CHUNK_SIZE):
                tile = self.tiles[0][y]
                self.display_tiles[0][y] = self.determine_display_tile(tile.tile_type, 0, y)
    
        elif side == Side.Right:
            #print('Regenerating right side')
            for y in range(CHUNK_SIZE):
                tile = self.tiles[last_tile][y]
                self.display_tiles[last_tile][y] = self.determine_display_tile(tile.tile_type, last_tile, y)

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
            chunk_offset = (x // CHUNK_SIZE, y // CHUNK_SIZE)
            neighbour_chunk = self.neighbours[chunk_offset]

            if neighbour_chunk:
                neighbour_tile = neighbour_chunk.tiles[local_pos[0]][local_pos[1]]

                if (self.position[0] == -1 and self.position[1] == 0):
                    print('x: ' + str(x) + ' y: ' + str(y) + ' ' + str(neighbour_tile.tile_type) + ' chunk_offset: ' + str(chunk_offset))

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