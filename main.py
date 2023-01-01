import pygame
import os
import sys
from music_player import MusicPlayer
from animated_sprite import AnimatedSprite

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
start_sprites = pygame.sprite.Group()
hero_sprites = pygame.sprite.Group()

settings = {
    'music_volume': 1,
    'sounds_volume': 1,
    'difficulty': 'normal',
}


def terminate():
    pygame.quit()
    sys.exit()


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
        # тут заменяем текстуру на error
        # в случае если картинка не найдена
        image = pygame.image.load(error_image)
        return image


def start_screen():
    start_image = load_image('start_background.png')
    start_screen_1 = pygame.sprite.Sprite(start_sprites)
    start_screen_1.image = start_image
    start_screen_1.rect = start_screen_1.image.get_rect()
    start_screen_1.rect.x = 0
    start_screen_1.rect.y = 0

    start_screen_2 = pygame.sprite.Sprite(start_sprites)
    start_screen_2.image = start_image
    start_screen_2.rect = start_screen_2.image.get_rect()
    start_screen_2.rect.x = 2180
    start_screen_2.rect.y = 0

    filler_image = pygame.transform.scale(load_image('tiles/pink_filler_tile.png'), (1100, 32))
    filler = pygame.sprite.Sprite(start_sprites)
    filler.image = filler_image
    filler.rect = filler.image.get_rect()
    filler.rect.x = 0
    filler.rect.y = 568

    top_tile_image = pygame.transform.scale(load_image('tiles/pink_top_tile.png'), (1100, 32))
    top_tile = pygame.sprite.Sprite(start_sprites)
    top_tile.image = top_tile_image
    top_tile.rect = top_tile.image.get_rect()
    top_tile.rect.x = 0
    top_tile.rect.y = 538

    start_screen_alice = AnimatedSprite(start_sprites, start_sprites, \
        pygame.transform.scale(load_image('alice/moving_D_fix.png'), (450, 165)), 4, 1, 910, 400)
    pressed_start = False

    while True:
        screen.fill('white')
        start_sprites.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pressed_start = True

        # движение фона стартового экрана
        if start_screen_1.rect.x > -2180 and not pressed_start:
            start_screen_1.rect.x -= 1
        elif not pressed_start:
            start_screen_1.rect.x += 2180
        if start_screen_2.rect.x > 0 and not pressed_start:
            start_screen_2.rect.x -= 1
        elif not pressed_start:
            start_screen_2.rect.x += 2180

        if not pressed_start:
            pass
        else:
            if start_screen_alice.rect.x < 1130:
                start_screen_alice.rect.x += 3
            else:
                return

        start_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
while True:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.switch_track('Loqiemean - Мартышка и технологии.mp3')
            player.play()
    pygame.display.flip()
    clock.tick(FPS)