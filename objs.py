import pygame, random, math


class Ship(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        # self.image = pygame.image.load(image_path).convert_alpha()

        self.damage = 0
        self.fuel = 500
        self.spacial_used = False

        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = 5
        self.movement = pygame.Vector2(0, 0)
        self.attackrect = pygame.Rect(self.rect.x + 80, self.rect.y - 200, 40, 20)
        self.laserbool = False
        self.missiles = []
        self.missilecount = 5
        self.missilecooldown = 0
        # self.layer_update = 3
        # self.prev_pos = []
        # for i in range(3):
        #     self.prev_pos.append((self.rect.x, self.rect.y))
    
    def laser(self, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.rect.x + 20, self.rect.y), (self.attackrect.x + 5, self.attackrect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.x + 20, self.rect.y), (self.attackrect.x + 5, self.attackrect.centery), 2)
        pygame.draw.line(screen, (255, 0, 0), (self.rect.right - 20, self.rect.y), (self.attackrect.right - 5, self.attackrect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 20, self.rect.y), (self.attackrect.right - 5, self.attackrect.centery), 2)
    def update(self, controller_connected, display_rect, joystick):
        # self.layer_update -= 1
        # if self.layer_update <= 0:
        #     self.prev_pos.append((self.rect.x, self.rect.y))
        #     if len(self.prev_pos) > 3:
        #         self.prev_pos.pop(0)
        #     self.layer_update = 3

        if self.missilecooldown > 0:
            self.missilecooldown -= 1

        if not controller_connected:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] and self.rect.x > display_rect.x + 100:
                if keys[pygame.K_LSHIFT] and self.fuel > 0:
                    self.movement.x = -self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.x = -self.speed
            elif keys[pygame.K_d] and self.rect.right < display_rect.right - 100:
                if keys[pygame.K_LSHIFT] and self.fuel > 0:
                    self.movement.x = self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.x = self.speed
            else:
                self.movement.x = 0

            if keys[pygame.K_w] and self.rect.y > display_rect.centery - 100:
                if keys[pygame.K_LSHIFT] and self.fuel > 0:
                    self.movement.y = -self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.y = -self.speed
            elif keys[pygame.K_s] and self.rect.bottom < display_rect.bottom - 100:
                if keys[pygame.K_LSHIFT] and self.fuel > 0:
                    self.movement.y = self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.y = self.speed
            else:
                self.movement.y = 0
            
            #change attack mode to mouse click later
            if keys[pygame.K_e] and not self.laserbool:
                self.laserbool = True
                self.fuel -= .2
            else:
                self.laserbool = False

            if keys[pygame.K_q] and len(self.missiles) < self.missilecount and self.missilecooldown == 0:
                self.missilecooldown = 50
                self.missilecount -= 1
                missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), self.attackrect)
                self.missiles.append(missile)
                # self.missiles[-1].outer = self
                # self.missiles[-1].image = pygame.image.load("missile.png").convert_alpha()
                # self.missiles[-1].image = pygame.transform.scale(self.missiles[-1].image, (50, 50))
                # self.missiles[-1].rect = self.missiles[-1].image.get_rect(center=(self.rect.x + 20, self.rect.y))
        else:
            if self.rect.x > display_rect.x + 100 and round(joystick.get_axis(0)) < 0:
                if joystick.get_axis(5) > 0 and self.fuel > 0:
                    self.movement.x = -self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.x = -self.speed
            elif self.rect.right < display_rect.right - 100 and round(joystick.get_axis(0)) > 0:
                if joystick.get_axis(5) > 0 and self.fuel > 0:
                    self.movement.x = self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.x = self.speed
            else:
                self.movement.x = 0
            if self.rect.y > display_rect.centery - 100 and round(joystick.get_axis(1)) < 0:
                if joystick.get_axis(5) > 0 and self.fuel > 0:
                    self.movement.y = -self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.y = -self.speed
            elif self.rect.bottom < display_rect.bottom - 100 and round(joystick.get_axis(1)) > 0:
                if joystick.get_axis(5) > 0 and self.fuel > 0:
                    self.movement.y = self.speed * 4
                    self.fuel -= 1
                else:
                    self.movement.y = self.speed
            else:
                self.movement.y = 0
            
            if joystick.get_button(5) and not self.laserbool:
                self.laserbool = True
            else:
                self.laserbool = False

            if joystick.get_button(4) and len(self.missiles) < self.missilecount and self.missilecooldown == 0:
                self.missilecooldown = 50
                self.missilecount -= 1
                missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), self.attackrect)
                self.missiles.append(missile)
                # self.missiles[-1].outer = self
                # self.missiles[-1].image = pygame.image.load("missile.png").convert_alpha()
                # self.missiles[-1].image = pygame.transform.scale(self.missiles[-1].image, (50, 50))
                # self.missiles[-1].rect = self.missiles[-1].image.get_rect(center=(self.rect.x + 20, self.rect.y))

        self.rect.move_ip(self.movement)
        self.attackrect.move_ip(self.movement.x/2, self.movement.y/2)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (255, 0, 255), (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 1)
        pygame.draw.rect(screen, (0, 255, 0), (self.attackrect.x, self.attackrect.y, self.attackrect.width, self.attackrect.height), 1)
        if self.laserbool:
            self.laser(screen)
        for missile in self.missiles:
            missile.update(self.missiles)
            missile.draw(screen)
        # for i in range(2, 0, -1):
        #     screen.blit(self.image, (self.prev_pos[i][0], self.prev_pos[i][1]))
        #     pygame.draw.rect(screen, (255, 0, 0), (self.prev_pos[i][0], self.prev_pos[i][1], self.image.get_width(), self.image.get_height()), 1)
    
    class Missile(pygame.sprite.Sprite):
        def __init__(self, image_path, position, attackrect):
            super().__init__()
            # self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=position)
            self.speed = 10
            self.target = attackrect.center

        def update(self, missiles):
            dx = self.target[0] - self.rect.x
            dy = self.target[1] - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance == 0:
                return
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.colliderect(pygame.Rect(self.target[0], self.target[1] - 10, 40, 20)):
                self.kill()
                missiles.remove(self)
        
        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

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