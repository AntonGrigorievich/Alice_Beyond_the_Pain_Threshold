import pygame
import os

class MusicPlayer:
    def __init__(self, filename):
        pygame.mixer.music.load(os.path.join('data/music', filename))

    def play(self, start_point):
        pygame.mixer.music.play(-1, start_point, 1)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

    def switch_track(self, new_filename):
        pygame.mixer.music.stop()
        self.music = pygame.mixer.music.load(os.path.join('data/music', new_filename))