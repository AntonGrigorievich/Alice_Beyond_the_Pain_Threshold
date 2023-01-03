import pygame
from config import load_image


class Coursor(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Coursor.image
        self.rect = self.image.get_rect()

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            self.rect.x = args[0].pos[0]
            self.rect.y = args[0].pos[1]
