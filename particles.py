import pygame
from config import width, height, all_sprites, load_image
import random


screen_rect = (0, 0, width, height)


class Particle(pygame.sprite.Sprite):
    #класс немного отличается от того что в учебнике
    #чтобы использовать разные картинки запрашиваем particle_image
    def __init__(self, pos, dx, dy, particle_image):
        super().__init__(all_sprites)
        image_set = [load_image(particle_image)]
        for scale in (5, 10, 20):
            image_set.append(pygame.transform.scale(image_set[0], (scale, scale)))
        
        self.image = random.choice(image_set)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        
    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        #уничтожается только при вылете за экран.
        #позже стоит добавить еще какие-то исключения
        if (not self.rect.colliderect(screen_rect)):
            self.kill()


def create_particles(position, count, image):
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(count):
        Particle(position, random.choice(numbers), random.choice(numbers), image)