import constants
import arcade
import math

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
        self.keys = 0
        self.knives = 0

        self.stat_text = arcade.Text(
            text = "",
            start_x = constants.SCREEN_WIDTH / 2,
            start_y = constants.STATS_HEIGHT * 3 / 7,
            color = arcade.color.BLACK,
            font_size = 7,
            font_name = "monospace",
            anchor_x = "center",
            anchor_y = "center",
            multiline = True,
            width = constants.SCREEN_WIDTH / (constants.NUM_HUMANS + constants.NUM_ZOMBIES),
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
    def reset_infection_time(self):
        self.infection_time = 0
    def inc_human_time(self, dt):
        self.human_time += dt
    def set_stat_text(self, new_text, new_spacing):
        self.stat_text.text = new_text
        self.stat_text.x = new_spacing

    def gain_item(self, item):
        if item.get_texture() == "antidote":
            self.antidotes += 1
        elif item.get_texture() == "key":
            self.keys += 1
        elif item.get_texture() == "knife":
            self.knives += 1
        
    def has_item(self, name):
        if name == "antidote" and self.antidotes:
            return True
        elif name == "key" and self.keys:
            return True
        elif name == "knife" and self.knives:
            return True


    def use_items(self, names):
        for name in names:
            if name == "antidote":
                self.antidotes -= 1
            elif name == "key":
                self.keys -= 1
            elif name == "knife":
                self.knives -= 1

    # DEPRECATED - SEE update_LoS_to_avg_z
    # Gets the average distance and direction of zoms
    # def update_avg_z(self, game):
    #     xcoords = []
    #     ycoords = []
    #     zom_close = False
    #     for zom in game.zombies_list:
    #         dist = arcade.get_distance_between_sprites(zom, self)
    #         if dist <= 100: #TODO : make not magic num
    #             zom_close = True
    #             xcoords.append(zom.center_x) #TODO : make weighted average using distance
    #             ycoords.append(zom.center_y)
    #     if zom_close:
    #         x_avg = sum(xcoords)/len(xcoords)
    #         y_avg = sum(ycoords)/len(ycoords)
            
    #         vect = (x_avg - self.center_x, y_avg - self.center_y)
    #         vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
    #         move_vect = -vect[0]/(vect_len), -vect[1]/(vect_len)
    #         return move_vect

    # line-of-sight-based alternative to update_avg_z
    def update_LoS_to_avg_z(self, game):
        xcoords = []
        ycoords = []
        zom_close = False
        for zom in game.zombies_list:
            if arcade.has_line_of_sight(self.position, zom.position, game.walls_list, constants.HUMAN_VISION, 2):
                zom_close = True
                xcoords.append(zom.center_x) #TODO : make weighted average using distance
                ycoords.append(zom.center_y)
        if zom_close:
            x_avg = sum(xcoords)/len(xcoords)
            y_avg = sum(ycoords)/len(ycoords)
            
            vect = (x_avg - self.center_x, y_avg - self.center_y)
            vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
            if self.has_item("knife") or self.has_item("antidote"):
                move_vect = vect[0]/(vect_len), vect[1]/(vect_len)
            else:
                move_vect = -vect[0]/(vect_len), -vect[1]/(vect_len)
            return move_vect

    def update_LoS_to_h(self, game):
        visible_hums = arcade.SpriteList()
        for hum in game.humans_list:
            if arcade.has_line_of_sight(self.position, hum.position, game.walls_list, constants.ZOMBIE_VISION, 2):
                visible_hums.append(hum)
        if visible_hums:
            nearest_hum, dist_to_nh = arcade.get_closest_sprite(self, visible_hums)
            vect = (nearest_hum.center_x - self.center_x, nearest_hum.center_y - self.center_y)
            vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
            move_vect = vect[0]/(vect_len), vect[1]/(vect_len)
            return move_vect

    def update_LoS_to_i(self, game):
        visible_items = arcade.SpriteList()
        for item in game.items_list:
            if arcade.has_line_of_sight(self.position, item.position, game.walls_list, constants.HUMAN_VISION, 2):
                visible_items.append(item)
        if visible_items:
            nearest_item, dist_to_ni = arcade.get_closest_sprite(self, visible_items)
            vect = (nearest_item.center_x - self.center_x, nearest_item.center_y - self.center_y)
            vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
            move_vect = vect[0]/(vect_len), vect[1]/(vect_len)
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
