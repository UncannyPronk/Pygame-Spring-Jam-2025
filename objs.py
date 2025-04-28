import pygame, random, math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.hp = 100
        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = 1
        self.power = 1
        self.movement = pygame.Vector2(0, 0)

    def update(self, player):
        if player.rect.centerx > self.rect.right:
            self.movement.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.movement.x -= self.speed
        else:
            self.movement.x = 0
        self.rect.move_ip(self.movement)

    def draw(self, player, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class FastEnemy(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.speed = 3
        self.power = .2
    
    def laser(self, player, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 2)
        pygame.draw.line(screen, (255, 0, 0), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 2)
    
    def draw(self, player, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if player.rect.x < self.rect.centerx < player.rect.right:
            self.laser(player, screen)
            player.hp -= self.power


class SlowEnemy(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.hp = 300
        self.power = 10
        self.missiles = []
        self.missilecount = 5
        self.missilecooldown = 0
    
    def update(self, player):
        if player.rect.centerx > self.rect.right:
            self.movement.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.movement.x -= self.speed
        else:
            self.movement.x = 0
        self.rect.move_ip(self.movement)

        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        if self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), player.rect)
            self.missiles.append(missile)
        
    def draw(self, player, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        for missile in self.missiles:
            missile.update(self.missiles, player, self.power)
            missile.draw(screen)
        
    class Missile(pygame.sprite.Sprite):
        def __init__(self, image_path, position, attackrect):
            super().__init__()
            # self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=position)
            self.speed = 4
            self.target = attackrect.topleft

        def update(self, missiles, player, power):
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance == 0:
                return
            dx = (dx / distance) * self.speed
            dy = self.speed
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.colliderect(pygame.Rect(player.rect.x, player.rect.y - 10, 40, 20)) or self.rect.bottom >= player.rect.y:
                player.hp -= power
                self.kill()
                missiles.remove(self)
        
        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))


class MiniBoss(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.hp = 1000
        self.speed = 5
        self.missiles = []
        self.missilecount = 5
        self.missilecooldown = 0
    
    def laser(self, player, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 2)
        pygame.draw.line(screen, (255, 0, 0), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 2)
    
    def update(self, player):
        if player.rect.centerx > self.rect.right:
            self.movement.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.movement.x -= self.speed
        else:
            self.movement.x = 0
        self.rect.move_ip(self.movement)

        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        if self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), player.rect)
            self.missiles.append(missile)
        
    def draw(self, player, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        for missile in self.missiles:
            missile.update(self.missiles, player)
            missile.draw(screen)
        if player.rect.x < self.rect.centerx < player.rect.right:
            self.laser(player, screen)
            player.hp -= 1
        
    class Missile(pygame.sprite.Sprite):
        def __init__(self, image_path, position, attackrect):
            super().__init__()
            # self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=position)
            self.speed = 4
            self.target = attackrect.topleft

        def update(self, missiles, player):
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance == 0:
                return
            dx = (dx / distance) * self.speed
            dy = self.speed
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.colliderect(pygame.Rect(player.rect.x, player.rect.y - 10, 40, 20)) or self.rect.bottom >= player.rect.y:
                self.kill()
                missiles.remove(self)
        
        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

class Boss(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.hp = 3000
        self.missiles = []
        self.missilecount = 5
        self.missilecooldown = 0
    
    def laser(self, player, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 2)
        pygame.draw.line(screen, (255, 0, 0), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 2)
    
    def update(self, player):
        if player.rect.centerx > self.rect.right:
            self.movement.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.movement.x -= self.speed
        else:
            self.movement.x = 0
        self.rect.move_ip(self.movement)

        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        if self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), player.rect)
            self.missiles.append(missile)
        
    def draw(self, player, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        for missile in self.missiles:
            missile.update(self.missiles, player)
            missile.draw(screen)
        if player.rect.x < self.rect.centerx < player.rect.right:
            self.laser(player, screen)
            player.hp -= 1
        
    class Missile(pygame.sprite.Sprite):
        def __init__(self, image_path, position, attackrect):
            super().__init__()
            # self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=position)
            self.speed = 4
            self.target = attackrect.topleft

        def update(self, missiles, player):
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance == 0:
                return
            dx = (dx / distance) * self.speed
            dy = self.speed
            self.rect.x += dx
            self.rect.y += dy
            if self.rect.colliderect(pygame.Rect(player.rect.x, player.rect.y - 10, 40, 20)) or self.rect.bottom >= player.rect.y:
                self.kill()
                missiles.remove(self)
        
        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

class Ship(pygame.sprite.Sprite):
    def __init__(self, image_path, position, display_rect):
        super().__init__()
        # self.image = pygame.image.load(image_path).convert_alpha()

        self.hp = 500
        self.fuel = 500
        self.spacial_used = False
        self.spacial_count = 500
        self.spacial_color = 255
        self.spacial_alpha = 255
        self.spacial_radius = display_rect.width/2
        self.spacial_surface = pygame.Surface((display_rect.w, display_rect.h))

        self.image = pygame.Surface((200, 100))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = 10
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
      
    def update(self, controller_connected, display_rect, joystick, enemy_list):
        # self.layer_update -= 1
        # if self.layer_update <= 0:
        #     self.prev_pos.append((self.rect.x, self.rect.y))
        #     if len(self.prev_pos) > 3:
        #         self.prev_pos.pop(0)
        #     self.layer_update = 3

        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        
        if self.spacial_count > 0 and self.spacial_used:
            self.spacial_count -= 1

        if not (self.spacial_used and self.spacial_count > 0):
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

                if keys[pygame.K_w] and self.rect.y > display_rect.y + 100:
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
                
                if pygame.mouse.get_pressed()[0] and not self.laserbool:
                    self.laserbool = True
                else:
                    self.laserbool = False
                
                if pygame.mouse.get_pressed()[0] and self.fuel > 0:
                    self.fuel -= .2
                else:
                    self.laserbool = False

                if pygame.mouse.get_pressed()[2] and len(self.missiles) < self.missilecount and self.missilecooldown == 0:
                    self.missilecooldown = 50
                    self.missilecount -= 1
                    missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), self.attackrect)
                    self.missiles.append(missile)

                if keys[pygame.K_SPACE] and not self.spacial_used:
                    self.spacial_used = True
                    for enemy in enemy_list:
                        enemy.hp = 0

                self.attackrect.center = pygame.mouse.get_pos()
            else:
                if self.rect.x > display_rect.x + 100 and int(joystick.get_axis(0)) < 0:
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
                if self.rect.y > display_rect.y + 100 and int(joystick.get_axis(1)) < 0:
                    if joystick.get_axis(5) > 0 and self.fuel > 0:
                        self.movement.y = -self.speed * 4
                        self.fuel -= 1
                    else:
                        self.movement.y = -self.speed
                    # print(round(joystick.get_axis(1)))
                elif self.rect.bottom < display_rect.bottom - 100 and round(joystick.get_axis(1)) > 0:
                    if joystick.get_axis(5) > 0 and self.fuel > 0:
                        self.movement.y = self.speed * 4
                        self.fuel -= 1
                    else:
                        self.movement.y = self.speed
                else:
                    self.movement.y = 0
                
                #attacks
                if joystick.get_button(5) and not self.laserbool:
                    self.laserbool = True
                    for enemy in enemy_list:
                        if self.attackrect.colliderect(enemy):
                            enemy.hp -= 1
                else:
                    self.laserbool = False
                
                if joystick.get_button(5) and self.fuel > 0:
                    self.fuel -= .2
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
                
                for missile in self.missiles:
                    for enemy in enemy_list:
                        if missile.rect.colliderect(enemy):
                            enemy.hp -= 10
                            break

                if joystick.get_axis(4) > 0 and not self.spacial_used:
                    self.spacial_used = True
                    for enemy in enemy_list:
                        enemy.hp = 0
                
                if round(joystick.get_axis(2)) > 0:
                    self.attackrect.x += 15
                elif int(joystick.get_axis(2)) < 0:
                    self.attackrect.x -= 15
                if round(joystick.get_axis(3)) > 0:
                    self.attackrect.y += 15
                elif int(joystick.get_axis(3)) < 0:
                    self.attackrect.y -= 15
                
        else:
            self.movement.x, self.movement.y = 0, 0

        self.rect.move_ip(self.movement)
        # self.attackrect.move_ip(self.movement.x/2, self.movement.y/2)

        # self.attackrect.centerx = display_rect.centerx + (self.rect.centerx - display_rect.centerx)/2
        # self.attackrect.centery = display_rect.centery - 200 + (self.rect.centery - display_rect.centery)/2

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
            self.speed = 4
            self.target = attackrect.topleft

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
        self.size = 1
        self.static = static
        if not static:
            self.pos = pygame.Vector2(random.randint(display_rect.centerx - 50, display_rect.centerx + 50), random.randint(display_rect.centery - 50, display_rect.centery + 50))

            self.movement = [random.randint(0, 8)]
            self.movement.append(8 - self.movement[0])
            if self.pos.x < display_rect.centerx - 10:
                self.movement[0] = -self.movement[0]
            self.pos.x += self.movement[0] * 60

            if self.pos.y < display_rect.centery - 10:
                self.movement[1] = -self.movement[1]
            self.pos.y += self.movement[1] * 60
        else:
            self.pos = pygame.Vector2(random.randint(display_rect.x, display_rect.right), random.randint(display_rect.y, display_rect.bottom))
                
    def update(self, display_rect, player):
        if not self.static:
            dist = int(math.sqrt((self.pos.x - (display_rect.centerx + self.movement[0]*60))**2 + (self.pos.y - (display_rect.centery + self.movement[1]*60))**2))
            if dist > 255:
                dist = 255
            if dist > 200:
                self.size = 2
            self.color = (dist, dist, dist)
            self.pos.x += self.movement[0]
            self.pos.y += self.movement[1]
        else:
            dist = int(math.sqrt((self.pos.x - display_rect.centerx)**2 + (self.pos.y - display_rect.centery)**2)) // 3
            rand = random.randint(30, 255)
            if player.spacial_used:
                if player.spacial_count > 0:
                    color = rand
                else:
                    color = rand - dist + player.spacial_alpha
            else:
                color = rand - dist
            if color < 0:
                color = 0
            if color > 255:
                color = 255
            self.color = (color, color, color)
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)