# tile.py
from settings import TILE_SIZE, CHUNK_SIZE

class Tile:
    def __init__(self, tile_type, position, texture_manager):
        self.tile_type = tile_type
        self.position = position
        self.texture_manager = texture_manager

    def render(self, surface, chunk_position, camera_position, screen_center):
        # Calculate the world position
        chunk_x, chunk_y = chunk_position
        tile_x, tile_y = self.position
        world_x = (chunk_x * CHUNK_SIZE + tile_x) * TILE_SIZE
        world_y = (chunk_y * CHUNK_SIZE + tile_y) * TILE_SIZE
    
        # Calculate the screen position
        screen_x = world_x - camera_position[0] + screen_center[0]
        screen_y = world_y - camera_position[1] + screen_center[1]
    
        # Get the texture based on tile type and variation
        texture = self.texture_manager.get_texture(self.tile_type)
    
        # Draw the tile's texture
        surface.blit(texture, (screen_x, screen_y))