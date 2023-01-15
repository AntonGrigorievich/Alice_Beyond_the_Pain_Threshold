import pygame
import random
from config import load_image, all_sprites, aid_group, hero_sprites

class AidKit(pygame.sprite.Sprite):
    images = [
        'bread.png', 'giantgummybear.png', 
        'gingerbreadman.png', 'loafbread.png',
        'sandwich.png', 'sushi.png'
    ]

    def __init__(self, x, y):
        super().__init__(all_sprites, aid_group)
        self.image = load_image(f'food/{random.choice(AidKit.images)}')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args, **kwargs):
        if pygame.sprite.spritecollideany(self, hero_sprites):
            pygame.mixer.Sound('data/sounds/eat.wav').play()
            self.kill()