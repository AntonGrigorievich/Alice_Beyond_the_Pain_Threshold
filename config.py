import sys

import pygame
import os

# сюда заносим все что может понадобиться одновременно в main и других классах
# для того чтобы избежать ошибки импорта

size = width, height = 1100, 600
tile_width = tile_height = 50

all_sprites = pygame.sprite.Group()
start_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
coursor_group = pygame.sprite.Group()
mob_group = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image
