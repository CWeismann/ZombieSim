from calendar import c
import arcade
import arcade.gui
import random
import math
import constants
from MovingSprite import MovingSprite
from Wall import Wall
from Item import Item

class ZombieSim(arcade.View):
    """
    The game itself
    """

    def __init__(self):
        """
        Initializes a new instance of the game, creating sprite lists
        Inputs: the width, height, and title of the screen
        """
        super().__init__()

        self.zombies_list = arcade.SpriteList()
        self.infected_list = arcade.SpriteList()
        self.humans_list = arcade.SpriteList()
        self.moving_list = arcade.SpriteList()
        self.walls_list = arcade.SpriteList(use_spatial_hash=True)
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

    def setup(self):
        """
        Sets up the walls, zombies, humans, and arcade background.
        Currently has capabilities for a random map of walls or a
        prebuilt "house"
        """
        arcade.set_background_color(arcade.color.WHITE)
        self.total_time = 0.0
                
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
                    item_type = random.randint(0,3)    
                    if item_type == 0:
                        item = Item("images/antidote.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
                        self.items_list.append(item)
                    elif item_type == 1:
                        item = Item("images/key.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
                        self.items_list.append(item)
                    elif item_type == 2:
                        item = Item("images/knife.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
                        self.items_list.append(item)
                    elif item_type == 3:
                        item = Item("images/gun.png", constants.SCALING/20, 50*i+225, 50*j+125 + constants.STATS_HEIGHT)
                        self.items_list.append(item)
                    self.all_sprites.append(item)
                    items += [item]
                    
        
        for wall in walls:
            self.walls_list.append(wall)
            self.all_sprites.append(wall)

                # Initialize Zombies
        zombies = []
        for i in range(constants.NUM_ZOMBIES):
            zombies += [MovingSprite("images/cross.png", constants.SCALING/20,self)]
            zombies[i].left = (i + 1) * constants.SCREEN_WIDTH/(constants.NUM_ZOMBIES+1)
            zombies[i].top = constants.SCREEN_HEIGHT*11/12 + constants.STATS_HEIGHT
            if random.randint(0,1):
                xvel = random.random() + constants.ZOMBIE_SPEED_MIN
            else:
                xvel = -(random.random() + constants.ZOMBIE_SPEED_MIN)
            if random.randint(0,1):
                yvel = random.random() + constants.ZOMBIE_SPEED_MIN
            else:
                yvel = -(random.random() + constants.ZOMBIE_SPEED_MIN)
            zombies[i].velocity = (xvel, yvel)
            zombies[i].base_speed = math.sqrt(xvel**2 + yvel**2)
            self.zombies_list.append(zombies[i])
            self.moving_list.append(zombies[i])
            self.all_sprites.append(zombies[i])
        
        #Initialize Humans
        humans = []
        for i in range(constants.NUM_HUMANS):
            humans += [MovingSprite("images/circleNoFill.png", constants.SCALING/20,self)]
            humans[i].left = (i + 1) * constants.SCREEN_WIDTH/(constants.NUM_HUMANS+1)
            humans[i].top = constants.SCREEN_HEIGHT/12 + constants.STATS_HEIGHT
            if random.randint(0,1):
                xvel = random.random() + constants.HUMAN_SPEED_MIN
            else:
                xvel = -(random.random() + constants.HUMAN_SPEED_MIN)
            if random.randint(0,1):
                yvel = random.random() + constants.HUMAN_SPEED_MIN
            else:
                yvel = -(random.random() + constants.HUMAN_SPEED_MIN)
            humans[i].velocity = (xvel, yvel)
            humans[i].base_speed = math.sqrt(xvel**2 + yvel**2)
            self.humans_list.append(humans[i])
            self.moving_list.append(humans[i])
            self.all_sprites.append(humans[i])

        

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
            if moving.has_item("gun"):
                items += "G"
            if moving.has_item("key"):
                items += "Ke"
            if moving.has_item("knife"):
                items += "Kn"

            spacing = (mcount-0.5)*constants.SCREEN_WIDTH/(constants.NUM_HUMANS + constants.NUM_ZOMBIES)
            moving.set_stat_text(f"Person {mcount}: {status}\nTime Survived: {moving.get_human_time()}\nSpeed: {moving.base_speed:1.1f}\nItems: {items}", spacing)

        for human in self.humans_list:
            human.inc_human_time(delta_time)

            # Check for human-zombie collisions
            zombies = human.collides_with_list(self.zombies_list) 
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
                if infected.has_item("antidote"):
                    infected.use_items(["antidote"])
                    self.make_zombie(infected)
                    self.make_human(infected)
                elif infected.has_item("knife"):
                    infected.use_items(["knife"])
                    self.kill(infected)
                elif infected.has_item("gun"):
                    infected.use_items(["gun"])
                    self.kill(infected)
                else:
                    self.make_zombie(infected)
        # Check if infected can pick up an item
            items = infected.collides_with_list(self.items_list)
            for item in items:
                if item:
                    infected.gain_item(item)
                    self.remove_item(item)
        
        # Check for wall and screen collisions
        for moving in self.moving_list:
            # if moving.path and len(moving.path) > 0:
            #     continue
            oldvel = moving.velocity

            # Slight workaround here for getting stuck in walls
            # Creates bizarre behavior when contacting wall edges repeatedly
            # Improvement- use boundary_bottom, boundary_top, etc. to check
            # if going to get stuck in wall and reverse other direction too?
            # Might be less of a problem when intelligent agents are introduced.
            struck_wall = moving.collides_with_list(self.walls_list)
            hit_wall_x = False
            hit_wall_y = False
            if struck_wall:
                wall_tex = struck_wall[0].get_texture()
                if wall_tex == "vert" or (moving.get_texture() == "zombie" and wall_tex == "vert_door"):
                    moving.velocity = (-oldvel[0],oldvel[1])
                    hit_wall_x = True
                    if oldvel[0] < 0:
                        moving.left = struck_wall[0].right
                    else:
                        moving.right = struck_wall[0].left
                elif wall_tex == "horiz" or (moving.get_texture() == "zombie" and wall_tex == "horiz_door"):         
                    moving.velocity = (oldvel[0],-oldvel[1]) 
                    hit_wall_y = True
                    if oldvel[1] < 0:
                        moving.bottom = struck_wall[0].top
                    else:
                        moving.top = struck_wall[0].bottom
                elif wall_tex == "vert_door" and moving.has_item("key") and moving.get_texture() != "zombie":
                    moving.use_items(["key"])
                    if oldvel[0] > 0:
                        moving.left = struck_wall[0].right
                    else:
                        moving.right = struck_wall[0].left
                    struck_wall[0].lock_door()
                elif wall_tex == "horiz_door" and moving.has_item("key") and moving.get_texture() != "zombie":
                    moving.use_items(["key"])
                    if oldvel[1] > 0:
                        moving.bottom = struck_wall[0].top
                    else:
                        moving.top = struck_wall[0].bottom
                    struck_wall[0].lock_door()

            hit_edge_x = False
            hit_edge_y = False
            if moving.bottom < constants.STATS_HEIGHT:
                moving.velocity = (oldvel[0],-oldvel[1])
                moving.bottom = constants.STATS_HEIGHT
                hit_edge_y = True
            if moving.left < 0:
                moving.velocity = (-oldvel[0],oldvel[1])
                moving.left = 0
                hit_edge_x = True
            if moving.top > constants.STATS_HEIGHT + constants.SCREEN_HEIGHT:
                moving.velocity = (oldvel[0],-oldvel[1])
                moving.top = constants.STATS_HEIGHT + constants.SCREEN_HEIGHT
                hit_edge_y = True
            if moving.right > constants.SCREEN_WIDTH:
                moving.velocity = (-oldvel[0],oldvel[1])
                moving.right = constants.SCREEN_WIDTH
                hit_edge_x = True

            # Human check for zom or items to move towards/away from
            if moving in self.humans_list: # or moving in self.infected_list:
                move_vector_z = moving.update_LoS_to_z(self)
                # DIRECTIONAL HANDLING CHANGES - BUGGY vvv
                if move_vector_z:
                    xvel = moving.velocity[0]
                    yvel = moving.velocity[1]
                    if not hit_edge_x and not hit_wall_x:
                        xvel = move_vector_z[0]*constants.HUMAN_SPEED_MIN
                    if not hit_edge_y and not hit_wall_y:
                        yvel = move_vector_z[1]*constants.HUMAN_SPEED_MIN
                    v_len = math.sqrt(xvel**2 + yvel**2)
                    moving.velocity = (xvel/v_len)*moving.sprite_speed, (yvel/v_len)*moving.sprite_speed
                
                

                # MOVE TOWARDS ITEMS - BUGGY
                # else:
                #     move_vector_i = moving.update_LoS_to_i(self)
                #     if move_vector_i and not struck_wall and not hit_edge:
                #         moving.velocity = (move_vector_i[0]*constants.SPEED-constants.SPEED/2), (move_vector_i[1]*constants.SPEED-constants.SPEED/2)
                #         v_len = math.sqrt(moving.velocity[0]**2 + moving.velocity[1]**2)
                #         moving.velocity = (moving.velocity[0]/v_len)*moving.sprite_speed, (moving.velocity[1]/v_len)*moving.sprite_speed

            # Zombie check for humans to move towards/away from
            if moving in self.zombies_list:
                move_vector = moving.update_LoS_to_h(self)
                moving.check_time += delta_time
                if move_vector and moving.check_time > constants.CHECK_TIME:
                    # print(move_vector)
                    moving.check_time = 0.0
                    moving.path = arcade.astar_calculate_path(moving.position,move_vector,moving.bar_list,True)
                    print(moving.path)
                    if moving.path:
                        moving.path.pop(0)
                    # print(move_vector)
                    # print(moving.position)
                    # print(moving.path)

                if moving.path and len(moving.path) > 1:
                    if math.sqrt((moving.center_x-moving.path[0][0])**2 + ((moving.center_y-moving.path[0][1])**2)) <= 30:
                        # print("SWITCH")
                        moving.path = moving.path[1:]
                    if moving.path:
                        x,y = moving.path[0]
                    elif move_vector:
                        x,y = move_vector
                    else:
                        continue
                    vect = (x - moving.center_x, y - moving.center_y)
                    angle = math.atan2(vect[1], vect[0])

                    change_x = math.cos(angle) * moving.sprite_speed
                    change_y = math.sin(angle) * moving.sprite_speed


                    vect_len = math.sqrt(change_x**2 + change_y**2)
                    
                    moving.velocity = (change_x/(vect_len))*moving.sprite_speed, (change_y/(vect_len))*moving.sprite_speed
                elif move_vector:
                    xvel = moving.velocity[0]
                    yvel = moving.velocity[1]
                    if not hit_edge_x and not hit_wall_x:
                        xvel = move_vector[0]*constants.ZOMBIE_SPEED_MIN
                    if not hit_edge_y and not hit_wall_y:
                        yvel = move_vector[1]*constants.ZOMBIE_SPEED_MIN
                    v_len = math.sqrt(xvel**2 + yvel**2)
                    moving.velocity = -(xvel/v_len)*moving.sprite_speed, -(yvel/v_len)*moving.sprite_speed
            


                # DIRECTIONAL HANDLING CHANGES - BUGGY vvv
                # if move_vector:
                #     xvel = moving.velocity[0]
                #     yvel = moving.velocity[1]
                #     if not hit_edge_x and not hit_wall_x:
                #         xvel = move_vector[0]*constants.HUMAN_SPEED_MIN
                #     if not hit_edge_y and not hit_wall_y:
                #         yvel = move_vector[1]*constants.HUMAN_SPEED_MIN
                #     v_len = math.sqrt(xvel**2 + yvel**2)
                #     moving.velocity = (xvel/v_len)*moving.sprite_speed, (yvel/v_len)*moving.sprite_speed

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
        oldvel = new_human.velocity
        velocity = (oldvel[0]+constants.HUMAN_SPEED_MIN-constants.ZOMBIE_SPEED_MIN, oldvel[1]+constants.HUMAN_SPEED_MIN-constants.ZOMBIE_SPEED_MIN)
        new_human.base_speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
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
        oldvel = new_zombie.velocity
        velocity = (oldvel[0]-constants.HUMAN_SPEED_MIN+constants.ZOMBIE_SPEED_MIN, oldvel[1]-constants.HUMAN_SPEED_MIN+constants.ZOMBIE_SPEED_MIN)
        new_zombie.base_speed = math.sqrt(velocity[0]**2 + velocity[1]**2)
        self.zombies_list.append(new_zombie)  
        if len(self.humans_list) == 0 and len(self.infected_list) == 0:
            print("GAME OVER - ZOMBIES WIN")
            game_over_view = GameOver()
            self.window.show_view(game_over_view)

    def kill(self, killed):
        if killed in self.humans_list:
            self.humans_list.remove(killed)
        if killed in self.infected_list:
            self.infected_list.remove(killed)
        if killed in self.zombies_list:
            self.zombies_list.remove(killed)
        killed.become_dead()
        if len(self.zombies_list) == 0:
            print("GAME OVER - HUMANS WIN")
            game_over_view = GameOver()
            self.window.show_view(game_over_view)
        # self.moving_list.remove(killed)
        #self.all_sprites.remove(killed)

    def remove_item(self, item):
        self.items_list.remove(item)
        self.all_sprites.remove(item)

class MenuScreen(arcade.View):
    def __init__(self):
        super().__init__()
        
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Render button
        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start", width=200, style=default_style)
        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200, style=default_style)

        self.v_box.add(start_button)
        self.v_box.add(settings_button)

        start_button.on_click = self.on_click_start
        settings_button.on_click = self.on_click_settings

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.GRAY_BLUE)

        # reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()
    
    def on_click_start(self, event):
        """ If the user presses the start button, start the simulation. """
        game_view = ZombieSim()
        game_view.setup()
        self.window.show_view(game_view)

    def on_click_settings(self, event):
        """ If the user presses the settings button, open the settings menu. """
        # message_box = arcade.gui.UIMessageBox(
        #     width=300,
        #     height=200,
        #     message_text=(
        #         "Settings Menu Goes Here"
        #     ),
        #     buttons=("Save",)
        # )

        # self.manager.add(message_box)

        settings_view = Settings()
        self.window.show_view(settings_view)

class Settings(arcade.View):
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Render button
        default_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (21, 19, 21),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }
        none_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.WHITE,
            "border_width": 2,
            "border_color": None,
            "bg_color": (41, 39, 41),
            
            # used if button is pressed
            "bg_color_pressed": (41, 39, 41),
            "border_color_pressed": None,  # also used when hovered
            "font_color_pressed": arcade.color.WHITE,
        }

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout(vertical=True,space_between=20)
        self.h_box_1 = arcade.gui.UIBoxLayout(vertical=False,space_between=10)
        self.h_box_2 = arcade.gui.UIBoxLayout(vertical=False,space_between=10)

        # Create the buttons
        plus_zom_button = arcade.gui.UIFlatButton(text="+", width=50, style=default_style)
        zom_button = arcade.gui.UIFlatButton(text=f"{constants.NUM_ZOMBIES} Zombies", width=200, style=none_style)
        minus_zom_button = arcade.gui.UIFlatButton(text="-", width=50, style=default_style)
        plus_hum_button = arcade.gui.UIFlatButton(text="+", width=50, style=default_style)
        hum_button = arcade.gui.UIFlatButton(text=f"{constants.NUM_HUMANS} Humans", width=200, style=none_style)
        minus_hum_button = arcade.gui.UIFlatButton(text="-", width=50, style=default_style)

        save_button = arcade.gui.UIFlatButton(text="Save", width=200, style=default_style)

        self.h_box_1.add(plus_zom_button)
        self.h_box_1.add(zom_button)
        self.h_box_1.add(minus_zom_button)
        self.h_box_2.add(plus_hum_button)
        self.h_box_2.add(hum_button)
        self.h_box_2.add(minus_hum_button)

        self.v_box.add(self.h_box_1)
        self.v_box.add(self.h_box_2)
        self.v_box.add(save_button)

        plus_zom_button.on_click = self.on_click_zp
        minus_zom_button.on_click = self.on_click_zm
        plus_hum_button.on_click = self.on_click_hp
        minus_hum_button.on_click = self.on_click_hm
        save_button.on_click = self.on_click_save

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    
    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.color.GRAY_BLUE)

        # reset the viewport
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()
    
    def on_click_zp(self, event):
        constants.NUM_ZOMBIES += 1
        self.h_box_1.children[1].text = f"{constants.NUM_ZOMBIES} Zombies"
    def on_click_zm(self, event):
        constants.NUM_ZOMBIES -= 1
        self.h_box_1.children[1].text = f"{constants.NUM_ZOMBIES} Zombies"
    def on_click_hp(self, event):
        constants.NUM_HUMANS += 1
        self.h_box_2.children[1].text = f"{constants.NUM_HUMANS} Humans"
    def on_click_hm(self, event):
        constants.NUM_HUMANS -= 1
        self.h_box_2.children[1].text = f"{constants.NUM_HUMANS} Humans"

    def on_click_save(self, event):
        start_view = MenuScreen()
        window.show_view(start_view)
        

class GameOver(arcade.View):
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        # Reset the viewport
        arcade.set_viewport(0, constants.SCREEN_WIDTH - 1, 0, constants.STATS_HEIGHT + constants.SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Game Over", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to restart", self.window.width / 2, self.window.height / 2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, restart the simulation. """
        game_view = ZombieSim()
        game_view.setup()
        self.window.show_view(game_view)

    

if __name__ == "__main__":
    window = arcade.Window(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT+constants.STATS_HEIGHT,constants.SCREEN_TITLE)
    start_view = MenuScreen()
    window.show_view(start_view)
    arcade.run()
    