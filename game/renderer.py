import pygame

from game.constants import *


class GameRenderer:
    def __init__(self, screen, width, height, font, large_font):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = font
        self.large_font = large_font

    def draw_playing(self, game):
        game.game_map.draw_background(self.screen)
        game.game_map.draw_buildings(self.screen, self.font)
        game.truck.draw(self.screen)
        if game.helicopter:
            game.helicopter.draw(self.screen)

        # HUD top-left: current score and cargo
        ui_text = self.font.render(
            f"Score: {game.score}/{game.config['win_ore_amount']} | Cargo: {game.truck.cargo}/{game.truck.max_cargo}",
            True, WHITE
        )
        ui_bg = ui_text.get_rect(topleft=(10, 10)).inflate(20, 10)
        pygame.draw.rect(self.screen, BLACK, ui_bg)
        self.screen.blit(ui_text, (20, 15))

        # HUD top-right: total cargo stolen by the helicopter
        heli_text = self.font.render(
            f"Stolen: {game.helicopter.total_stolen}/{game.config['fail_stolen_amount']}",
            True, RED
        )
        heli_bg = heli_text.get_rect(topright=(self.width - 10, 10)).inflate(20, 10)
        pygame.draw.rect(self.screen, BLACK, heli_bg)
        self.screen.blit(heli_text, heli_bg.move(10, 5))

        # Event message centered at the bottom (e.g. "Cargo loaded!"), fades after a timer
        if game.message_timer > 0:
            msg_surface = self.font.render(game.message, True, WHITE)
            msg_rect = msg_surface.get_rect(center=(self.width // 2, self.height - 40))
            bg_rect = msg_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            self.screen.blit(msg_surface, msg_rect)
            game.message_timer -= 1

        # Warning overlay when the truck runs out of fuel
        if game.truck.fuel <= 0:
            no_fuel = self.font.render("Out of fuel!", True, RED)
            text_pos = no_fuel.get_rect(center=(self.width // 2, self.height // 2))
            bg_rect = text_pos.inflate(20, 20)
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            self.screen.blit(no_fuel, text_pos)

        # Debug overlay: enabled by holding Ctrl when clicking Start Game
        if game.debug_mode:
            debug_lines = [
                "DEBUG MODE",
                f"Truck x={game.truck.x:.1f} y={game.truck.y:.1f}",
                f"Speed={game.truck.speed:.2f}  Angle={game.truck.angle:.1f}",
                f"Fuel={game.truck.fuel:.1f}  Cargo={game.truck.cargo}/{game.truck.max_cargo}",
                f"Heli state={game.helicopter.state}  Stolen={game.helicopter.total_stolen}",
                f"Score={game.score}/{game.config['win_ore_amount']}",
            ]
            debug_font = pygame.font.Font(None, 24)
            line_height = 20
            # Vertically centered on the left side
            start_y = self.height // 2 - (len(debug_lines) * line_height) // 2
            for i, line in enumerate(debug_lines):
                text_surf = debug_font.render(line, True, ORANGE)
                self.screen.blit(text_surf, (10, start_y + i * line_height))

    def draw_paused(self, game):
        game.game_map.draw_background(self.screen)
        game.game_map.draw_buildings(self.screen, self.font)
        game.truck.draw(self.screen)
        if game.helicopter:
            game.helicopter.draw(self.screen)

        # Draw a semi-transparent overlay over the game
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Pause menu box
        box = pygame.Rect(self.width // 2 - 130, 120, 260, 380)
        pygame.draw.rect(self.screen, DARK_GRAY, box, border_radius=12)
        pygame.draw.rect(self.screen, WHITE, box, 2, border_radius=12)

        pause_title = self.large_font.render("PAUSED", True, WHITE)
        self.screen.blit(pause_title, pause_title.get_rect(center=(self.width // 2, 160)))

        game.btn_pause_continue.draw(self.screen)
        game.btn_pause_reset.draw(self.screen)
        game.btn_pause_menu.draw(self.screen)
        game.btn_pause_quit.draw(self.screen)

    def draw_win(self, btn_back):
        self.screen.fill(GREEN)
        win_text = self.large_font.render("YOU WIN!", True, BLACK)
        self.screen.blit(win_text, win_text.get_rect(center=(self.width // 2, self.height // 2 - 50)))
        btn_back.draw(self.screen)

    def draw_game_over(self, btn_back):
        self.screen.fill(RED)
        lose_text = self.large_font.render("GAME OVER!", True, BLACK)
        desc = self.font.render("The helicopter stole too much cargo!", True, BLACK)
        self.screen.blit(lose_text, lose_text.get_rect(center=(self.width // 2, self.height // 2 - 50)))
        self.screen.blit(desc, desc.get_rect(center=(self.width // 2, self.height // 2 + 10)))
        btn_back.draw(self.screen)
