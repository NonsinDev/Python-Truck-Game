import os
import pygame


class ScrollBackground:
    # Geschwindigkeiten der scrollenden Layer (menu_bg_1 bis menu_bg_N) in Pixel/Frame
    LAYER_SPEEDS = [0.2, 0.6, 1.0, -0.7]
    # Höhe für Layer 4 (unten anliegend, nicht vollbild)
    BOTTOM_LAYER_HEIGHT = 300

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.layers = []       # scrollende Layer: [surface, x_pos, speed, y_pos]
        self.static_bg = None  # statisches Hintergrundbild (menu_bg_static.png)
        self.menu_truck = None # LKW-Bild für das Hauptmenü (menu_truck.png)

        # Statisches Bild laden (wird als erstes gezeichnet)
        for ext in ("png", "jpg", "jpeg", "bmp"):
            img_path = os.path.join("assets", f"menu_bg_static.{ext}")
            if os.path.exists(img_path):
                raw = pygame.image.load(img_path).convert_alpha()
                self.static_bg = pygame.transform.scale(raw, (width, height))
                break

        # Scrollende Layer laden
        for i, speed in enumerate(self.LAYER_SPEEDS, start=1):
            is_bottom = (i == len(self.LAYER_SPEEDS))  # letzter Layer = unten anliegend
            for ext in ("png", "jpg", "jpeg", "bmp"):
                img_path = os.path.join("assets", f"menu_bg_{i}.{ext}")
                if os.path.exists(img_path):
                    raw = pygame.image.load(img_path).convert_alpha()
                    if is_bottom:
                        target_h = self.BOTTOM_LAYER_HEIGHT
                        scale_factor = target_h / raw.get_height()
                        scaled_w = max(width + 1, int(raw.get_width() * scale_factor))
                        surface = pygame.transform.scale(raw, (scaled_w, target_h))
                        y_pos = height - target_h
                    else:
                        scale_factor = height / raw.get_height()
                        scaled_w = max(width + 1, int(raw.get_width() * scale_factor))
                        surface = pygame.transform.scale(raw, (scaled_w, height))
                        y_pos = 0
                    self.layers.append([surface, 0.0, speed, y_pos])
                    break

        # LKW-Bild laden (menu_truck.png)
        for ext in ("png", "jpg", "jpeg", "bmp"):
            img_path = os.path.join("assets", f"menu_truck.{ext}")
            if os.path.exists(img_path):
                raw = pygame.image.load(img_path).convert_alpha()
                target_w = 600
                scale_factor = target_w / raw.get_width()
                target_h = int(raw.get_height() * scale_factor)
                self.menu_truck = pygame.transform.scale(raw, (target_w, target_h))
                break

    def update(self):
        for layer in self.layers:
            layer[1] += layer[2]
            if layer[1] >= layer[0].get_width():
                layer[1] = 0.0

    def draw(self, screen):
        if not self.layers and not self.static_bg:
            return False
        screen.fill((0, 0, 0))
        if self.static_bg:
            screen.blit(self.static_bg, (0, 0))
        for surface, x_pos, _, y_pos in self.layers:
            img_w = surface.get_width()
            x = int(x_pos) - img_w
            while x < self.width:
                screen.blit(surface, (x, y_pos))
                x += img_w
        return True
