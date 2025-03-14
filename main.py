import pygame, sys
from ant import Ant
from pygame import Vector2 as vec2

pygame.init()

class Game:
    def __init__(self, size):
        self.size = size
        self.display = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.grid = self.create_grid()
        self.ants = []
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.markers = []

        for i in range (10):
            self.ants.append(Ant(self.display, "blue", False, vec2(40, 40), 0))


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


    def degredate_markers(self):
        for marker in self.markers:
            marker.degredate()

    def remove_dead_markers(self):
        for marker in self.markers.copy():
            if marker.strength <= 0.0:
                # print("removed")
                self.markers.remove(marker)

    def draw_markers(self):
        for marker in self.markers:
            marker.draw(self.surface)

    def update_markers(self):
        self.degredate_markers()
        self.remove_dead_markers()
        # print(len(self.markers))
        self.draw_markers()
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ants[0].is_wondering = not self.ants[0].is_wondering
                        self.ants[0].is_returning_home = not self.ants[0].is_returning_home
                        self.ants[1].is_wondering = not self.ants[1].is_wondering
                        self.ants[1].is_returning_home = not self.ants[1].is_returning_home
                        self.ants[2].is_wondering = not self.ants[2].is_wondering
                        self.ants[2].is_returning_home = not self.ants[2].is_returning_home
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
                place, marker = ant.move(self.markers)
                if place and marker not in self.markers:
                    # print("adding new marker")
                    self.markers.append(marker)
                elif place:
                    # print("swapping marker")
                    # print(self.markers.index(marker))
                    self.markers[self.markers.index(marker)] = marker
                ant.draw(self.display)
                
                
            # for ant in self.ants:

            # self.remove_dead_markers()
            pygame.display.update()


if __name__ == "__main__":
    Game((400, 400)).run()