import pygame
from pygame import Vector2 as vec2

class Spawn:
    def __init__(self, world_pos=vec2(40, 40), color=(0, 0, 255), radius=20):
        self.world_pos = world_pos
        self.pos = vec2((world_pos.x / 4), (world_pos.y / 4))
        self.color = color
        self.radius = radius

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
        pygame.draw.circle(surf, self.color, self.world_pos, self.radius)