import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        # self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.movement = pygame.Vector2(0, 0)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x = -self.speed
        elif keys[pygame.K_d]:
            self.movement.x = self.speed
        else:
            self.movement.x = 0

        if keys[pygame.K_w]:
            self.movement.y = -self.speed
        elif keys[pygame.K_s]:
            self.movement.y = self.speed
        else:
            self.movement.y = 0

        self.rect.move_ip(self.movement)
    def draw(self, screen):
        screen.blit(self.image, self.rect)