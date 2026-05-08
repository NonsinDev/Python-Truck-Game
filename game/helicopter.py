import pygame
import math
import random
from game.constants import DARK_GRAY, BLACK


class Helicopter:
    def __init__(self, config):
        self.config = config
        self.x = -100
        self.y = -100

        # Place base outside screen bounds
        angles = [0, 90, 180, 270]
        spawn_angle = math.radians(random.choice(angles))
        dist = 800
        self.base_x = 400 + math.cos(spawn_angle) * dist
        self.base_y = 300 + math.sin(spawn_angle) * dist

        self.target_x = 0
        self.target_y = 0
        self.state = "IDLE"  # IDLE, APPROACHING, STEALING, RETURNING
        self.timer = random.randint(180, 400)
        self.steal_timer = 0
        self.empty_cargo_timer = 0
        self.rotor_angle = 0
        self.total_stolen = 0

    def update(self, truck):
        self.rotor_angle = (self.rotor_angle + 25) % 360
        speed = self.config["heli_speed"]

        if self.state == "IDLE":
            self.timer -= 1
            if self.timer <= 0:
                self.x = self.base_x
                self.y = self.base_y
                self.state = "APPROACHING"

        elif self.state == "APPROACHING":
            dx = truck.x - self.x
            dy = truck.y - self.y
            dist = math.hypot(dx, dy)
            if dist < speed:
                self.x = truck.x
                self.y = truck.y
                self.state = "STEALING"
                self.steal_timer = 60
                self.empty_cargo_timer = 0
            else:
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed

        elif self.state == "STEALING":
            # Hover directly over the truck
            self.x = truck.x
            self.y = truck.y

            if truck.cargo > 0:
                self.steal_timer -= 1
                self.empty_cargo_timer = 0
                if self.steal_timer <= 0:
                    # Steal cargo
                    steal_amount = min(truck.cargo, self.config["heli_steal_amount"])
                    truck.cargo -= steal_amount
                    self.total_stolen += steal_amount

                    self.state = "RETURNING"
                    self.target_x = self.base_x
                    self.target_y = self.base_y
            else:
                # Truck has no cargo
                if self.config["heli_leaves"]:
                    self.empty_cargo_timer += 1
                    if self.empty_cargo_timer >= 300:  # 5 seconds at 60 fps
                        self.state = "RETURNING"
                        self.target_x = self.base_x
                        self.target_y = self.base_y
                else:
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
        # Draw fuselage
        pygame.draw.ellipse(heli_body, DARK_GRAY, (5, 10, 30, 20))
        # Draw cockpit
        pygame.draw.circle(heli_body, BLACK, (30, 20), 6)

        rect = heli_body.get_rect(center=(self.x, self.y))
        surface.blit(heli_body, rect)

        # Draw rotor blades
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

