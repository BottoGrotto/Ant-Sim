import pygame
from pygame import Vector2 as vec2

class Food:
    def __init__(self, pos=vec2(100, 100), amount=1):
        self.pos = pos
        self.pos_corrected = vec2(int(pos.x * 4 + 2), int(pos.y * 4 + 2))
        self.amount = amount

    def __eq__(self, other):
        if self.pos == other.pos:
            return True
        else:
            return False
        
    def to_dict(self):
        dict = self.__dict__
        dict['pos_corrected'] = (self.pos_corrected.x, self.pos_corrected.y)
        dict['pos'] = (self.pos.x, self.pos.y)
        return dict
    
    def un_dict(self):
        dict = self.__dict__
        dict['pos_corrected'] = vec2(self.pos_corrected)
        dict['pos'] = vec2(self.pos)
        return dict

    def draw(self, surf):
        self.un_dict()
        x = int(self.pos.x * 4) + 2
        y = int(self.pos.y * 4) + 2
        # print(x, y)
        # print(x * 4 + 2, y * 4 + 2)

        pygame.draw.circle(surf, (168, 99, 59), (x, y), 4)