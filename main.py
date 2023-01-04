import pygame
import os
import time
import sys
from music_player import MusicPlayer
from animated_sprite import AnimatedSprite
from coursor import Coursor
from player import Hero
from map import Map
from config import size, load_image, all_sprites, start_sprites, hero_sprites


pygame.mixer.pre_init(44000, -16, 1, 512)
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Beyond')
pygame.mouse.set_visible(False)

FPS = 30
clock = pygame.time.Clock()
# Говно получилось ☹︎
# либо иначе записать либо готовую музыку брать
player = MusicPlayer('where.mp3')

settings = {
    'music_volume': 1,
    'sounds_volume': 1,
    'difficulty': 'normal',
}


def terminate():
    pygame.quit()
    sys.exit()


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
                                        pygame.transform.scale(load_image('alice/moving_D.png'), (450, 165)), 4, 1, 910,
                                        400)
    pressed_start = False

    font = pygame.font.Font('data/fonts/orange kid.ttf', 20)
    text = font.render('press any key', True, '#ffffff')

    curs = Coursor(start_sprites)

    while True:
        screen.fill('white')
        start_sprites.draw(screen)
        if not pressed_start:
            screen.blit(text, (40, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                curs.update(event)
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pressed_start = True
                pygame.mixer.Sound('data/sounds/click.wav').play()

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
                player.pause()
                return

        start_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
map = Map('test_map.tmx')
character = Hero((100, 100))
curs = Coursor(all_sprites)
last_move = 0
while True:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            character.sleepy = True
        elif event.type == pygame.MOUSEMOTION:
            curs.update(event)
        elif event.type == pygame.KEYDOWN:
            last_move = time.time()

    if time.time() - last_move >= 5:
        character.sleepy = True
    else:
        character.sleepy = False

    map.render(screen)
    all_sprites.draw(screen)
    all_sprites.update()

    pygame.display.flip()
    clock.tick(FPS)
