# tile.py
from settings import TILE_SIZE, CHUNK_SIZE

class Tile:
    def __init__(self, tile_type, position, texture_manager):
        self.tile_type = tile_type
        self.position = position
        self.pixel_position = (position[0] * TILE_SIZE, position[1] * TILE_SIZE)
        self.texture_manager = texture_manager
        self.items = []

    def render(self, surface, screen_offset):
        # Calculate the world position
        screen_x = self.pixel_position[0] + screen_offset[0]
        screen_y = self.pixel_position[1] + screen_offset[1]

        # Get the texture based on tile type and variation
        texture = self.texture_manager.get_texture(self.tile_type)
    
        # Draw the tile's texture
        surface.blit(texture, (screen_x, screen_y))
        
        for item in self.items:
            item.render(surface, screen_offset)