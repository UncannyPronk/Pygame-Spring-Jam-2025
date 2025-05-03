import pygame, sys, random
from pygame import *
from pygame.locals import *
from objs import Ship, Star, FastEnemy, SlowEnemy
from dialogue_system import speak

clock = pygame.time.Clock()
fps = 60
controller_connected = False
joy : pygame.joystick.JoystickType | None = None

def eventloop(player, display_rect):
    global controller_connected, joy
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == KEYDOWN:
            if ev.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        if ev.type == pygame.JOYDEVICEADDED:
            controller_connected = True
            joy = pygame.joystick.Joystick(ev.device_index)
            player.attackrect.center = display_rect.center
        if ev.type == pygame.JOYDEVICEREMOVED:
            controller_connected = False

def draw_status(screen, player, i=0):
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, player.hp, 20))
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 500, 20), 2)

    pygame.draw.rect(screen, (255, 255, 0), (20, 50, player.fuel//5, 20))
    pygame.draw.rect(screen, (255, 255, 255), (20, 50, 100, 20), 2)

    # dialogue_list = ["Hello There", "How are you doing?", "Testing", "Tested!"]
    # while i < len(dialogue_list):
    #     pygame.display.flip()
    #     screen.fill((0, 0, 0))
    #     speak(screen, display_rect, "C:/Users/janar/OneDrive/Pictures/Screenshots/Screenshot 2025-03-08 213325.png", "C:/Users/janar/OneDrive/Pictures/hd-miyamoto-musashi-wallpaper-whatspaper.jpg", "C:/Users/janar/OneDrive/Pictures/hanuman.jpg", i, dialogue_list)
    #     for ev in pygame.event.get():
    #         if ev.type == QUIT:
    #             pygame.quit()
    #         if ev.type == KEYDOWN:
    #             if ev.key == K_a:
    #                 i += 1
    #             if ev.key == K_ESCAPE:
    #                 pygame.quit()

def draw(screen, star_list, enemy_list):
    screen.fill((0, 0, 6))
    for star in star_list:
        star.draw(screen)
    if player.spacial_used:
        if player.spacial_count > 480 and player.spacial_count%2 == 0:
            screen.fill((255, 255, 255))
        if player.spacial_radius > display_rect.height/2:
            player.spacial_radius -= 50
        if player.spacial_color > 0:
            player.spacial_color -= 2
        if player.spacial_color < 0:
            player.spacial_color = 0
        player.spacial_surface.fill((0, 255, 0))
        pygame.draw.circle(player.spacial_surface, (player.spacial_color, player.spacial_color, player.spacial_color), (display_rect.centerx, display_rect.centery), int(player.spacial_radius))
        player.spacial_surface.set_colorkey((0, 255, 0))
        if player.spacial_alpha > 0 and player.spacial_count == 0:
            player.spacial_alpha -= 1
        player.spacial_surface.set_alpha(player.spacial_alpha)
        screen.blit(player.spacial_surface, (0, 0))

    for enemy in enemy_list:
        enemy.draw(player, screen)

    player.draw(screen)
    # return star_list
    # pygame.draw.rect(screen, (255, 0, 0), (display_rect.centerx - 100, display_rect.centery - 50, 200, 100))

def stars():
    if random.randint(0, 1) == 0:
        if player.spacial_used == True and player.spacial_count == 0:
            star_list.append(Star(display_rect))
        elif player.spacial_used == False:
            star_list.append(Star(display_rect))
    for star in star_list:
        star.update(display_rect, player)        
        if not Rect(star.pos.x, star.pos.y, star.size, star.size).colliderect(display_rect):
            star_list.remove(star)
            break

def gameloop(screen):
    global display_rect, player, joysticks, star_list
    running = True
    joysticks = {}
    display_rect = screen.get_rect()
    player = Ship((display_rect.centerx, display_rect.bottom - 300), display_rect)
    star_list = []
    enemy_list = [FastEnemy((100, 220)), SlowEnemy((400, 350))]
    for i in range(120):
        star_list.append(Star(display_rect, True))
    pygame.mixer.music.load("assets/audio/star_focus.mp3")
    pygame.mixer.music.play(-1)
    while running:
        eventloop(player, display_rect)
        clock.tick(fps)
        pygame.display.flip()

        stars()
        
        player.update(controller_connected, display_rect, joy, enemy_list)
        for enemy in enemy_list:
            enemy.update(player)
            if enemy.hp <= 0:
                enemy_list.remove(enemy)
        
        draw(screen, star_list, enemy_list)
        draw_status(screen, player)

        if player.hp <= 0:
            running = False