import pygame
import math
import sys

# Pygame initialisieren
pygame.init()

# Bildschirmgröße
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Transport Spiel")

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
BLUE = (50, 100, 200)
YELLOW = (220, 220, 50)
BROWN = (139, 69, 19)

# Schriftarten
try:
    font = pygame.font.SysFont(None, 36)
except:
    font = pygame.font.Font(None, 36)

# Fahrzeug Klasse
class Vehicle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0 # in Grad
        self.speed = 0
        self.max_speed = 6.0
        self.acceleration = 0.15
        self.friction = 0.94
        self.turn_speed = 4.0
        
        self.fuel = 100.0
        self.fuel_consumption = 0.05
        self.cargo = 0
        self.max_cargo = 10
        
        # Größe des Fahrzeugs
        self.width = 40
        self.height = 20

    def update(self, keys):
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
        elif self.speed < -self.max_speed:
            self.speed = -self.max_speed

        # Winkel in Radiant umrechnen für die Bewegung
        rad = math.radians(self.angle)
        
        # Neue Position berechnen
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

        # Bildschirmränder begrenzen
        self.x = max(20, min(WIDTH - 20, self.x))
        self.y = max(20, min(HEIGHT - 20, self.y))

    def draw(self, surface):
        # Surface für das Fahrzeug erstellen (mit transparentem Hintergrund)
        vehicle_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Karosserie zeichnen
        pygame.draw.rect(vehicle_surface, BLUE, (0, 0, self.width, self.height))
        
        # Front/Fahrerkabine zeichnen (zur Richtungsanzeige)
        pygame.draw.rect(vehicle_surface, YELLOW, (self.width - 12, 2, 10, self.height - 4))
        
        # Wenn Ladung vorhanden, zeichne ein kleines Rechteck auf der Ladefläche
        if self.cargo > 0:
            pygame.draw.rect(vehicle_surface, BROWN, (5, 2, 18, self.height - 4))

        # Fahrzeug rotieren
        rotated_surface = pygame.transform.rotate(vehicle_surface, -self.angle)
        
        # Rotierte Surface zentrieren
        rect = rotated_surface.get_rect(center=(self.x, self.y))
        
        # Zeichnen
        surface.blit(rotated_surface, rect)
        
        # Tankanzeige über dem Fahrzeug
        fuel_bar_width = 40
        fuel_ratio = max(0, self.fuel) / 100.0
        pygame.draw.rect(surface, RED, (self.x - 20, self.y - 25, fuel_bar_width, 5))
        pygame.draw.rect(surface, GREEN, (self.x - 20, self.y - 25, int(fuel_bar_width * fuel_ratio), 5))

# Zonen für Stationen
class Zone:
    def __init__(self, x, y, w, h, color, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text

    def draw(self, surface):
        # Rand und Füllung der Zone
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 3)
        
        # Text in die Mitte setzen
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        # Weißer Hintergrund für den Text für bessere Lesbarkeit
        bg_rect = text_rect.inflate(10, 5)
        pygame.draw.rect(surface, WHITE, bg_rect)
        pygame.draw.rect(surface, BLACK, bg_rect, 2)
        
        surface.blit(text_surf, text_rect)

def main():
    clock = pygame.time.Clock()
    
    # Spieler initialisieren (Start in der Mitte)
    player = Vehicle(WIDTH // 2, HEIGHT // 2)
    
    # Stationen erstellen
    gas_station = Zone(50, 50, 160, 100, YELLOW, "Tankstelle")
    warehouse = Zone(WIDTH - 210, 50, 160, 100, RED, "Lager")
    endpoint = Zone(WIDTH - 210, HEIGHT - 150, 160, 100, GREEN, "Endpunkt")
    
    score = 0
    message = "Bewege das Fahrzeug mit W, A, S, D"
    message_timer = 180 # Zeigt die Nachricht für ~3 Sekunden

    running = True
    while running:
        # Event Loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Tasten abfragen
        keys = pygame.key.get_pressed()
        
        # Fahrzeug updaten
        player.update(keys)

        # Einfache Bounding-Box für Kollisionen
        player_rect = pygame.Rect(player.x - player.width//2, player.y - player.height//2, player.width, player.height)

        # Interaktion mit Tankstelle
        if player_rect.colliderect(gas_station.rect):
            if player.fuel < 100:
                player.fuel += 0.5
                if player.fuel > 100:
                    player.fuel = 100
                message = "Tank wird aufgefüllt..."
                message_timer = 10

        # Interaktion mit Lager (Aufladen)
        elif player_rect.colliderect(warehouse.rect):
            if player.cargo == 0:
                player.cargo = player.max_cargo
                message = "Ladung erfolgreich geladen!"
                message_timer = 90

        # Interaktion mit Endpunkt (Abladen)
        elif player_rect.colliderect(endpoint.rect):
            if player.cargo > 0:
                score += player.cargo
                player.cargo = 0
                message = "Ladung erfolgreich ausgeliefert! +10 Punkte"
                message_timer = 90

        # Alles Zeichnen
        screen.fill(GRAY) # Hintergrund (Asphalt)
        
        gas_station.draw(screen)
        warehouse.draw(screen)
        endpoint.draw(screen)
        
        player.draw(screen)

        # UI oben links (Punkte & Status)
        ui_text = font.render(f"Punkte: {score} | Ladung: {player.cargo}/{player.max_cargo}", True, WHITE)
        ui_bg = ui_text.get_rect(topleft=(10, 10)).inflate(20, 10)
        pygame.draw.rect(screen, BLACK, ui_bg)
        screen.blit(ui_text, (20, 15))

        # Ausgabemeldungen (zentriert unten)
        if message_timer > 0:
            msg_text = font.render(message, True, WHITE)
            msg_rect = msg_text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
            bg_rect = msg_rect.inflate(20, 10)
            pygame.draw.rect(screen, BLACK, bg_rect)
            screen.blit(msg_text, msg_rect)
            message_timer -= 1

        # Warnung wenn der Tank leer ist
        if player.fuel <= 0:
            out_of_fuel = font.render("Ohne Benzin liegen geblieben!", True, RED)
            bg_rect = out_of_fuel.get_rect(center=(WIDTH//2, HEIGHT//2)).inflate(20, 20)
            pygame.draw.rect(screen, BLACK, bg_rect)
            screen.blit(out_of_fuel, out_of_fuel.get_rect(center=(WIDTH//2, HEIGHT//2)))

        # Display aktualisieren
        pygame.display.flip()
        
        # Framerate auf 60 FPS begrenzen
        clock.tick(60)

    # Pygame beenden
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
