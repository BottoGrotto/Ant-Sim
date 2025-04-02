import pygame, sys, json
from pygame import Vector2 as vec2
from wall import Wall
from food import Food
from spawn import Spawn
from timer import Timer

class Editor:
    def __init__(self, screen_size):
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Map Editor")
        self.clock = pygame.time.Clock()
        self.screen_size = screen_size
        self.wall_dict = {}
        self.food_dict = {}
        self.spawn = Spawn()
        self.placing = True
        self.save_timer = Timer(30000)
        self.pop_up_timer = Timer(1000)
        self.save_timer.start(loop=True)
        # self.pop_up_timer.start(loop=True)
    
    # def load(self):
    #     with open("map.json", "w") as f:
    #         json.dump({"walls": self.wall_dict, "food": self.food_dict}, f, indent=4)

    def save(self):
        wall_data = []
        for i in self.wall_dict:
            wall_data.append(self.wall_dict[i].to_dict())

        food_data = []
        for i in self.food_dict:
            food_data.append(self.food_dict[i].to_dict())

        with open("map.json", "w") as f:
            json.dump({"walls": wall_data, "food": food_data, "spawn": self.spawn.to_dict()}, f, indent=4)
        self.pop_up_timer.start()
        pygame.display.set_caption("Map Editor - Saved!")

    def load_map(self):
        with open("map.json", "r") as f:
            data = json.load(f)

        for wall in data["walls"]:
            wall_obj = Wall(vec2(wall["pos"]), wall["color"])
            self.wall_dict.update({f"{int(wall_obj.pos.x)};{int(wall_obj.pos.y)}": wall_obj})

        for food in data["food"]:
            food_obj = Food(vec2(food['pos']), food["amount"])
            self.food_dict.update({f"{int(food_obj.pos.x)};{int(food_obj.pos.y)}": food_obj})

        self.spawn = Spawn(vec2(data['spawn']['world_pos']))

    def draw(self):
        for wall in self.wall_dict.values():
            wall.draw(self.screen)
        for food in self.food_dict.values():
            food.draw(self.screen)

        self.spawn.draw(self.screen)    
        
    def run(self):
        self.load_map()
        while True:
            self.screen.fill((255, 255, 255))
            self.clock.tick(60)
            if self.pop_up_timer.has_expired():
                pygame.display.set_caption("Map Editor")
                self.save_timer.restart()
            if self.save_timer.has_expired():
                self.save()
            mouse_pos = pygame.mouse.get_pos()
            mouse_buttons = pygame.mouse.get_pressed()

            mouse_grid_pos = vec2(int(mouse_pos[0] / 4), int(mouse_pos[1] / 4))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.placing = not self.placing
                    if event.key == pygame.K_s:
                        self.save()
                    if event.key == pygame.K_SPACE:
                        self.spawn.world_pos = vec2(mouse_pos[0], mouse_pos[1])

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
                        


            self.draw()
            pygame.display.update()
        
if __name__ == "__main__":
    pygame.init()
    editor = Editor((800, 800))
    editor.run()