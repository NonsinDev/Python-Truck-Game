import os
import pygame

from game.constants import *

# Absolute path to the assets/ folder, independent of the working directory
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "assets")


class MenuRenderer:

    def __init__(self, screen, width, height, font, large_font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.large_font = large_font

        # Scale background to screen size (.convert() for performance, no transparency needed)
        bg_raw = pygame.image.load(os.path.join(ASSETS_DIR, "menu_bg.png")).convert()
        self.bg = pygame.transform.scale(bg_raw, (width, height))

        # Logo: fixed width, height calculated proportionally (.convert_alpha() for transparency)
        logo_raw = pygame.image.load(os.path.join(ASSETS_DIR, "menu_title.png")).convert_alpha()
        logo_w = 550
        logo_h = int(logo_raw.get_height() * logo_w / logo_raw.get_width())
        self.logo = pygame.transform.scale(logo_raw, (logo_w, logo_h))

        # Truck: 130% of one third of the screen width, height proportional
        truck_raw = pygame.image.load(os.path.join(ASSETS_DIR, "menu_truck.png")).convert_alpha()
        truck_w = int((width // 3) * 1.3)
        truck_h = int(truck_raw.get_height() * truck_w / truck_raw.get_width())
        self.truck = pygame.transform.scale(truck_raw, (truck_w, truck_h))

    def draw_menu(self, btn_play, btn_quit):
        self.screen.blit(self.bg, (0, 0))

        # Logo centered near top
        logo_rect = self.logo.get_rect(center=(self.width // 2 , 160))
        self.screen.blit(self.logo, logo_rect)

        # Truck centered at bottom
        truck_rect = self.truck.get_rect(midbottom=(self.width // 2 + 125, self.height + 80))
        self.screen.blit(self.truck, truck_rect)

        btn_play.draw(self.screen)
        btn_quit.draw(self.screen)

    def draw_settings(self, game):
        self.screen.fill(DARK_GRAY)
        title = self.large_font.render("SELECT MODE", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 50)))

        pygame.draw.rect(self.screen, (40, 40, 40), (30, 100, 260, self.height - 200))
        label_modes = self.font.render("Game Modes", True, YELLOW)
        self.screen.blit(label_modes, (50, 120))

        for mode_name, btn in game.mode_buttons.items():
            if mode_name == game.current_mode:
                pygame.draw.rect(self.screen, YELLOW, btn.rect.inflate(10, 10), 3)
            btn.draw(self.screen)

        pygame.draw.rect(self.screen, (50, 50, 50), (310, 100, self.width - 340, self.height - 200))
        label_settings = self.font.render("Settings (click to change)", True, YELLOW)
        self.screen.blit(label_settings, (330, 120))
        hint = self.font.render("Adjust values with + and -", True, WHITE)
        self.screen.blit(hint, (330, 155))

        start_y = 200
        game.plus_buttons = []
        game.minus_buttons = []
        for i, key in enumerate(game.settings_keys):
            val = game.config[key]
            text = self.font.render(f"{key}: {val}", True, WHITE)
            self.screen.blit(text, text.get_rect(topleft=(330, start_y + i * 40)))

            btn_size = 30
            m_rect = pygame.Rect(self.width - 120, start_y + i * 40 - 2, btn_size, btn_size)
            p_rect = pygame.Rect(self.width - 80,  start_y + i * 40 - 2, btn_size, btn_size)
            game.minus_buttons.append(m_rect)
            game.plus_buttons.append(p_rect)

            m_color = RED if m_rect.collidepoint(game.mouse_pos) else (150, 50, 50)
            pygame.draw.rect(self.screen, m_color, m_rect)
            m_label = self.font.render("-", True, WHITE)
            self.screen.blit(m_label, m_label.get_rect(center=m_rect.center))

            p_color = GREEN if p_rect.collidepoint(game.mouse_pos) else (50, 150, 50)
            pygame.draw.rect(self.screen, p_color, p_rect)
            p_label = self.font.render("+", True, WHITE)
            self.screen.blit(p_label, p_label.get_rect(center=p_rect.center))

        game.btn_back.draw(self.screen)
        game.btn_start_game.draw(self.screen)
