import pygame
from pygame import Vector2 as vec2

class Wall:
    def __init__(self, pos=vec2(0, 0), color=(0,0,0)):
        self.pos = pos
        self.world_pos = vec2((pos.x * 4), (pos.y * 4))
        self.color = color
        self.width = 4
        self.height = 4
    
    def draw(self, surf):
        pygame.draw.rect(surf, self.color, (self.world_pos.x, self.world_pos.y, 4, 4))

    