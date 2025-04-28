import pygame
from gameloop import gameloop

pygame.init()
monitor_size = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
pygame.joystick.init()

if __name__ == "__main__":
    gameloop(screen)