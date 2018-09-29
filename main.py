from os import path
from random import choice, random

from board import Board
from item import Item
from menu import Menu
from player import Player
from screen import Camera, TiledMap
from walls import Obstacle
from zombie import Zombie
from settings import *
from functions import quit, collide_hit_rect, draw_player_health, get_hit


class TheGame:
    def __init__(self, width, height):
        pg.mixer.pre_init(44100, 16, 1, 2048)
        pg.init()
        self.width = width
        self.height = height
        self.board = Board(width, height)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = None
        self.map_img = None
        self.map_rect = None
        self.player_img = None
        self.intro_img = None
        self.zombie_img = None
        self.bullet_images = {}
        self.player = None
        self.fog = pg.Surface(self.board.surface.get_size())
        self.light_mask = None
        self.splats = []
        self.gun_smoke = []
        self.zombie_death_smoke = []
        self.items_images = {}
        self.sound_effects = {}
        self.weapon_sounds = {}
        self.zombie_moan_sounds = []
        self.zombie_pain_sounds = []
        self.zombie_die_sounds = []
        self.player_pain_sounds = []
        self.player_die_sounds = []
        self.img_folder = None
        self.dim_screen = pg.Surface(self.board.surface.get_size())
        self.load_data()
        self.light_rect = self.light_mask.get_rect()
        self.map_data = self.map.make_map()
        self.night = True
        self.new()
        self.camera = Camera(self.map.width, self.map.height)
        self.fps_clock = pg.time.Clock()
        self.dt = None
        self.menu = Menu(self)
        self.game_paused = False

    def load_data(self):
        self.dim_screen.set_alpha(80)
        self.dim_screen.fill((0, 0, 0))
        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'images')
        items_img_folder = path.join(self.img_folder, 'items')
        map_folder = path.join(game_folder, 'maps')
        sounds_folder = path.join(game_folder, 'sounds')
        splats_folder = path.join(self.img_folder, 'splat')
        self.map = TiledMap(path.join(map_folder, 'clab_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.intro_img = pg.image.load(path.join(self.img_folder, INTRO_IMG))
        self.player_img = pg.image.load(path.join(self.img_folder, PLAYER_IMAGE_NAKED))
        self.zombie_img = pg.image.load(path.join(self.img_folder, ZOMBIE_IMAGE))
        self.bullet_images['large'] = pg.image.load(path.join(self.img_folder, BULLET_IMG))
        self.bullet_images['large'] = pg.transform.scale(self.bullet_images['large'], (5, 10))
        self.bullet_images['small'] = pg.transform.scale(self.bullet_images['large'], (3, 7))
        for smoke in FLASH_SMOKE:
            self.gun_smoke.append(pg.image.load(path.join(game_folder, 'images/smokes/Flash/{}'.format(smoke))))
        for smoke in GREEN_SMOKE:
            self.zombie_death_smoke.append(pg.image.load(path.join(game_folder, 'images/smokes/Green smoke/{}'.format(smoke))))
        for splat in SPLATS:
            splat_img = pg.image.load(path.join(splats_folder, splat))
            splat_img = pg.transform.scale(splat_img, (64, 64))
            self.splats.append(splat_img)
        for item in ITEM_IMAGES:
            self.items_images[item] = pg.image.load(path.join(items_img_folder, ITEM_IMAGES[item]))
            if item == 'shotgun':
                self.items_images[item] = pg.transform.scale(self.items_images[item], (2 * ITEM_SIZE, ITEM_SIZE))
            else:
                self.items_images[item] = pg.transform.scale(self.items_images[item], (ITEM_SIZE, ITEM_SIZE))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(self.img_folder, LIGHT_MASK))
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        for sound in SOUND_EFFECTS:
            self.sound_effects[sound] = pg.mixer.Sound(path.join(sounds_folder, SOUND_EFFECTS[sound]))
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for sound in WEAPON_SOUNDS[weapon]:
                track = pg.mixer.Sound(path.join(sounds_folder, sound))
                track.set_volume(0.3)
                self.weapon_sounds[weapon].append(track)
        for sound in ZOMBIE_MOAN_SOUNDS:
            track = pg.mixer.Sound(path.join(sounds_folder, sound))
            track.set_volume(0.4)
            self.zombie_moan_sounds.append(track)
        for sound in ZOMBIE_PAIN_SOUNDS:
            track = pg.mixer.Sound(path.join(sounds_folder, sound))
            track.set_volume(0.5)
            self.zombie_pain_sounds.append(track)
        for sound in ZOMBIE_DIE_SOUNDS:
            track = pg.mixer.Sound(path.join(sounds_folder, sound))
            track.set_volume(0.8)
            self.zombie_die_sounds.append(track)
        for sound in PLAYER_DEATH_SOUNDS:
            track = pg.mixer.Sound(path.join(sounds_folder, sound))
            track.set_volume(0.6)
            self.player_die_sounds.append(track)
        for sound in PLAYER_PAIN_SOUNDS:
            track = pg.mixer.Sound(path.join(sounds_folder, sound))
            track.set_volume(0.5)
            self.player_pain_sounds.append(track)

    def run(self, difficulty):
        if difficulty == "easy":
            zombie_speed = 1
            zombie_attack = 1
        elif difficulty == "normal":
            zombie_speed = 1.2
            zombie_attack = 2
        elif difficulty == "hard":
            zombie_speed = 1.5
            zombie_attack = 3
        else:
            zombie_speed = 1.7
            zombie_attack = 5
        while True:
            self.dt = self.fps_clock.tick(FPS) / 1000
            self.handle_events()
            if not self.game_paused:
                self.update()
            self.draw()
            pg.display.flip()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.shield < PLAYER_SHIELD:
                hit.kill()
                self.sound_effects['heal'].play()
                self.player.add_shield(BIG_HEALTH_PACK)
            if hit.type == 'shotgun':
                hit.kill()
                self.sound_effects['shotgun_pickup'].play()
                self.player.weapon = 'shotgun'
                self.player.all_weapons.append('shotgun')
            if hit.type == 'pistol':
                hit.kill()
                self.sound_effects['pistol_pickup'].play()
                self.player.weapon = 'pistol'
                self.player.all_weapons.append('pistol')
        hits = pg.sprite.spritecollide(self.player, self.zombies, False, collide_hit_rect)
        for hit in hits:
            self.player.shield -= ZOMBIE_DMG
            hit.vel = vector(0, 0)
            if random() < 0.5:
                choice(self.player_pain_sounds).play()
            if self.player.shield <= 0:
                pg.time.wait(500)
                choice(self.player_die_sounds).play()
                self.menu.game_over()
        if hits:
            get_hit(self.player)
            self.player.position += vector(KICKBACK, 0).rotate(-hits[0].rotation)
        hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
        for hit in hits:
            hit.shield -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vector(0, 0)
            get_hit(hit)
            if random() < 0.7:
                choice(self.zombie_pain_sounds).play()

    def handle_events(self):
        self.player.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit()
                if event.key == pg.K_p:
                    self.game_paused = not self.game_paused
                if event.key == pg.K_n:
                    self.night = not self.night

    def new(self):
        for tile_object in self.map.tmxdata.objects:
            object_center = vector(tile_object.x + tile_object.width / 2,
                                   tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, object_center.x, object_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Zombie(self, object_center.x, object_center.y)
            if tile_object.name in ['health', 'shotgun', 'pistol']:
                Item(self, object_center, tile_object.name)

    def draw(self):
        self.board.surface.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Zombie):
                sprite.draw_shield()
            self.board.surface.blit(sprite.image, self.camera.apply(sprite))
        if self.night:
            self.render_fog()
        draw_player_health(self.board.surface, 20, 10, self.player.shield / PLAYER_SHIELD)
        self.board.draw_zombies_left(len(self.zombies))
        if self.game_paused:
            self.board.surface.blit(self.dim_screen, (0, 0))
            self.board.draw_pause()

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.board.surface.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)


if __name__ == "__main__":
    game = TheGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    # game.menu.game_intro()
    game.run("easy")
