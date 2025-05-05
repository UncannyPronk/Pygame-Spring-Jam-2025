import pygame, random, math
from constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.hp = 100
        self.max_hp = self.hp
        self.image = pygame.image.load("assets/images/enemy.png")
        self.rect = self.image.get_frect(center=position)
        self.speed = 10
        self.power = 3
        self.velocity = pygame.Vector2(0, 0)
        self.explosion_sound = pygame.Sound("assets/audio/explosion.wav")

    def set_power_factor(self,factor):
        self.power *= factor
        return self
    def set_hp(self,hp):
        self.hp = hp
        self.max_hp = hp
        return self

    def update(self, player):
        # Get target direction (towards player horizontally only)
        direction = pygame.Vector2(player.rect.centerx - self.rect.centerx, 0)
        if direction.length() != 0:
            direction.normalize_ip()
            self.velocity += direction * 1  # acceleration = 1
        else:
            if self.velocity.length() != 0:
                decel = self.velocity.normalize() * -1
                self.velocity += decel
                if self.velocity.length_squared() < 1:
                    self.velocity = pygame.Vector2(0, 0)

        # Clamp to max speed
        if self.velocity.length() > self.speed:
            self.velocity.scale_to_length(self.speed)

        # Update float position
        self.rect.topleft += self.velocity


    def draw(self, player, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

class FastEnemy(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.speed = 7
        self.power = .4
        self.image = pygame.image.load("assets/images/enemy.png")
        self.original_position = position
    
    def update(self, player):
        super().update(player)
        self.rect.y = self.original_position[1] - 20 * math.cos(pygame.time.get_ticks()/200)

    def laser(self, player, screen):
        start_point1 = self.rect.move(10,0).midleft
        end_point1 = player.rect.move(-5,0).center
        start_point2 = self.rect.move(-10,0).midright
        end_point2 = player.rect.move(5,0).center

        pygame.draw.line(screen, (255, 0, 0), start_point1, end_point1, 4)
        pygame.draw.line(screen, (255, 255, 255), start_point1, end_point1, 2)
        pygame.draw.line(screen, (255, 0, 0), start_point2, end_point2, 4)
        pygame.draw.line(screen, (255, 255, 255), start_point2, end_point2, 2)
    
    def draw(self, player, screen):
        if player.rect.x + 50 < self.rect.centerx < player.rect.right-50:
            self.laser(player, screen)
            player.hp -= self.power
        screen.blit(self.image, self.rect)


class SlowEnemy(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.speed = .05
        self.hp = 300
        self.max_hp = self.hp

        self.power = 10
        self.missiles = []
        self.missilecount = 5
        self.missilecooldown = 0
        self.image = pygame.image.load("assets/images/enemy.png")
        self.original_position = position
    
    def update(self, player):
        if player.rect.centerx > self.rect.right:
            self.velocity.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.velocity.x -= self.speed
        else:
            self.velocity.x = 0
        self.rect.move_ip(self.velocity)

        self.rect.y = self.original_position[1] - 14 * math.cos(pygame.time.get_ticks()/300)
        
        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        if self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = self.Missile("assets/images/enemy_missile.png", self.rect.center, player.rect)
            self.missiles.append(missile)
        

    def draw(self, player, screen):
        screen.blit(self.image, self.rect)
        for missile in self.missiles:
            missile.update(self.missiles, player, self.power)
            missile.draw(screen)
        
    class Missile(pygame.sprite.Sprite):
        def __init__(self, image_path, position, attackrect):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.explosion_sound = pygame.Sound("assets/audio/explosion.wav")

            self.rect = self.image.get_rect(center=position)
            self.speed = 4
            # Calculate direction vector towards the center of attackrect
            target_x, target_y = attackrect.center
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance == 0:
                self.velocity = pygame.Vector2(0, self.speed)
            else:
                self.velocity = pygame.Vector2(dx / distance * self.speed, dy / distance * self.speed)
            
            self.image = pygame.transform.rotate(self.image,self.velocity.angle_to(pygame.Vector2(0,1)))

        def update(self, missiles, player, power):
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y
            # Check collision with player
            hitbox = pygame.Rect(0,0,150,70)
            hitbox.center = player.rect.center
            if self.rect.colliderect(hitbox):
                player.hp -= power
                self.kill()
                if self in missiles:
                    missiles.remove(self)
        def draw(self, screen):
            if self.rect.top > screen.get_height():
                self.kill()
            screen.blit(self.image, (self.rect.x, self.rect.y))


class MiniBoss(Enemy):
    def __init__(self, position):
        super().__init__(position)
        self.hp = 1000
        self.max_hp = self.hp

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
            self.velocity.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.velocity.x -= self.speed
        else:
            self.velocity.x = 0
        self.rect.move_ip(self.velocity)

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
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=position)
            self.speed = 4
            self.target = attackrect.topleft
            self.explosion_sound = pygame.Sound("assets/audio/explosion.wav")


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
        self.max_hp = self.hp

        self.missiles = pygame.sprite.Group()
        self.missilecount = 5
        self.missilecooldown = 0
    
    def laser(self, player, screen):
        pygame.draw.line(screen, (255, 0, 0), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.x + 20, self.rect.bottom), (player.rect.x + 5, player.rect.centery), 2)
        pygame.draw.line(screen, (255, 0, 0), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 4)
        pygame.draw.line(screen, (255, 255, 255), (self.rect.right - 20, self.rect.bottom), (player.rect.right - 5, player.rect.centery), 2)
    
    def update(self, player):
        if player.rect.centerx > self.rect.right:
            self.velocity.x += self.speed
        elif player.rect.centerx < self.rect.x:
            self.velocity.x -= self.speed
        else:
            self.velocity.x = 0
        self.rect.move_ip(self.velocity)

        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        if self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = self.Missile("missile.png", (self.rect.centerx, self.rect.y), player.rect)
            self.missiles.add(missile)
        
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
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(center=position)
            self.speed = 4
            self.target = attackrect.topleft
            self.explosion_sound = pygame.Sound("assets/audio/explosion.wav")

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
        
        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))


# --- Ship Class ---
class Ship(pygame.sprite.Sprite):
    """Player ship with velocity, attack, and special ability."""
    def __init__(self, position, display_rect):
        super().__init__()
        self.ship_normal = pygame.image.load("assets/images/ship_normal.png").convert_alpha()
        self.ship_up = pygame.image.load("assets/images/ship_up.png").convert_alpha()
        self.ship_down = pygame.image.load("assets/images/ship_down.png").convert_alpha()
        self.crosshair = pygame.image.load("assets/images/crosshair.png").convert_alpha()
        self.base_image = self.ship_normal
        self.image = self.base_image.copy()

        self.laser_sound = pygame.Sound("assets/audio/laserShoot.wav")
        self.laser_sound.set_volume(0.3)
        self.spacial_sound = pygame.Sound("assets/audio/space.wav")
        self.explosion_sound = pygame.Sound("assets/audio/explosion.wav")


        self.hp = 500
        self.max_hp = 500
        self.fuel = 500
        self.max_fuel = 500
        self.spacial_used = False
        self.spacial_count = 500
        self.spacial_color = 255
        self.spacial_alpha = 255
        self.spacial_radius = display_rect.width / 2
        self.spacial_surface = pygame.Surface((display_rect.w, display_rect.h), pygame.SRCALPHA)

        self.rect = self.image.get_rect(center=position)
        self.acceleration = 2
        self.speed = 20
        self.boost_multiplier = 4
        self.velocity = pygame.Vector2(0, 0)
        self.friction = 0.85

        self.angle = 0.0
        self.target_angle = 0.0
        self.rotation_speed = 8.0  # degrees per frame

        self.velocity = pygame.Vector2(0, 0)
        self.attackrect = pygame.Rect(self.rect.x + 80, self.rect.y - 200, 40, 20)
        self.laserbool = False
        self.missiles = pygame.sprite.Group()
        self.missilecount = 5
        self.missilecooldown = 0
        self.laser_damage = 0.3

    def reset(self, position, display_rect,level:int=0):
        """Reset the ship's state for a retry after game over."""
        if level == 0:
            self.hp = 500 
        else:
            self.max_hp+=100
            self.hp += 200
            self.hp = min(self.max_hp,self.fuel)
        if level == 0:
            self.fuel = 500
        else:
            self.fuel = min(self.fuel+200,self.max_fuel)

        
        self.spacial_used = False
        self.spacial_count = 500
        self.spacial_color = 255
        self.spacial_alpha = 255
        self.spacial_radius = display_rect.width / 2
        self.velocity = pygame.Vector2(0, 0)
        self.angle = 0.0
        self.target_angle = 0.0
        self.velocity = pygame.Vector2(0, 0)
        self.missiles.empty()
        self.missilecount = 5 + 2 * level
        self.missilecooldown = 0
        self.rect = self.image.get_rect(center=position)
        self.attackrect = pygame.Rect(self.rect.x + 80, self.rect.y - 200, 40, 20)
        self.laser_damage = 0.3 + 0.2 * level


    def _apply_velocity_input(self, move_x, move_y, boost):
        """Apply velocity input to velocity and set target angle."""
        move = pygame.Vector2(move_x, move_y)
        if move.length_squared() > 0:
            move = move.normalize()
            # speed = self.speed * (self.boost_multiplier if boost and self.fuel > 0 else 1)
            self.velocity += move * self.acceleration
            self.velocity.clamp_magnitude_ip(self.speed)
            self.target_angle = move.angle_to(pygame.Vector2(0, -1))
            
            self.target_angle = (self.target_angle + 180) % 360 - 180

            if boost and self.fuel > 0:
                self.fuel -= 1
        else:
            self.target_angle = 0

    def _handle_keyboard(self):
        keys = pygame.key.get_pressed()
        move_x = (keys[KEY_RIGHT] - keys[KEY_LEFT])
        move_y = (keys[KEY_DOWN] - keys[KEY_UP])
        boost = keys[KEY_SHIFT]
        self._apply_velocity_input(move_x, move_y, boost)


    def _handle_joystick(self, joystick):
        axis_x = joystick.get_axis(JOY_AXIS_X)
        axis_y = joystick.get_axis(JOY_AXIS_Y)
        axis_speed = joystick.get_axis(JOY_AXIS_SPEED)
        boost = axis_speed > 0
        self._apply_velocity_input(axis_x, axis_y, boost)

    def update(self, controller_connected, display_rect, joystick, enemy_list):
        # Input
        if not (self.spacial_used and self.spacial_count > 0):
            if controller_connected and joystick:
                self._handle_joystick(joystick)
            else:
                self._handle_keyboard()
        else:
            self.velocity *= self.friction  # Slow down if special is active

        # Apply friction
        self.velocity *= self.friction
        if self.velocity.length() < 0.1:
            self.velocity = pygame.Vector2(0, 0)

        # Update position
        self.rect.center += self.velocity

        # Clamp to display rect
        self.rect.clamp_ip(display_rect)

        # Smoothly interpolate angle
        angle_diff = self.target_angle - self.angle 
        self.angle += angle_diff * 0.15  # interpolation factor
        self.angle = pygame.math.clamp(self.angle,-45,45)

        # Rotate image
        if self.velocity.y == 0:
            self.base_image = self.ship_normal
        elif self.velocity.y > 0:
            self.base_image = self.ship_down
        elif self.velocity.y < 0:
            self.base_image = self.ship_up

        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Cooldowns and special
        if self.missilecooldown > 0:
            self.missilecooldown -= 1
        if self.spacial_count > 0 and self.spacial_used:
            self.spacial_count -= 1

        if controller_connected and joystick:
            self._update_attack_joystick(display_rect,joystick,enemy_list)
        else:

            self._update_attack(display_rect,enemy_list)

        for missile in self.missiles.copy():
            missile.update(self.missiles,enemy_list)

    def laser(self, screen):
        """Draws the ship's laser attack with rotated start points."""
        center = pygame.Vector2(self.rect.center)

        # Offsets before rotation
        offset1 = pygame.Vector2(-50, 0)  # midright side
        offset2 = pygame.Vector2(50, 0)   # midleft side

        # Rotate offsets
        offset1 = offset1.rotate(-self.angle)  # Pygame rotates counterclockwise, so negate angle
        offset2 = offset2.rotate(-self.angle)

        # Calculate rotated start points
        start_point1 = center + offset1
        start_point2 = center + offset2

        end_point1 = self.attackrect.move(-10, 0).center
        end_point2 = self.attackrect.move(10, 0).center


        # Draw lasers
        pygame.draw.line(screen, (255, 0, 0), start_point1, end_point1, 4)
        pygame.draw.line(screen, (255, 255, 255), start_point1, end_point1, 2)
        pygame.draw.line(screen, (255, 0, 0), start_point2, end_point2, 4)
        pygame.draw.line(screen, (255, 255, 255), start_point2, end_point2, 2)

    def get_collided_enemies(self, enemy_list):
        """Return a list of enemies currently colliding with the ship's attack rect."""
        
        collided = []
        for enemy in enemy_list:
            if self.attackrect.colliderect(enemy.rect):
                collided.append(enemy)
        return collided

    def _update_attack(self, display_rect, enemy_list):
        # Attacks
        mouse_pressed = pygame.mouse.get_just_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_released = pygame.mouse.get_just_released()

        if mouse_pressed[MOUSE_LEFT]:
            self.laserbool = True
            self.laser_sound.play(-1)
        elif mouse_released[MOUSE_LEFT]:
            self.laserbool = False
            self.laser_sound.stop()

        if self.laserbool:
            for enemy in enemy_list:
                if enemy.rect.colliderect(self.attackrect):
                    enemy.hp -= self.laser_damage
                    if enemy.hp <= 0:
                        enemy.kill()

        if mouse_buttons[MOUSE_LEFT] and self.fuel > 0:
            self.fuel -= .2
        else:
            self.laserbool = False

        if mouse_buttons[MOUSE_RIGHT] and len(self.missiles) < self.missilecount and self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = PlayerMissile("missile.png", (self.rect.centerx, self.rect.y), self.attackrect)
            self.missiles.add(missile)
    
        keys = pygame.key.get_pressed()
        if keys[KEY_SPACE] and not self.spacial_used:
            self.spacial_used = True
            self.spacial_sound.play()
            for enemy in enemy_list:
                enemy.kill()
        self.attackrect.center = pygame.mouse.get_pos()

    def _update_attack_joystick(self, display_rect, joystick, enemy_list):
        # Attacks
        if joystick.get_button(JOY_BTN_LASER) and not self.laserbool:
            self.laserbool = True
            for enemy in enemy_list:
                if self.attackrect.colliderect(enemy):
                    enemy.hp -= 1
                    if enemy.hp < 0:
                        enemy.kill()
        else:
            self.laserbool = False

        if joystick.get_button(JOY_BTN_LASER) and self.fuel > 0:
            self.fuel -= .2
        else:
            self.laserbool = False

        if joystick.get_button(JOY_BTN_MISSILE) and len(self.missiles) < self.missilecount and self.missilecooldown == 0:
            self.missilecooldown = 50
            self.missilecount -= 1
            missile = PlayerMissile("missile.png", (self.rect.centerx, self.rect.y), self.attackrect)
            self.missiles.add(missile)

        for missile in self.missiles:
            for enemy in missile.get_collided_targets(enemy_list):
                enemy.hp -= 10
                break

        if joystick.get_axis(JOY_AXIS_SPACIAL) > 0 and not self.spacial_used:
            self.spacial_used = True
            for enemy in enemy_list:
                enemy.hp = 0

        # Attack rect velocity
        if round(joystick.get_axis(JOY_AXIS_ATTACK_X)) > 0:
            self.attackrect.x += 15
        elif int(joystick.get_axis(JOY_AXIS_ATTACK_X)) < 0:
            self.attackrect.x -= 15
        if round(joystick.get_axis(JOY_AXIS_ATTACK_Y)) > 0:
            self.attackrect.y += 15
        elif int(joystick.get_axis(JOY_AXIS_ATTACK_Y)) < 0:
            self.attackrect.y -= 15

    def draw(self, screen):
        """Draws the ship and its attacks."""
        if self.laserbool:
            rotated = pygame.transform.rotate(self.crosshair,-int(pygame.time.get_ticks())%360)
            r = rotated.get_rect(center = self.attackrect.center)
            screen.blit(rotated,r)
        else:
            r = self.crosshair.get_rect(center = self.attackrect.center)
            screen.blit(self.crosshair,r)
        if self.laserbool:
            self.laser(screen)
        # for missile in self.missiles:
        #     missile.draw(screen)
        self.missiles.draw(screen)

        screen.blit(self.image, (self.rect.x, self.rect.y))
# --- Player Missile Class ---
class PlayerMissile(pygame.sprite.Sprite):
    """Missile fired by the player, moves in a straight line toward the center of attackrect given at launch."""
    def __init__(self, image_path, position, attackrect):
        super().__init__()
        self.base_image = pygame.image.load("assets/images/player_missile.png").convert_alpha()
        self.explosion_sound = pygame.Sound("assets/audio/explosion.wav")
        self.missile_sound = pygame.Sound("assets/audio/missile.wav")
        self.missile_sound.set_volume(0.4)


        self.rect = self.base_image.get_rect(center=position)
        self.speed = 8
        # Calculate direction vector towards the center of attackrect
        target_x, target_y = attackrect.center
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            self.velocity = pygame.Vector2(0, self.speed)
        else:
            self.velocity = pygame.Vector2(dx / distance * self.speed, dy / distance * self.speed)
        self.missile_sound.play()
    def kill(self):
        super().kill()
        self.explosion_sound.play()
        self.missile_sound.stop()
    def get_collided_targets(self, targets):
        for target in targets :
            hitbox = pygame.Rect(0,0,150,70)
            hitbox.center = target.rect.center
            if self.rect.colliderect(hitbox):
                yield target

    def update(self, missiles, targets=None):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if targets:
            for target in self.get_collided_targets(targets):
                target.hp -= 10
                self.kill()

                if self in missiles:
                    missiles.remove(self)
                break
        self.image  = pygame.transform.rotate(self.base_image, self.velocity.angle_to(pygame.Vector2(0, -1)))
        self.rect = self.image.get_rect(center = self.rect.center)

    # def draw(self, screen):
        # screen.blit(rotated_image, (self.rect.x, self.rect.y))

class Star:
    def __init__(self, display_rect, static=False):
        self.color = (0, 0, 0)
        self.size = 1
        self.static = static
        if not static:
            self.pos = pygame.Vector2(random.randint(display_rect.centerx - 50, display_rect.centerx + 50), random.randint(display_rect.centery - 50, display_rect.centery + 50))

            self.velocity = [random.randint(0, 8)]
            self.velocity.append(8 - self.velocity[0])
            if self.pos.x < display_rect.centerx - 10:
                self.velocity[0] = -self.velocity[0]
            self.pos.x += self.velocity[0] * 60

            if self.pos.y < display_rect.centery - 10:
                self.velocity[1] = -self.velocity[1]
            self.pos.y += self.velocity[1] * 60
        else:
            self.pos = pygame.Vector2(random.randint(display_rect.x, display_rect.right), random.randint(display_rect.y, display_rect.bottom))
                
    def update(self, display_rect, player):
        if not self.static:
            dist = int(math.sqrt((self.pos.x - (display_rect.centerx + self.velocity[0]*60))**2 + (self.pos.y - (display_rect.centery + self.velocity[1]*60))**2))
            if dist > 255:
                dist = 255
            if dist > 200:
                self.size = 2
            self.color = (dist, dist, dist)
            self.pos.x += self.velocity[0]
            self.pos.y += self.velocity[1]
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