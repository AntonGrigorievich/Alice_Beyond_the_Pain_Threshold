import pygame
import os
from music_player import MusicPlayer

pygame.mixer.pre_init(44000, -16, 1, 512)
pygame.init()

size = width, height = 1100, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Beyond')
FPS = 30
clock = pygame.time.Clock()
tile_width = tile_height = 50
player = MusicPlayer('Loqiemean - Вайолентово.mp3')

all_sprites = pygame.sprite.Group()

settings = {
    'music_volume': 1,
    'sounds_volume': 1,
    'difficulty' : 'normal',
}

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    error_image = ''
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
        #тут заменяем текстуру на error
        #в случае если картинка не найдена
        image = pygame.image.load(error_image)
        return image


running = True
while running:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()