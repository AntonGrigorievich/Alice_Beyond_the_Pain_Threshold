import pygame
import random
import time
import sys
from music_player import MusicPlayer
from animated_sprite import AnimatedSprite
from camera import Camera
from coursor import Coursor
from player import Hero
from map import Map
from config import size, load_image, all_sprites, start_sprites, hero_sprites, coursor_group, mob_group, block_group, \
    weapon_group, end_sprites
from mob_near import MobNear

pygame.mixer.pre_init(44000, -16, 1, 512)
pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Beyond')
pygame.mouse.set_visible(False)

FPS = 30
clock = pygame.time.Clock()

start_screen_songs_set = [
    'temperatura',
    'plenka',
    'Descend',
    'On the Run',
]
songs_start_point = {
    'temperatura.mp3': 16.0,
    'plenka.mp3': 4.0,
    'Descend.mp3': 0.0,
    'On the Run.mp3': 0.0,
}
track = f'{random.choice(start_screen_songs_set)}.mp3'
player = MusicPlayer(track)


def terminate():
    pygame.quit()
    sys.exit()


def end_screen():
    end_image = pygame.transform.scale(load_image('AI_background.png'), (1100, 1024))
    end_screen = pygame.sprite.Sprite(end_sprites)
    end_screen.image = end_image
    end_screen.rect = end_screen.image.get_rect()
    end_screen.rect.x = 0
    end_screen.rect.y = -200

    curs = Coursor(end_sprites)

    player.set_volume(0.5)
    player.switch_track('Whos Ready for Tomorrow.mp3')
    player.play(0.0)

    font_1 = pygame.font.Font('data/fonts/orange kid.ttf', 85)
    font_2 = pygame.font.Font('data/fonts/orange kid.ttf', 45)
    font_3 = pygame.font.Font('data/fonts/orange kid.ttf', 30)

    game_over_sign = font_1.render('GAME OVER', True, '#ffffff')
    killcount_sign = font_2.render(f"YOU'VE TAKEN {character.killcount} LIVES", True, '#ffffff')
    time_alive_sign = font_3.render(f"AND LIVED FOR {(time.time() - character.time_alive) // 60} MINUTES", True, '#ffffff')
    restart_sign = font_3.render('PRESS ANY KEY TO RESTART', True, '#ffffff')

    while True:
        screen.fill('white')
        end_sprites.draw(screen)
        screen.blit(game_over_sign, (395, 50))
        screen.blit(killcount_sign, (395, 130))
        screen.blit(time_alive_sign, (410, 180))
        screen.blit(restart_sign, (410, 560))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                curs.update(event)
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound('data/sounds/click.wav').play()
                player.switch_track(track)
                player.play(songs_start_point[track])
                infinite_round()

        end_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


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
                                        400, 0.5)
    pressed_start = False

    font = pygame.font.Font('data/fonts/orange kid.ttf', 20)
    text = font.render('press any key', True, '#ffffff')

    curs = Coursor(start_sprites)

    player.set_volume(0.5)
    player.play(songs_start_point[track])

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
                player.switch_track('TheOnlyThingTheyFearIsYou.mp3')
                return

        start_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)


def pause(screen, message):
    font = pygame.font.Font('data/fonts/orange kid.ttf', 80)
    text = font.render(message, True, ('#C74DFF'))
    text_2 = font.render(message, True, ('#40E3E2'))
    text_x = size[0] // 2 - text.get_width() // 2
    text_y = size[1] // 2 - text.get_height() // 2

    s = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
    s.fill((128, 128, 128, 200))
    screen.blit(s, (0, 0))

    screen.blit(text, (text_x, text_y))
    screen.blit(text_2, (text_x + 3, text_y + 3))


def infinite_round():
    start_screen()

    character = Hero((100, 100), screen)

    for i in range(7):
        lst_enemy.append(MobNear(10, 200 * i, character, screen))
    for i in range(7):
        lst_enemy.append(MobNear(1300, 200 * i, character, screen))
    for i in range(1, 6):
        lst_enemy.append(MobNear(200 * i, 10, character, screen))
    for i in range(1, 6):
        lst_enemy.append(MobNear(200 * i, 1300, character, screen))

    curs = Coursor(coursor_group)
    camera = Camera()

    font = pygame.font.Font('data/fonts/orange kid.ttf', 15)
    subject_sign = font.render('Kill as much as you can', True, '#ffffff')
    controls_sign = font.render('use WASD to move and IJKL to fight', True, '#ffffff')

    infinite_map.render(all_sprites, block_group)
    last_wave = time.time()

    last_move = 0
    player.set_volume(0.5)
    player.play(17.0)
    run = True
    while True:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(len(lst_enemy), character.killcount)
            elif event.type == pygame.MOUSEMOTION:
                curs.update(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if run:
                        last_wave = time.time() + 120
                        player.set_volume(0.05)
                    else:
                        last_wave = time.time() - 120 
                        player.set_volume(0.1)
                    run = not run
                last_move = time.time()

        if time.time() - last_move >= 5:
            character.sleepy = True
        else:
            character.sleepy = False

        if time.time() - last_wave >= 10:
            spawn_enemies(lst_enemy, character, screen)
            last_wave = time.time()

        if not character.is_alive:
            character.kill()
            curs.kill()
            for enemy in lst_enemy:
                enemy.kill()
            for sprite in all_sprites:
                sprite.kill()
            end_screen()

        all_sprites.draw(screen)
        mob_group.draw(screen)
        hero_sprites.draw(screen)
        weapon_group.draw(screen)
        coursor_group.draw(screen)
        screen.blit(subject_sign, (900, 10))
        screen.blit(controls_sign, (900, 30))
        if run:
            all_sprites.update()
            weapon_group.update(screen)
            camera.update(character)
            for sprite in all_sprites:
                camera.apply(sprite)
        else:
            pause(screen, 'Pause')

        pygame.display.flip()
        clock.tick(FPS)


start_screen()


infinite_map = Map('infinite_round_map.tmx')  # (200, 70)•(860, 420)

lst_enemy = []
character = Hero((100, 100), screen)

def spawn_enemies(enemy_list, charachter, screen):
    for _ in range(7):
        enemy_list.append(MobNear(random.randrange(-700, 700), random.randrange(-700, 700), charachter, screen))

for i in range(2, 7):
    lst_enemy.append(MobNear(10, 200 * i, character, screen))
for i in range(7):
    lst_enemy.append(MobNear(1300, 200 * i, character, screen))
for i in range(2, 6):
    lst_enemy.append(MobNear(200 * i, 10, character, screen))
for i in range(1, 6):
    lst_enemy.append(MobNear(200 * i, 1300, character, screen))

curs = Coursor(coursor_group)
camera = Camera()

font = pygame.font.Font('data/fonts/orange kid.ttf', 15)
subject_sign = font.render('Kill as much as you can', True, '#ffffff')
controls_sign = font.render('use WASD to move and IJKL to fight', True, '#ffffff')

infinite_map.render(all_sprites, block_group)
last_wave = time.time()

last_move = 0
player.set_volume(0.5)
player.play(17.0)
run = True
while True:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(len(lst_enemy), character.killcount)
        elif event.type == pygame.MOUSEMOTION:
            curs.update(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if run:
                    last_wave = time.time() + 120
                    player.set_volume(0.05)
                else:
                    last_wave = time.time() - 120 
                    player.set_volume(0.1)
                run = not run
            last_move = time.time()

    if time.time() - last_move >= 5:
        character.sleepy = True
    else:
        character.sleepy = False

    if time.time() - last_wave >= 10:
        spawn_enemies(lst_enemy, character, screen)
        last_wave = time.time()

    if not character.is_alive:
        curs.kill()
        character.kill()
        for enemy in lst_enemy:
            enemy.kill()
        for sprite in all_sprites:
            sprite.kill()
        end_screen()

    all_sprites.draw(screen)
    mob_group.draw(screen)
    hero_sprites.draw(screen)
    weapon_group.draw(screen)
    coursor_group.draw(screen)
    screen.blit(subject_sign, (900, 10))
    screen.blit(controls_sign, (900, 30))
    if run:
        all_sprites.update()
        weapon_group.update(screen)
        camera.update(character)
        for sprite in all_sprites:
            camera.apply(sprite)
    else:
        pause(screen, 'Pause')

    pygame.display.flip()
    clock.tick(FPS)
