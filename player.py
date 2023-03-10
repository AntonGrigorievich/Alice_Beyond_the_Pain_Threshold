import pygame
import time
from config import load_image, all_sprites, hero_sprites, block_group, weapon_group, aid_group
from animated_sprite import AnimatedSprite


class Hero(pygame.sprite.Sprite):
    # 37x56
    image = pygame.transform.scale(load_image("alice/stay_S.png"), (100, 116))
    image_d = pygame.transform.scale(load_image("alice/stay_D.png"), (74, 110))
    image_a = pygame.transform.scale(load_image("alice/stay_A.png"), (74, 112))
    image_w = pygame.transform.scale(load_image("alice/stay_W.png"), (100, 116))
    image_s = pygame.transform.scale(load_image("alice/stay_S.png"), (100, 116))

    def __init__(self, position, screen):
        super().__init__(hero_sprites, all_sprites)
        # self.map = map
        # self.map_size = self.map.get_size_map()
        self.size = (37, 56)
        self.health = 10
        self.speed = 10
        self.killcount = 0
        self.direction = 's'
        self.idle()
        self.timer = 0
        self.x, self.y = position
        self.time_alive = time.time()
        self.is_alive = True
        self.sleepy = False
        self.damaged = False
        self.attacking = False
        self.bash = None
        self.win = screen

        self.frames_run_down = []
        self.frames_run_count_down = 0
        self.run_down = 'alice/moving_S.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.run_down), (400, 116)), 4, 1, self.frames_run_down)

        self.frames_run_left = []
        self.frames_run_count_left = 0
        self.run_left = 'alice/moving_A.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.run_left), (300, 112)), 4, 1, self.frames_run_left)

        self.frames_run_right = []
        self.frames_run_count_right = 0
        self.run_right = 'alice/moving_D.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.run_right), (300, 112)), 4, 1, self.frames_run_right)

        self.frames_run_up = []
        self.frames_run_count_up = 0
        self.run_up = 'alice/moving_W.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.run_up), (400, 116)), 4, 1, self.frames_run_up)

        self.frames_falling_asleep = []
        self.frames_falling_asleep_count = 0
        self.falling_asleep = 'alice/sleep/falling_asleep.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.falling_asleep), (520, 116)), 5, 1,
                       self.frames_falling_asleep)

        self.frames_sleeping = []
        self.frames_sleeping_count = 0
        self.sleeping = 'alice/sleep/sleeping.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.sleeping), (312, 116)), 3, 1, self.frames_sleeping)

        self.frames_hurt_right = []
        self.frames_hurt_right_count = 0
        self.hurt_right = 'alice/hurt_D.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.hurt_right), (152, 112)), 2, 1, self.frames_hurt_right)

        self.frames_hurt_left = []
        self.frames_hurt_left_count = 0
        self.hurt_left = 'alice/hurt_A.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.hurt_left), (152, 112)), 2, 1, self.frames_hurt_left)

        self.frames_hurt_down = []
        self.frames_hurt_down_count = 0
        self.hurt_down = 'alice/hurt_S.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.hurt_down), (196, 116)), 2, 1, self.frames_hurt_down)

        self.frames_hurt_up = []
        self.frames_hurt_up_count = 0
        self.hurt_up = 'alice/hurt_W.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.hurt_up), (196, 116)), 2, 1, self.frames_hurt_up)

    def cut_sheet(self, sheet, columns, rows, frames):
        self.rect = pygame.Rect(self.x, self.y, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def idle(self):
        if self.direction == 'd':
            self.image = Hero.image_d
        elif self.direction == 'a':
            self.image = Hero.image_a
        elif self.direction == 'w':
            self.image = Hero.image_w
        elif self.direction == 's':
            self.image = Hero.image_s

    def get_rect_center(self):
        return self.rect.center

    def animated_move(self, frames_run_count, frames_run):
        frames_run_count = (frames_run_count + 1) % len(frames_run)
        self.image = frames_run[frames_run_count]
        return frames_run_count, frames_run

    def get_direction(self):
        return self.direction

    def move(self):
        pygame.draw.rect(self.win, (255, 0, 0), (self.rect.centerx - 25, self.rect.y - 20, 50, 10))
        pygame.draw.rect(self.win, (0, 128, 0),
                         (self.rect.centerx - 25, self.rect.y - 20, 50 - (5 * (10 - self.health)), 10))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and keys[pygame.K_w]:
            self.direction = 'dw'
            self.frames_run_count_up, self.frames_run_up = self.animated_move(self.frames_run_count_up,
                                                                              self.frames_run_up)
            self.rect.x += self.speed
            self.rect.y -= self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.x -= self.speed
                self.rect.y += self.speed

        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.direction = 'ds'
            self.frames_run_count_down, self.frames_run_down = self.animated_move(self.frames_run_count_down,
                                                                                  self.frames_run_down)
            self.rect.x += self.speed
            self.rect.y += self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.x -= self.speed
                self.rect.y -= self.speed

        elif keys[pygame.K_a] and keys[pygame.K_w]:
            self.direction = 'aw'
            self.frames_run_count_down, self.frames_run_up = self.animated_move(self.frames_run_count_down,
                                                                                self.frames_run_up)
            self.rect.x -= self.speed
            self.rect.y -= self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.x += self.speed
                self.rect.y += self.speed

        elif keys[pygame.K_a] and keys[pygame.K_s]:
            self.direction = 'as'
            self.frames_run_count_down, self.frames_run_down = self.animated_move(self.frames_run_count_down,
                                                                                  self.frames_run_down)
            self.rect.x -= self.speed
            self.rect.y += self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.x += self.speed
                self.rect.y -= self.speed

        elif keys[pygame.K_d]:
            self.direction = 'd'
            self.frames_run_count_right, self.frames_run_right = self.animated_move(self.frames_run_count_right,
                                                                                    self.frames_run_right)
            self.rect.x += self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.x -= self.speed

        elif keys[pygame.K_a]:
            self.direction = 'a'
            self.frames_run_count_left, self.frames_run_left = self.animated_move(self.frames_run_count_left,
                                                                                  self.frames_run_left)
            self.rect.x -= self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.x += self.speed

        elif keys[pygame.K_w]:
            self.direction = 'w'
            self.frames_run_count_up, self.frames_run_up = self.animated_move(self.frames_run_count_up,
                                                                              self.frames_run_up)
            self.rect.y -= self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.y += self.speed

        elif keys[pygame.K_s]:
            self.direction = 's'
            self.frames_run_count_down, self.frames_run_down = self.animated_move(self.frames_run_count_down,
                                                                                  self.frames_run_down)
            self.rect.y += self.speed
            if pygame.sprite.spritecollideany(self, block_group):
                self.rect.y -= self.speed

    def attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_l]:
            # self.frames_attack_right_count, self.frames_attack_right = self.animated_move(
            #     self.frames_attack_right_count,
            #     self.frames_attack_right)
            if not self.bash:
                self.attacking = True
                self.bash = AnimatedSprite(weapon_group, all_sprites,
                                           pygame.transform.scale(load_image('alice/attack_D.png'), (760, 110)),
                                           3, 1, 520, 240, 0.8)
                hero_sprites.add(self.bash)
                all_sprites.remove(self.bash)

        elif keys[pygame.K_j]:
            if not self.bash:
                self.attacking = True
                self.bash = AnimatedSprite(weapon_group, all_sprites,
                                           pygame.transform.scale(load_image('alice/attack_A.png'), (760, 110)),
                                           3, 1, 390, 265, 0.8)
                hero_sprites.add(self.bash)
                all_sprites.remove(self.bash)

        elif keys[pygame.K_i]:
            if not self.bash:
                self.attacking = True
                self.bash = AnimatedSprite(weapon_group, all_sprites,
                                           pygame.transform.scale(load_image('alice/attack_W.png'), (300, 200)),
                                           3, 1, 500, 130, 0.8)
                hero_sprites.add(self.bash)
                all_sprites.remove(self.bash)

        elif keys[pygame.K_k]:
            if not self.bash:
                self.attacking = True
                self.bash = AnimatedSprite(weapon_group, all_sprites,
                                           pygame.transform.scale(load_image('alice/attack_S.png'), (300, 200)),
                                           3, 1, 500, 230, 0.8)
                hero_sprites.add(self.bash)
                all_sprites.remove(self.bash)

    def get_damage(self):
        self.health -= 1
        pygame.mixer.Sound('data/sounds/hurt.wav').play()
        if self.direction == 'd':
            self.frames_hurt_right_count, self.frames_hurt_right = self.animated_move(self.frames_hurt_right_count,
                                                                                      self.frames_hurt_right)
        elif self.direction == 'a':
            self.frames_hurt_left_count, self.frames_hurt_left = self.animated_move(self.frames_hurt_left_count,
                                                                                    self.frames_hurt_left)
        elif self.direction == 's':
            self.frames_hurt_down_count, self.frames_hurt_down = self.animated_move(self.frames_hurt_down_count,
                                                                                    self.frames_hurt_down)
        elif self.direction == 'w':
            self.frames_hurt_up_count, self.frames_hurt_up = self.animated_move(self.frames_hurt_up_count,
                                                                                self.frames_hurt_up)

    def fall_sleep(self):
        if self.direction == 's':
            self.frames_falling_asleep_count, self.frames_falling_asleep = self.animated_move(
                self.frames_falling_asleep_count,
                self.frames_falling_asleep)

    def sleep(self):
        if self.direction == 's':
            self.frames_sleeping_count, self.frames_sleeping = self.animated_move(self.frames_sleeping_count,
                                                                                  self.frames_sleeping)

    def update(self, *args, **kwargs):
        self.idle()
        self.move()
        self.attack()
        if self.sleepy:
            self.fall_sleep()
            self.sleep()
        if self.damaged:
            self.damaged = False
            self.get_damage()
        if self.attacking:
            if self.bash.cur_frame >= 6:
                self.bash.kill()
                self.attacking = False
                self.bash = False
        if self.health <= 0:
            self.is_alive = False
        if pygame.sprite.spritecollideany(self, aid_group):
            self.health += 1