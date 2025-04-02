import pygame
from pygame import Vector2 as vec2

class Marker:
    def __init__(self, pos=vec2(0, 0), color=(0,0,0), strength=0):
        self.child = None
        self.pos = pos
        self.world_pos = vec2((pos.x * 4) + 2, (pos.y * 4) + 2)
        self.color = color
        self.strength = strength
        self.marker_colors = [(144, 19, 194), (5, 235, 55), (255, 108, 10)]
        self.type = 0
    
    def check_child(self):
        if self.child:
            if self.child.strength <= 0.01:
                self.child = None

    def degredate(self, deg_speed):
        if self.strength >= 0.001:
            self.strength -= deg_speed + (2 - self.type) * 0.001
        else:
            self.strength = 0.00

    def degregation_speed(self, home_pos, screen_size):
        if self.type == 0:
            max_dist = home_pos.distance_to(vec2(screen_size[0], screen_size[1]))
            dist = home_pos.distance_to(self.pos)
            return dist / max_dist
        return 0.0001

    def __eq__(self, value):
        if value.pos == self.pos:
            return True
        return False
        # print(self.strength)

    def draw(self, surf):
        # color = pygame.Color()
        pygame.draw.circle(surf, (self.color[0], self.color[1], self.color[2], self.strength * 225), (self.pos.x * 4 + 2, self.pos.y * 4 + 2), 4)
        # pygame.draw.circle(surf, (self.color[0], self.color[1], self.color[2], self.strength * 200), (self.pos.x * 4 + 2, self.pos.y * 4 + 2), 3)
        # pygame.draw.circle(surf, (self.color[0], self.color[1], self.color[2], self.strength * 255), (self.pos.x * 4 + 2, self.pos.y * 4 + 2), 2)
