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

NIGHT_COLOR = (40, 40, 40)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = 'light_med.png'

PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
PLAYER_LIVES = 3
PLAYER_SHIELD = 1000
PLAYER_SPEED = 400
PLAYER_ROTATION_SPEED = 150
PLAYER_IMAGE_NAKED = 'hitman1_hold.png'
PLAYER_IMAGE_PISTOL = 'hitman1_gun.png'
PLAYER_IMAGE_SHOTGUN = 'hitman1_machine.png'
PLAYER_IMAGE_UZI = 'hitman1_silencer.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
LIVES_IMG = 'lives_icon.png'

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
KICKBACK = 10
BULLET_IMG = 'bulletYellowSilver_outline.png'
WEAPONS = {}
WEAPONS['pistol'] = {
    'bullet_speed': 500,
    'bullet_lifetime': 1000,
    'rate': 300,
    'kickback': 200,
    'spread': 5,
    'damage': 10,
    'bullet_size': 'large',
    'bullet_count': 1,
}
WEAPONS['shotgun'] = {
    'bullet_speed': 400,
    'bullet_lifetime': 500,
    'rate': 900,
    'kickback': 200,
    'spread': 20,
    'damage': 5,
    'bullet_size': 'small',
    'bullet_count': 12,
}
WEAPONS['uzi'] = {
    'bullet_speed': 500,
    'bullet_lifetime': 500,
    'rate': 100,
    'kickback': 150,
    'spread': 10,
    'damage': 3,
    'bullet_size': 'small',
    'bullet_count': 1,
}
WEAPONS['rifle'] = {
    'bullet_speed': 700,
    'bullet_lifetime': 2000,
    'rate': 1500,
    'kickback': 700,
    'spread': 2,
    'damage': 50,
    'bullet_size': 'long',
    'bullet_count': 1,
}
BARREL_OFFSET = vector(30, 10)
SMOKE_DURATION = 40

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
SPLAT_LAYER = 1
PLAYER_LAYER = 2
ZOMBIE_LAYER = 2
BULLET_LAYER = 3
SMOKE_LAYER = 5

ITEM_BOB_RANGE = 20
ITEM_BOB_SPEED = 0.4
BIG_HEALTH_PACK = 300
ITEM_SIZE = 30
ITEM_IMAGES = {
    'health': 'genericItem_color_102.png',
    'mini_health': 'genericItem_color_100.png',
    'water': 'genericItem_color_118.png',
    'beer': 'genericItem_color_119.png',
    'coffee': 'genericItem_color_124.png',
    'usb_flash': 'genericItem_color_099.png',
    'id_card': 'genericItem_color_151.png',
    'key': 'genericItem_color_155.png',
    'money': 'genericItem_color_158.png',
    'pistol': 'pistol.png',
    'shotgun': 'shotgun.png',
    'rifle': 'rifle.png',
    'uzi': 'uzi.png'
}
GREEN_SMOKE = [
    'fart00.png',
    'fart01.png',
    'fart02.png',
    'fart03.png',
    'fart04.png',
    'fart05.png',
    'fart06.png',
    'fart07.png',
    'fart08.png',
]
FLASH_SMOKE = [
    'flash00.png',
    'flash01.png',
    'flash02.png',
    'flash03.png',
    'flash04.png',
    'flash05.png',
    'flash06.png',
    'flash07.png',
    'flash08.png',
]
SPLATS = [
    'bloodsplats_0003.png',
    'bloodsplats_0004.png',
    'bloodsplats_0006.png',
    'bloodsplats_0007.png',
]
SOUND_EFFECTS = {
    'heal': 'healed.wav',
    'pistol_pickup': 'pistol_reload.wav',
    'uzi_pickup': 'pistol_reload.wav',
    'rifle_pickup': 'rifle_pickup.wav',
    'shotgun_pickup': 'shotgun_reload.wav'
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
ZOMBIE_DIE_SOUNDS = [
    'zombie_die.wav'
]
WEAPON_SOUNDS = {
    'pistol': [
        'pistol.ogg',
        'pistol2.ogg',
        'pistol3.ogg'
    ],
    'shotgun': [
        'shotgun.ogg',
        'shotgun2.ogg',
        'shotgun3.ogg'
    ],
    'rifle': [
        'rifle.ogg',
        'rifle2.ogg',
        'rifle3.ogg'
    ],
    'uzi': [
        'pistol.ogg',
        'pistol2.ogg',
        'pistol3.ogg'
    ]
}
