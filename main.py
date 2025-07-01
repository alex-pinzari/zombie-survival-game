import sys
import pygame
import random

from utils import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
    SHOP_ZONE_X, SHOP_RIGHT_EDGE, SHOP_ENTER_Y,
    screen, clock, font,
    bg_regular, bg_ex, shop_bg,
    _heart_image, _coin_image,
    zombi_sound, cling_sound, game_over_screen
)

from player import Player
from zombie import Zombie
from bullet import Bullet
from coin   import Coin

# Game loop
def main():
    player   = Player((100, SCREEN_HEIGHT // 2))
    bullets  = pygame.sprite.Group()
    zombies  = pygame.sprite.Group()
    coins    = pygame.sprite.Group()
    pgroup   = pygame.sprite.GroupSingle(player)

    level  = 1
    spawn  = 5
    bg_idx = 0

    in_shop      = False
    prev_pos     = (0, 0)
    prev_bg      = 0
    menu_active  = False

    running = True
    while running:
        dt = clock.tick(FPS)
        # events
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # shop enter / exit detection 
        if (not in_shop and bg_idx == 0 and not zombies
                and player.rect.bottom >= SCREEN_HEIGHT):
            x, _ = player.hitbox.midbottom
            if SHOP_ZONE_X[0] <= x <= SHOP_ZONE_X[1]:
                in_shop   = True
                prev_pos  = player.rect.topleft
                prev_bg   = bg_idx
                player.rect.topleft = (SCREEN_WIDTH // 2 - player.rect.width // 2, 0)
                menu_active = False

        if in_shop and keys[pygame.K_w] and player.rect.top <= 0:
            x, _ = player.hitbox.midbottom
            if SHOP_ZONE_X[0] <= x <= SHOP_ZONE_X[1]:
                in_shop   = False
                bg_idx    = prev_bg
                player.rect.topleft = prev_pos
                menu_active = False

        # draw background 
        if in_shop:
            screen.blit(shop_bg, (0, 0))
        else:
            screen.blit(bg_regular if bg_idx == 0 else bg_ex, (0, -200))
            lvl_surf = font.render(f"Level {level}", True, (0, 0, 0))
            screen.blit(lvl_surf, (SCREEN_WIDTH//2 - lvl_surf.get_width()//2, 10))

        # in-shop logic
        if in_shop:
            player.update(dt, True)
            if player.rect.right > SHOP_RIGHT_EDGE:
                player.rect.right = SHOP_RIGHT_EDGE

            player.hitbox.center = player.rect.center
            if (not menu_active and player.rect.bottom > SHOP_ENTER_Y
                    and player.rect.right >= SHOP_RIGHT_EDGE):
                menu_active = True

            pgroup.draw(screen)

            if menu_active:
                menu_rect = pygame.Rect(200, 150, 800, 400)
                pygame.draw.rect(screen, (50, 50, 50), menu_rect)
                pygame.draw.rect(screen, (200, 200, 200), menu_rect, 4)
                title = font.render("SHOP", True, (255, 255, 255))
                screen.blit(title, (menu_rect.x+20, menu_rect.y+20))
                opt1  = font.render("1) Buy Heart (5 coins)",           True, (255,255,255))
                opt2  = font.render("2) Increase Fire Rate 10% (10 coins)", True, (255,255,255))
                screen.blit(opt1, (menu_rect.x+20, menu_rect.y+80))
                screen.blit(opt2, (menu_rect.x+20, menu_rect.y+140))

                if keys[pygame.K_1] and player.coins >= 5:
                    player.hearts += 1
                    player.coins  -= 5
                if keys[pygame.K_2] and player.coins >= 10:
                    player.shoot_cd = int(player.shoot_cd * 0.9)
                    player.coins   -= 10
                if keys[pygame.K_a]:
                    menu_active = False

        # regular level logic
        else:
            if player.rect.right >= SCREEN_WIDTH:          # reached end → next screen
                bg_idx = (bg_idx + 1) % 2
                player.rect.x = 0
                for i in range(spawn):
                    zx = SCREEN_WIDTH + i*80
                    zy = random.randint(100, SCREEN_HEIGHT - 100)
                    zombies.add(Zombie((zx, zy), health=(level+1)//2))
                zombi_sound.play()
                level += 1
                spawn += 1

            player.update(dt, False)
            bullets.update(dt)
            zombies.update(dt)
            coins.update(dt)

            # out-of-screen zombies cleanup
            for z in list(zombies):
                if z.rect.right < 0:
                    z.kill()

            # create bullet when fired flag set
            if player.fired:
                bx, by = player.hitbox.midright
                bullets.add(Bullet((bx, by-30)))

            # bullet-zombie collisions
            for b in list(bullets):
                hits = pygame.sprite.spritecollide(b, zombies, False, pygame.sprite.collide_rect)
                if hits:
                    for z in hits:
                        z.take_damage()
                        if z.health <= 0:
                            coins.add(Coin(z.rect.center))
                            z.kill()
                    b.kill()

            # zombie-player collisions
            for z in list(zombies):
                if z.hitbox.colliderect(player.hitbox):
                    player.take_damage()
                    z.take_damage()
                    if z.health <= 0:
                        coins.add(Coin(z.rect.center))
                        z.kill()
                    if player.hearts <= 0:
                        game_over_screen()
                        running = False

            # coin pickups
            for _ in pygame.sprite.spritecollide(player, coins, True):
                player.coins += 1
                cling_sound.play()

            bullets.draw(screen)
            coins.draw(screen)
            pgroup.draw(screen)
            zombies.draw(screen)

        # HUD 
        for i in range(player.hearts):
            screen.blit(_heart_image, (20 + i*65, 10))
        coin_txt = font.render(str(player.coins), True, (255, 255, 255))
        tx = SCREEN_WIDTH - coin_txt.get_width() - _coin_image.get_width() - 30
        screen.blit(coin_txt, (tx, 10))
        screen.blit(_coin_image, (SCREEN_WIDTH - _coin_image.get_width() - 10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
