import pygame
import os

class MusicPlayer:
    def __init__(self, filename):
        self.music = pygame.mixer.music.load(os.path.join('data/music', filename))

    def play(self):
        self.music.play(-1, 0.0, 1)

    def pause(self):
        self.music.pause()

    def unpause(self):
        self.music.unpause()

    def set_volume(self, volume):
        self.music.set_volume(volume)

    def switch_track(self, new_filename):
        self.music.stop()
        self.music = pygame.mixer.music.load(os.path.join('data/music', new_filename))