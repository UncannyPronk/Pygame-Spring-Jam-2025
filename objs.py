import pygame, random, math

class Ship(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        # self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.movement = pygame.Vector2(0, 0)
        self.space_erase = False
    def update(self, controller_connected, display_rect, joystick):
        if not controller_connected:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.rect.x > display_rect.x + 100:
                self.movement.x = -self.speed
            elif keys[pygame.K_d] and self.rect.right < display_rect.right - 100:
                self.movement.x = self.speed
            else:
                self.movement.x = 0

            if keys[pygame.K_w] and self.rect.y > display_rect.centery - 100:
                self.movement.y = -self.speed
            elif keys[pygame.K_s] and self.rect.bottom < display_rect.bottom - 100:
                self.movement.y = self.speed
            else:
                self.movement.y = 0
        else:
            self.movement.x = joystick.get_axis(0) * self.speed
            self.movement.y = joystick.get_axis(1) * self.speed

        self.rect.move_ip(self.movement)
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Star:
    def __init__(self, display_rect, static=False):
        self.color = (0, 0, 0)
        self.size = 2
        self.static = static
        if not static:
            self.pos = pygame.Vector2(random.randint(display_rect.centerx - 50, display_rect.centerx + 50), random.randint(display_rect.centery - 50, display_rect.centery + 50))
            self.movement = [random.randint(0, 8)]
            self.movement.append(8 - self.movement[0])
            if self.pos.x < display_rect.centerx - 10:
                self.movement[0] = -self.movement[0]
            if self.pos.y < display_rect.centery - 10:
                self.movement[1] = -self.movement[1]
        else:
            self.size = 1
            self.pos = pygame.Vector2(random.randint(display_rect.x, display_rect.right), random.randint(display_rect.y, display_rect.bottom))
                
    def update(self, display_rect):
        if not self.static:
            dist = int(math.sqrt((self.pos.x - display_rect.centerx)**2 + (self.pos.y - display_rect.centery)**2)) // 2
            if dist > 255:
                dist = 255
        else:
            dist = random.randint(10, 255)
        self.color = (dist, dist, dist)
        if not self.static:
            self.pos.x += self.movement[0]
            self.pos.y += self.movement[1]
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, int(self.size))