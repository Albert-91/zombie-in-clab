import pygame

from functions import vector

FPS = 80
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
MENU_FONT_COLOR = (255, 0, 0)

START_POSITION_X = 350
START_POSITION_Y = 150

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
PLAYER_LIVES = 3
PLAYER_SHIELD = 1000
PLAYER_SPEED = 200
PLAYER_ROTATION_SPEED = 200
PLAYER_IMAGE = 'hitman1_silencer.png'
PLAYER_HIT_RECT = pygame.Rect(0, 0, 35, 35)

ZOMBIE_WIDTH = 23
ZOMBIE_HEIGHT = 28
ZOMBIE_SHIELD = 8
ZOMBIE_SPEED_EASY = 70
ZOMBIE_SPEED_NORM = 30
ZOMBIE_SPEED_HARD = 40
ZOMBIE_SPEED_HELL = 50
ZOMBIE_IMAGE = 'zombie1_hold.png'
ZOMBIE_HIT_RECT = pygame.Rect(0, 0, 30, 30)
QUANTITY_OF_ZOMBIES = 0

BULLET_IMG = 'bulletYellowSilver_outline.png'
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BARREL_OFFSET = vector(30, 10)

WALL_COLOR = (0, 0, 0)
WALL_SIZE = 10

INTRO_SPRITE_WIDTH = 40
INTRO_SPRITE_HEIGHT = 40
INTRO_SPRITE_POS_X = 0.37

OPTIONS_SPRITE_WIDTH = 45
OPTIONS_SPRITE_HEIGHT = 45
OPTIONS_SPRITE_POS_X = 0.3

DIFFICULT_SPRITE_WIDTH = 40
DIFFICULT_SPRITE_HEIGHT = 40
DIFFICULT_SPRITE_POS_X = 0.25

