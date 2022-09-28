from calendar import c
import arcade
import random
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STATS_HEIGHT = 100
SCREEN_TITLE = "Zombie Sim"
SCALING = 2.0

NUM_ZOMBIES = 2
NUM_HUMANS = 5
INCUBATION_PERIOD = 10.0 # seconds
SPEED = 3.0
WALL_GEN = 2 # larger value = fewer walls; SUGGESTED: 2
DOOR_GEN = 10 # larger value = fewer doors; SUGGESTED: 10?
ITEM_GEN = 10 # larger value = fewer items; SUGGESTED: 10

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
        self.vert_door_texture = arcade.load_texture("images/dashVert.png")
        self.horiz_door_texture = arcade.load_texture("images/dashHoriz.png")
        if image == "images/vert.png":
            self.texture = self.vert_texture
        elif image == "images/horiz.png":
            self.texture = self.horiz_texture
        elif image == "images/dashVert.png":
            self.texture = self.vert_door_texture
        elif image == "images/dashHoriz.png":
            self.texture = self.horiz_door_texture

    def get_texture(self):
        if self.texture == self.vert_texture:
            return "vert"
        elif self.texture == self.horiz_texture:
            return "horiz"
        elif self.texture == self.vert_door_texture:
            return "vert_door"
        elif self.texture == self.horiz_door_texture:
            return "horiz_door"


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
        self.dead_texture = arcade.load_texture("images/circleCrossedOut.png")

        self.human_time = 0.0
        self.infection_time = 0.0

        self.antidotes = 0
        self.knives = 0

        self.stat_text = arcade.Text(
            text = "",
            start_x = SCREEN_WIDTH / 2,
            start_y = STATS_HEIGHT * 3 / 7,
            color = arcade.color.BLACK,
            font_size = 7,
            font_name = "monospace",
            anchor_x = "center",
            anchor_y = "center",
            multiline = True,
            width = SCREEN_WIDTH / (NUM_HUMANS + NUM_ZOMBIES),
            align = "center"
        )
        self.sprite_speed = 0

    # Texture changes for role changes
    def become_human(self):
        self.texture = self.human_texture
    def become_infected(self):
        self.texture = self.infected_texture
    def become_zombie(self):
        self.texture = self.zombie_texture
    def become_dead(self):
        self.velocity = (0,0)
        self.texture = self.dead_texture

    # Returns the amount of time that an infected has been infected
    def get_infection_time(self):
        return self.infection_time
    def get_human_time(self):
        if self.human_time < 0.1:
            return "N/A"
        minutes = int(self.human_time) // 60
        seconds = int(self.human_time) % 60
        centiss = int((self.human_time - minutes*60 - seconds)*100)
        return f"{minutes:02d}:{seconds:02d}.{centiss:02d}"
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

    def gain_item(self, item):
        if item.get_texture() == "antidote":
            self.antidotes += 1
        elif item.get_texture() == "knife":
            self.knives += 1

    def has_item(self, name):
        if name == "antidote" and self.antidotes:
            return True
        elif name == "knife" and self.knives:
            return True

    def use_items(self, names):
        for name in names:
            if name == "antidote":
                self.antidotes -= 1
            elif name == "knife":
                self.knives -= 1

    # Gets the average distance and direction of zoms
    def update_avg_z(self, game):
        xcoords = []
        ycoords = []
        zom_close = False
        for zom in game.zombies_list:
            dist = arcade.get_distance_between_sprites(zom, self)
            if dist <= 50: #TODO : make not magic num
                zom_close = True
                xcoords.append(zom.center_x) #TODO : make weighted average using distance
                ycoords.append(zom.center_y)
        if zom_close:
            x_avg = sum(xcoords)/len(xcoords)
            y_avg = sum(ycoords)/len(ycoords)
            
            vect = (x_avg - self.center_x, y_avg - self.center_y)
            vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
            move_vect = -vect[0]/(vect_len), -vect[1]/(vect_len)
            print(move_vect)
            return move_vect


    # Returns the current texture of the sprite
    def get_texture(self):
        if self.texture == self.human_texture:
            return "human"
        elif self.texture == self.infected_texture:
            return "infected"
        elif self.texture == self.zombie_texture:
            return "zombie"
        elif self.texture == self.dead_texture:
            return "dead"

class Item(arcade.Sprite):
    def __init__(self, image, scale, x, y):
        """
        Initializes a new Item sprite
        Inputs: the starting sprite image, and the scaling of the screen
        """
        super().__init__(image, scale)

        self.center_x = x
        self.center_y = y

        self.antidote_texture = arcade.load_texture("images/antidote.png")
        self.bicycle_texture = arcade.load_texture("images/bicycle.png")
        self.binoculars_texture = arcade.load_texture("images/binoculars.png")
        self.bicycle_texture = arcade.load_texture("images/bullets.png")
        self.disguise_texture = arcade.load_texture("images/disguise.png")
        self.dog_texture = arcade.load_texture("images/dog.png")
        self.gun_texture = arcade.load_texture("images/gun.png")
        self.key_texture = arcade.load_texture("images/key.png")
        self.knife_texture = arcade.load_texture("images/knife.png")
        self.medpack_texture = arcade.load_texture("images/medpack.png")
        self.scanner_texture = arcade.load_texture("images/scanner.png")

    # Returns the current texture of the sprite
    def get_texture(self):
        if self.texture == self.antidote_texture:
            return "antidote"
        elif self.texture == self.knife_texture:
            return "knife"
        else:
            return "other"


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

        self.antidotes_list = arcade.SpriteList()
        self.knives_list = arcade.SpriteList()
        self.items_list = arcade.SpriteList()

        self.all_sprites = arcade.SpriteList()

        # Set up Timer
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text = "00:00.00",
            start_x = SCREEN_WIDTH*14/15,
            start_y = SCREEN_HEIGHT*14/15 + STATS_HEIGHT,
            color = arcade.color.BLACK,
            font_size = 10,
            font_name= "monospace",
            anchor_x = "center"
        )
        # Set up score
        self.score_text = arcade.Text(
            text = f"{NUM_HUMANS} Humans vs. {NUM_ZOMBIES} Zombies",
            start_x = SCREEN_WIDTH / 2,
            start_y = STATS_HEIGHT * 6 / 7,
            color = arcade.color.BLACK,
            font_size = 20,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            anchor_y = "center"
        )
        # self.stats_text = arcade.Text(
        #     text = "",
        #     start_x = SCREEN_WIDTH / 2,
        #     start_y = STATS_HEIGHT / 4,
        #     color = arcade.color.BLACK,
        #     font_size = 5,
        #     font_name = "courier",
        #     anchor_x = "center",
        #     anchor_y = "center"
        # )

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
        items = []
        doors = []
        # DEFAULT MAP WITHOUT ITEMS
        # for i in range(8):
        #     if i == 3 or i == 4:
        #         continue
        #     walls += [Wall("images/vert.png", SCALING/5, 200, 50*i+150)]
        #     walls += [Wall("images/vert.png", SCALING/5, 600, 50*i+150)]
        #     walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 100)]
        #     walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 500)]

        # RANDOM MAP WITH ITEMS
        for i in range(9):
            for j in range(9):
                no_wall = random.randint(0, WALL_GEN)
                no_door = random.randint(0, DOOR_GEN)
                if not no_wall and j != 8:
                    if not no_door:
                        walls += [Wall("images/dashVert.png", SCALING/50, 50*i+200, 50*j+150 + STATS_HEIGHT)]
                    else:
                        walls += [Wall("images/vert.png", SCALING/5, 50*i+200, 50*j+150 + STATS_HEIGHT)]
                no_wall = random.randint(0, WALL_GEN)
                no_door = random.randint(0, DOOR_GEN)
                if not no_wall and i != 8:
                    if not no_door:
                        walls += [Wall("images/dashHoriz.png", SCALING/5, 50*i+200, 50*j+100 + STATS_HEIGHT)]
                    else:
                        walls += [Wall("images/horiz.png", SCALING/5, 50*i+200, 50*j+100 + STATS_HEIGHT)]
                no_item = random.randint(0, ITEM_GEN)
                if not no_item and i != 8 and j != 8:
                    item_type = random.randint(0,1)
                    if item_type == 0:
                        item = Item("images/knife.png", SCALING/20, 50*i+225, 50*j+125 + STATS_HEIGHT)
                        self.items_list.append(item)
                    elif item_type == 1:
                        item = Item("images/antidote.png", SCALING/20, 50*i+225, 50*j+125 + STATS_HEIGHT)
                        self.items_list.append(item)
                    self.all_sprites.append(item)
                    items += [item]
                    
        
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
        self.timer_text.text = f"{minutes:02d}:{seconds:02d}.{centiss:02d}"
        self.score_text.text = f"{len(self.humans_list)+len(self.infected_list)} Humans vs. {len(self.zombies_list)} Zombies"
        
        mcount = 0
        for moving in self.moving_list:
            mcount += 1
            status = ""
            if moving.get_texture() == "zombie":
                status = f"Zombified"
            elif moving.get_texture() == "infected":
                status = f"Infected"
            elif moving.get_texture() == "human":
                status = f"Healthy"
            elif moving.get_texture() == "dead":
                status = f"Dead"
            items = ""
            if moving.has_item("antidote"):
                items += "A"
            if moving.has_item("knife"):
                items += "K"

            spacing = (mcount-0.5)*SCREEN_WIDTH/(NUM_HUMANS+NUM_ZOMBIES)
            sprite_vel = moving.velocity
            moving.sprite_speed = math.sqrt(moving.velocity[0]**2 + moving.velocity[1]**2)
            moving.set_stat_text(f"Person {mcount}: {status}\nTime Survived: {moving.get_human_time()}\nSpeed: {moving.sprite_speed:1.1f}\nItems: {items}", spacing)

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

        
        for human in self.humans_list:
            human.inc_human_time(delta_time)
            zombies = human.collides_with_list(self.zombies_list) # Check for human-zombie collisions
            used_items = []
            for zombie in zombies:
                if human.has_item("antidote"):
                    self.make_human(zombie)
                    used_items += ["antidote"]
                elif human.has_item("knife"):
                    self.kill(zombie)
                    used_items += ["knife"]
                else:
                    self.make_infected(human)
                human.use_items(used_items)
            items = human.collides_with_list(self.items_list)
            for item in items:
                if item:
                    human.gain_item(item)
                    self.remove_item(item)

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
                wall_tex = struck_wall[0].get_texture()
                if wall_tex == "vert" or (moving.get_texture() == "zombie" and wall_tex == "vert_door"):
                    moving.velocity = (-oldvel[0],oldvel[1])
                    if oldvel[0] < 0:
                        moving.left = struck_wall[0].right
                    else:
                        moving.right = struck_wall[0].left
                elif wall_tex == "horiz" or (moving.get_texture() == "zombie" and wall_tex == "horiz_door"):         
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

            if moving in self.humans_list:
                move_vector = None
                move_vector = moving.update_avg_z(self) # Update move vector

                if move_vector:
                    moving.velocity = move_vector[0]*moving.sprite_speed*SPEED-SPEED/2, move_vector[1]*moving.sprite_speed*SPEED-SPEED/2
                    

        self.all_sprites.update()


    def on_draw(self):
        """
        Render the sprites on the screen
        """
        arcade.start_render()
        self.all_sprites.draw()
        self.timer_text.draw()
        self.score_text.draw()
        # self.stats_text.draw()
        for i in self.moving_list:
            i.get_stat_text().draw()
        arcade.draw_line(0, STATS_HEIGHT, SCREEN_WIDTH, STATS_HEIGHT, arcade.color.BLACK, 3)
        arcade.draw_line(0, STATS_HEIGHT*2/3, SCREEN_WIDTH, STATS_HEIGHT*2/3, arcade.color.BLACK, 3)
        for i in range(NUM_HUMANS+NUM_ZOMBIES-1):
            xco = (i+1)/(NUM_HUMANS+NUM_ZOMBIES)*SCREEN_WIDTH
            arcade.draw_line(xco, 0, xco, STATS_HEIGHT*2/3, arcade.color.BLACK, 3)

    def make_human(self, new_human):
        """
        Makes a zombie into a human - TO BE IMPLEMENTED?
        Inputs: the sprite to be changed
        """
        self.zombies_list.remove(new_human)
        new_human.become_human()
        self.humans_list.append(new_human)

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

    def kill(self, killed):
        if killed in self.humans_list:
            self.humans_list.remove(killed)
        if killed in self.infected_list:
            self.infected_list.remove(killed)
        if killed in self.zombies_list:
            self.zombies_list.remove(killed)
        killed.become_dead()
        # self.moving_list.remove(killed)
        #self.all_sprites.remove(killed)

    def remove_item(self, item):
        self.items_list.remove(item)
        self.all_sprites.remove(item)

if __name__ == "__main__":
    app = ZombieSim(SCREEN_WIDTH,SCREEN_HEIGHT+STATS_HEIGHT,SCREEN_TITLE)
    app.setup()
    arcade.run()

def controlled_run(game, num_runs):
    app = ZombieSim(SCREEN_WIDTH,SCREEN_HEIGHT+STATS_HEIGHT,SCREEN_TITLE)
    app.setup()
    arcade.run()