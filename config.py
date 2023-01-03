import pygame
import os

# сюда заносим все что может понадобиться одновременно в main и других классах
# для того чтобы избежать ошибки импорта

size = width, height = 1100, 600
tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
block_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    error_image = 'data/arrow.png'
    try:
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image
    except Exception:
        # тут заменяем текстуру на error
        # в случае если картинка не найдена
        image = pygame.image.load(error_image)
        return image
