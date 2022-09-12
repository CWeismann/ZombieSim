import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Zombie Sim"
SCALING = 2.0

NUM_ZOMBIES = 2
NUM_HUMANS = 5
INCUBATION_PERIOD = 10.0

WALL_LENGTH = SCALING * 25 # May be inaccurate - testing needed

class Wall(arcade.Sprite):
    def __init__(self, image, scale, left, top):
        """"""
        super().__init__(image, scale)
        self.left = left
        self.top = top
        self.vert_texture = arcade.load_texture("images/vert.png")
        self.horiz_texture = arcade.load_texture("images/horiz.png")
        if image == "images/vert.png":
            self.texture = self.vert_texture
        else:
            self.texture = self.horiz_texture

    def get_texture(self):
        if self.texture == self.vert_texture:
            return "vert"
        else:
            return "horiz"
    
    # def get_edge_range(self):
    #     topEdge = (self.top - WALL_LENGTH/10.0, self.top + WALL_LENGTH/10.0)
    #     bottomEdge = (self.bottom - WALL_LENGTH/10.0, self.bottom + WALL_LENGTH/10.0)
    #     leftEdge = (self.left - WALL_LENGTH/10.0, self.left + WALL_LENGTH/10.0)
    #     rightEdge = (self.right - WALL_LENGTH/10.0, self.right + WALL_LENGTH/10.0)
    #     return [topEdge, bottomEdge, leftEdge, rightEdge]
        

class MovingSprite(arcade.Sprite):
    def __init__(self, image, scale):
        """"""
        super().__init__(image, scale)

        self.human_texture = arcade.load_texture("images/circleNoFill.png")
        self.infected_texture = arcade.load_texture("images/circleFill.png")
        self.zombie_texture = arcade.load_texture("images/cross.png")

        self.infection_time = 0

    def become_human(self):
        self.texture = self.human_texture
    def become_infected(self):
        self.texture = self.infected_texture
    def become_zombie(self):
        self.texture = self.zombie_texture

    def get_infection_time(self):
        return self.infection_time

    def inc_infection_time(self, dt):
        self.infection_time += dt

class ZombieSim(arcade.Window):
    """DOCSTRING"""

    def __init__(self, width, height, title):
        """"""
        super().__init__(width, height, title)

        self.zombies_list = arcade.SpriteList()
        self.infected_list = arcade.SpriteList()
        self.humans_list = arcade.SpriteList()
        self.moving_list = arcade.SpriteList()

        self.walls_list = arcade.SpriteList()

        self.all_sprites = arcade.SpriteList()


    def setup(self):
        """"""
        arcade.set_background_color(arcade.color.WHITE)
        
        zombies = []
        for i in range(NUM_ZOMBIES):
            zombies += [MovingSprite("images/cross.png", SCALING/20)]
            zombies[i].left = 30 * (i + 1)
            zombies[i].top = 30
            zombies[i].velocity = (random.random()*4-2, random.random()*4-2)
            self.zombies_list.append(zombies[i])
            self.moving_list.append(zombies[i])
            self.all_sprites.append(zombies[i])
        
        humans = []
        for i in range(NUM_HUMANS):
            humans += [MovingSprite("images/circleNoFill.png", SCALING/20)]
            humans[i].left = 30 * (i + 1)
            humans[i].top = 230
            humans[i].velocity = (random.random()*4-2, random.random()*4-2)
            self.humans_list.append(humans[i])
            self.moving_list.append(humans[i])
            self.all_sprites.append(humans[i])
        
        walls = []
        for i in range(8):
            walls += [Wall("images/vert.png", SCALING/5, 200, 50*i+150)]
            walls += [Wall("images/vert.png", SCALING/5, 600, 50*i+150)]
            walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 100)]
        walls += [Wall("images/vert.png", SCALING/5, 200, 350)]
        walls += [Wall("images/vert.png", SCALING/5, 200, 400)]
        
        for wall in walls:
            self.walls_list.append(wall)
            self.all_sprites.append(wall)

    def on_update(self, delta_time: float = 1/60):
        """"""

        for human in self.humans_list:
            if human.collides_with_list(self.zombies_list):
                self.make_infected(human)
            
        for infected in self.infected_list:
            infected.inc_infection_time(delta_time)
            if infected.get_infection_time() >= INCUBATION_PERIOD:
                self.make_zombie(infected)
        
        for moving in self.moving_list:
            oldvel = moving.velocity

            struck_wall = moving.collides_with_list(self.walls_list)
            if struck_wall:
                # edges = struck_wall[0].get_edge_range()
                if struck_wall[0].get_texture() == "vert":
                    # if moving.bottom >= edges[0][0] and moving.bottom <= edges[0][1]:
                    #     moving.velocity = (-oldvel[0],-oldvel[1])
                    # elif moving.top >= edges[1][0] and moving.top <= edges[1][1]:
                    #     moving.velocity = (-oldvel[0],-oldvel[1])
                    # else:
                    moving.velocity = (-oldvel[0],oldvel[1])
                    # moving.left -= 2*oldvel[0]
                else:
                    # if moving.right >= edges[2][0] and moving.right <= edges[2][1]:
                    #     moving.velocity = (-oldvel[0],-oldvel[1])
                    # elif moving.left >= edges[3][0] and moving.left <= edges[3][1]:
                    #     moving.velocity = (-oldvel[0],-oldvel[1])
                    # else:           
                    moving.velocity = (oldvel[0],-oldvel[1]) 
                    # moving.top -= 2*oldvel[1]

            if moving.bottom < 0:
                moving.velocity = (oldvel[0],-oldvel[1])
            if moving.left < 0:
                moving.velocity = (-oldvel[0],oldvel[1])
            if moving.top > self.height:
                moving.velocity = (oldvel[0],-oldvel[1])
            if moving.right > self.width:
                moving.velocity = (-oldvel[0],oldvel[1])
        
        self.all_sprites.update()


    def on_draw(self):
        """"""
        arcade.start_render()
        self.all_sprites.draw()

    def make_human(self, new_human):
        """"""
        pass

    def make_infected(self, new_infected):
        """"""
        self.humans_list.remove(new_infected)
        new_infected.become_infected()
        self.infected_list.append(new_infected)
    
    def make_zombie(self, new_zombie):
        """"""
        self.infected_list.remove(new_zombie)
        new_zombie.become_zombie()
        self.zombies_list.append(new_zombie)  
        if len(self.humans_list) == 0:
            arcade.close_window()

if __name__ == "__main__":
    app = ZombieSim(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
    app.setup()
    arcade.run()
