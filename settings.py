import pygame as pg
from functions import vector

GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

FPS = 80
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
MENU_FONT_COLOR = (255, 0, 0)
BAR_LENGTH = 100
BAR_HEIGHT = 20

START_POSITION_X = 350
START_POSITION_Y = 150

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
PLAYER_LIVES = 3
PLAYER_SHIELD = 1000
PLAYER_SPEED = 400
PLAYER_ROTATION_SPEED = 150
PLAYER_IMAGE = 'hitman1_silencer.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

ZOMBIE_WIDTH = 23
ZOMBIE_HEIGHT = 28
ZOMBIE_SHIELD = 100
ZOMBIE_SPEEDS_EASY = [70, 90, 110, 130, 150]
# ZOMBIE_SPEED_NORM = 30
# ZOMBIE_SPEED_HARD = 40
# ZOMBIE_SPEED_HELL = 50
ZOMBIE_IMAGE = 'zombie1_hold.png'
ZOMBIE_HIT_RECT = pg.Rect(0, 0, 30, 30)
ZOMBIE_DMG = 5
DETECT_RADIUS = 400
AVOID_RADIUS = 80
KNOCKBACK = 10

BULLET_IMG = 'bulletYellowSilver_outline.png'
BULLET_WIDTH = 5
BULLET_HEIGHT = 10
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BULLET_DMG = 20
BARREL_OFFSET = vector(30, 10)
KICKBACK = 200
GUN_SPREAD = 5
SMOKE_DURATION = 40

WALL_SIZE = 10

INTRO_IMG = 'menu_head.png'
INTRO_SPRITE_WIDTH = 40
INTRO_SPRITE_HEIGHT = 40
INTRO_SPRITE_POS_X = 0.37

OPTIONS_SPRITE_WIDTH = 45
OPTIONS_SPRITE_HEIGHT = 45
OPTIONS_SPRITE_POS_X = 0.3

DIFFICULT_SPRITE_WIDTH = 40
DIFFICULT_SPRITE_HEIGHT = 40
DIFFICULT_SPRITE_POS_X = 0.25

ITEM_LAYER = 1
PLAYER_LAYER = 2
ZOMBIE_LAYER = 2
BULLET_LAYER = 3
SMOKE_LAYER = 5

ITEM_BOB_RANGE = 20
ITEM_BOB_SPEED = 0.4
BIG_HEALTH_PACK = 300
ITEM_SIZE = 40
ITEM_IMAGES = {
    'health': 'genericItem_color_102.png',
    'mini_health': 'genericItem_color_100.png',
    'water': 'genericItem_color_118.png',
    'beer': 'genericItem_color_119.png',
    'coffee': 'genericItem_color_124.png',
    'usb_flash': 'genericItem_color_099.png',
    'id_card': 'genericItem_color_151.png',
    'key': 'genericItem_color_155.png',
    'money': 'genericItem_color_158.png'
}

PLAYER_PAIN_SOUNDS = [
    'pain1.wav',
    'pain2.wav',
    'pain3.wav',
    'pain4.wav',
    'pain5.wav',
    'pain6.wav'
]
PLAYER_DEATH_SOUNDS = [
    'die1.wav',
    'die2.wav'
]
ZOMBIE_MOAN_SOUNDS = [
    'zombie-1.wav',
    'zombie-2.wav',
    'zombie-3.wav',
    'zombie-4.wav',
    'zombie-5.wav'
]
ZOMBIE_PAIN_SOUNDS = [
    'monster-2.wav',
    'monster-3.wav',
    'monster-4.wav',
    'monster-5.wav',
    'monster-6.wav',
    'monster-7.wav',
]
GUN_SOUNDS = [
    'pistol.ogg',
    'pistol2.ogg',
    'pistol3.ogg'
]
