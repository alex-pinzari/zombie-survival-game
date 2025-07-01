# utils.py
"""
Utility / shared-state module for the zombie-shooter game.
Everything that the other modules need (constants, screen,
clock, asset-loaders, global sounds & images, helper funcs)
lives here so it is defined exactly once.
"""

import pygame
import os

# ────────────────────────────────
#  Pygame init & global objects
# ────────────────────────────────
pygame.init()

# ---------- constants ----------
SCREEN_WIDTH  = 1200
SCREEN_HEIGHT = 700
FPS           = 60

SHOP_ZONE_X      = (460, 965)
SHOP_RIGHT_EDGE  = 870
SHOP_ENTER_Y     = 540

# ---------- core objects ----------
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock  = pygame.time.Clock()
font   = pygame.font.Font(None, 36)

# ────────────────────────────────
#  Asset-caching helpers
# ────────────────────────────────
_image_cache: dict[str, pygame.Surface] = {}
_sound_cache: dict[str, pygame.mixer.Sound] = {}


def load_image(name: str) -> pygame.Surface:
    """Load an image from assets/<name>.png with caching + safe fallback."""
    if name not in _image_cache:
        try:
            path = os.path.join("assets", f"{name}.png")
            _image_cache[name] = pygame.image.load(path).convert_alpha()
        except pygame.error:
            print(f"[WARN] Missing image {name}.png – using placeholder.")
            _image_cache[name] = pygame.Surface((50, 50))
    return _image_cache[name]


def load_sound(name: str) -> pygame.mixer.Sound:
    """Load a wav sound from assets/<name>.wav with caching + silent fallback."""
    if name not in _sound_cache:
        try:
            path = os.path.join("assets", f"{name}.wav")
            _sound_cache[name] = pygame.mixer.Sound(path)
        except pygame.error:
            print(f"[WARN] Missing sound {name}.wav – using dummy sound.")
            _sound_cache[name] = pygame.mixer.Sound(file=None)
    return _sound_cache[name]


# ────────────────────────────────
#  Pre-load frequently-used assets
# ────────────────────────────────
zombi_sound   = load_sound("zombi_sound")
dmg_sound     = load_sound("dmg_sound")
gunshot_sound = load_sound("gunshot_sound")
cling_sound   = load_sound("cling")

_heart_image  = pygame.transform.rotozoom(load_image("heart"),   0, 0.2)
_coin_image   = pygame.transform.rotozoom(load_image("bitcoin"), 0, 0.2)

bg_regular = load_image("bg")
bg_ex      = load_image("bg_ex")
shop_bg    = load_image("shop")


# ────────────────────────────────
#  Helper UI
# ────────────────────────────────
def game_over_screen() -> None:
    """Fades to GAME OVER, waits 3 s."""
    screen.fill((0, 0, 0))
    txt = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2,
                      SCREEN_HEIGHT // 2 - txt.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
