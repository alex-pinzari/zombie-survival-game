import pygame
from utils import SCREEN_WIDTH

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 4))         # Yellow rectangle
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.speed = 12

    def update(self, dt):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
