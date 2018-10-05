
import pygame

# size of screen

WINDOW_WIDTH = 1300 # px
WINDOW_HEIGHT = 700 # px

WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

METER_PER_PIXAR = 2

FPS = 30 # fps

# flag

FLAG_HP = 5000
FLAG_HP_WARNING = 1500

# team mate

TEAM_SIZE = 5


# tank

TANK_ANGLE_TO_ROTATE = 5 # degree

TANK_SPEED = 2 # m/s

TANK_VIEWRANGE = 50 # m

TANK_TIME_RELOAD = 1000 # ms

TANK_HP = 1000

TANK_ALPHA_FOR_BULLET_FIRE = 40

TANK_RAM = 10

# bullet

BULLET_SPEED = 1/10 # m/ms

BULLET_DAMAGE = 200 

BLUE = (0,0,255) 

BULLET_TIME_REFLECT_WALL = 1

BULLET_MAX_DISTANCE = 350

#player
PLAYER_CONTROL_TANK = 3

# stragy

ENEMY_RANDOM_ATTACK = 0.6


ALLY_RANDOM_ATTACK = .8

ANGLE_PERCENT = 5

TIMER = 5000