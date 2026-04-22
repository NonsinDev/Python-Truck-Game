import pygame
import math
from constants import BLUE, YELLOW, BROWN, RED, GREEN

class Fahrzeug:
    def __init__(self, x, y, config):
        self.x = x
        self.y = y
        self.angle = 0 # in Grad
        self.speed = 0
        self.config = config
        
        self.update_stats()
        
        self.acceleration = 0.15
        self.friction = 0.94
        self.turn_speed = 4.0
        
        self.fuel = 100.0
        self.cargo = 0
        
        # Größe des Fahrzeugs
        self.width = 40
        self.height = 20

    def update_stats(self):
        self.max_speed = self.config["max_speed"]
        self.fuel_consumption = self.config["fuel_consumption"]
        self.max_cargo = self.config["max_cargo"]

    def update(self, keys, width, height):
        # Lenken (nur wenn das Fahrzeug sich bewegt)
        if abs(self.speed) > 0.1:
            if keys[pygame.K_a]:
                self.angle -= self.turn_speed
            if keys[pygame.K_d]:
                self.angle += self.turn_speed

        # Beschleunigen / Bremsen
        if self.fuel > 0:
            if keys[pygame.K_w]:
                self.speed += self.acceleration
                self.fuel -= self.fuel_consumption
            elif keys[pygame.K_s]:
                self.speed -= self.acceleration
                self.fuel -= self.fuel_consumption

        # Reibung anwenden
        self.speed *= self.friction

        # Geschwindigkeit begrenzen
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < -self.max_speed * 0.4:  # Rückwärtsgang begrenzt auf 40%
            self.speed = -self.max_speed * 0.4

        # Winkel in Radiant umrechnen
        rad = math.radians(self.angle)
        
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        # Bildschirmränder begrenzen
        self.x = max(20, min(width - 20, self.x))
        self.y = max(20, min(height - 20, self.y))

    def draw(self, surface):
        vehicle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Karosserie zeichnen
        pygame.draw.rect(vehicle_surface, BLUE, (0, 0, self.width, self.height))
        # Fahrerkabine
        pygame.draw.rect(vehicle_surface, YELLOW, (self.width - 12, 2, 10, self.height - 4))
        
        if self.cargo > 0:
            pygame.draw.rect(vehicle_surface, BROWN, (5, 2, 18, self.height - 4))

        rotated_surface = pygame.transform.rotate(vehicle_surface, -self.angle)
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        surface.blit(rotated_surface, rect)
        
        # Tankanzeige
        fuel_bar_width = 40
        fuel_ratio = max(0, self.fuel) / 100.0
        pygame.draw.rect(surface, RED, (self.x - 20, self.y - 25, fuel_bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.x - 20, self.y - 25, int(fuel_bar_width * fuel_ratio), 5))
