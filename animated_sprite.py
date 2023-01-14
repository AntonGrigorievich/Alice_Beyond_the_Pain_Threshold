import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, group, all_sprites, sheet, columns, rows, x, y, speed):
        super().__init__(group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.speed = speed

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, *args):
        # +0.5 чтобы анимацию сделать медленнее (int(1,5) = 1)
        self.cur_frame = (self.cur_frame + self.speed) % len(self.frames)
        self.image = self.frames[int(self.cur_frame)]
