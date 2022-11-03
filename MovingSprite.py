import constants
import arcade
import math
from enum import IntEnum

class SPEEDSTATE(IntEnum):
    '''
    Enum for the speed state of the sprite.
    '''

    CRAWL = 1
    WALK = 2
    RUN = 3

class Mood(IntEnum):
    RELAXED = 1
    MOTIVATED = 2
    ALERT = 3

class MovingSprite(arcade.Sprite):
    def __init__(self, image, scale, game):
        """
        Initializes a new MovingSprite sprite (Human/Zombie/Infected)
        Inputs: the starting sprite image, and the scaling of the screen
        """
        super().__init__(image, scale)

        self.human_texture = arcade.load_texture("images/circleNoFill.png")
        self.infected_texture = arcade.load_texture("images/circleFill.png")
        self.zombie_texture = arcade.load_texture("images/cross.png")
        self.dead_texture = arcade.load_texture("images/circleCrossedOut.png")

        self.human_time = 0.0 # Time spent as a human
        self.infection_time = 0.0 # Time spent as an infected

        self.antidotes = 0
        self.keys = 0
        self.knives = 0
        self.guns = 0

        self.path = []


        # Generate the text for the stats
        self.stat_text = arcade.Text(
            text = "",
            start_x = constants.SCREEN_WIDTH / 2,
            start_y = constants.STATS_HEIGHT * 3 / 7,
            color = arcade.color.BLACK,
            font_size = 50 / (constants.NUM_HUMANS + constants.NUM_ZOMBIES),
            font_name = "monospace",
            anchor_x = "center",
            anchor_y = "center",
            multiline = True,
            width = constants.SCREEN_WIDTH / (constants.NUM_HUMANS + constants.NUM_ZOMBIES),
            align = "center"
        )
        
        self.base_speed = 0 # speed before modifiers
        self.speed_state = SPEEDSTATE.WALK
        self.sprite_speed = int(self.speed_state) * self.base_speed

        self.bar_list = arcade.AStarBarrierList(self, game.walls_list, 10, 0, constants.SCREEN_WIDTH, constants.STATS_HEIGHT, constants.SCREEN_HEIGHT)

    # Texture changes for role changes
    def become_human(self):
        self.texture = self.human_texture
        self.set_speed_state(SPEEDSTATE.WALK)

    def become_infected(self):
        self.texture = self.infected_texture
        self.set_speed_state(SPEEDSTATE.CRAWL)

    def become_zombie(self):
        self.texture = self.zombie_texture
        self.set_speed_state(SPEEDSTATE.WALK)

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
        elif item.get_texture() == "gun":
            self.guns += 1
        
    def has_item(self, name):
        if name == "antidote" and self.antidotes:
            return True
        elif name == "key" and self.keys:
            return True
        elif name == "knife" and self.knives:
            return True
        elif name == "gun" and self.guns:
            return True


    def use_items(self, names):
        for name in names:
            if name == "antidote":
                self.antidotes -= 1
            elif name == "key":
                self.keys -= 1
            elif name == "knife":
                self.knives -= 1
            elif name == "gun":     #eventually will change this to use bullets
                self.guns -= 1

    def update_LoS_to_z(self, game):
        xcoords = []
        ycoords = []
        zom_close = False
        for zom in game.zombies_list:
            if arcade.has_line_of_sight(self.position, zom.position, game.walls_list, int(constants.HUMAN_VISION * (int(zom.speed_state)/1.5)), 2):
                if self.has_item("gun"):
                    self.use_items(["gun"])
                    game.kill(zom)
                zom_close = True
                xcoords.append(zom.center_x)
                ycoords.append(zom.center_y)
        if zom_close:
            self.set_speed_state(SPEEDSTATE.RUN)
            x_avg = sum(xcoords)/len(xcoords)
            y_avg = sum(ycoords)/len(ycoords)
            ##
            return x_avg, y_avg
            ##
            vect = (x_avg - self.center_x, y_avg - self.center_y)
            vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
            if self.has_item("knife") or self.has_item("antidote"):
                move_vect = vect[0]/(vect_len), vect[1]/(vect_len)
            else:
                move_vect = -vect[0]/(vect_len), -vect[1]/(vect_len)
            return move_vect # returns a normalized vector of the direction to move
        else:
            self.set_speed_state(SPEEDSTATE.WALK)

    def update_LoS_to_h(self, game):
        visible_hums = arcade.SpriteList()
        for hum in game.humans_list:
            if arcade.has_line_of_sight(self.position, hum.position, game.walls_list, int(constants.ZOMBIE_VISION * (int(hum.speed_state)/1.5)), 2):
                visible_hums.append(hum)
        if len(visible_hums) > 0:
            self.set_speed_state(SPEEDSTATE.RUN)
            nearest_hum, dist_to_nh = arcade.get_closest_sprite(self, visible_hums)
            return (nearest_hum.center_x, nearest_hum.center_y)
            vect = (nearest_hum.center_x - self.center_x, nearest_hum.center_y - self.center_y)
            vect_len = math.sqrt(vect[0]**2 + vect[1]**2)
            move_vect = vect[0]/(vect_len), vect[1]/(vect_len)
            return move_vect
        else:
            self.set_speed_state(SPEEDSTATE.WALK)

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

    def set_speed_state(self,newspeed):
        if self.speed_state == newspeed:
            if self.sprite_speed!=0:
                xvel = self.velocity[0]
                yvel = self.velocity[1]
                v_len = math.sqrt(xvel**2 + yvel**2)
                self.velocity = (xvel/v_len)*self.sprite_speed, (yvel/v_len)*self.sprite_speed
            return
        self.speed_state = newspeed
        self.sprite_speed = int(self.speed_state) * self.base_speed

        xvel = self.velocity[0]
        yvel = self.velocity[1]
        v_len = math.sqrt(xvel**2 + yvel**2)
        self.velocity = (xvel/v_len)*self.sprite_speed, (yvel/v_len)*self.sprite_speed

    def makeHumanDecision(self, game):
        # DECISION TREE - In Active Development
        visibleZom = False
        for zom in game.zombies_list:
            if arcade.has_line_of_sight(self.position,zom.position,game.walls_list,constants.HUMAN_VISION):
                visibleZom = True
                break
        visibleItem = False
        for item in game.items_list:
            if arcade.has_line_of_sight(self.position,item.position,game.walls_list,constants.HUMAN_VISION):
                visibleItem = True
                break
        if self.mood == Mood.RELAXED:
            if visibleZom:
                self.mood = Mood.ALERT
            elif visibleItem:
                self.mood = Mood.MOTIVATED
            else:
                pass # a* to random point?
        if self.mood == Mood.MOTIVATED:
            if visibleZom:
                self.mood = Mood.ALERT
            elif visibleItem:
                pass # a* to item
            else:
                self.mood = Mood.RELAXED
        if self.mood == Mood.ALERT:
            if visibleZom:
                if self.hasItem("gun"):
                    pass # shoot zom
                elif self.hasItem("knife") or self.hasItem("antidote"):
                    pass # a* to zom
                if self.visibleDoor:
                    # if zom through door:
                        # a* to best spot
                    # else:
                        # a* through door
                    pass
                else:
                    pass # a* to best spot
        else:
            self.mood = Mood.RELAXED