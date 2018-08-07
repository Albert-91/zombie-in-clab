import pygame


class Drawable:

    def __init__(self, width, height, x, y, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.surface = pygame.Surface.convert_alpha(self.surface)
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)
