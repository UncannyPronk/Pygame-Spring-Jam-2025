import math
import pygame
import sys
import random
from pygame.locals import *
from objs import Ship, Star, Enemy,FastEnemy, SlowEnemy, MiniBoss, Boss
from dialogue_system import speak
from constants import *
FPS = 60

LEVELS = [
    [(FastEnemy,(100, 70),100,None)],
    [(FastEnemy,(100, 70),200,0.8), (SlowEnemy,(400, 150),200,None)],
    [(FastEnemy,(100, 70),250,0.8,0.4), (FastEnemy,(400, 150),250,1.2,0.5),(FastEnemy,(400, 220),250,1.2,0.7)],
    [(MiniBoss,(100, 150),None,None)],
    [(SlowEnemy,(400, 70),600,0.7,1.8), (SlowEnemy,(400, 150),600,0.7)],
    [(SlowEnemy,(400, 0),500,None,0.3),(FastEnemy,(100, 70),600,0.8,0.5),(SlowEnemy,(400, 150),450,None),(FastEnemy,(400, 220),400,1.2,1.3)],
    [(Boss,(400,190),None,None)],

]

spacial_used = False

class Game:
    def __init__(self, screen: pygame.Surface):
        global spacial_used
        self.screen = screen
        self.font = pygame.font.SysFont("monospace",24)
        self.clock = pygame.time.Clock()
        self.display_rect = self.screen.get_rect()
        self.player = Ship((self.display_rect.centerx, self.display_rect.bottom - 300), self.display_rect)
        if spacial_used:
            self.player.spacial_used = True
        self.stars = [Star(self.display_rect, True) for _ in range(120)]
        self.enemies = pygame.sprite.Group()
        self.controller_connected = False
        self.enemy_surf = pygame.image.load("assets/images/enemy.png").convert_alpha()
        self.enemy_surf = pygame.transform.scale_by(self.enemy_surf,1.5)
        self.keyboard_layout = "QWERTY"
        switch_to_qwerty()
        self.joy = None
        self.running = True
        self.level = 0
        self.state = "title"
        self.set_state("title")
        pygame.mixer.music.load("assets/audio/star_focus.mp3")
        pygame.mixer.music.play(-1,0,100)
        self.set_level(0)

    def set_level(self,level:int=0):
        if level >= len(LEVELS):
            self.set_state("win")
            return
        self.level = level
        had_boss = False
        if level >0:
            had_boss = any(c[0] in [MiniBoss,Boss] for c in LEVELS[level-1])
        self.enemies.empty()
        self.player.reset(self.display_rect.center if level==0 else self.player.rect.center,self.display_rect,level)
        has_boss = False
        for data in LEVELS[level]:
            cls = data[0]
            if not has_boss:
                has_boss = cls in [MiniBoss,Boss]
            
            pos = data[1]
            hp = data[2]
            power = data[3]
            speed = data[4] if len(data)>4 else None
            enemy : Enemy = cls(pos)
            if hp is not None:
                enemy.set_hp(hp)
            if power is not None:
                enemy.set_power_factor(power)
            if speed is not None:
                enemy.set_speed_factor(speed)
            self.enemies.add(enemy)
        if has_boss:
            pygame.mixer.music.load("assets/audio/boss.mp3")
            pygame.mixer.music.play(-1,0,100)
        elif had_boss:
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.queue("assets/audio/star_focus.mp3",loops=-1)


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.JOYDEVICEADDED:
                self.controller_connected = True
                self.joy = pygame.joystick.Joystick(event.device_index)
                self.player.attackrect.center = self.display_rect.center
            if event.type == pygame.JOYDEVICEREMOVED:
                self.controller_connected = False

    def update_stars(self):
        if random.randint(0, 1) == 0:
            if self.player.spacial_used and self.player.spacial_count == 0:
                self.stars.append(Star(self.display_rect))
            elif not self.player.spacial_used:
                self.stars.append(Star(self.display_rect))
        for star in self.stars[:]:
            star.update(self.display_rect, self.player)
            star_rect = pygame.Rect(star.pos.x, star.pos.y, star.size, star.size)
            if not self.display_rect.colliderect(star_rect):
                self.stars.remove(star)

    def update_enemies(self):
        for enemy in list(self.enemies):
            enemy.update(self.player)
            if hasattr(enemy, 'hp') and enemy.hp <= 0:
                self.enemies.remove(enemy)
        if len(self.enemies) == 0:
            if self.player.spacial_used and self.player.spacial_count > 0:
                return
            self.set_level(self.level+1)

    def draw_meter(self, color, rect, max_value, current_value):
        """Draws a meter based on the given color, rect, max value, and current value."""
        # Calculate the width of the filled portion of the meter
        filled_width = int(rect[2] * (current_value / max_value))
        
        # Draw the filled portion of the meter
        pygame.draw.rect(self.screen, color, (rect[0], rect[1], filled_width, rect[3]))
        
        # Draw the outline of the meter
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)


    def draw_status(self):
        self.draw_meter((255, 0, 0), pygame.Rect(20, 20, 500, 20), self.player.max_hp, self.player.hp)
        self.draw_meter((255, 255, 0), pygame.Rect(20, 50, 100, 20), self.player.max_fuel, self.player.fuel)
        self.draw_meter((255, 0, 255), pygame.Rect(20, 80, 50, 20), self.player.missile_max,self.player.missile_float)


        for i,enemy in enumerate(self.enemies):
            self.draw_meter(COLOR_DEEP_PURPLE,(self.display_rect.right-120,20+30*i,100,20),enemy.max_hp,enemy.hp)


        # self.screen.blit(self.font.render(str(self.player.target_angle),True,"white"))
        # self.label(self.display_rect.move(-50,20).topright,str(round(self.clock.get_fps())),'white')

    def draw(self):
        self.screen.fill((0, 0, 6))
        for star in self.stars:
            star.draw(self.screen)
        if self.player.spacial_used:
            if self.player.spacial_count > 480 and self.player.spacial_count % 2 == 0:
                self.screen.fill((255, 255, 255))
            if self.player.spacial_radius > self.display_rect.height / 2:
                self.player.spacial_radius -= 50
            if self.player.spacial_color > 0:
                self.player.spacial_color -= 2
            if self.player.spacial_color < 0:
                self.player.spacial_color = 0
            self.player.spacial_surface.fill((0, 255, 0))
            pygame.draw.circle(
                self.player.spacial_surface,
                (self.player.spacial_color,) * 3,
                (self.display_rect.centerx, self.display_rect.centery),
                int(self.player.spacial_radius)
            )
            self.player.spacial_surface.set_colorkey((0, 255, 0))
            if self.player.spacial_alpha > 0 and self.player.spacial_count == 0:
                self.player.spacial_alpha -= 1
            self.player.spacial_surface.set_alpha(self.player.spacial_alpha)
            self.screen.blit(self.player.spacial_surface, (0, 0))
        for enemy in self.enemies:
            enemy.draw(self.player, self.screen)
        self.player.draw(self.screen)

    def _game(self):
        global spacial_used
        if self.player.hp < 0:
            self.set_state("game over")
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_ESCAPE]:
            self.set_state("title")
        
        if self.player.spacial_used:
            spacial_used = True
        self.update_stars()
        self.player.update(self.controller_connected, self.display_rect, self.joy, self.enemies)
        self.update_enemies()
        self.draw()
        self.draw_status()
        self.label(self.display_rect.move(0,20).midtop,f"LEVEL {self.level+1}","white","black")

    def button(self, center, text, color, bgcolor=None, border_color=None, border_width=2, hover_color=(80, 80, 80), radius=8):
        """Draws a button, blits it, and returns pressed (True/False)."""
        inflate_width = 20  # Additional width to inflate the base rect
        inflate_height = 10  # Additional height to inflate the base rect

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_just_pressed()[0]
        surf = self.font.render(text, True, color)
        rect = surf.get_rect(center=center)
        rect.inflate_ip(inflate_width, inflate_height)  # Inflate the rect

        button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        button_rect = button_surf.get_rect(center=center)

        # Draw background
        if bgcolor:
            pygame.draw.rect(button_surf, bgcolor, button_surf.get_rect(), border_radius=radius)
        # Draw border
        if border_color:
            pygame.draw.rect(button_surf, border_color, button_surf.get_rect(), border_width, border_radius=radius)
        # Draw text
        button_surf.blit(surf, ((rect.width - surf.get_width()) // 2, (rect.height - surf.get_height()) // 2))

        hovered = button_rect.collidepoint(mouse_pos)
        pressed = click and hovered

        # Hover effect
        if hovered:
            hover_overlay = pygame.Surface(button_surf.get_size(), pygame.SRCALPHA)
            hover_overlay.fill((*hover_color, 80))
            button_surf.blit(hover_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        self.screen.blit(button_surf, button_rect)
        return pressed

    def label(self, center, text, color, bgcolor=None, radius=0, border_color=None, border_width=0):
        """Draws a non-interactive label and blits it."""
        surf = self.font.render(text, True, color, bgcolor)
        rect = surf.get_rect(center=center)
        if bgcolor or border_color:
            label_surf = pygame.Surface((rect.width + 10, rect.height + 6), pygame.SRCALPHA)
            label_rect = label_surf.get_rect(center=center)
            if bgcolor:
                pygame.draw.rect(label_surf, bgcolor, label_surf.get_rect(), border_radius=radius)
            if border_color and border_width > 0:
                pygame.draw.rect(label_surf, border_color, label_surf.get_rect(), border_width, border_radius=radius)
            label_surf.blit(surf, (5, 3))
            self.screen.blit(label_surf, label_rect)
        else:
            self.screen.blit(surf, rect)

    def _title(self):
        title_surf = self.font.render("SPACE E-RACER", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.display_rect.centerx, 100))
        self.screen.blit(title_surf, title_rect)
        r = self.enemy_surf.get_rect(center=  self.display_rect.move(0,-150).center)
        r.y += - 10 * math.cos(pygame.time.get_ticks()/300)
        self.screen.blit(self.enemy_surf,r)

        play_pressed = self.button(
            self.display_rect.center,
            "Play",
            "white",
            COLOR_GREEN
        )

        options_pressed = self.button(
            self.display_rect.move(0, 50).center,
            "Options",
            "white",
            COLOR_TEAL
        )


        credits_pressed = self.button(
            self.display_rect.move(0,100).center,
            "Credits",
            "white",
            COLOR_BLUE
        )

        instructions_pressed = self.button(
            self.display_rect.move(0, 150).center,
            "Instructions",
            "white",
            COLOR_DEEP_ORANGE
        )


        quit_pressed = self.button(
            self.display_rect.move(0,200).center,
            "Quit",
            "white",
            COLOR_RED
        )

        if instructions_pressed:
            self.set_state("instructions")

        if credits_pressed:
            self.set_state("credits")
        if options_pressed:
            self.set_state("options")
        if play_pressed or (self.joy and self.joy.get_button(JOY_BTN_LASER)):
            self.set_state("game")

        if quit_pressed:
            self.running = False

    def _credits(self):
        credits_surf = self.font.render("Credits", True, (255, 255, 255))
        credits_rect = credits_surf.get_rect(center=(self.display_rect.centerx, 100))
        self.screen.blit(credits_surf, credits_rect)

        self.label(self.display_rect.center,"Jana",COLOR_AMBER)
        self.label(self.display_rect.move(0,50).center,"Baturay",COLOR_CYAN)

        back_pressed = self.button(
            self.display_rect.move(0,100).center,
            "Back",
            "white",
            COLOR_BLUE
        )

        if back_pressed:
            self.set_state("title")

    def _game_over(self):
        game_over_surf = self.font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(self.display_rect.centerx, 100))
        self.screen.blit(game_over_surf, game_over_rect)

        retry_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery - 50),
            "Retry",
            "white",
            COLOR_GREEN
        )

        title = self.button(
            (self.display_rect.centerx, self.display_rect.centery),
            "Title screen",
            "white",
            COLOR_BLUE
        )


        quit_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery + 50),
            "Quit",
            "white",
            COLOR_RED
        )

        if retry_pressed:
            self.set_state("game")

        if title:
            self.set_state("title")
        if quit_pressed:
            self.running = False

    def _win(self):
        win_surf = self.font.render("You Win!", True, (0, 255, 0))
        win_rect = win_surf.get_rect(center=(self.display_rect.centerx, 100))
        self.screen.blit(win_surf, win_rect)

        back_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery + 50),
            "Back to Title",
            "white",
            COLOR_BLUE
        )

        if back_pressed:
            self.set_state("title")


    def _options(self):
        fullscreen_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery - 50),
            "Toggle Fullscreen",
            "white",
            COLOR_GREEN
        )

        layout_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery),
            f"LAYOUT : {self.keyboard_layout}",
            "white",
            COLOR_DEEP_ORANGE
        )

        back_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery + 50),
            "Back",
            "white",
            COLOR_BLUE
        )

        if fullscreen_pressed:
            pygame.display.toggle_fullscreen()

        if layout_pressed:
            self.keyboard_layout = "AZERTY" if self.keyboard_layout == "QWERTY" else "QWERTY"
            if self.keyboard_layout == "AZERTY":
                switch_to_azerty()
            else:
                switch_to_qwerty()

        if back_pressed:
            self.set_state("title")

    def _instructions(self):
        instructions = [
            "Instructions:",
            "Move: WASD or Left Stick",
            "Boost: Shift or RT",
            "Aim: Mouse or Right Stick",
            "Laser: Left Click or RB",
            "Missile: Right Click or LB",
            "Special: Space or LT",
            "Avoid enemy fire.",
            "Clear all enemies to advance.",
            "Defeat the boss to win."
        ]


        y_offset = 100
        for line in instructions:
            self.label(
                (self.display_rect.centerx, y_offset),
                line,
                "white"
            )
            y_offset += 40

        back_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery + 200),
            "Back",
            "white",
            COLOR_BLUE
        )

        if back_pressed:
            self.set_state("title")

    def set_state(self,state):
        if self.state == "game" and state !="game":
            pygame.mixer.music.load("assets/audio/star_focus.mp3")
            pygame.mixer.music.play(-1)
        self.state = state
        self.player.laser_sound.stop()

        if state == "game":
            self.set_level(0)
            self.stars = [Star(self.display_rect, True) for _ in range(120)]

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill((0,0,0))
            if self.state == "game":
                self._game()
            elif self.state == "instructions":
                self._instructions()
            elif self.state == "title":
                self._title()
            elif self.state == "credits":
                self._credits()
            elif self.state == "game over":
                self._game_over()
            elif self.state == "win":
                self._win()
            elif self.state == "options":
                self._options()
            pygame.display.flip()
            self.clock.tick(FPS)
