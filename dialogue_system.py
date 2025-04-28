import pygame
from pygame import *
from pygame.locals import *



def write(screen, blit=True, text='sample text', position=(0, 0), color=(0, 0, 0), fontsize=20, font='arial'):
    font = pygame.font.SysFont(font, fontsize)
    text = font.render(text, True, color)
    if blit:
        screen.blit(text, position)
        rect = text.get_rect()
        rect.topleft = position[0], position[1]
        return rect
    else:
        return text, position

def speak(screen, display_rect, bgpath, sprite1path, sprite2path, i, text=["Sample Text"]):
    bgimg = pygame.image.load(bgpath)
    sprite1 = pygame.image.load(sprite1path)
    sprite2 = pygame.image.load(sprite2path)
    screen.blit(pygame.transform.scale(bgimg, (display_rect.w, display_rect.h)), (0, 0))
    screen.blit(pygame.transform.scale(sprite1, (300, display_rect.h - 300)), (200, 300))
    screen.blit(pygame.transform.scale(sprite2, (300, display_rect.h - 300)), (display_rect.w - 500, 300))
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, display_rect.w, 300))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, display_rect.w, 300), 5)
    write(screen, text=text[i], position=(32, 32), color=(255, 255, 255), fontsize=30)