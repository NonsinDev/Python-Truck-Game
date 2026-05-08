import random
import pygame

from game.constants import *
from game.building import Building


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.gas_station = None
        self.warehouse = None
        self.delivery = None
        self._road_nodes = []
        self._road_edges = []

    def generate(self):
        bw, bh = 160, 100
        mx = 100 + bw // 2
        my = 80 + bh // 2
        xs = [mx, self.width // 2, self.width - mx]
        ys = [my, self.height - my]
        nodes = [(x, y) for y in ys for x in xs]
        edges = [
            (0, 1), (1, 2),
            (3, 4), (4, 5),
            (0, 3), (1, 4), (2, 5),
        ]
        self._road_nodes = nodes
        self._road_edges = edges

        chosen = random.sample(range(len(nodes)), 3)

        def make(idx, color, label):
            cx, cy = nodes[idx]
            return Building(cx - bw // 2, cy - bh // 2, bw, bh, color, label)

        self.gas_station = make(chosen[0], YELLOW, "Gas Station")
        self.warehouse   = make(chosen[1], RED,    "Warehouse")
        self.delivery    = make(chosen[2], GREEN,  "Delivery")

    def draw_background(self, screen):
        screen.fill(DARK_GREEN)
        road_w = 60
        if not self._road_nodes:
            return
        for (i, j) in self._road_edges:
            x1, y1 = self._road_nodes[i]
            x2, y2 = self._road_nodes[j]
            pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), road_w)
        for (x, y) in self._road_nodes:
            pygame.draw.circle(screen, GRAY, (x, y), road_w // 2)
        for (i, j) in self._road_edges:
            x1, y1 = self._road_nodes[i]
            x2, y2 = self._road_nodes[j]
            dx, dy = x2 - x1, y2 - y1
            length = max(1, (dx**2 + dy**2) ** 0.5)
            nx, ny = dx / length, dy / length
            dash_len, gap = 20, 20
            step = dash_len + gap
            pos = step
            while pos + dash_len < length:
                sx = int(x1 + nx * pos)
                sy = int(y1 + ny * pos)
                ex = int(x1 + nx * (pos + dash_len))
                ey = int(y1 + ny * (pos + dash_len))
                pygame.draw.line(screen, WHITE, (sx, sy), (ex, ey), 2)
                pos += step

    def draw_buildings(self, screen, font):
        self.gas_station.draw(screen, font)
        self.warehouse.draw(screen, font)
        self.delivery.draw(screen, font)
