import pygame
import math
import random
from constants import DARK_GRAY, BLACK, RED

class Hubschrauber:
    def __init__(self, config):
        self.config = config
        self.x = -100
        self.y = -100
        
        # Basis außerhalb des Bildschirms festlegen
        angles = [0, 90, 180, 270]
        spawn_angle = math.radians(random.choice(angles))
        dist = 800
        self.base_x = 400 + math.cos(spawn_angle) * dist
        self.base_y = 300 + math.sin(spawn_angle) * dist
        
        self.target_x = 0
        self.target_y = 0
        self.state = "IDLE"  # IDLE, APPROACHING, STEALING, RETURNING
        self.timer = random.randint(180, 400)  # Timer, bis der Heli spawnt
        self.steal_timer = 0
        self.empty_cargo_timer = 0 # Timer für 10 Sekunden ohne Ladung
        self.rotor_angle = 0
        self.total_stolen = 0

    def update(self, lkw):
        self.rotor_angle = (self.rotor_angle + 25) % 360
        speed = self.config["heli_speed"]

        if self.state == "IDLE":
            self.timer -= 1
            if self.timer <= 0:
                # Spawne an der Basis
                self.x = self.base_x
                self.y = self.base_y
                self.state = "APPROACHING"

        elif self.state == "APPROACHING":
            dx = lkw.x - self.x
            dy = lkw.y - self.y
            dist = math.hypot(dx, dy)
            if dist < speed:
                self.x = lkw.x
                self.y = lkw.y
                self.state = "STEALING"
                self.steal_timer = 60
                self.empty_cargo_timer = 0
            else:
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed

        elif self.state == "STEALING":
            # Bleibt über dem Spieler stehen
            self.x = lkw.x
            self.y = lkw.y
            
            if lkw.cargo > 0:
                self.steal_timer -= 1
                self.empty_cargo_timer = 0
                if self.steal_timer <= 0:
                    # Klau Ladung
                    steal_amount = min(lkw.cargo, self.config["heli_steal_amount"])
                    lkw.cargo -= steal_amount
                    self.total_stolen += steal_amount
                    
                    # Fliege zur Basis zurück
                    self.state = "RETURNING"
                    self.target_x = self.base_x
                    self.target_y = self.base_y
            else:
                # LKW hat keine Ladung
                if self.config["heli_leaves"]:
                    self.empty_cargo_timer += 1
                    if self.empty_cargo_timer >= 300: # Festgelegt auf 5 Sekunden (300 Frames)
                        # Konfigurierte Zeit um, fliege zur Basis zurück
                        self.state = "RETURNING"
                        self.target_x = self.base_x
                        self.target_y = self.base_y
                else:
                    # Falls der Heli nicht abzieht, bleibt der Timer auf 0
                    self.empty_cargo_timer = 0

        elif self.state == "RETURNING":
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < speed:
                self.state = "IDLE"
                self.timer = random.randint(300, 600)
            else:
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed

    def draw(self, surface):
        if self.state == "IDLE":
            return
            
        heli_body = pygame.Surface((40, 40), pygame.SRCALPHA)
        # Karosserie
        pygame.draw.ellipse(heli_body, DARK_GRAY, (5, 10, 30, 20))
        # Cockpit
        pygame.draw.circle(heli_body, BLACK, (30, 20), 6)
        
        rect = heli_body.get_rect(center=(self.x, self.y))
        surface.blit(heli_body, rect)
        
        # Rotoren zeichnen
        p1_x = self.x + math.cos(math.radians(self.rotor_angle)) * 30
        p1_y = self.y + math.sin(math.radians(self.rotor_angle)) * 30
        p2_x = self.x + math.cos(math.radians(self.rotor_angle + 180)) * 30
        p2_y = self.y + math.sin(math.radians(self.rotor_angle + 180)) * 30
        pygame.draw.line(surface, BLACK, (p1_x, p1_y), (p2_x, p2_y), 3)
        
        p3_x = self.x + math.cos(math.radians(self.rotor_angle + 90)) * 30
        p3_y = self.y + math.sin(math.radians(self.rotor_angle + 90)) * 30
        p4_x = self.x + math.cos(math.radians(self.rotor_angle + 270)) * 30
        p4_y = self.y + math.sin(math.radians(self.rotor_angle + 270)) * 30
        pygame.draw.line(surface, BLACK, (p3_x, p3_y), (p4_x, p4_y), 3)
        
        if self.state == "STEALING":
            font = pygame.font.Font(None, 24)
            t = font.render("Dieb!", True, RED)
            surface.blit(t, (self.x - 20, self.y - 40))
