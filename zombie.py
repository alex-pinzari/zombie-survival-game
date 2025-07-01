import pygame
from utils import load_image, SCREEN_HEIGHT

class Zombie(pygame.sprite.Sprite):
    def __init__(self, pos, health=1):
        super().__init__()
        raw = {
            'walk':   ['z_walk1','z_walk2'],
            'damage': ['z_dmg'],
            'attack': ['z_attack']
        }
        self.animations = {}
        for state, names in raw.items():
            self.animations[state] = []
            for name in names:
                img = load_image(name)
                w, h = img.get_size()
                self.animations[state].append(pygame.transform.scale(img, (w//2, h//2)))
        self.state = 'walk'
        self.frame = 0
        self.image = self.animations['walk'][0]
        self.rect  = self.image.get_rect(topleft=pos)
        hw = int(self.rect.width * 0.8)
        hh = int(self.rect.height * 0.8)
        self.hitbox = pygame.Rect(0, 0, hw, hh)
        self.hitbox.center = self.rect.center
        self.anim_timer = 0
        self.anim_speed = 200
        self.speed      = 2
        self.health     = health
        self.max_health = health

    def update(self, dt):
        self.rect.x -= self.speed
        min_y = 288 - self.rect.height
        self.rect.y = max(min_y, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        self.hitbox.center = self.rect.center
        self.anim_timer += dt
        frames = self.animations[self.state]
        if self.anim_timer >= self.anim_speed:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(frames)
        cx, cy = self.hitbox.center
        self.image = frames[self.frame]
        self.rect  = self.image.get_rect(center=(cx, cy))
        self.hitbox.center = self.rect.center

    def take_damage(self):
        self.health -= 1
        if self.health <= (self.max_health / 2):
            self.state = 'damage'
            self.frame = 0
            self.anim_timer = 0
