import pygame
import sys
import os
import json

# Game Configuration
CONFIG_FILE = "config.json"

GAME_MODES = {
    "Leicht": {
        "max_speed": 8.0,
        "fuel_consumption": 0.01,
        "max_cargo": 15,
        "win_ore_amount": 50,
        "fail_stolen_amount": 100,
        "heli_speed": 2.0,
        "heli_steal_amount": 3,
        "heli_leaves": True
    },

    "Normal": {
        "max_speed": 6.0,
        "fuel_consumption": 0.03,
        "max_cargo": 10,
        "win_ore_amount": 100,
        "fail_stolen_amount": 50,
        "heli_speed": 3.0,
        "heli_steal_amount": 5,
        "heli_leaves": True
    },

    "Schwer": {
        "max_speed": 4.0,
        "fuel_consumption": 0.05,
        "max_cargo": 10,
        "win_ore_amount": 100,
        "fail_stolen_amount": 30,
        "heli_speed": 5.0,
        "heli_steal_amount": 8,
        "heli_leaves": False
    }

}


def load_config():
    default = GAME_MODES["Normal"]
    if not os.path.exists(CONFIG_FILE):
        save_config(default)
        return default.copy()
    try:
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
            # Make sure all required keys are in the loaded config
            for k, v in default.items():
                if k not in cfg:
                    cfg[k] = v
            return cfg
    except:
        return default.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)

from constants import *
from button import Button
from fahrzeug import Fahrzeug
from hubschrauber import Hubschrauber
from gebaeude import Gebaeude

class Game:
    def __init__(self):
        pygame.init()
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Top-Down Transport Spiel")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        self.config = load_config()
        self.state = STATE_MENU
        
        self.lkw = None
        self.hubschrauber = None
        self.score = 0
        self.message = ""
        self.message_timer = 0
        self.current_mode = "Normal"

        
        self.tankstelle = Gebaeude(20, 20, 160, 100, YELLOW, "Tankstelle")
        self.lager = Gebaeude(self.width - 180, 20, 160, 100, RED, "Lager")
        self.endpunkt = Gebaeude(self.width - 180, self.height - 120, 160, 100, GREEN, "Endpunkt")
        
        # Buttons
        self.btn_play = Button(self.width//2 - 100, 250, 200, 60, "Spielen", self.font, WHITE, YELLOW)
        self.btn_quit = Button(self.width//2 - 100, 350, 200, 60, "Beenden", self.font, WHITE, RED)
        
        # Mode Selection Screen Buttons
        self.btn_start_game = Button(self.width - 250, self.height - 80, 200, 50, "Spiel starten", self.font, WHITE, GREEN)
        self.btn_back = Button(50, self.height - 80, 250, 50, "Zurück zum Menü", self.font, WHITE, YELLOW)
        self.btn_playing_menu = Button(self.width - 160, self.height - 60, 150, 40, "Menü", self.font, WHITE, YELLOW)
        
        self.mode_buttons = {}
        modes = ["Leicht", "Normal", "Schwer", "Custom"]
        for i, m in enumerate(modes):
            self.mode_buttons[m] = Button(50, 160 + i * 70, 220, 50, m, self.font, WHITE, BLUE)

        
        self.settings_keys = list(GAME_MODES["Normal"].keys())

        self.selected_setting = 0
        self.plus_buttons = []
        self.minus_buttons = []
        self.running = True



    def reset_game(self):
        self.lkw = Fahrzeug(150, 110, self.config)
        self.score = 0
        self.hubschrauber = Hubschrauber(self.config)
        self.message = "Bewege das Fahrzeug mit W, A, S, D"
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
                        self.reset_game()
                        self.state = STATE_PLAYING
                    elif self.btn_back.is_hovered:
                        self.state = STATE_MENU
                    
                    for m_name, btn in self.mode_buttons.items():
                        if btn.is_hovered:
                            self.current_mode = m_name
                            if m_name in GAME_MODES:
                                self.config = GAME_MODES[m_name].copy()
                                save_config(self.config)
                    
                    # Settings adjustment via Mouse
                    # Settings adjustment via Buttons
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


                if event.type == pygame.KEYDOWN:
                    pass # Keyboard controls removed per user request
                
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
                    if self.btn_playing_menu.is_hovered:
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
            self.lkw.update(keys, self.width, self.height)
            self.hubschrauber.update(self.lkw)
            
            lkw_rect = pygame.Rect(self.lkw.x - self.lkw.width//2, self.lkw.y - self.lkw.height//2, self.lkw.width, self.lkw.height)

            if lkw_rect.colliderect(self.tankstelle.rect):
                if self.lkw.fuel < 100:
                    self.lkw.fuel += 1
                    if self.lkw.fuel > 100:
                        self.lkw.fuel = 100
                    self.message = "Tank wird aufgefüllt..."
                    self.message_timer = 10

            elif lkw_rect.colliderect(self.lager.rect):
                self.lkw.cargo = self.lkw.max_cargo
                self.message = "Ladung erfolgreich geladen!"
                self.message_timer = 90

            elif lkw_rect.colliderect(self.endpunkt.rect):
                if self.lkw.cargo > 0:
                    delivered = self.lkw.cargo
                    self.score += delivered
                    self.lkw.cargo = 0
                    self.message = f"Ladung abgeliefert! +{delivered} Punkte"
                    self.message_timer = 90
            
            # Win/Fail Bedingungen
            if self.score >= self.config["win_ore_amount"]:
                self.state = STATE_WIN
            if self.hubschrauber.total_stolen >= self.config["fail_stolen_amount"]:
                self.state = STATE_GAME_OVER
            
            self.btn_playing_menu.check_hover(self.mouse_pos)
                
        elif self.state in [STATE_WIN, STATE_GAME_OVER]:
            self.btn_back.check_hover(self.mouse_pos)

    def draw_background(self):
        # Grüner Hintergrund (Gras)
        self.screen.fill(DARK_GREEN)
        
        # Straßennetz zeichnen
        pygame.draw.rect(self.screen, GRAY, (130, 90, 640, 40))
        pygame.draw.rect(self.screen, GRAY, (130, 90, 40, 400))
        pygame.draw.rect(self.screen, GRAY, (130, 450, 640, 40))
        
        # Straßenmarkierungen
        for x in range(130, 770, 40):
            pygame.draw.rect(self.screen, WHITE, (x, 108, 20, 4))
            pygame.draw.rect(self.screen, WHITE, (x, 468, 20, 4))
        for y in range(90, 490, 40):
            pygame.draw.rect(self.screen, WHITE, (148, y, 4, 20))

    def draw(self):
        if self.state == STATE_MENU:
            self.screen.fill(BLUE)
            title = self.large_font.render("TRUCK TRANSPORT", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(self.width//2, 100)))
            self.btn_play.draw(self.screen)
            self.btn_quit.draw(self.screen)

            
        elif self.state == STATE_SETTINGS:
            self.screen.fill(DARK_GRAY)
            title = self.large_font.render("MODUS WÄHLEN", True, WHITE)
            self.screen.blit(title, title.get_rect(center=(self.width//2, 50)))
            
            # Left side: Mode Buttons
            pygame.draw.rect(self.screen, (40, 40, 40), (30, 100, 260, self.height - 200))
            label_modes = self.font.render("Spiel-Modi", True, YELLOW)
            self.screen.blit(label_modes, (50, 120))
            
            for m_name, btn in self.mode_buttons.items():
                # Highlight active mode
                if m_name == self.current_mode:
                    pygame.draw.rect(self.screen, YELLOW, btn.rect.inflate(10, 10), 3)
                btn.draw(self.screen)
            
            # Right side: Settings
            pygame.draw.rect(self.screen, (50, 50, 50), (310, 100, self.width - 340, self.height - 200))
            label_settings = self.font.render("Einstellungen (Klicken zum Ändern)", True, YELLOW)
            self.screen.blit(label_settings, (330, 120))
            
            inst = self.font.render("Werte rechts mit + und - anpassen", True, WHITE)
            self.screen.blit(inst, (330, 155))
            
            start_y = 200
            self.plus_buttons = []
            self.minus_buttons = []
            for i, key in enumerate(self.settings_keys):
                val = self.config[key]
                text = self.font.render(f"{key}: {val}", True, WHITE)
                rect = text.get_rect(topleft=(330, start_y + i * 40))
                self.screen.blit(text, rect)
                
                # Draw +/- Buttons on the right
                btn_size = 30
                m_rect = pygame.Rect(self.width - 120, start_y + i * 40 - 2, btn_size, btn_size)
                p_rect = pygame.Rect(self.width - 80, start_y + i * 40 - 2, btn_size, btn_size)
                
                self.minus_buttons.append(m_rect)
                self.plus_buttons.append(p_rect)
                
                # Minus Button
                m_color = RED if m_rect.collidepoint(self.mouse_pos) else (150, 50, 50)
                pygame.draw.rect(self.screen, m_color, m_rect)
                m_label = self.font.render("-", True, WHITE)
                self.screen.blit(m_label, m_label.get_rect(center=m_rect.center))
                
                # Plus Button
                p_color = GREEN if p_rect.collidepoint(self.mouse_pos) else (50, 150, 50)
                pygame.draw.rect(self.screen, p_color, p_rect)
                p_label = self.font.render("+", True, WHITE)
                self.screen.blit(p_label, p_label.get_rect(center=p_rect.center))

                
            self.btn_back.draw(self.screen)
            self.btn_start_game.draw(self.screen)
            
        elif self.state == STATE_PLAYING:
            self.draw_background()
            self.tankstelle.draw(self.screen, self.font)
            self.lager.draw(self.screen, self.font)
            self.endpunkt.draw(self.screen, self.font)
            
            self.lkw.draw(self.screen)
            if self.hubschrauber:
                self.hubschrauber.draw(self.screen)

            # UI oben
            ui_text = self.font.render(f"Punkte: {self.score}/{self.config['win_ore_amount']} | Ladung: {self.lkw.cargo}/{self.lkw.max_cargo}", True, WHITE)
            ui_bg = ui_text.get_rect(topleft=(10, 10)).inflate(20, 10)
            pygame.draw.rect(self.screen, BLACK, ui_bg)
            self.screen.blit(ui_text, (20, 15))
            
            # Heli Diebstahl UI
            heli_text = self.font.render(f"Geklaut: {self.hubschrauber.total_stolen}/{self.config['fail_stolen_amount']}", True, RED)
            heli_bg = heli_text.get_rect(topright=(self.width - 10, 10)).inflate(20, 10)
            pygame.draw.rect(self.screen, BLACK, heli_bg)
            self.screen.blit(heli_text, heli_bg.move(10, 5))

            if self.message_timer > 0:
                msg_text = self.font.render(self.message, True, WHITE)
                msg_rect = msg_text.get_rect(center=(self.width // 2, self.height - 40))
                bg_rect = msg_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, BLACK, bg_rect)
                self.screen.blit(msg_text, msg_rect)
                self.message_timer -= 1

            if self.lkw.fuel <= 0:
                out_of_fuel = self.font.render("Ohne Benzin liegen geblieben!", True, RED)
                bg_rect = out_of_fuel.get_rect(center=(self.width//2, self.height//2)).inflate(20, 20)
                pygame.draw.rect(self.screen, BLACK, bg_rect)
                self.screen.blit(out_of_fuel, bg_rect)
            
            self.btn_playing_menu.draw(self.screen)

        elif self.state == STATE_WIN:
            self.screen.fill(GREEN)
            win_txt = self.large_font.render("GEWONNEN!", True, BLACK)
            self.screen.blit(win_txt, win_txt.get_rect(center=(self.width//2, self.height//2 - 50)))
            self.btn_back.draw(self.screen)
            
        elif self.state == STATE_GAME_OVER:
            self.screen.fill(RED)
            fail_txt = self.large_font.render("VERLOREN!", True, BLACK)
            fail_desc = self.font.render("Der Hubschrauber hat zu viel gestohlen!", True, BLACK)
            self.screen.blit(fail_txt, fail_txt.get_rect(center=(self.width//2, self.height//2 - 50)))
            self.screen.blit(fail_desc, fail_desc.get_rect(center=(self.width//2, self.height//2 + 10)))
            self.btn_back.draw(self.screen)

        pygame.display.flip()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
