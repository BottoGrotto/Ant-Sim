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
        self.is_following_food = False
        self.img = pygame.image.load("ant-16px.png")
        self.ant = AntSprite(self.img, self.pos, -self.direction)
        self.drop_marker_timer = Timer(random.randint(250, 400))
        self.marker_search_cooldown = Timer(600)
        self.marker_search_cooldown.start(loop=True)
        self.drop_marker_timer.start(loop=True)
        self.home_pos = vec2(int(self.pos.x / 4), int(self.pos.y / 4))

        self.following_marker = None
        self.last_marker = None

    def detect_food(self, food_list):
        for idx, food in enumerate(food_list):
            if self.pos.distance_to(food.pos_corrected) <= 8:  # Adjust the distance threshold as needed
                self.holding_food = True
                self.is_wondering = False
                self.is_returning_home = True
                food.amount -= 1
                if food.amount <= 0:
                    food_list.remove(food)
                return idx, True
        return 0, False


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
                temp_marker.child = self.last_marker
                place_marker = True
                self.last_marker = temp_marker
                self.following_marker = temp_marker

            if random.randint(0, 30) == 0:
                self.direction += random.randint(10, 360) * random.randint(-1, 1)
                if abs(self.direction) > 360:
                    self.direction = 360 - abs(self.direction)
                self.ant.update_dir(270 - self.direction)
        
        if self.is_returning_home:
            if self.pos.distance_to(vec2(self.home_pos.x * 4 + 2, self.home_pos.y * 4 + 2)) - 20 <= 20:
                self.is_returning_home = False
                self.is_wondering = False
                self.is_following_food = True
                self.holding_food = False
                self.drop_marker_timer.stop()
                self.marker_search_cooldown.start()
                self.following_marker = self.last_marker
                self.direction = 360 - (vec2(self.last_marker.pos.x * 4 + 2, self.last_marker.pos.y * 4 + 2) - self.pos).angle_to(vec2(1, 0))
                self.ant.update_dir(270 - self.direction)
                # print("Returned home")
                return place_marker, temp_marker
            # pygame.draw.circle(self.screen, (0, 0, 255), vec2(self.home_pos.x * 4 + 2, self.home_pos.y * 4 + 2), 2)

            if self.marker_search_cooldown.has_expired():
                last_marker = self.following_marker
                for i in range(-3, 4):
                    for j in range(-3, 4):
                        if (i, j) == (0, 0):
                            continue
                        if self.ant_i + i < 0 or self.ant_i + i >= self.screen.get_width() / 4 and self.ant_j + j < 0 or self.ant_j + j >= self.screen.get_height() / 4:
                            continue
                        marker = markers.get(f"{self.ant_i + i}{self.ant_j + j}")
                        if marker:
                            marker_pos = vec2(marker.pos.x * 4 + 2, marker.pos.y * 4 + 2)
                            last_marker_pos = vec2(last_marker.pos.x * 4 + 2, last_marker.pos.y * 4 + 2)
                            home_pos_corrected = vec2(self.home_pos.x * 4 + 2, self.home_pos.y * 4 + 2)
                            if marker.type == 0 and (marker.strength < last_marker.strength) or (marker_pos.distance_to(home_pos_corrected) - 20 < last_marker_pos.distance_to(home_pos_corrected) - 20):
                                self.following_marker = markers.get(f"{self.ant_i + i}{self.ant_j + j}")
                                last_marker = marker
                                print("New Path")
                            # self.direction = (self.following_marker.pos - self.grid_pos).angle_to(vec2(1, 0))
                            # self.ant.update_dir(270 - self.direction)
                                break
                        pygame.draw.circle(self.screen, (255, 0, 0), ((self.ant_i + i) * 4 + 2, (self.ant_j + j) * 4 + 2), 2)

            marker_pos = vec2(self.following_marker.pos.x * 4 + 2, self.following_marker.pos.y * 4 + 2)
            if self.pos.distance_to(marker_pos) < 10 if self.following_marker else False:
                self.following_marker = self.following_marker.child
                # print("switched")
            
            if self.following_marker:
                # print(self.grid_pos.distance_to(self.last_marker.pos))
                # print(self.pos.distance_to(vec2(self.following_marker.pos.x * 4 + 2, self.following_marker.pos.y * 4 + 2)))
                pygame.draw.circle(self.screen, (255, 0, 0), marker_pos, 2)
                self.direction = 360 - (marker_pos - self.pos).angle_to(vec2(1, 0))
                # print(self.direction)
                if abs(self.direction) > 360:
                    self.direction = 360 - abs(self.direction)
                # print(self.direction)
            self.ant.update_dir(270 - self.direction)

            if self.drop_marker_timer.has_expired():
                temp_marker.type = 1
                temp_marker.pos = vec2(self.ant_i , self.ant_j)
                temp_marker.color = temp_marker.marker_colors[1]
                temp_marker.strength = 1
                temp_marker.child = self.last_marker
                place_marker = True
                self.last_marker = temp_marker
        
        # if self.is_following_food:
            
        # print(ant_i, ant_j)
        # print(-self.direction)
        # print(vec2(1*math.cos(math.radians(self.direction)), 1*math.sin(math.radians(self.direction))))
        self.pos += vec2(1*math.cos(math.radians(self.direction)), 1*math.sin(math.radians(self.direction)))
        return place_marker, temp_marker
    
    def find_nearest_marker(self, markers, type=0):
        nearest_marker = None
        max_strength = -1
        for marker in markers:
            if marker.type != type:
                continue
            if marker.strength > max_strength:
                max_strength = marker.strength
                nearest_marker = marker
        return nearest_marker
    
    def find_food(self):
        pass


    def draw(self, surf):
        self.ant.update_pos(self.pos)
        surf.blit(self.ant.image, self.ant.rect)
        # print(self.pos, self.ant.rect)

