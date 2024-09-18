from enum import Enum
from settings import TILE_SIZE

class Variation(Enum):
    OuterBottomLeft = 1
    OuterLeft = 2
    OuterTopLeft = 3
    OuterTop = 4
    OuterTopRight = 5
    OuterRight = 6
    OuterBottomRight = 7
    OuterBottom = 8
    InnerBottomLeft = 9
    InnerLeft = 10
    InnerTopLeft = 11
    InnerTop = 12
    InnerTopRight = 13
    InnerRight = 14
    InnerBottomRight = 14
    InnerBottom = 15
    Main = 16

class Textures:
    texture_offsets = {
        Variation.OuterBottomLeft: (0, 96),
        Variation.OuterLeft: (0, 48),
        Variation.OuterTopLeft: (0, 0),
        Variation.OuterTop: (48, 0),
        Variation.OuterTopRight: (96, 0),
        Variation.OuterRight: (96, 48),
        Variation.OuterBottomRight: (96, 96),
        Variation.OuterBottom: (48, 96),
        Variation.InnerBottomLeft: (0, 96),
        Variation.InnerLeft: (0, 192),
        Variation.InnerTopLeft: (0, 144),
        Variation.InnerTop: (48, 144),
        Variation.InnerTopRight: (96, 144),
        Variation.InnerRight: (96, 192),
        Variation.InnerBottomRight: (96, 240),
        Variation.InnerBottom: (48, 240),
        Variation.Main: (48, 192)
    }

    def __init__(self, spritesheet):
        grass_coords = (48, 48)
        mud_coords = (1008, 432)

        self.grass = {}
        self.mud = {}

        for pos in Variation:
            self.grass[pos] = spritesheet.image_at(
                (grass_coords[0] + self.texture_offsets[pos][0], grass_coords[1] + self.texture_offsets[pos][1], TILE_SIZE, TILE_SIZE),
                (0, 0, 0)
            )

            self.mud[pos] = spritesheet.image_at(
                (mud_coords[0] + self.texture_offsets[pos][0], mud_coords[1] + self.texture_offsets[pos][1], TILE_SIZE, TILE_SIZE),
                (0, 0, 0)
            )