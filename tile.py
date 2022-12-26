import pygame
from main import load_image, all_sprites, \
    tile_height, tile_width

class Tile(pygame.sprite.Sprite):
    tile_images = {

    }

    def __init__(self, tile_type, pos_x, pos_y, group):
        super.__init__(group, all_sprites)
        self.image = Tile.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y
        )