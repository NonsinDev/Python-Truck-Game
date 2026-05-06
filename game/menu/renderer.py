import os
import pygame

from game.constants import *


class MenuRenderer:
    # --- LKW-Bild ---
    TRUCK_OFFSET_X = 0    # horizontaler Versatz vom Zentrum (positiv = rechts)
    TRUCK_OFFSET_Y = 150  # Y-Position von oben

    # --- Titel-Bild ---
    TITLE_SCALE = 8.0  # Skalierungsfaktor (1.0 = Originalgröße)
    TITLE_Y     = 140  # Y-Mitte des Titelbildes

    def __init__(self, screen, width, height, font, large_font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.large_font = large_font

        # Titelbild (ersetzt den Text)
        self.menu_title = None
        for ext in ("png", "jpg", "jpeg", "bmp"):
            img_path = os.path.join("assets", f"menu_title.{ext}")
            if os.path.exists(img_path):
                raw = pygame.image.load(img_path).convert_alpha()
                if self.TITLE_SCALE != 1.0:
                    w = int(raw.get_width() * self.TITLE_SCALE)
                    h = int(raw.get_height() * self.TITLE_SCALE)
                    raw = pygame.transform.scale(raw, (w, h))
                self.menu_title = raw
                break

    def draw_menu(self, background, btn_play, btn_quit):
        if not background.draw(self.screen):
            self.screen.fill(BLUE)
        if background.menu_truck:
            truck = background.menu_truck
            x = (self.width - truck.get_width()) // 2 + self.TRUCK_OFFSET_X
            self.screen.blit(truck, (x, self.TRUCK_OFFSET_Y))
        if self.menu_title:
            self.screen.blit(self.menu_title, self.menu_title.get_rect(center=(self.width // 2, self.TITLE_Y)))
        else:
            title = self.large_font.render("CARGO CLASH: SKY HEIST", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, self.TITLE_Y)))
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
