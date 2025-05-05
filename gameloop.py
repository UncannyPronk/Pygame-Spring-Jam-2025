import pygame
import sys
import random
from pygame.locals import *
from objs import Ship, Star, FastEnemy, SlowEnemy
from dialogue_system import speak
from constants import *
FPS = 60

LEVELS = [
    [(FastEnemy,(100, 70),20,None)],
    [(FastEnemy,(100, 70),800,0.8), (SlowEnemy,(400, 150),None,None)],
    [(FastEnemy,(100, 70),None,None), (SlowEnemy,(400, 150),None,None)],

]


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("monospace",24)
        self.clock = pygame.time.Clock()
        self.display_rect = self.screen.get_rect()
        self.player = Ship((self.display_rect.centerx, self.display_rect.bottom - 300), self.display_rect)
        self.stars = [Star(self.display_rect, True) for _ in range(120)]
        self.enemies = pygame.sprite.Group()
        self.controller_connected = False
        self.joy = None
        self.running = True
        self.level = 0
        self.state = "title"
        pygame.mixer.music.load("assets/audio/star_focus.mp3")
        pygame.mixer.music.play(-1)
        self.set_level(0)

    def set_level(self,level:int=0):
        if level >= len(LEVELS):
            self.state = "win"
            return
        self.level = level
        
        self.enemies.empty()
        self.player.reset(self.display_rect.center if level==0 else self.player.rect.center,self.display_rect)
        for data in LEVELS[level]:
            cls = data[0]
            pos = data[1]
            hp = data[2]
            power = data[3]
            
            enemy = cls(pos)
            if hp is not None:
                enemy.set_hp(hp)
            if power is not None:
                enemy.set_power_factor(power)
            self.enemies.add(enemy)



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

        for i,enemy in enumerate(self.enemies):
            self.draw_meter(COLOR_DEEP_PURPLE,(self.display_rect.right-120,20+30*i,100,20),enemy.max_hp,enemy.hp)


        # self.screen.blit(self.font.render(str(self.player.target_angle),True,"white"))
        self.label(self.display_rect.move(-50,-20).topright,str(round(self.clock.get_fps())),'white')

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
        if self.player.hp < 0:
            self.state = "game over"
        self.update_stars()
        self.player.update(self.controller_connected, self.display_rect, self.joy, self.enemies)
        self.update_enemies()
        self.draw()
        self.draw_status()
        self.label(self.display_rect.move(0,10).midtop,f"LEVEL {self.level}","white",None)

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
        title_surf = self.font.render("Spring Jam 2025", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.display_rect.centerx, 100))
        self.screen.blit(title_surf, title_rect)


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

        quit_pressed = self.button(
            self.display_rect.move(0,150).center,
            "Quit",
            "white",
            COLOR_RED
        )

        if credits_pressed:
            self.state = "credits"
        if options_pressed:
            self.state = "options"
        if play_pressed or (self.joy and self.joy.get_button(JOY_BTN_LASER)):
            self.state = "game"
            self.set_level(0)
            self.stars = [Star(self.display_rect, True) for _ in range(120)]

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
            self.state = "title"

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
            self.state = "game"
            self.set_level(0)
            self.stars = [Star(self.display_rect, True) for _ in range(120)]
        if title:
            self.state = "title"
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
            self.state = "title"


    def _options(self):
        fullscreen_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery - 50),
            "Toggle Fullscreen",
            "white",
            COLOR_GREEN
        )

        back_pressed = self.button(
            (self.display_rect.centerx, self.display_rect.centery + 50),
            "Back",
            "white",
            COLOR_BLUE
        )

        if fullscreen_pressed:
            pygame.display.toggle_fullscreen()

        if back_pressed:
            self.state = "title"

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.fill((0,0,0))
            if self.state == "game":
                self._game()
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
