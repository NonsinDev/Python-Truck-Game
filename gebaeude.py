import pygame
from constants import BLACK, WHITE

class Gebaeude:
    def __init__(self, x, y, w, h, color, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect, 0, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=10)
        
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        
        bg_rect = text_rect.inflate(10, 5)
        pygame.draw.rect(surface, WHITE, bg_rect)
        pygame.draw.rect(surface, BLACK, bg_rect, 2)
        
        surface.blit(text_surf, text_rect)
