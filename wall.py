import pygame
from pygame import Vector2 as vec2

class Wall:
    def __init__(self, pos=vec2(0, 0), color=(0,0,0)):
        self.pos = pos
        self.world_pos = vec2((pos.x * 4), (pos.y * 4))
        self.color = color
        self.width = 4
        self.height = 4

    def to_dict(self):
        dict = self.__dict__
        dict['world_pos'] = (self.world_pos.x, self.world_pos.y)
        dict['pos'] = (self.pos.x, self.pos.y)
        return dict
    
    def un_dict(self):
        dict = self.__dict__
        dict['world_pos'] = vec2(self.world_pos)
        dict['pos'] = vec2(self.pos)
        return dict
    
    def draw(self, surf):
        self.un_dict()
        pygame.draw.rect(surf, self.color, (self.world_pos.x, self.world_pos.y, 4, 4))

    