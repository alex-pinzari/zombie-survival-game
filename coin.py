import pygame
from utils import _coin_image

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = _coin_image
        self.rect  = self.image.get_rect(center=pos)
