import pygame, sys, random
from pygame import *
from pygame.locals import *
from objs import Ship, Star

clock = pygame.time.Clock()
fps = 60
controller_connected = False
joy = None

def eventloop():
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
        if ev.type == pygame.JOYDEVICEREMOVED:
            controller_connected = False

def draw_status(screen, player):
    pygame.draw.rect(screen, (255, 0, 0), (20, 20, player.damage*2, 20))
    pygame.draw.rect(screen, (255, 255, 255), (20, 20, 200, 20), 2)

    pygame.draw.rect(screen, (255, 255, 0), (20, 50, player.fuel//5, 20))
    pygame.draw.rect(screen, (255, 255, 255), (20, 50, 100, 20), 2)

def draw(screen):
    screen.fill((0, 0, 0))
    for star in star_list:
        star.draw(screen)
    player.draw(screen)
    # pygame.draw.rect(screen, (255, 0, 0), (display_rect.centerx - 100, display_rect.centery - 50, 200, 100))

def stars():
    if random.randint(0, 10) == 0:
        star_list.append(Star(display_rect))
    for star in star_list:
        star.update(display_rect)
        if not Rect(star.pos.x, star.pos.y, star.size, star.size).colliderect(display_rect):
            star_list.remove(star)
            break

def gameloop(screen):
    global display_rect, player, joysticks, star_list
    running = True
    joysticks = {}
    display_rect = screen.get_rect()
    player = Ship("assets/ship.png", (display_rect.centerx, display_rect.bottom - 300))
    star_list = []
    for i in range(80):
        star_list.append(Star(display_rect, True))
    while running:
        eventloop()
        clock.tick(fps)
        pygame.display.flip()

        stars()
        
        player.update(controller_connected, display_rect, joy)
        
        draw(screen)
        draw_status(screen, player)