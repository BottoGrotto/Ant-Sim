import pygame, math, random
from pygame import Vector2 as vec2
from sprites import AntSprite
from timer import Timer
from marker import Marker

class Ant:
    def __init__(self, screen, color, holding_food, pos, direction):
        self.screen = screen
        self.color = color
        self.holding_food = holding_food
        self.pos = pos
        self.direction = direction
        self.is_wondering = True
        self.is_returning_home = False
        self.img = pygame.image.load("ant-16px.png")
        self.ant = AntSprite(self.img, self.pos, -self.direction)
        self.drop_marker_timer = Timer(random.randint(250, 400))
        self.marker_search_cooldown = Timer(200)
        self.marker_search_cooldown.start(loop=True)
        self.drop_marker_timer.start(loop=True)
        self.grid_pos = vec2(int(self.pos.x / 4), int(self.pos.y / 4))


    def move(self, markers):
        place_marker = False
        temp_marker = Marker()

        self.ant_i = int(self.pos.x / 4)
        self.ant_j = int(self.pos.y / 4)

        if self.pos.x > self.screen.get_width() or self.pos.y > self.screen.get_height() or self.pos.x < 0 or self.pos.y < 0:
            if self.pos.x > self.screen.get_width():
                self.pos.x -= 2
            elif self.pos.x < 1:
                self.pos.x += 2

            if self.pos.y > self.screen.get_height():
                self.pos.y -= 2
            elif self.pos.y < 1:
                self.pos.y += 2
            
            if self.direction < 0:
                self.direction = 360 + self.direction
            # mini_angle = (360 - self.direction)
            self.direction -= 90
            self.ant.update_dir(270 - self.direction)

        if self.is_wondering:
            if self.drop_marker_timer.has_expired():
                # if grid[ant_i][ant_j][0] 
                # grid[ant_i][ant_j][0] = 1
                # grid[ant_i][ant_j][1] = 1
                # print("Dropped marker")
                temp_marker.type = 0
                temp_marker.pos = vec2(self.ant_i , self.ant_j)
                temp_marker.color = temp_marker.marker_colors[0]
                temp_marker.strength = 1
                place_marker = True

            if random.randint(0, 30) == 0:
                self.direction += random.randint(10, 360) * random.randint(-1, 1)
                if abs(self.direction) > 360:
                    self.direction = 360 - abs(self.direction)
                self.ant.update_dir(270 - self.direction)
        
        elif self.is_returning_home:
            if self.marker_search_cooldown.has_expired():
                nearest_marker = self.find_nearest_marker_nearby(markers, 0)
                if nearest_marker:
                    # print(nearest_marker)
                    # print(self.grid_pos, nearest_marker.pos)
                    direction_to_marker = (nearest_marker.pos - self.grid_pos).angle_to(vec2(0, 0))
                    # print(direction_to_marker)
                    self.direction = direction_to_marker
                    self.ant.update_dir(270 - self.direction)
                elif random.randint(0, 30) == 0:
                    self.direction += random.randint(10, 360) * random.randint(-1, 1)
                    if abs(self.direction) > 360:
                        self.direction = 360 - abs(self.direction)
                    self.ant.update_dir(270 - self.direction)

            if self.drop_marker_timer.has_expired():
                temp_marker.type = 1
                temp_marker.pos = self.grid_pos
                temp_marker.color = temp_marker.marker_colors[1]
                temp_marker.strength = 1
                place_marker = True
        
        # print(ant_i, ant_j)
        # print(-self.direction)
        self.pos += vec2(1*math.cos(math.radians(self.direction)), 1*math.sin(math.radians(self.direction)))
        return place_marker, temp_marker
    
    def find_nearest_marker_nearby(self, markers, type=0):
        nearby = [vec2(0, 1), vec2(1, 0), vec2(0, -1), vec2(-1, 0), vec2(1, 1), vec2(-1, -1), vec2(1, -1), vec2(-1, 1), vec2(-1, 2), vec2(1, 2), vec2(2, 1), vec2(2, -1), vec2(-2, 1), vec2(-2, -1), vec2(1, -2), vec2(-1, -2), vec2(0, 2), vec2(2, 0), vec2(0, -2), vec2(-2, 0), vec2(2, 2), vec2(-2, -2), vec2(2, -2), vec2(-2, 2)]
        # for i in nearby:
        #     pygame.draw.circle(self.screen, (255, 0, 0), (self.ant_i * 4 + i.x * 4, self.ant_j * 4 + i.y * 4), 2)
        self.grid_pos = vec2(self.ant_i, self.ant_j)

        nearest_marker = None
        
        for marker in markers:
            if marker.type != type:
                continue
            if nearest_marker is None:
                nearest_marker = marker
            
            # self.grid_pos.distance_to(marker.pos) < self.grid_pos.distance_to(nearest_marker.pos) or 

            if marker.strength < nearest_marker.strength:
                nearest_marker = marker
            # for pos in nearby:
            #     pos = vec2(pos.x + self.grid_pos.x, pos.y + self.grid_pos.y)
            #     if pos.x > 0 and pos.y > 0 and pos.x < int(self.screen.get_width() / 4) and pos.y < int(self.screen.get_height() / 4):
            #         if marker.pos == pos:
                        
        # print(nearest_marker.pos)    
        if nearest_marker:
            nearest_marker.color = (255, 255, 0)
            nearest_marker.draw(self.screen)
        return nearest_marker
    
    def find_food(self):
        pass


    def draw(self, surf):
        self.ant.update_pos(self.pos)
        surf.blit(self.ant.image, self.ant.rect)
        # print(self.pos, self.ant.rect)

