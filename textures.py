from settings import TILE_SIZE

class Textures:

    def __init__(self, spritesheet):
        grass_texture_x = 88
        grass_texture_y = 232
        self.grass = spritesheet.image_at((grass_texture_x, grass_texture_y, TILE_SIZE, TILE_SIZE), (0, 0, 0))

        mud_texture_x = 664
        mud_texture_y = 232
        self.mud = spritesheet.image_at((mud_texture_x, mud_texture_y, TILE_SIZE, TILE_SIZE), (0, 0, 0))