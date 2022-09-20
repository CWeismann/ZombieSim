from calendar import c
import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STATS_HEIGHT = 100
SCREEN_TITLE = "Zombie Sim"
SCALING = 2.0

NUM_ZOMBIES = 2
NUM_HUMANS = 5
INCUBATION_PERIOD = 10.0 # seconds
SPEED = 3.0
WALL_GEN = 2 # larger value = more walls

WALL_LENGTH = SCALING * 25 # May be inaccurate - testing needed

class Wall(arcade.Sprite):
    def __init__(self, image, scale, left, top):
        """
        Initializes a new Wall sprite
        Inputs: the starting sprite image, the scaling of the screen,
                the x coordinate of the left of the sprite, and the y
                coordinate of the top of the sprite
        """
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


class MovingSprite(arcade.Sprite):
    def __init__(self, image, scale):
        """
        Initializes a new MovingSprite sprite (Human/Zombie/Infected)
        Inputs: the starting sprite image, and the scaling of the screen
        """
        super().__init__(image, scale)

        self.human_texture = arcade.load_texture("images/circleNoFill.png")
        self.infected_texture = arcade.load_texture("images/circleFill.png")
        self.zombie_texture = arcade.load_texture("images/cross.png")

        self.human_time = 0
        self.infection_time = 0

        self.stat_text = arcade.Text(
            text = "",
            start_x = SCREEN_WIDTH / 2,
            start_y = STATS_HEIGHT / 4,
            color = arcade.color.BLACK,
            font_size = 5,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            anchor_y = "center"
        )

    # Texture changes for role changes
    def become_human(self):
        self.texture = self.human_texture
    def become_infected(self):
        self.texture = self.infected_texture
    def become_zombie(self):
        self.texture = self.zombie_texture

    # Returns the amount of time that an infected has been infected
    def get_infection_time(self):
        return self.infection_time
    def get_human_time(self):
        return self.human_time
    def get_stat_text(self):
        return self.stat_text
    # Increases the amount of time that an infected has been infected
    def inc_infection_time(self, dt):
        self.infection_time += dt
    def inc_human_time(self, dt):
        self.human_time += dt
    def set_stat_text(self, new_text, new_spacing):
        self.stat_text.text = new_text
        self.stat_text.x = new_spacing
    # Returns the current texture of the sprite
    def get_texture(self):
        if self.texture == self.human_texture:
            return "human"
        elif self.texture == self.infected_texture:
            return "infected"
        else:
            return "zombie"

class ZombieSim(arcade.Window):
    """
    The game itself
    """

    def __init__(self, width, height, title):
        """
        Initializes a new instance of the game, creating sprite lists
        Inputs: the width, height, and title of the screen
        """
        super().__init__(width, height, title)

        self.zombies_list = arcade.SpriteList()
        self.infected_list = arcade.SpriteList()
        self.humans_list = arcade.SpriteList()
        self.moving_list = arcade.SpriteList()

        self.walls_list = arcade.SpriteList()

        self.all_sprites = arcade.SpriteList()

        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text = "00:00:00",
            start_x = SCREEN_WIDTH*14/15,
            start_y = SCREEN_HEIGHT*14/15 + STATS_HEIGHT,
            color = arcade.color.BLACK,
            font_size = 10,
            font_name= "courier",
            anchor_x = "center"
        )
        self.score_text = arcade.Text(
            text = f"{NUM_HUMANS} Humans vs. {NUM_ZOMBIES} Zombies",
            start_x = SCREEN_WIDTH / 2,
            start_y = STATS_HEIGHT * 3 / 4,
            color = arcade.color.BLACK,
            font_size = 30,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            anchor_y = "center"
        )
        self.stats_text = arcade.Text(
            text = "",
            start_x = SCREEN_WIDTH / 2,
            start_y = STATS_HEIGHT / 4,
            color = arcade.color.BLACK,
            font_size = 5,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            anchor_y = "center"
        )

    def setup(self):
        """
        Sets up the walls, zombies, humans, and arcade background.
        Currently has capabilities for a random map of walls or a
        prebuilt "house"
        """
        arcade.set_background_color(arcade.color.WHITE)
        self.total_time = 0.0
        
        # Initialize Zombies
        zombies = []
        for i in range(NUM_ZOMBIES):
            zombies += [MovingSprite("images/cross.png", SCALING/20)]
            zombies[i].left = (i + 1) * SCREEN_WIDTH/(NUM_ZOMBIES+1)
            zombies[i].top = SCREEN_HEIGHT*11/12 + STATS_HEIGHT
            zombies[i].velocity = (random.random()*SPEED-SPEED/2, random.random()*SPEED-SPEED/2)
            self.zombies_list.append(zombies[i])
            self.moving_list.append(zombies[i])
            self.all_sprites.append(zombies[i])
        
        #Initialize Humans
        humans = []
        for i in range(NUM_HUMANS):
            humans += [MovingSprite("images/circleNoFill.png", SCALING/20)]
            humans[i].left = (i + 1) * SCREEN_WIDTH/(NUM_HUMANS+1)
            humans[i].top = SCREEN_HEIGHT/12 + STATS_HEIGHT
            humans[i].velocity = (random.random()*SPEED-SPEED/2, random.random()*SPEED-SPEED/2)
            self.humans_list.append(humans[i])
            self.moving_list.append(humans[i])
            self.all_sprites.append(humans[i])
        

        # Initialize Walls
        walls = []
        # DEFAULT MAP
        # for i in range(8):
        #     if i == 3 or i == 4:
        #         continue
        #     walls += [Wall("images/vert.png", SCALING/5, 200, 50*i+150)]
        #     walls += [Wall("images/vert.png", SCALING/5, 600, 50*i+150)]
        #     walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 100)]
        #     walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 500)]

        # RANDOM MAP
        for i in range(9):
            for j in range(9):
                flip = random.randint(0,WALL_GEN)
                if not flip and j != 8:
                    walls += [Wall("images/vert.png", SCALING/5, 50*i+200, 50*j+150 + STATS_HEIGHT)]
                flip = random.randint(0,WALL_GEN)
                if not flip and i != 8:
                    walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 50*j+100 + STATS_HEIGHT)]
        
        for wall in walls:
            self.walls_list.append(wall)
            self.all_sprites.append(wall)

    def on_update(self, delta_time: float = 1/60):
        """
        Runs each time the game is updated, checking for human/zombie
        collisions, infected turning into zombies, and wall/edge collisions
        Inputs: the time passed since the last update
        """

        self.total_time += delta_time
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        centiss = int((self.total_time - minutes*60 - seconds)*100)
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}:{centiss:02d}"
        self.score_text.text = f"{len(self.humans_list)+len(self.infected_list)} Humans vs. {len(self.zombies_list)} Zombies"
        
        mcount = 0
        for moving in self.moving_list:
            mcount += 1
            status = ""
            if moving.get_texture() == "zombie":
                status = f"Zombified"
            elif moving.get_texture() == "infected":
                status = f"Infected"
            else:
                status = f"Healthy"
            spacing = (mcount-0.5)*SCREEN_WIDTH/(NUM_HUMANS+NUM_ZOMBIES)
            moving.set_stat_text(f"Person {mcount}:\n{status}", spacing)
            print(spacing)

        # self.stats_text.text = f"|"
        # mcount = 0
        # for i in self.moving_list:
        #     # if i.get_texture() != "zombie":
        #     mcount += 1
        #     self.stats_text.text += f"  Person {mcount}: "
        #     if i.get_texture() == "zombie":
        #         self.stats_text.text += f"Zombified  |"
        #     elif i.get_texture() == "infected":
        #         self.stats_text.text += f"Infected  |"
        #     else:
        #         self.stats_text.text += f"Healthy  |"
        # self.stats_text.text += f"  |  "
        # mcount = 0
        # for i in self.zombies_list:
        #     mcount += 1
        #     self.stats_text.text += f"Zombie {mcount}: Zombified  |  "

        # Check for human-zombie collisions
        for human in self.humans_list:
            if human.collides_with_list(self.zombies_list):
                self.make_infected(human)

        # Check if any infected should become a zombie    
        for infected in self.infected_list:
            infected.inc_infection_time(delta_time)
            if infected.get_infection_time() >= INCUBATION_PERIOD:
                self.make_zombie(infected)
        
        # Check for wall and screen collisions
        for moving in self.moving_list:
            oldvel = moving.velocity

            # Slight workaround here for getting stuck in walls
            # Creates bizarre behavior when contacting wall edges repeatedly
            # Improvement- use boundary_bottom, boundary_top, etc. to check
            # if going to get stuck in wall and reverse other direction too?
            # Might be less of a problem when intelligent agents are introduced.
            struck_wall = moving.collides_with_list(self.walls_list)
            if struck_wall:
                if struck_wall[0].get_texture() == "vert":
                    moving.velocity = (-oldvel[0],oldvel[1])
                    if oldvel[0] < 0:
                        moving.left = struck_wall[0].right
                    else:
                        moving.right = struck_wall[0].left
                else:         
                    moving.velocity = (oldvel[0],-oldvel[1]) 
                    if oldvel[1] < 0:
                        moving.bottom = struck_wall[0].top
                    else:
                        moving.top = struck_wall[0].bottom

            if moving.bottom < STATS_HEIGHT:
                moving.velocity = (oldvel[0],-oldvel[1])
            if moving.left < 0:
                moving.velocity = (-oldvel[0],oldvel[1])
            if moving.top > self.height:
                moving.velocity = (oldvel[0],-oldvel[1])
            if moving.right > self.width:
                moving.velocity = (-oldvel[0],oldvel[1])
        
        self.all_sprites.update()


    def on_draw(self):
        """
        Render the sprites on the screen
        """
        arcade.start_render()
        self.all_sprites.draw()
        self.timer_text.draw()
        self.score_text.draw()
        self.stats_text.draw()
        for i in self.moving_list:
            i.get_stat_text().draw()
        arcade.draw_line(0, STATS_HEIGHT, SCREEN_WIDTH, STATS_HEIGHT, arcade.color.BLACK, 3)
        arcade.draw_line(0, STATS_HEIGHT/2, SCREEN_WIDTH, STATS_HEIGHT/2, arcade.color.BLACK, 3)
        for i in range(NUM_HUMANS+NUM_ZOMBIES-1):
            xco = (i+1)/(NUM_HUMANS+NUM_ZOMBIES)*SCREEN_WIDTH
            arcade.draw_line(xco, 0, xco, STATS_HEIGHT/2, arcade.color.BLACK, 3)

    def make_human(self, new_human):
        """
        Makes a zombie into a human - TO BE IMPLEMENTED?
        Inputs: the sprite to be changed
        """
        pass

    def make_infected(self, new_infected):
        """
        Makes a human into an infected
        Inputs: the sprite to be changed
        """
        self.humans_list.remove(new_infected)
        new_infected.become_infected()
        self.infected_list.append(new_infected)
    
    def make_zombie(self, new_zombie):
        """
        Makes an infected into a zombie
        Inputs: the sprite to be changed
        """
        self.infected_list.remove(new_zombie)
        new_zombie.become_zombie()
        self.zombies_list.append(new_zombie)  
        # if len(self.humans_list) == 0:
        #     arcade.close_window() #REPLACE THIS WITH GAME OVER

if __name__ == "__main__":
    app = ZombieSim(SCREEN_WIDTH,SCREEN_HEIGHT+STATS_HEIGHT,SCREEN_TITLE)
    app.setup()
    arcade.run()
