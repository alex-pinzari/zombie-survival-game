import pygame
from utils import load_image, gunshot_sound, dmg_sound, SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        raw = {
            'idle':   ['ply1'],
            'walk':   ['plw1','plw2'],
            'shoot':  ['plsh'],
            'damage': ['pldmg']
        }
        self.animations = {}
        for state, names in raw.items():
            self.animations[state] = []
            for name in names:
                img = load_image(name)
                w, h = img.get_size()
                self.animations[state].append(pygame.transform.scale(img, (w//2, h//2)))
        self.sounds = {'shoot': gunshot_sound, 'damage': dmg_sound}
        self.state = 'idle'
        self.frame = 0
        self.image = self.animations['idle'][0]
        self.rect  = self.image.get_rect(topleft=pos)
        hit_w = int(self.rect.width * 0.8)
        hit_h = int(self.rect.height * 0.8)
        self.hitbox = pygame.Rect(0, 0, hit_w, hit_h)
        self.hitbox.center = self.rect.center
        self.anim_timer   = 0
        self.anim_speed   = 150
        self.immune       = False
        self.immune_timer = 0
        self.immune_dur   = 700
        self.hearts       = 3
        self.coins        = 0
        self.speed        = 5
        self.start_x      = pos[0]
        self.shoot_cd     = 500
        self.shoot_timer  = self.shoot_cd
        self.fired        = False

    def update(self, dt, in_shop=False):
        if self.immune:
            self.immune_timer += dt
            if self.immune_timer >= self.immune_dur:
                self.immune       = False
                self.immune_timer = 0

        keys = pygame.key.get_pressed()
        dx = dy = 0
        shoot_anim = False
        self.fired = False

        if keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_s]: dy = self.speed
        if keys[pygame.K_d]: dx = self.speed
        elif keys[pygame.K_a] and self.rect.x > self.start_x:
            dx = -self.speed

        self.rect.x += dx
        self.rect.y += dy

        if not in_shop:
            min_y = 288 - self.rect.height
            self.rect.y = max(min_y, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        else:
            self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))

        if keys[pygame.K_SPACE]: shoot_anim = True
        self.shoot_timer += dt
        if shoot_anim and self.shoot_timer >= self.shoot_cd:
            self.sounds['shoot'].play()
            self.fired = True
            self.shoot_timer = 0

        self.hitbox.center = self.rect.center

        new_state = 'idle'
        if shoot_anim:
            new_state = 'shoot'
        elif dx or dy:
            new_state = 'walk'
        if new_state != self.state:
            self.state = new_state
            self.frame = 0
            self.anim_timer = 0

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
        if not self.immune:
            self.hearts -= 1
            self.immune = True
            self.sounds['damage'].play()
            self.state = 'damage'
            self.frame = 0
            self.anim_timer = 0
