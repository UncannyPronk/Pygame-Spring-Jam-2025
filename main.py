import pygame
from gameloop import gameloop

pygame.init()
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
pygame.joystick.init()

if __name__ == "__main__":
    gameloop(screen)