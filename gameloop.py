import pygame, sys, random
from pygame import *
from pygame.locals import *
from objs import Ship

clock = pygame.time.Clock()
fps = 60

def eventloop():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

def draw(screen):
    screen.fill((0, 0, 0))
    player.draw(screen)
    # pygame.draw.rect(screen, (255, 0, 0), (display_rect.centerx - 100, display_rect.centery - 50, 200, 100))

def gameloop(screen):
    global display_rect, player
    running = True
    display_rect = screen.get_rect()
    player = Ship("assets/ship.png", (display_rect.centerx, display_rect.bottom - 300))
    while running:
        eventloop()
        clock.tick(fps)
        pygame.display.flip()
        
        player.update()
        
        draw(screen)