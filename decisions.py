from enum import Enum
import arcade
import constants

class Mood(Enum):
    RELAXED = 1
    MOTIVATED = 2
    ALERT = 3

# -- UPDATE THIS BEHAVIOR [ZSim] --
# move_vector_z = moving.update_LoS_to_z(self)
# # DIRECTIONAL HANDLING CHANGES - BUGGY vvv
# if move_vector_z:
#     xvel = moving.velocity[0]
#     yvel = moving.velocity[1]
#     if not hit_edge_x and not hit_wall_x:
#         xvel = move_vector_z[0]*constants.HUMAN_SPEED_MIN
#     if not hit_edge_y and not hit_wall_y:
#         yvel = move_vector_z[1]*constants.HUMAN_SPEED_MIN
#     v_len = math.sqrt(xvel**2 + yvel**2)
#     moving.velocity = (xvel/v_len)*moving.sprite_speed, (yvel/v_len)*moving.sprite_speed

def makeHumanDecision(human, game):
    visibleZom = False
    for zom in game.zombies_list:
        if arcade.has_line_of_sight(human.position,zom.position,game.walls_list,constants.HUMAN_VISION):
            visibleZom = True
            break
    visibleItem = False
    for item in game.items_list:
        if arcade.has_line_of_sight(human.position,item.position,game.walls_list,constants.HUMAN_VISION):
            visibleItem = True
            break
    if human.mood == Mood.RELAXED:
        if visibleZom:
            human.mood = Mood.ALERT
        elif visibleItem:
            human.mood = Mood.MOTIVATED
        else:
            pass # a* to random point?
    if human.mood == Mood.MOTIVATED:
        if visibleZom:
            human.mood = Mood.ALERT
        elif visibleItem:
            pass # a* to item
        else:
            human.mood = Mood.RELAXED
    if human.mood == Mood.ALERT:
        if visibleZom:
            if human.hasItem("gun"):
                pass # shoot zom
            elif human.hasItem("knife") or human.hasItem("antidote"):
                pass # a* to zom
            if human.visibleDoor:
                # if zom through door:
                    # a* to best spot
                # else:
                    # a* through door
                pass
            else:
                pass # a* to best spot
    else:
        human.mood = Mood.RELAXED

def makeInfectedDecision(infected, game):
    visibleItem = False
    for item in game.items_list:
        if arcade.has_line_of_sight(infected.position,item.position,game.walls_list,constants.HUMAN_VISION):
            visibleItem = True
            break
    if infected.mood == Mood.RELAXED:
        if visibleItem:
            infected.mood = Mood.MOTIVATED
        else:
            pass # a* to random point?
    if infected.mood == Mood.MOTIVATED:
        if visibleItem:
            pass # a* to item
        else:
            infected.mood = Mood.RELAXED

def makeZombieDecision(zombie):
    if zombie.mood == Mood.RELAXED:
        if zombie.visibleHuman:
            zombie.mood = Mood.ALERT
        else:
            pass # a* to random
    else:
        if zombie.visibleHuman:
            pass # a* to human
        else:
            zombie.mood = Mood.RELAXED