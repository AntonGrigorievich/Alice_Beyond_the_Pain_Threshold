import pygame
import pytmx
from config import all_sprites
from tile import Tile

class Map:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f'data/maps/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tilesize = self.map.tilewidth

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                # image = self.map.get_tile_image(x, y, 0)
                # screen.blit(image, (x * self.tilesize, y * self.tilesize))
                tile = pygame.sprite.Sprite(all_sprites)
                tile.image = self.map.get_tile_image(x, y, 0)
                tile.rect = tile.image.get_rect()
                tile.rect.move(
                    x * self.tilesize, y * self.tilesize
                )
                tile

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]