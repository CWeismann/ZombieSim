SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
STATS_HEIGHT = 100
SCREEN_TITLE = "Zombie Sim"
SCALING = 2.0

NUM_ZOMBIES = 2 # SUGGESTED 2
NUM_HUMANS = 5 # SUGGESTED: 5

INCUBATION_PERIOD = 10.0 # seconds; SUGGESTED: 10.0
HUMAN_VISION = 75
ZOMBIE_VISION = 150

HUMAN_SPEED_MIN = 0.15
ZOMBIE_SPEED_MIN = 0.15 #TODO: was 0.05

# MAX_SPEED = 0.75
SPEED = 1
WALL_GEN = 2 # larger value = fewer walls; SUGGESTED: 2
DOOR_GEN = 10 # larger value = fewer doors; SUGGESTED: 10
ITEM_GEN = 10 # larger value = fewer items; SUGGESTED: 10

WALL_LENGTH = SCALING * 10 # May be inaccurate - testing needed

CHECK_TIME = 1.0 # how often a* is recalculated

MAP_NUMBER = 0
TOTAL_MAPS = 2