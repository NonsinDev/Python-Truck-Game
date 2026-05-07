import pygame
import sys

from game.constants import *
from game.button import Button
from game.truck import Truck
from game.helicopter import Helicopter
from game.config import GAME_MODES
from game.menu.renderer import MenuRenderer
from game.map import GameMap
from game.renderer import GameRenderer


class Game:
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Cargo Clash: Sky Heist")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

        self.config = GAME_MODES["Normal"].copy()
        self.state = STATE_MENU

        self.truck = None
        self.helicopter = None
        self.score = 0
        self.message = ""
        self.message_timer = 0
        self.current_mode = "Normal"
        self.mouse_pos = (0, 0)
        self.debug_mode = False

        self.game_map = GameMap(self.width, self.height)
        self.menu_renderer = MenuRenderer(self.screen, self.width, self.height, self.font, self.large_font)
        self.game_renderer = GameRenderer(self.screen, self.width, self.height, self.font, self.large_font)

        # Main menu buttons
        self.btn_play = Button(self.width // 2 - 100, 250, 200, 60, "Play", self.font, WHITE, YELLOW)
        self.btn_quit = Button(self.width // 2 - 100, 350, 200, 60, "Quit", self.font, WHITE, RED)

        # Settings screen buttons
        self.btn_start_game = Button(self.width - 250, self.height - 80, 200, 50, "Start Game", self.font, WHITE, GREEN)
        self.btn_back = Button(50, self.height - 80, 250, 50, "Back to Menu", self.font, WHITE, YELLOW)

        # Pause menu buttons
        self.btn_pause_continue = Button(self.width // 2 - 100, 180, 200, 60, "Continue",  self.font, WHITE, GREEN)
        self.btn_pause_reset    = Button(self.width // 2 - 100, 260, 200, 60, "Reset",     self.font, WHITE, ORANGE)
        self.btn_pause_menu     = Button(self.width // 2 - 100, 340, 200, 60, "Main Menu", self.font, WHITE, YELLOW)
        self.btn_pause_quit     = Button(self.width // 2 - 100, 420, 200, 60, "Quit",      self.font, WHITE, RED)

        # Mode buttons
        self.mode_buttons = {}
        for i, mode in enumerate(["Easy", "Normal", "Hard", "Custom"]):
            self.mode_buttons[mode] = Button(50, 160 + i * 70, 220, 50, mode, self.font, WHITE, BLUE)

        self.settings_keys = list(GAME_MODES["Normal"].keys())
        self.plus_buttons = []
        self.minus_buttons = []
        self.running = True

    def reset_game(self):
        self.game_map.generate()
        self.truck = Truck(self.width // 2, self.height // 2, self.config)
        self.score = 0
        self.helicopter = Helicopter(self.config)
        self.message = "Move the truck with W, A, S, D"
        self.message_timer = 180

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        self.mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif self.state == STATE_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_play.is_hovered:
                        self.state = STATE_SETTINGS
                    elif self.btn_quit.is_hovered:
                        self.running = False

            elif self.state == STATE_SETTINGS:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_start_game.is_hovered:
                        keys = pygame.key.get_pressed()
                        self.debug_mode = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif self.btn_back.is_hovered:
                        self.state = STATE_MENU

                    for mode_name, btn in self.mode_buttons.items():
                        if btn.is_hovered:
                            self.current_mode = mode_name
                            if mode_name in GAME_MODES:
                                self.config = GAME_MODES[mode_name].copy()

                    for i, (p_rect, m_rect) in enumerate(zip(self.plus_buttons, self.minus_buttons)):
                        clicked_plus = p_rect.collidepoint(self.mouse_pos)
                        clicked_minus = m_rect.collidepoint(self.mouse_pos)
                        if clicked_plus or clicked_minus:
                            self.current_mode = "Custom"
                            key = self.settings_keys[i]
                            val = self.config[key]
                            if isinstance(val, bool):
                                self.config[key] = not val
                            elif clicked_minus:
                                if isinstance(val, int):
                                    self.config[key] = max(1, val - 1)
                                else:
                                    self.config[key] = round(max(0.01, val - 0.1), 2)
                            elif clicked_plus:
                                if isinstance(val, int):
                                    self.config[key] = val + 1
                                else:
                                    self.config[key] = round(val + 0.1, 2)

            elif self.state in (STATE_GAME_OVER, STATE_WIN):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_back.is_hovered:
                        self.state = STATE_MENU

            elif self.state == STATE_PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = STATE_PAUSED

            elif self.state == STATE_PAUSED:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = STATE_PLAYING
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_pause_continue.is_hovered:
                        self.state = STATE_PLAYING
                    elif self.btn_pause_reset.is_hovered:
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif self.btn_pause_menu.is_hovered:
                        self.state = STATE_MENU
                    elif self.btn_pause_quit.is_hovered:
                        self.running = False

    def update(self):
        if self.state == STATE_MENU:
            self.btn_play.check_hover(self.mouse_pos)
            self.btn_quit.check_hover(self.mouse_pos)

        elif self.state == STATE_SETTINGS:
            self.btn_start_game.check_hover(self.mouse_pos)
            self.btn_back.check_hover(self.mouse_pos)
            for btn in self.mode_buttons.values():
                btn.check_hover(self.mouse_pos)

        elif self.state == STATE_PLAYING:
            keys = pygame.key.get_pressed()
            self.truck.update(keys, self.width, self.height)
            self.helicopter.update(self.truck)

            truck_rect = pygame.Rect(
                self.truck.x - self.truck.width // 2,
                self.truck.y - self.truck.height // 2,
                self.truck.width,
                self.truck.height
            )

            if truck_rect.colliderect(self.game_map.gas_station.rect):
                if self.truck.fuel < 100:
                    self.truck.fuel = min(100, self.truck.fuel + 1)
                    self.message = "Refueling..."
                    self.message_timer = 10
            elif truck_rect.colliderect(self.game_map.warehouse.rect):
                self.truck.cargo = self.truck.max_cargo
                self.message = "Cargo loaded!"
                self.message_timer = 90
            elif truck_rect.colliderect(self.game_map.delivery.rect):
                if self.truck.cargo > 0:
                    delivered = self.truck.cargo
                    self.score += delivered
                    self.truck.cargo = 0
                    self.message = f"Cargo delivered! +{delivered} points"
                    self.message_timer = 90

            if self.score >= self.config["win_ore_amount"]:
                self.state = STATE_WIN
            if self.helicopter.total_stolen >= self.config["fail_stolen_amount"]:
                self.state = STATE_GAME_OVER

        elif self.state == STATE_PAUSED:
            self.btn_pause_continue.check_hover(self.mouse_pos)
            self.btn_pause_reset.check_hover(self.mouse_pos)
            self.btn_pause_menu.check_hover(self.mouse_pos)
            self.btn_pause_quit.check_hover(self.mouse_pos)

        elif self.state in (STATE_WIN, STATE_GAME_OVER):
            self.btn_back.check_hover(self.mouse_pos)

    def draw(self):
        if self.state == STATE_MENU:
            self.menu_renderer.draw_menu(self.btn_play, self.btn_quit)
        elif self.state == STATE_SETTINGS:
            self.menu_renderer.draw_settings(self)
        elif self.state == STATE_PLAYING:
            self.game_renderer.draw_playing(self)
        elif self.state == STATE_PAUSED:
            self.game_renderer.draw_paused(self)
        elif self.state == STATE_WIN:
            self.game_renderer.draw_win(self.btn_back)
        elif self.state == STATE_GAME_OVER:
            self.game_renderer.draw_game_over(self.btn_back)
        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
