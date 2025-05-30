import pygame, math, random
from pygame import Vector2 as vec2
from sprites import AntSprite
from timer import Timer
from marker import Marker

class Ant:
    total_food_collected = 0
    def __init__(self, screen, color, holding_food, pos, direction):
        self.screen = screen
        self.color = color
        self.holding_food = holding_food
        self.pos = pos
        self.ant_i = int(self.pos.x / 4)
        self.ant_j = int(self.pos.y / 4)

        self.direction = direction
        self.is_wondering = True
        self.is_returning_home = False
        self.is_following_food = False
        self.img = pygame.image.load("ant-16px.png")
        self.ant = AntSprite(self.img, self.pos, self.direction)
        self.drop_marker_timer = Timer(random.randint(250, 400))
        self.marker_search_cooldown = Timer(600)
        self.join_cooldown = Timer(random.randint(400, 1000))
        
        self.marker_search_cooldown.start(loop=True)
        self.drop_marker_timer.start(loop=True)
        self.home_pos = vec2(int(self.pos.x / 4), int(self.pos.y / 4))
        self.home_marker = Marker(self.home_pos, (0, 0, 0), 1)
        # self.death_timer = Timer(random.randint(30000, 40000))
        # self.death_timer.start()

        self.following_marker = None
        self.last_marker = None


    def drop_marker(self, type, pos=None):
        temp_marker = Marker()
        place_marker = False
        if self.drop_marker_timer.has_expired():
            temp_marker.type = type
            if pos:
                temp_marker.pos = pos
                temp_marker.world_pos = vec2(pos.x * 4 + 2, pos.y * 4 + 2)
            else:
                temp_marker.pos = vec2(self.ant_i , self.ant_j)
                temp_marker.world_pos = vec2(self.ant_i * 4 + 2, self.ant_j * 4 + 2)
            temp_marker.color = temp_marker.marker_colors[type]
            temp_marker.strength = 1
            temp_marker.child = self.last_marker
            # temp_marker.arrow.update_pos(temp_marker.world_pos)
            # if self.last_marker:
            #     temp_marker.arrow.update_dir((temp_marker.world_pos - self.last_marker.world_pos).angle_to(vec2(1, 0)))
            place_marker = True
            self.last_marker = temp_marker
            # if type == 0 and not self.is_returning_home and not self.is_following_food:
            #     self.following_marker = temp_marker
        return (place_marker, temp_marker)
    
    def check_if_home(self):
        if self.pos.distance_to(vec2(self.home_pos.x * 4 + 2, self.home_pos.y * 4 + 2)) <= 22:
            self.holding_food = False
            self.is_returning_home = False
            self.is_following_food = True
            self.following_marker = self.last_marker
            # self.is_wondering = True
            Ant.total_food_collected += 1
            # print(Ant.total_food_collected)
            return True
        if self.pos.distance_to(vec2(self.home_pos.x * 4 + 2, self.home_pos.y * 4 + 2)) <= 40:
            self.direction = 360 - (vec2(self.ant_i, self.ant_j) - self.home_pos).angle_to(vec2(1, 0))
            self.following_marker = self.home_marker
        return False
    
    def check_surrounding(self, m_type, s_type = None):
        closest_marker = Marker(pos=vec2(self.ant_i, self.ant_j), strength=1)
        # print(self.markers)
        search_area = -3
        # if self.is_following_food:
        #     search_area = -1
        # if self.is_returning_home:
        #     search_area = -4
        for i in range(search_area, abs(search_area) + 1):
            for j in range(search_area, abs(search_area) + 1):
                if (i, j) == (0, 0):
                    continue
                if self.ant_i + i < 0 or self.ant_i + i >= self.screen.get_width() / 4 and self.ant_j + j < 0 or self.ant_j + j >= self.screen.get_height() / 4:
                    continue
                
                marker = self.markers.get(f"{self.ant_i + i};{self.ant_j + j}")
                # print(marker)
                if marker:
                    # print("marker found!")
                    home_pos = vec2(self.home_pos.x * 4, self.home_pos.y * 4)
                    if m_type == 0 or m_type == 2:
                        # (marker.world_pos.distance_to(home_pos) < closest_marker.world_pos.distance_to(home_pos)) if random.randint(0, 20) == 0 else 
                        if m_type == 2:
                            if random.randint(0, 10) == 0:
                                if marker.type == m_type and marker.strength < closest_marker.strength and marker.world_pos.distance_to(home_pos) < closest_marker.world_pos.distance_to(home_pos):
                                    closest_marker = marker
                                    
                            elif marker.type == m_type and marker.strength < closest_marker.strength:
                                closest_marker = marker
                        elif marker.type == m_type and marker.strength < closest_marker.strength:
                            closest_marker = marker
                    elif m_type == 1:
                        if random.randint(0, 10) == 0:
                            food = self.find_food(self.food_dict)
                            if food:
                                if marker.type == m_type and marker.strength < closest_marker.strength and marker.pos_corrected.distance_to(food.pos_corrected) < closest_marker.world_pos.distance_to(food.world_pos):
                                    closest_marker = marker
                                    
                        elif marker.type == m_type and marker.strength < closest_marker.strength:
                            closest_marker = marker
                        # pygame.draw.circle(self.screen, (255, 255, 0), vec2((self.ant_i + i) * 4 + 2, (self.ant_j + j) * 4 + 2), 2)
                        # print("Swapped closest!")
                # else:
                # pygame.draw.circle(self.screen, (255, 0, 0), vec2((self.ant_i + i) * 4 + 2, (self.ant_j + j) * 4 + 2), 2)
        # if closest_marker == Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
        #     self.
        return closest_marker

    def nav_wander(self):
        if random.randint(0, 20) == 0:
            self.direction += random.randint(10, 45) * random.randint(-1, 1)
            if abs(self.direction) > 360:
                self.direction = abs(self.direction) - 360

        if self.holding_food:
            # print("Nav Wander")
            temp = self.check_surrounding(0)
            if temp and temp != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                self.following_marker = temp
                self.is_returning_home = True
                self.is_wondering = False
            self.check_if_home()
  
            self.ant.update_dir(self.direction)
            return self.drop_marker(1)

        if self.is_following_food:
            temp = self.check_surrounding(1)
            if temp and temp != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                self.following_marker = temp
                self.is_wondering = False

                self.ant.update_dir(self.direction)
                return self.drop_marker(2)
        if random.randint(0, 50) == 0 and self.join_cooldown.has_expired():
            temp = self.check_surrounding(1)
            temp2 = self.check_surrounding(2)
            if temp2 and temp2 != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):  
                if temp and temp != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                    self.is_wondering = False
                    self.is_following_food = True
                    self.place_marker = False
                    self.following_marker = temp

                    self.ant.update_dir(self.direction)
                    return self.drop_marker(2)

        self.ant.update_dir(self.direction)
        return self.drop_marker(0)

    def nav_home(self):
        if self.following_marker:
            if self.pos.distance_to(self.following_marker.world_pos) <= 5:
                temp = self.following_marker.child
                if not temp: 
                    temp = self.check_surrounding(0)
                    temp2 = self.check_surrounding(2)
                    if temp2 and temp2 != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                        temp = temp2
                    if not temp or temp == Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                        self.is_wondering = True
                        self.is_returning_home = False
                        return self.drop_marker(1)
                self.following_marker = temp
            elif random.randint(0, 10) == 0:
                temp = self.check_surrounding(0)
                temp2 = self.check_surrounding(2)
                if temp2 and temp2 != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                    temp = temp2
                # print(temp.pos, self.ant_i, self.ant_j)
                if temp and temp != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                    self.following_marker = temp
                    # print("Following difference marker")
        else:
            # print("Nav Home no marker")
            temp = self.check_surrounding(0)
            temp2 = self.check_surrounding(2)
            if temp and temp2 != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                temp = temp2
            if not temp or temp == Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                self.is_wondering = True
                self.is_returning_home = False
                return self.drop_marker(1)
            # if temp == Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
            #     self.is_wondering = True
            self.following_marker = temp
        # print(self.following_marker.pos)
        # pygame.draw.circle(self.screen, (0, 0, 255), self.following_marker.world_pos, 2)
        
        self.direction = 360 - (self.following_marker.world_pos - self.pos).angle_to(vec2(1, 0))
        self.ant.update_dir(self.direction)
        # self.following_marker = self.following_marker.child
        return self.drop_marker(1)


    def nav_food(self):
        if self.following_marker:
            if self.pos.distance_to(self.following_marker.world_pos) <= 0.5:
                temp = self.following_marker.child
                if not temp:
                    
                    # print("No child")
                    # temp = self.check_surrounding(1)
                    # if not temp or temp == Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
                    self.is_wondering = True
                    self.join_cooldown = Timer(random.randint(400, 1000))
                    self.join_cooldown.start()
                    self.is_returning_home = False
                    self.ant.update_dir(self.direction)
                    return self.drop_marker(2)
                self.following_marker = temp
            elif random.randint(0, 20) == 0:
                food = self.find_food(self.food_dict) 
                if food:
                    self.direction = 360 - (food.pos_corrected - self.pos).angle_to(vec2(1, 0))
                    self.ant.update_dir(self.direction)
                    return self.drop_marker(2)
            # elif random.randint(0, 40) == 0:
            #     temp = self.check_surrounding(1)
            #     if temp and temp != Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
            #         self.following_marker = temp
            
        else:
            food = self.find_food(self.food_dict)
            if food:
                self.direction = 360 - (food.pos_corrected - self.pos).angle_to(vec2(1, 0))
                self.ant.update_dir(self.direction)
                return self.drop_marker(2)
            # if random.randint(0, 20) == 0:
            #     temp = self.check_surrounding(1)
            #     if not temp or temp == Marker(pos=vec2(self.ant_i, self.ant_j), strength=1):
            #         self.is_wondering = True
            #         self.join_cooldown = Timer(random.randint(400, 1000))
            #         self.join_cooldown.start()
            #         return self.drop_marker(2)  
            #     self.following_marker = temp
            # else:
            self.is_wondering = True
            # # self.following_marker = temp
            # return self.drop_marker(2)
        self.direction = 360 - (self.following_marker.world_pos - self.pos).angle_to(vec2(1, 0))
        self.ant.update_dir(self.direction)
        # self.following_marker = self.following_marker.child
        if self.place_marker:
            return self.drop_marker(2)
        else:
            return (False, Marker())

    def navigate(self, markers, wall_dict, food_dict):
        self.markers = markers
        self.wall_dict = wall_dict
        self.food_dict = food_dict
        self.ant_i = int(self.pos.x / 4)
        self.ant_j = int(self.pos.y / 4)

        if self.is_wondering:
            return self.nav_wander()
        elif self.is_returning_home:
            if not self.check_if_home():
                return self.nav_home()
            return (False, Marker())
        else:
            return self.nav_food()
        
    def check_collision(self, wall_dict):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) == (0, 0):
                    continue
                if self.ant_i + i < 0 or self.ant_i + i >= self.screen.get_width() / 4 and self.ant_j + j < 0 or self.ant_j + j >= self.screen.get_height() / 4:
                    continue
                wall = wall_dict.get(f"{self.ant_i + i};{self.ant_j + j}")
                if wall:
                    # if abs((wall.world_pos - self.pos).angle_to(vec2(1, 0)) - self.direction) <= 45:
                    #     print(abs((wall.world_pos - self.pos).angle_to(vec2(1, 0))))

                    temp_pos = self.pos + vec2(1*math.cos(math.radians(self.direction)), 1*math.sin(math.radians(self.direction)))
                    # print(temp_pos, wall.world_pos)
                    if (temp_pos.x >= wall.world_pos.x and temp_pos.x <= wall.world_pos.x + wall.width) and (temp_pos.y >= wall.world_pos.y and temp_pos.y <= wall.world_pos.y + wall.height):
                        # print("Hit!")
                        self.direction = self.direction + 180
                        # if abs(self.direction) > 360:
                        #     self.direction = 360 - abs(self.direction)
                        self.pos += vec2(1*math.cos(math.radians(self.direction)), 1*math.sin(math.radians(self.direction)))
    
                        self.ant.update_dir(self.direction)
                        return True
        return False


    
    def move(self, markers, wall_dict, food_dict):
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

            self.direction -= 90
            self.ant.update_dir(self.direction)
      
        result = self.navigate(markers, wall_dict, food_dict)
        
            # if not self.is_returning_home:
            #     self.is_returning_home = True
            # if not self.is_following_food:
            #     self.is_following_food = True
        if self.check_collision(wall_dict) and not self.is_wondering:
            self.is_wondering = True

        self.pos += vec2(1*math.cos(math.radians(self.direction)), 1*math.sin(math.radians(self.direction)))
        
        return result
    
    def find_food(self, food_dict):
        search_area = -3
        # last_food = food_dict.get(f"{self.ant_i};{self.ant_j}")
        for i in range(search_area, abs(search_area) + 1):
            for j in range(search_area, abs(search_area) + 1):
                if self.ant_i + i < 0 or self.ant_i + i >= self.screen.get_width() / 4 and self.ant_j + j < 0 or self.ant_j + j >= self.screen.get_height() / 4:
                    continue
                food = food_dict.get(f"{self.ant_i + i};{self.ant_j + j}")
                if food:
                    return food
        return None

    def detect_food(self, food_dict):
        search_area = -1
        if self.is_following_food:
            search_area = -1
        for i in range(search_area, abs(search_area) + 1):
            for j in range(search_area, abs(search_area) + 1):
                if self.ant_i + i < 0 or self.ant_i + i >= self.screen.get_width() / 4 and self.ant_j + j < 0 or self.ant_j + j >= self.screen.get_height() / 4:
                    continue
                food = food_dict.get(f"{self.ant_i + i};{self.ant_j + j}")
                # print(food)
                if food:
                    self.place_marker = True
                    self.drop_marker(1, pos=vec2(self.ant_i + i, self.ant_j + j))

                    return f"{self.ant_i + i};{self.ant_j + j}", True
        return "", False        
        


    def move_deprecated(self, markers):
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
                                # print("New Path")
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
    
    # def find_food(self):
    #     pass


    def draw(self, surf, info):
        self.ant.update_pos(self.pos)
        if self.holding_food:
            pygame.draw.circle(surf, (168, 99, 59), self.pos + vec2(5*math.cos(math.radians(self.direction)), 5*math.sin(math.radians(self.direction))), 3)
        surf.blit(self.ant.image, self.ant.rect)
        if info:
            if self.is_wondering:
                pygame.draw.circle(surf, (255, 0, 38), self.pos, 2)
            elif self.is_returning_home:
                pygame.draw.circle(surf, (2, 2, 247), self.pos, 2)
            else:
                pygame.draw.circle(surf, (252, 244, 3), self.pos, 2)
        
        # print(self.pos, self.ant.rect)

