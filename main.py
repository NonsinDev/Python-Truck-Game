import pygame
import sys
import os
import json

from game.constants import *
from game.button import Button
from game.truck import Truck
from game.helicopter import Helicopter
from game.building import Building

CONFIG_FILE = "config.json"
DEFAULT_CONFIG_FILE = "default_config.json"


def load_game_modes():
    with open(DEFAULT_CONFIG_FILE, "r") as f:
        return json.load(f)


GAME_MODES = load_game_modes()


def load_config():
    default = GAME_MODES["Normal"]
    if not os.path.exists(CONFIG_FILE):
        save_config(default)
        return default.copy()
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            # Fill in any missing keys with defaults
            for key, value in default.items():
                if key not in cfg:
                    cfg[key] = value
            return cfg
    except:
        return default.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)


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

        self.config = load_config()
        self.state = STATE_MENU

        self.truck = None
        self.helicopter = None
        self.score = 0
        self.message = ""
        self.message_timer = 0
        self.current_mode = "Normal"
        self.mouse_pos = (0, 0)
        self.debug_mode = False

        # Buildings
        self.gas_station = Building(20, 20, 160, 100, YELLOW, "Gas Station")
        self.warehouse = Building(self.width - 180, 20, 160, 100, RED, "Warehouse")
        self.delivery = Building(self.width - 180, self.height - 120, 160, 100, GREEN, "Delivery")

        # Main menu buttons
        self.btn_play = Button(self.width // 2 - 100, 250, 200, 60, "Play", self.font, WHITE, YELLOW)
        self.btn_quit = Button(self.width // 2 - 100, 350, 200, 60, "Quit", self.font, WHITE, RED)

        # Settings screen buttons
        self.btn_start_game = Button(self.width - 250, self.height - 80, 200, 50, "Start Game", self.font, WHITE, GREEN)
        self.btn_back = Button(50, self.height - 80, 250, 50, "Back to Menu", self.font, WHITE, YELLOW)
        self.btn_ingame_menu = Button(self.width - 160, self.height - 60, 150, 40, "Menu", self.font, WHITE, YELLOW)

        # Mode buttons
        self.mode_buttons = {}
        modes = ["Easy", "Normal", "Hard", "Custom"]
        for i, mode in enumerate(modes):
            self.mode_buttons[mode] = Button(50, 160 + i * 70, 220, 50, mode, self.font, WHITE, BLUE)

        self.settings_keys = list(GAME_MODES["Normal"].keys())
        self.plus_buttons = []
        self.minus_buttons = []
        self.running = True

    def reset_game(self):
        self.truck = Truck(150, 110, self.config)
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
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == STATE_MENU:
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
                                save_config(self.config)

                    # Adjust settings via plus/minus buttons
                    for i, (p_rect, m_rect) in enumerate(zip(self.plus_buttons, self.minus_buttons)):
                        clicked_plus = p_rect.collidepoint(self.mouse_pos)
                        clicked_minus = m_rect.collidepoint(self.mouse_pos)

                        if clicked_plus or clicked_minus:
                            self.current_mode = "Custom"
                            key = self.settings_keys[i]
                            val = self.config[key]

                            if isinstance(val, bool):
                                self.config[key] = not val
                            else:
                                if clicked_minus:
                                    if isinstance(val, int):
                                        self.config[key] = max(1, val - 1)
                                    else:
                                        self.config[key] = round(max(0.01, val - 0.1), 2)
                                elif clicked_plus:
                                    if isinstance(val, int):
                                        self.config[key] = val + 1
                                    else:
                                        self.config[key] = round(val + 0.1, 2)
                            save_config(self.config)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_back.is_hovered:
                        save_config(self.config)
                        self.state = STATE_MENU

            elif self.state in [STATE_GAME_OVER, STATE_WIN]:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_back.is_hovered:
                        self.state = STATE_MENU

            elif self.state == STATE_PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_ingame_menu.is_hovered:
                        self.state = STATE_MENU

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

            if truck_rect.colliderect(self.gas_station.rect):
                if self.truck.fuel < 100:
                    self.truck.fuel += 1
                    if self.truck.fuel > 100:
                        self.truck.fuel = 100
                    self.message = "Refueling..."
                    self.message_timer = 10

            elif truck_rect.colliderect(self.warehouse.rect):
                self.truck.cargo = self.truck.max_cargo
                self.message = "Cargo loaded!"
                self.message_timer = 90

            elif truck_rect.colliderect(self.delivery.rect):
                if self.truck.cargo > 0:
                    delivered = self.truck.cargo
                    self.score += delivered
                    self.truck.cargo = 0
                    self.message = f"Cargo delivered! +{delivered} points"
                    self.message_timer = 90

            # Check win/lose conditions
            if self.score >= self.config["win_ore_amount"]:
                self.state = STATE_WIN
            if self.helicopter.total_stolen >= self.config["fail_stolen_amount"]:
                self.state = STATE_GAME_OVER

            self.btn_ingame_menu.check_hover(self.mouse_pos)

        elif self.state in [STATE_WIN, STATE_GAME_OVER]:
            self.btn_back.check_hover(self.mouse_pos)

    def draw_background(self):
        # Green background (grass)
        self.screen.fill(DARK_GREEN)

        # Draw roads
        pygame.draw.rect(self.screen, GRAY, (130, 90, 640, 40))
        pygame.draw.rect(self.screen, GRAY, (130, 90, 40, 400))
        pygame.draw.rect(self.screen, GRAY, (130, 450, 640, 40))

        # Draw road markings
        for x in range(130, 770, 40):
            pygame.draw.rect(self.screen, WHITE, (x, 108, 20, 4))
            pygame.draw.rect(self.screen, WHITE, (x, 468, 20, 4))
        for y in range(90, 490, 40):
            pygame.draw.rect(self.screen, WHITE, (148, y, 4, 20))

    def draw(self):
        if self.state == STATE_MENU:
            self.screen.fill(BLUE)
            title = self.large_font.render("CARGO CLASH: SKY HEIST", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 100)))
            self.btn_play.draw(self.screen)
            self.btn_quit.draw(self.screen)

        elif self.state == STATE_SETTINGS:
            self.screen.fill(DARK_GRAY)
            title = self.large_font.render("SELECT MODE", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(self.width // 2, 50)))

            # Left side: mode buttons
            pygame.draw.rect(self.screen, (40, 40, 40), (30, 100, 260, self.height - 200))
            label_modes = self.font.render("Game Modes", True, YELLOW)
            self.screen.blit(label_modes, (50, 120))

            for mode_name, btn in self.mode_buttons.items():
                if mode_name == self.current_mode:
                    pygame.draw.rect(self.screen, YELLOW, btn.rect.inflate(10, 10), 3)
                btn.draw(self.screen)

            # Right side: settings
            pygame.draw.rect(self.screen, (50, 50, 50), (310, 100, self.width - 340, self.height - 200))
            label_settings = self.font.render("Settings (click to change)", True, YELLOW)
            self.screen.blit(label_settings, (330, 120))

            hint = self.font.render("Adjust values with + and -", True, WHITE)
            self.screen.blit(hint, (330, 155))

            start_y = 200
            self.plus_buttons = []
            self.minus_buttons = []
            for i, key in enumerate(self.settings_keys):
                val = self.config[key]
                text = self.font.render(f"{key}: {val}", True, WHITE)
                rect = text.get_rect(topleft=(330, start_y + i * 40))
                self.screen.blit(text, rect)

                btn_size = 30
                m_rect = pygame.Rect(self.width - 120, start_y + i * 40 - 2, btn_size, btn_size)
                p_rect = pygame.Rect(self.width - 80, start_y + i * 40 - 2, btn_size, btn_size)

                self.minus_buttons.append(m_rect)
                self.plus_buttons.append(p_rect)

                m_color = RED if m_rect.collidepoint(self.mouse_pos) else (150, 50, 50)
                pygame.draw.rect(self.screen, m_color, m_rect)
                m_label = self.font.render("-", True, WHITE)
                self.screen.blit(m_label, m_label.get_rect(center=m_rect.center))

                p_color = GREEN if p_rect.collidepoint(self.mouse_pos) else (50, 150, 50)
                pygame.draw.rect(self.screen, p_color, p_rect)
                p_label = self.font.render("+", True, WHITE)
                self.screen.blit(p_label, p_label.get_rect(center=p_rect.center))

            self.btn_back.draw(self.screen)
            self.btn_start_game.draw(self.screen)

        elif self.state == STATE_PLAYING:
            self.draw_background()
            self.gas_station.draw(self.screen, self.font)
            self.warehouse.draw(self.screen, self.font)
            self.delivery.draw(self.screen, self.font)

            self.truck.draw(self.screen)
            if self.helicopter:
                self.helicopter.draw(self.screen)

            # Score and cargo display
            ui_text = self.font.render(
                f"Score: {self.score}/{self.config['win_ore_amount']} | Cargo: {self.truck.cargo}/{self.truck.max_cargo}",
                True, WHITE
            )
            ui_bg = ui_text.get_rect(topleft=(10, 10)).inflate(20, 10)
            pygame.draw.rect(self.screen, BLACK, ui_bg)
            self.screen.blit(ui_text, (20, 15))

            # Helicopter theft display
            heli_text = self.font.render(
                f"Stolen: {self.helicopter.total_stolen}/{self.config['fail_stolen_amount']}",
                True, RED
            )
            heli_bg = heli_text.get_rect(topright=(self.width - 10, 10)).inflate(20, 10)
            pygame.draw.rect(self.screen, BLACK, heli_bg)
            self.screen.blit(heli_text, heli_bg.move(10, 5))

            if self.message_timer > 0:
                msg_surface = self.font.render(self.message, True, WHITE)
                msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height - 40))
                bg_rect = msg_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, BLACK, bg_rect)
                self.screen.blit(msg_surface, msg_rect)
                self.message_timer -= 1

            if self.truck.fuel <= 0:
                no_fuel = self.font.render("Out of fuel!", True, RED)
                text_pos = no_fuel.get_rect(center=(self.width // 2, self.height // 2))
                bg_rect = text_pos.inflate(20, 20)
                pygame.draw.rect(self.screen, BLACK, bg_rect)
                self.screen.blit(no_fuel, text_pos)

            self.btn_ingame_menu.draw(self.screen)

            if self.debug_mode:
                debug_lines = [
                    f"DEBUG MODE",
                    f"Truck x={self.truck.x:.1f} y={self.truck.y:.1f}",
                    f"Speed={self.truck.speed:.2f}  Angle={self.truck.angle:.1f}",
                    f"Fuel={self.truck.fuel:.1f}  Cargo={self.truck.cargo}/{self.truck.max_cargo}",
                    f"Heli state={self.helicopter.state}  Stolen={self.helicopter.total_stolen}",
                    f"Score={self.score}/{self.config['win_ore_amount']}",
                ]
                debug_font = pygame.font.Font(None, 24)
                for i, line in enumerate(debug_lines):
                    text_surf = debug_font.render(line, True, ORANGE)
                    self.screen.blit(text_surf, (10, self.height - 165 + i * 20))

        elif self.state == STATE_WIN:
            self.screen.fill(GREEN)
            win_text = self.large_font.render("YOU WIN!", True, BLACK)
            self.screen.blit(win_text, win_text.get_rect(center=(self.width // 2, self.height // 2 - 50)))
            self.btn_back.draw(self.screen)

        elif self.state == STATE_GAME_OVER:
            self.screen.fill(RED)
            lose_text = self.large_font.render("GAME OVER!", True, BLACK)
            desc = self.font.render("The helicopter stole too much cargo!", True, BLACK)
            self.screen.blit(lose_text, lose_text.get_rect(center=(self.width // 2, self.height // 2 - 50)))
            self.screen.blit(desc, desc.get_rect(center=(self.width // 2, self.height // 2 + 10)))
            self.btn_back.draw(self.screen)

        pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()
