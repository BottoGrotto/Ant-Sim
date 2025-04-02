import pygame
from pygame import Vector2 as vec2

pos1 = vec2(0, 0)
pos2 = vec2(100, 100)
pos3 = vec2(100, 100)

def degregation_speed(self, home_pos, screen_size):
    max_dist = home_pos.distance_to(vec2(screen_size[0], screen_size[1]))
    dist = home_pos.distance_to(pos3)
    return (dist / max_dist) * 0.0001 + 0.0001


print(degregation_speed(None, pos1, pos2))