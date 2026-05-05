import pygame
from game.constants import BLACK, WHITE


class Building:
    def __init__(self, x, y, width, height, color, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.label = label

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect, 0, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=10)

        text_surface = font.render(self.label, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # White background behind the text
        bg_rect = text_rect.inflate(10, 5)
        pygame.draw.rect(surface, WHITE, bg_rect)
        pygame.draw.rect(surface, BLACK, bg_rect, 2)

        surface.blit(text_surface, text_rect)
