import pygame, sys, random
from ant import Ant
from pygame import Vector2 as vec2
from food import Food
from wall import Wall

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
        self.food_list = []
        food_pos = vec2(60, 60)
        for i in range (6):
            for j in range(6):
                self.food_list.append(Food(vec2(food_pos.x + i, food_pos.y + j), 1000))

        for i in range (6):
            for j in range(6):
                self.food_list.append(Food(vec2(70 + i, 10 + j), 10))

        for i in range (500):
            self.ants.append(Ant(self.display, "blue", False, vec2(40, 40), random.randint(0, 360)))


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
            self.markers[marker].degredate()

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
        self.degredate_markers()
        self.remove_dead_markers()
        self.check_children()
        # self.draw_markers()
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
    
    def run(self):
        while True:
            self.display.fill((255, 255, 255))
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    self.wall_dict.update({f"{int(pos[0] / 4)};{int(pos[1] / 4)}": Wall(vec2(int(pos[0] / 4), int(pos[1] / 4)), (255, 0, 0))})
                    # print(pos)
                    # print(self.grid[int(pos[1] / 4)][int(pos[0] / 4)])
                    # self.grid[int(pos[1] / 4)][int(pos[0] / 4)][0] = 1
                    # self.grid[int(pos[1] / 4)][int(pos[0] / 4)][1] = 1
                    # self.markers.update({f"{int(pos[1] / 4)};{int(pos[0] / 4)}": Marker(vec2(int(pos[1] / 4), int(pos[0] / 4)), (0, 0, 0), 1)})
                    # self.markers.update({f"{int(pos[1] / 4)};{int(pos[0] / 4)}": Marker(vec2(int(pos[1] / 4), int(pos[0] / 4)), (0, 0, 0), 1)})
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ants[0].is_wondering = not self.ants[0].is_wondering
                        self.ants[0].is_returning_home = not self.ants[0].is_returning_home
                        self.ants[0].holding_food = not self.ants[0].holding_food

                        # if self.ants[0].is_returning_home:
                        #     self.ants[0].marker_search_cooldown.start()
                        # else:
                        #     self.ants[0].marker_search_cooldown.stop()


            # self.diminish_grid()
            # self.draw_grid()
            # self.draw_markers()
            # self.display.blit()
            self.update_markers()
            self.display.blit(self.surface, (0, 0))
            
            for ant in self.ants:
                if not ant.holding_food:
                    food, has_food = ant.detect_food(self.food_list)
                    if has_food:
                        ant.holding_food = True
                        ant.is_wondering = False
                        ant.is_following_food = False
                        ant.is_returning_home = True
                        self.food_list[food].amount -= 1
                        if self.food_list[food].amount <= 0:
                            self.food_list.pop(food)
                place, marker = ant.move(self.markers)
                if place:
                    self.markers.update({f"{int(marker.pos.x)};{int(marker.pos.y)}": marker})
                ant.draw(self.display)
            for wall in self.wall_dict:
                self.wall_dict[wall].draw(self.display)
                
            for food in self.food_list:
                food.draw(self.display)

            pygame.draw.circle(self.display, (0, 0, 255), (40, 40), 20)
            pygame.display.update()


if __name__ == "__main__":
    Game((400, 400)).run()