from calendar import c
import arcade
import random
import math
import constants
from MovingSprite import MovingSprite
from Wall import Wall
from Item import Item

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

        self.walls_list = arcade.SpriteList(use_spatial_hash=True)

        self.antidotes_list = arcade.SpriteList()
        self.knives_list = arcade.SpriteList()
        self.items_list = arcade.SpriteList()

        self.all_sprites = arcade.SpriteList()

        # Set up Timer
        self.total_time = 0.0
        self.timer_text = arcade.Text(
            text = "00:00.00",
            start_x = constants.SCREEN_WIDTH*14/15,
            start_y = constants.SCREEN_HEIGHT*14/15 + constants.STATS_HEIGHT,
            color = arcade.color.BLACK,
            font_size = 10,
            font_name= "monospace",
            anchor_x = "center"
        )
        # Set up score
        self.score_text = arcade.Text(
            text = f"{constants.NUM_HUMANS} Humans vs. {constants.NUM_ZOMBIES} Zombies",
            start_x = constants.SCREEN_WIDTH / 2,
            start_y = constants.STATS_HEIGHT * 6 / 7,
            color = arcade.color.BLACK,
            font_size = 20,
            font_name = "Kenney Pixel Square",
            anchor_x = "center",
            anchor_y = "center"
        )
        # self.stats_text = arcade.Text(
        #     text = "",
        #     start_x = constants.SCREEN_WIDTH / 2,
        #     start_y = constants.STATS_HEIGHT / 4,
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
        for i in range(constants.NUM_ZOMBIES):
            zombies += [MovingSprite("images/cross.png", constants.SCALING/20)]
            zombies[i].left = (i + 1) * constants.SCREEN_WIDTH/(constants.NUM_ZOMBIES+1)
            zombies[i].top = constants.SCREEN_HEIGHT*11/12 + constants.STATS_HEIGHT
            zombies[i].velocity = (random.random()*constants.SPEED-constants.SPEED/2, random.random()*constants.SPEED-constants.SPEED/2)
            self.zombies_list.append(zombies[i])
            self.moving_list.append(zombies[i])
            self.all_sprites.append(zombies[i])
        
        #Initialize Humans
        humans = []
        for i in range(constants.NUM_HUMANS):
            humans += [MovingSprite("images/circleNoFill.png", constants.SCALING/20)]
            humans[i].left = (i + 1) * constants.SCREEN_WIDTH/(constants.NUM_HUMANS+1)
            humans[i].top = constants.SCREEN_HEIGHT/12 + constants.STATS_HEIGHT
            humans[i].velocity = (random.random()*constants.SPEED-constants.SPEED/2, random.random()*constants.SPEED-constants.SPEED/2)
            self.humans_list.append(humans[i])
            self.moving_list.append(humans[i])
            self.all_sprites.append(humans[i])
        
        # Initialize Walls
        walls = []
        items = []
        # DEFAULT MAP WITHOUT ITEMS
        # for i in range(8):
        #     if i == 3 or i == 4:
        #         continue
        #     walls += [Wall("images/vert.png", constants.SCALING/5, 200, 50*i+150)]
        #     walls += [Wall("images/vert.png", constants.SCALING/5, 600, 50*i+150)]
        #     walls += [Wall("images/horiz.png", constants.SCALING/5, 50*i+200, 100)]
        #     walls += [Wall("images/horiz.png", constants.SCALING/5, 50*i+200, 500)]

        # RANDOM MAP WITH ITEMS
        for i in range(9):
            for j in range(9):
                no_wall = random.randint(0, constants.WALL_GEN)
                no_door = random.randint(0, constants.DOOR_GEN)
                if not no_wall and j != 8:
                    if not no_door:
                        walls += [Wall("images/dashVert.png", constants.SCALING/5, 50*i+200, 50*j+150 + constants.STATS_HEIGHT)]
                    else:
                        walls += [Wall("images/vert.png", constants.SCALING/5, 50*i+200, 50*j+150 + constants.STATS_HEIGHT)]
                no_wall = random.randint(0, constants.WALL_GEN)
                no_door = random.randint(0, constants.DOOR_GEN)
                if not no_wall and i != 8:
                    if not no_door:
                        walls += [Wall("images/dashHoriz.png", constants.SCALING/5, 50*i+200, 50*j+100 + constants.STATS_HEIGHT)]
                    else:
                        walls += [Wall("images/horiz.png", constants.SCALING/5, 50*i+200, 50*j+100 + constants.STATS_HEIGHT)]
                no_item = random.randint(0, constants.ITEM_GEN)
                if not no_item and i != 8 and j != 8:
                    item_type = random.randint(0,2)    
                    if item_type == 0:
                        item = Item("images/antidote.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
                        self.items_list.append(item)
                    elif item_type == 1:
                        item = Item("images/key.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
                        self.items_list.append(item)
                    elif item_type == 2:
                        item = Item("images/knife.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
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
            if moving.has_item("key"):
                items += "Ke"
            if moving.has_item("knife"):
                items += "Kn"

            spacing = (mcount-0.5)*constants.SCREEN_WIDTH/(constants.NUM_HUMANS + constants.NUM_ZOMBIES)
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
            if infected.get_infection_time() >= constants.INCUBATION_PERIOD:
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
                elif wall_tex == "vert_door":
                    if moving.get_texture() == "zombie":
                        moving.velocity = (-oldvel[0],oldvel[1]) 
                        if oldvel[0] < 0:
                            moving.left = struck_wall[0].right
                        else:
                            moving.right = struck_wall[0].left
                    elif moving.has_item("key"):
                        moving.use_items(["key"])
                        if oldvel[0] > 0:
                            moving.left = struck_wall[0].right
                        else:
                            moving.right = struck_wall[0].left
                        struck_wall[0].lock_door()
                elif wall_tex == "horiz_door":
                    if moving.get_texture() == "zombie":
                        moving.velocity = (oldvel[0],-oldvel[1]) 
                        if oldvel[1] < 0:
                            moving.bottom = struck_wall[0].top
                        else:
                            moving.top = struck_wall[0].bottom
                    elif moving.has_item("key"):
                        moving.use_items(["key"])
                        if oldvel[1] > 0:
                            moving.bottom = struck_wall[0].top
                        else:
                            moving.top = struck_wall[0].bottom
                        struck_wall[0].lock_door()
            hit_edge = False
            if moving.bottom < constants.STATS_HEIGHT:
                moving.velocity = (oldvel[0],-oldvel[1])
                moving.bottom = constants.STATS_HEIGHT
                hit_edge = True
            if moving.left < 0:
                moving.velocity = (-oldvel[0],oldvel[1])
                moving.left = 0
                hit_edge = True
            if moving.top > self.height:
                moving.velocity = (oldvel[0],-oldvel[1])
                moving.top = self.height
                hit_edge = True
            if moving.right > self.width:
                moving.velocity = (-oldvel[0],oldvel[1])
                moving.right = self.width
                hit_edge = True

            if moving in self.humans_list or moving in self.infected_list:
                move_vector_z = moving.update_LoS_to_avg_z(self)

                if move_vector_z and not struck_wall and not hit_edge: # if their move vector exists, update their velocity. For now, they just run away.
                    moving.velocity = (move_vector_z[0]*constants.SPEED-constants.SPEED/2), (move_vector_z[1]*constants.SPEED-constants.SPEED/2) #TODO: code should not work differently for positive and negative movement
                    v_len = math.sqrt(moving.velocity[0]**2 + moving.velocity[1]**2)
                    moving.velocity = (moving.velocity[0]/v_len)*moving.sprite_speed, (moving.velocity[1]/v_len)*moving.sprite_speed
                # MOVE TOWARDS ITEMS - BUGGY
                # else:
                #     move_vector_i = moving.update_LoS_to_i(self)
                #     if move_vector_i and not struck_wall and not hit_edge:
                #         moving.velocity = (move_vector_i[0]*constants.SPEED-constants.SPEED/2), (move_vector_i[1]*constants.SPEED-constants.SPEED/2)
                #         v_len = math.sqrt(moving.velocity[0]**2 + moving.velocity[1]**2)
                #         moving.velocity = (moving.velocity[0]/v_len)*moving.sprite_speed, (moving.velocity[1]/v_len)*moving.sprite_speed


            if moving in self.zombies_list:
                move_vector = moving.update_LoS_to_h(self)
                if move_vector and not struck_wall and not hit_edge:
                    moving.velocity = (move_vector[0]*constants.SPEED-constants.SPEED/2), (move_vector[1]*constants.SPEED-constants.SPEED/2)
                    v_len = math.sqrt(moving.velocity[0]**2 + moving.velocity[1]**2)
                    moving.velocity = (moving.velocity[0]/v_len)*moving.sprite_speed, (moving.velocity[1]/v_len)*moving.sprite_speed


                # if self.humans_list:
                #     nearest_human, dist_to_nh = arcade.get_closest_sprite(moving, self.humans_list)
                #     move_vector = (nearest_human.position[0]-moving.position[0], nearest_human.position[1]-moving.position[1])
                #     if move_vector and not struck_wall and not hit_edge: # if their move vector exists, update their velocity. For now, they just run away.
                #         moving.velocity = (move_vector[0]*constants.SPEED-constants.SPEED/2), (move_vector[1]*constants.SPEED-constants.SPEED/2)
                #         v_len = math.sqrt(moving.velocity[0]**2 + moving.velocity[1]**2)
                #         moving.velocity = (moving.velocity[0]/v_len)*moving.sprite_speed, (moving.velocity[1]/v_len)*moving.sprite_speed

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
        arcade.draw_line(0, constants.STATS_HEIGHT, constants.SCREEN_WIDTH, constants.STATS_HEIGHT, arcade.color.BLACK, 3)
        arcade.draw_line(0, constants.STATS_HEIGHT*2/3, constants.SCREEN_WIDTH, constants.STATS_HEIGHT*2/3, arcade.color.BLACK, 3)
        for i in range(constants.NUM_HUMANS + constants.NUM_ZOMBIES - 1):
            xco = (i+1)/(constants.NUM_HUMANS + constants.NUM_ZOMBIES)*constants.SCREEN_WIDTH
            arcade.draw_line(xco, 0, xco, constants.STATS_HEIGHT*2/3, arcade.color.BLACK, 3)

    def make_human(self, new_human):
        """
        Makes a zombie into a human
        Inputs: the sprite to be changed
        """
        self.zombies_list.remove(new_human)
        new_human.become_human()
        new_human.reset_infection_time()
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
    app = ZombieSim(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT+constants.STATS_HEIGHT,constants.SCREEN_TITLE)
    app.setup()
    arcade.run()

def controlled_run(game, num_runs):
    app = ZombieSim(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT+constants.STATS_HEIGHT,constants.SCREEN_TITLE)
    app.setup()
    arcade.run()