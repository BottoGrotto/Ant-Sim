import pygame
from pygame import Vector2 as vec2

class AntSprite(pygame.sprite.Sprite):
    def __init__(self, img, pos, direction):
        super().__init__()
        self.img_size = img.get_size()
        self.image = pygame.transform.scale(img, (int(self.img_size[0]*1), int(self.img_size[1]*1)))  # Assign the loaded image
        self.og_image = self.image.copy()
        self.rect = self.image.get_rect()  # Get the sprite's rectangle
        # self.img = 
        self.pos = pos
        self.rect.x = pos.x    # Set the initial x position
        self.rect.y = pos.y    # Set the initial y position
        self.angle = direction
        self.update_dir(direction)
        
    def update_dir(self, direction):
        self.image = pygame.transform.rotate(self.og_image, 270 - direction)
        self.rect = self.image.get_rect(center=self.rect.center)
        # self.angle = direction

    def update_pos(self, pos):
        # self.image = pygame.transform.rotate(self.image, direction - self.angle)
        # self.rect = self.image.get_rect(center=pos)
        self.rect.x = pos.x - self.rect.width/2
        self.rect.y = pos.y - self.rect.height/2
        # self.angle = direction
        