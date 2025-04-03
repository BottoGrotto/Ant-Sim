import pygame, sys, random, json
from ant import Ant
from pygame import Vector2 as vec2
from food import Food
from wall import Wall
from spawn import Spawn

pygame.init()

class Game:
    def __init__(self, size):
        self.size = size
        self.display = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.grid = self.create_grid()
        self.ants = []
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.markers = {}
        self.wall_dict = {}
        self.food_dict = {}
        food_pos = vec2(60, 60)
        # for i in range (6):
        #     for j in range(6):
        #         self.food_dict.update({f"{int(food_pos.x + i)};{int(food_pos.y + j)}": Food(vec2(food_pos.x + i, food_pos.y + j), 1000)})

        # for i in range (6):
        #     for j in range(6):
        #         self.food_list.append(Food(vec2(70 + i, 10 + j), 10))
        self.spawn = Spawn()

        self.load_map()

        # print(self.spawn.world_pos)
        for i in range (800):
            self.ants.append(Ant(self.display, "blue", False, self.spawn.world_pos.copy(), random.randint(0, 360)))

        self.draw_ants = 0
        self.last_food_count = 0
        self.pause = False
        self.info = True
        self.placing = True



    def create_grid(self):
        grid = list(range(int(self.size[1]/ 4)))
        for idx, v in enumerate(grid):
            grid[idx] = list(range(int(self.size[0] / 4)))
            for jdx, v in enumerate(grid[idx]):
                grid[idx][jdx] = list(range(2))
                grid[idx][jdx][0] = 0
                grid[idx][jdx][1] = 0
        return grid
    
    # def diminish_grid(self):
    #     for idx, row in enumerate(self.grid):
    #         for jdx, col in enumerate(self.grid[idx]):
    #             if self.grid[idx][jdx][0] > 0.1:
    #                 self.grid[idx][jdx][0] -= 0.001
    #                 # print(self.grid[idx][jdx][0])
    #             else:
    #                 self.grid[idx][jdx][1] = 0.0

    def draw_grid(self):
        gap = 4
        for i in range(int(self.size[0]/4)):
            pygame.draw.line(self.display, "white", (0, gap), (self.size[0], gap), 1)
            gap += 4
        gap = 4
        for j in range(int(self.size[1]/4)):
            pygame.draw.line(self.display, "white", (gap, 0), (gap, self.size[1]), 1)
            gap += 4

    def check_children(self):
        for marker in self.markers:
            self.markers[marker].check_child()

    def degredate_markers(self):
        for marker in self.markers:
            # deg_speed = self.markers[marker].degregation_speed()
            deg_speed = 0.0001
            self.markers[marker].degredate(deg_speed)

    def remove_dead_markers(self):
        for marker in self.markers.copy():
            if self.markers[marker].strength <= 0.0:
                # print("removed")
                del self.markers[marker]

    def draw_markers(self):
        for marker in self.markers:
            # if self.markers[marker].type == 2:
            self.markers[marker].draw(self.surface)

    def update_markers(self):
        if not self.pause:
            self.degredate_markers()
            self.remove_dead_markers()
            self.check_children()
        if self.draw_ants == 1 or self.draw_ants == 2:
            self.draw_markers()
        else:
            self.surface.fill("white")
        # for idx, row in enumerate(self.grid):
        #     for jdx, col in enumerate(self.grid):
        #         strength = self.grid[idx][jdx][0]
        #         if strength == 0:
        #             continue
        #         ptype = self.grid[idx][jdx][1]
        #         if strength != 0 and ptype != 0:
        #             color = self.pharamon_colors[ptype - 1]
        #             # print(color, strength)
        #             pygame.draw.circle(self.display, (color[0], color[1], color[2], strength * 255), (idx * 4 + 2, jdx * 4 + 2), 2)
    def load_map(self):
        with open("map.json", "r") as f:
            data = json.load(f)

        for wall in data["walls"]:
            wall_obj = Wall(vec2(wall["pos"]), wall["color"])
            self.wall_dict.update({f"{int(wall_obj.pos.x)};{int(wall_obj.pos.y)}": wall_obj})

        for food in data["food"]:
            food_obj = Food(vec2(food['pos']), food["amount"])
            self.food_dict.update({f"{int(food_obj.pos.x)};{int(food_obj.pos.y)}": food_obj})

        self.spawn = Spawn(vec2(data["spawn"]["world_pos"]))
    
    def run(self):
        while True:
            self.display.fill((255, 255, 255))
            self.clock.tick(60)
            pygame.display.set_caption('FPS: ' + str(int(self.clock.get_fps())) + " Ants: " + str(len(self.ants)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                   
                    # print(pos)
                    # print(self.grid[int(pos[1] / 4)][int(pos[0] / 4)])
                    # self.grid[int(pos[1] / 4)][int(pos[0] / 4)][0] = 1
                    # self.grid[int(pos[1] / 4)][int(pos[0] / 4)][1] = 1
                    # self.markers.update({f"{int(pos[1] / 4)};{int(pos[0] / 4)}": Marker(vec2(int(pos[1] / 4), int(pos[0] / 4)), (0, 0, 0), 1)})
                    # self.markers.update({f"{int(pos[1] / 4)};{int(pos[0] / 4)}": Marker(vec2(int(pos[1] / 4), int(pos[0] / 4)), (0, 0, 0), 1)})
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                    if event.key == pygame.K_o:
                        self.draw_ants += 1
                        if self.draw_ants >= 3:
                            self.draw_ants = 0
                    if event.key == pygame.K_i:
                        self.info = not self.info
                    if event.key == pygame.K_d:
                        self.placing = not self.placing
                    


                        # if self.ants[0].is_returning_home:
                        #     self.ants[0].marker_search_cooldown.start()
                        # else:
                        #     self.ants[0].marker_search_cooldown.stop()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            mouse_grid_pos = vec2(int(mouse_pos[0] / 4), int(mouse_pos[1] / 4))

            if mouse_buttons[0]:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        pos = vec2(int(mouse_grid_pos.x + i), int(mouse_grid_pos.y + j))

                        if self.placing:
                            self.wall_dict.update({f"{int(pos.x)};{int(pos.y)}": Wall(pos, (255, 0, 0))})
                        elif self.wall_dict.get(f"{int(pos.x)};{int(pos.y)}"):
                            del self.wall_dict[f"{int(pos.x)};{int(pos.y)}"]

            if mouse_buttons[2]:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        pos = vec2(int(mouse_grid_pos.x + i), int(mouse_grid_pos.y + j))

                        if self.placing:
                            self.food_dict.update({f"{int(pos.x)};{int(pos.y)}": Food(pos, 20)})
                        elif self.food_dict.get(f"{int(pos.x)};{int(pos.y)}"):
                            del self.food_dict[f"{int(pos.x)};{int(pos.y)}"]
            # self.diminish_grid()
            # self.draw_grid()
            # self.draw_markers()
            # self.display.blit()
            self.update_markers()
            self.display.blit(self.surface, (0, 0))
            
            for wall in self.wall_dict:
                self.wall_dict[wall].draw(self.display)
            
            for ant in self.ants:
                # if ant.death_timer.has_expired():
                #     self.ants.remove(ant)
                #     continue
                if not self.pause:
                    if not ant.holding_food:
                        # print(self.food_dict)
                        food, has_food = ant.detect_food(self.food_dict)
                        if has_food:
                            ant.holding_food = True
                            ant.is_wondering = False
                            ant.is_following_food = False
                            ant.is_returning_home = True
                            self.food_dict[food].amount -= 1
                            if self.food_dict[food].amount <= 0:
                                del self.food_dict[food]
                    place, marker = ant.move(self.markers, self.wall_dict, self.food_dict)
                    if place:
                        place_over = False
                        mk = self.markers.get(f"{int(marker.pos.x)};{int(marker.pos.y)}")
                        if mk:
                            if mk.strength < 0.25:
                                place_over = True
                        if not mk or marker.type != 0 or place_over:
                            self.markers.update({f"{int(marker.pos.x)};{int(marker.pos.y)}": marker})
                
                
                if self.draw_ants == 0 or self.draw_ants == 2:
                    ant.draw(self.display, self.info)
            
                
            for food in self.food_dict:
                self.food_dict[food].draw(self.display)
            
            for i in range(0, Ant.total_food_collected - self.last_food_count):
                if random.randint(0, 10) == 0:
                    self.ants.append(Ant(self.display, "blue", False, self.spawn.world_pos.copy(), random.randint(0, 360)))
            self.last_food_count = Ant.total_food_collected
                        
            # pygame.draw.circle(self.display, (0, 0, 255), (40, 40), 20)
            self.spawn.draw(self.display)
            pygame.display.update()


if __name__ == "__main__":
    Game((800, 800)).run()