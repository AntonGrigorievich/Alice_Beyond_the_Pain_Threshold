import pygame
from config import load_image, all_sprites, mob_group, hero_sprites


class MobNear(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("mob/enemy_near/enemy_stay.png"), (100, 100))

    def __init__(self, x, y, hero):
        super().__init__(mob_group, all_sprites)
        self.image = MobNear.image
        self.mask = pygame.mask.from_surface(self.image)
        self.hp = 5
        self.speed = 2.5
        self.x, self.y = x, y
        self.character = hero
        self.is_alive = True
        self.is_free = True
        self.direction = 'a'
        self.dist = 150

        self.frames_run_left = []
        self.frames_run_count_left = 0
        self.run_left = 'mob/enemy_near/enemy_move.png'
        sheet_run = pygame.transform.scale(load_image(self.run_left), (600, 100))
        self.cut_sheet(pygame.transform.flip(sheet_run, True, False), 6, 1, self.frames_run_left)

        self.frames_run_right = []
        self.frames_run_count_right = 0
        self.run_right = 'mob/enemy_near/enemy_move.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.run_right), (600, 100)), 6, 1, self.frames_run_right)

        self.frames_attack_right = []
        self.frames_attack_right_count = 0
        self.attack_right = 'mob/enemy_near/enemy_attack_right.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.attack_right), (1100, 100)), 11, 1,
                       self.frames_attack_right)

        self.frames_attack_left = []
        self.frames_attack_left_count = 0
        self.attack_left = 'mob/enemy_near/enemy_attack_left.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.attack_left), (1100, 100)), 11, 1,
                       self.frames_attack_left)

        self.frames_death_right = []
        self.frames_death_right_count = 0
        self.death_right = 'mob/enemy_near/enemy_death.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.death_right), (1900, 100)), 19, 1,
                       self.frames_death_right)

        self.frames_death_left = []
        self.frames_death_left_count = 0
        self.death_left = 'mob/enemy_near/enemy_death.png'
        sheet_death_left = pygame.transform.scale(load_image(self.death_left), (1900, 100))
        self.cut_sheet(pygame.transform.flip(sheet_death_left, True, False), 19, 1, self.frames_death_left)

        self.frames_idle_left = []
        self.frames_idle_count_left = 0
        self.idle_left = 'mob/enemy_near/enemy_idle.png'
        sheet_idle = pygame.transform.scale(load_image(self.idle_left), (900, 100))
        self.cut_sheet(pygame.transform.flip(sheet_idle, True, False), 9, 1, self.frames_idle_left)

        self.frames_idle_right = []
        self.frames_idle_count_right = 0
        self.idle_right = 'mob/enemy_near/enemy_idle.png'
        self.cut_sheet(pygame.transform.scale(load_image(self.idle_right), (900, 100)), 9, 1, self.frames_idle_right)

    def cut_sheet(self, sheet, columns, rows, frames):
        self.rect = pygame.Rect(self.x, self.y, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def animated_move(self, frames_run_count, frames_run):
        frames_run_count = (frames_run_count + 1) % len(frames_run)
        self.image = frames_run[frames_run_count]
        return frames_run_count, frames_run

    def get_damage(self, hp):
        self.hp -= hp
        if self.hp <= 0:
            self.is_alive = False
            if self.direction == 'd':
                self.frames_death_right_count, self.frames_death_right = self.animated_move(
                    self.frames_death_right_count, self.frames_death_right)
            elif self.direction == 'a':
                self.frames_death_left_count, self.frames_death_left = self.animated_move(
                    self.frames_death_left_count, self.frames_death_left)

    def attack(self):
        if pygame.sprite.spritecollideany(self, hero_sprites) and self.is_alive:
            if self.direction == 'a':
                self.frames_attack_left_count, self.frames_attack_left = self.animated_move(
                    self.frames_attack_left_count, self.frames_attack_left)
            elif self.direction == 'd':
                self.frames_attack_right_count, self.frames_attack_right = self.animated_move(
                    self.frames_attack_right_count, self.frames_attack_right)

    def idle(self):
        if self.is_free:
            if self.direction == 'a':
                self.frames_idle_count_left, self.frames_idle_left = self.animated_move(
                    self.frames_idle_count_left, self.frames_idle_left)
            elif self.direction == 'd':
                self.frames_idle_count_right, self.frames_idle_right = self.animated_move(
                    self.frames_idle_count_right, self.frames_idle_right)

    def move(self):
        pos = self.character.get_rect_center()
        if self.is_alive:
            if abs(self.rect.centerx - pos[0]) < self.dist and abs(self.rect.centery - pos[1]) < self.dist:
                self.is_free = False
                if self.rect.centerx != pos[0] and self.rect.centery != pos[1]:
                    if self.rect.centerx > pos[0] and self.rect.centery > pos[1]:
                        self.direction = 'a'
                        self.frames_run_count_left, self.frames_run_left = self.animated_move(
                            self.frames_run_count_left,
                            self.frames_run_left)
                        self.rect.centerx -= self.speed
                        self.rect.centery -= self.speed
                    elif self.rect.centerx < pos[0] and self.rect.centery < pos[1]:
                        self.direction = 'd'
                        self.frames_run_count_right, self.frames_run_right = self.animated_move(
                            self.frames_run_count_right,
                            self.frames_run_right)
                        self.rect.centerx += self.speed
                        self.rect.centery += self.speed
                    elif self.rect.centerx < pos[0] and self.rect.centery > pos[1]:
                        self.direction = 'd'
                        self.frames_run_count_right, self.frames_run_right = self.animated_move(
                            self.frames_run_count_right,
                            self.frames_run_right)
                        self.rect.centerx += self.speed
                        self.rect.centery -= self.speed
                    elif self.rect.centerx > pos[0] and self.rect.centery < pos[1]:
                        self.direction = 'a'
                        self.frames_run_count_left, self.frames_run_left = self.animated_move(
                            self.frames_run_count_left,
                            self.frames_run_left)
                        self.rect.centerx -= self.speed
                        self.rect.centery += self.speed

                elif self.rect.centery != pos[1]:
                    if self.rect.centery < pos[1]:
                        self.frames_run_count_right, self.frames_run_right = self.animated_move(
                            self.frames_run_count_right,
                            self.frames_run_right)
                        self.rect.centery += self.speed

                    elif self.rect.centery > pos[1]:
                        self.frames_run_count_right, self.frames_run_right = self.animated_move(
                            self.frames_run_count_right,
                            self.frames_run_right)
                        self.rect.centery -= self.speed

                elif self.rect.centerx != pos[0]:
                    if self.rect.centerx < pos[0]:
                        self.direction = 'd'
                        self.rect.centerx += self.speed
                        self.frames_run_count_right, self.frames_run_right = self.animated_move(
                            self.frames_run_count_right,
                            self.frames_run_right)
                    elif self.rect.centerx > pos[0]:
                        self.direction = 'a'
                        self.rect.centerx -= self.speed
                        self.frames_run_count_left, self.frames_run_left = self.animated_move(
                            self.frames_run_count_left,
                            self.frames_run_left)
            else:
                self.is_free = True

    def update(self, *args, **kwargs):
        self.idle()
        self.move()
        self.attack()