import pygame
from drawable import Drawable


class Rooms(Drawable, pygame.sprite.Sprite):
    wall_lines = None

    def __init__(self, x, y, width=1000, height=600, color=(0, 0, 0)):
        super(Rooms, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        wall_width = 10
        wall_color = (0, 0, 0)
        wall_corners = [(150, 200), (0, 200), (0, 0), (200, 0), (200, 200), (190, 200), (300, 200), (200, 200),
                        (200, 0), (400, 0), (400, 200), (340, 200), (520, 200), (400, 200), (400, 0), (600, 0),
                        (600, 200), (560, 200), (700, 200), (600, 200), (600, 0), (800, 0), (800, 200), (740, 200),
                        (820, 200), (800, 200), (800, 0), (995, 0), (995, 200), (860, 200), (995, 200), (995, 280)]
        pygame.draw.lines(self.surface, wall_color, False, wall_corners, wall_width)
        Rooms.wall_lines = pygame.draw.lines(self.surface, wall_color, False, wall_corners, wall_width)
