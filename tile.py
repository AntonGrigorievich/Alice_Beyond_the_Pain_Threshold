import pygame
from config import all_sprites, load_image, \
    tile_height, tile_width

class Tile(pygame.sprite.Sprite):
    tile_images = {

    }

    def __init__(self, pos_x, pos_y, group):
        super.__init__(group, all_sprites)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y
        )