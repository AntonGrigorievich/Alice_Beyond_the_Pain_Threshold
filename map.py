import pygame
import pytmx

class Map:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f'data/maps/{filename}')
        self.height = self.map.height
        self.width = self.map.width
        self.tilesize = self.map.tilewidth

    def render(self, group, block_group):
        walls_id = [1, 9, 13]
        for y in range(self.height):
            for x in range(self.width):
                tile = pygame.sprite.Sprite()
                tile.image = self.map.get_tile_image(x, y, 0)
                tile.rect = tile.image.get_rect()
                tile.rect.x = x * self.tilesize
                tile.rect.y = y * self.tilesize
                group.add(tile)
                if self.map.tiledgidmap[self.map.get_tile_gid(x, y, 0)] in walls_id:
                    block_group.add(tile)

    def get_tile_id(self, pos):
        return self.map.tiledgidmap[self.map.get_tile_gid(*pos, 0)]