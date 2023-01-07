import pygame
import pytmx

class Map:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f'data/maps/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tilesize = self.map.tilewidth

    def render(self, group):
        for y in range(self.height):
            for x in range(self.width):
                # image = self.map.get_tile_image(x, y, 0)
                # screen.blit(image, (x * self.tilesize, y * self.tilesize))
                tile = pygame.sprite.Sprite(group)
                tile.image = self.map.get_tile_image(x, y, 0)
                tile.rect = tile.image.get_rect()
                tile.rect.x = x * self.tilesize
                tile.rect.y = y * self.tilesize

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]