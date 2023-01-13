import math

import pygame
from config import load_image, all_sprites, mob_group


# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, hero, char, direction):
#         super().__init__(all_sprites)
#         self.speed = 5
#         self.char, self.direction = char, direction
#         self.hero = hero
#         self.image = pygame.transform.scale(load_image("mob/enemy_far/enemy_bullet.png"), (19, 7))
#         # self.rect = pygame.Rect(self.char[0], self.char[1], 19, 7)
#         self.rect = self.image.get_rect(center=(self.char[0], self.char[1]))
#         # self.mask = pygame.mask.from_surface(self.image)
#         self.rect.centerx = self.char[0]
#         self.rect.centery = self.char[1]
#
#     def get_direction(self):
#         pos = self.hero.get_rect_center()
#         if self.rect.centerx != pos[0] and self.rect.centery != pos[1]:
#             if self.rect.centerx > pos[0] and self.rect.centery > pos[1]:
#                 self.direction = 'aw'
#             elif self.rect.centerx < pos[0] and self.rect.centery < pos[1]:
#                 self.direction = 'ds'
#             elif self.rect.centerx < pos[0] and self.rect.centery > pos[1]:
#                 self.direction = 'dw'
#             elif self.rect.centerx > pos[0] and self.rect.centery < pos[1]:
#                 self.direction = 'as'
#         elif self.rect.centery != pos[1]:
#             if self.rect.centery < pos[1]:
#                 self.direction = 's'
#             elif self.rect.centery > pos[1]:
#                 self.direction = 'w'
#         elif self.rect.centerx != pos[0]:
#             if self.rect.centerx < pos[0]:
#                 self.direction = 'd'
#             elif self.rect.centerx > pos[0]:
#                 self.direction = 'a'
#
#     def move(self):
#         pos = self.hero.get_rect_center()
#         x1, y1, x2, y2 = pos[0], pos[1], self.rect.centerx, self.rect.centery
#         print(self.direction)
#         # if self.direction == 'aw':
#         #     a = -1
#         #     k = abs(y2 - y1) / abs(x2 - x1) * a
#         #     b = y1 - x1 * k
#         #     self.rect.centerx -= self.speed
#         #     self.rect.centery -= k * self.speed + b
#         # elif self.direction == 'ds':
#         #     a = -1
#         #     k = abs(y2 - y1) / abs(x2 - x1) * a
#         #     b = y1 - x1 * k
#         #     self.rect.centerx += self.speed
#         #     self.rect.centery += k * self.speed + b
#         # elif self.direction == 'dw':
#         #     a = 1
#         #     k = abs(y2 - y1) / abs(x2 - x1) * a
#         #     b = y1 - x1 * k
#         #     self.rect.centerx += self.speed
#         #     self.rect.centery -= k * self.speed + b
#         # elif self.direction == 'as':
#         #     a = 1
#         #     k = abs(y2 - y1) / abs(x2 - x1) * a
#         #     b = y1 - x1 * k
#         #     self.rect.centerx -= self.speed
#         #     self.rect.centery += k * self.speed + b
#         if self.direction == 's':
#             self.rect.centery += self.speed
#         elif self.direction == 'w':
#             self.rect.centery -= self.speed
#         elif self.direction == 'd':
#             self.rect.centerx += self.speed
#         elif self.direction == 'a':
#             self.rect.centerx -= self.speed
#
#     def update(self):
#         self.get_direction()
#         self.move()
#
#     # if self.direction == 'd':
#     #     self.rect.centerx += self.speed
#     # if self.direction == 'a':
#     #     self.rect.centerx -= self.speed
#     # if self.direction == 'w':
#     #     self.rect.centery -= self.speed
#     # if self.direction == 's':
#     #     self.rect.centery += self.speed
#
#     # for mob in pygame.sprite.spritecollide(self, mob_group, dokill=False):
#     #     mob.get_damage(10)
#     #     self.kill()
#     # if pygame.sprite.spritecollideany(self, block_group):
#     #     self.kill()

# class Bullet(pygame.sprite.Sprite):
#     def __init__(self, hero, char):
#         super().__init__(all_sprites)
#         self.char = char
#         self.hero = hero
#         self.image = pygame.transform.scale(load_image("mob/enemy_far/enemy_bullet.png"), (19, 7))
#         self.rect = self.image.get_rect(center=(self.char[0], self.char[1]))
#         self.start = pygame.math.Vector2(self.rect.center)
#         self.end = self.start
#         self.speed = 5
#         self.all_bullets = []
#
#     def move(self):
#
#         mouse = self.hero.get_rect_center()
#         distance = mouse - self.start
#         position = pygame.math.Vector2(self.start)
#         speed = distance.normalize() * self.speed
#         self.all_bullets.append([position, speed])
#         print(self.all_bullets)
#         for position, speed in self.all_bullets:
#             position += speed
#             pos_x = int(position.x)
#             pos_y = int(position.y)
#             # self.rect.centerx = pos_x
#             self.rect.move(pos_x,pos_y)
#             # self.rect.centery = pos_y
#
#     def update(self):
#         self.move()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, end_x, end_y):
        super().__init__(all_sprites)
        self.pos = (start_x, start_y)
        mx, my = end_x, end_y
        self.dir = (mx - start_x, my - start_y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        # self.bullet = pygame.Surface((7, 2)).convert_alpha()
        # self.bullet.fill((255, 255, 255))
        # self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.image = pygame.transform.scale(load_image("mob/enemy_far/enemy_bullet.png"), (19, 7))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 2

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed,
                    self.pos[1] + self.dir[1] * self.speed)

    def draw(self, surf):
        rect = self.image.get_rect(center=self.pos)
        surf.blit(self.image, rect)



