      import pygame
from gameloop import Game

pygame.init()
# monitor_size = pygame.display.Info().current_w, pygame.display.Info().current_h
monitor_size = (1600,900)
screen = pygame.display.set_mode(monitor_size)
pygame.joystick.init()

if __name__ == "__main__":
    Game(screen).run()