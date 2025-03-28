import pygame
from pygame import Vector2 as vec2

class Food:
    def __init__(self, pos=vec2(100, 100), amount=1):
        self.pos = pos
        self.pos_corrected = vec2(int(pos.x * 4 + 2), int(pos.y * 4 + 2))
        self.amount = amount

    def draw(self, surf):
        x = int(self.pos.x * 4) + 2
        y = int(self.pos.y * 4) + 2
        # print(x, y)
        # print(x * 4 + 2, y * 4 + 2)
        pygame.draw.circle(surf, (168, 99, 59), (x, y), 2)