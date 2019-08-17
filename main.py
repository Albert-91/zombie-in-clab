from os import path
from random import choice, random

from zombie_game.board import Board
from zombie_game.functions import quit_game, collide_hit_rect, draw_player_health, get_hit
from zombie_game.item import Item
from zombie_game.menu import Menu
from zombie_game.player import Player
from zombie_game.screen import Camera, TiledMap
from zombie_game.settings import *
from zombie_game.walls import Obstacle
from zombie_game.zombie import Zombie


class Game:

    def __init__(self):
        pg.mixer.pre_init(44100, 16, 1, 2048)
        pg.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.board = Board(self.width, self.height)
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.zombies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.locked_rooms = pg.sprite.Group()
        self.bonus_items = pg.sprite.Group()
        self.playing = True
        self.destroyed = False
        self.map = None
        self.map_img = None
        self.map_rect = None
        self.intro_img = None
        self.zombie_img = None
        self.bullet_images = {}
        self.player_img = None
        self.player = None
        self.player_start_pos = None
        self.player_pain_sounds = []
        self.player_die_sounds = []
        self.locked_room_key = None
        self.locked_first_room = None
        self.locked_room_card = []
        self.fog = pg.Surface(self.board.surface.get_size())
        self.light_mask = None
        self.splats = []
        self.gun_smoke = []
        self.zombie_death_smoke = []
        self.items_images = {}
        self.sound_effects = {}
        self.weapon_sounds = {}
        self.zombie_speeds = ZOMBIE_SPEEDS
        self.zombie_moan_sounds = []
        self.zombie_pain_sounds = []
        self.zombie_die_sounds = []
        self.locked_door_sound = None
        self.dim_screen = pg.Surface(self.board.surface.get_size())
        self.lives_img = None
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.sounds_folder = path.join(self.game_folder, 'sounds')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.score_list = []
        self.character_type = 'hitman1_'
        self.mini_map_img = None
        self.load_data()
        self.light_rect = self.light_mask.get_rect()
        self.night = True
        self.new()
        self.mini_map = pg.Surface([self.map_rect.width / 15, self.map_rect.height / 15], pg.SRCALPHA, 32)
        self.mini_map_img = pg.image.load(path.join(self.map_folder, 'clab_map.png'))
        self.mini_map_img = pg.transform.scale(self.mini_map_img, (int(self.map_rect.width / 15), int(self.map_rect.height / 15)))
        self.camera = Camera(self, self.map.width, self.map.height)
        self.fps_clock = pg.time.Clock()
        self.dt = None
        self.game_paused = False
        self.damage = None
        self.menu = Menu(self)
        self.bonus = True

    def load_data(self):
        self.dim_screen.set_alpha(80)
        self.dim_screen.fill((0, 0, 0))
        self.load_scoreboard(SCOREBOARD)
        self.player_img = pg.image.load(path.join(self.img_folder, self.character_type + PLAYER_IMAGE_NAKED))
        self.zombie_img = pg.image.load(path.join(self.img_folder, ZOMBIE_IMAGE))
        self.load_bullets()
        self.lives_img = pg.image.load(path.join(self.img_folder, LIVES_IMG))
        self.lives_img = pg.transform.scale(self.lives_img, (20, 20))
        self.load_flash_smoke()
        self.load_green_smoke()
        self.load_splats()
        self.load_items()
        self.fog.fill(NIGHT_COLOR)
        self.load_light_mask()
        self.load_sounds()

    def load_flash_smoke(self):
        for smoke in FLASH_SMOKE:
            self.gun_smoke.append(pg.image.load(path.join(self.game_folder, 'images/smokes/Flash/{}'.format(smoke))))

    def load_green_smoke(self):
        for smoke in GREEN_SMOKE:
            self.zombie_death_smoke.append(
                pg.image.load(path.join(self.game_folder, 'images/smokes/Green smoke/{}'.format(smoke))))

    def load_light_mask(self):
        self.light_mask = pg.image.load(path.join(self.img_folder, LIGHT_MASK))
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)

    def load_sounds(self):
        for sound in SOUND_EFFECTS:
            self.sound_effects[sound] = pg.mixer.Sound(path.join(self.sounds_folder, SOUND_EFFECTS[sound]))
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            self._add_sounds(WEAPON_SOUNDS[weapon], self.weapon_sounds[weapon], 0.3)
        self._add_sounds(ZOMBIE_MOAN_SOUNDS, self.zombie_moan_sounds, 0.4)
        self._add_sounds(ZOMBIE_PAIN_SOUNDS, self.zombie_pain_sounds, 0.5)
        self._add_sounds(ZOMBIE_DIE_SOUNDS, self.zombie_die_sounds, 0.8)
        self._add_sounds(PLAYER_DEATH_SOUNDS, self.player_die_sounds, 0.6)
        self._add_sounds(PLAYER_PAIN_SOUNDS, self.player_pain_sounds, 0.5)

    def load_items(self):
        items_img_folder = path.join(self.img_folder, 'items')
        for item in ITEM_IMAGES:
            self.items_images[item] = pg.image.load(path.join(items_img_folder, ITEM_IMAGES[item]))
            if item == 'shotgun' or item == 'rifle':
                self.items_images[item] = pg.transform.scale(self.items_images[item], (2 * ITEM_SIZE, ITEM_SIZE))
            else:
                self.items_images[item] = pg.transform.scale(self.items_images[item], (ITEM_SIZE, ITEM_SIZE))

    def load_splats(self):
            splats_folder = path.join(self.img_folder, 'splat')
            for splat in SPLATS:
                splat_img = pg.image.load(path.join(splats_folder, splat))
                splat_img = pg.transform.scale(splat_img, (64, 64))
                self.splats.append(splat_img)

    def load_bullets(self):
        self.bullet_images['large'] = pg.image.load(path.join(self.img_folder, BULLET_IMG))
        self.bullet_images['long'] = pg.transform.scale(self.bullet_images['large'], (5, 15))
        self.bullet_images['large'] = pg.transform.scale(self.bullet_images['large'], (5, 10))
        self.bullet_images['small'] = pg.transform.scale(self.bullet_images['large'], (3, 7))

    def load_scoreboard(self, scoreboard):
        with open(path.join(self.game_folder, scoreboard), 'r') as f:
            temp_list = [line.rstrip('\n') for line in f]
            for i in temp_list:
                word = i.split()
                self.score_list.append((word[0], word[1]))

    def _add_sounds(self, source, sound_list, volume=1.0):
        for sound in source:
            track = pg.mixer.Sound(path.join(self.sounds_folder, sound))
            track.set_volume(volume)
            sound_list.append(track)

    def run(self, difficult, name):
        self.player.name = name
        self.playing = True
        self.set_params_to_difficult(difficult)
        while self.playing:
            self.dt = self.fps_clock.tick(FPS) / 1000
            self.handle_events()
            if not self.game_paused:
                self.update()
            self.draw()
            pg.display.flip()

    def set_params_to_difficult(self, difficult):
        if difficult == "easy":
            self.zombie_speeds = ZOMBIE_SPEEDS
            self.damage = ZOMBIE_DMG
        elif difficult == "normal":
            self.zombie_speeds = [i * ZOMBIE_NORMAL_RATIO for i in ZOMBIE_SPEEDS]
            self.damage = ZOMBIE_DMG * ZOMBIE_NORMAL_RATIO
        elif difficult == "hard":
            self.zombie_speeds = [i * ZOMBIE_HARD_RATIO for i in ZOMBIE_SPEEDS]
            self.damage = ZOMBIE_DMG * ZOMBIE_HARD_RATIO
        else:
            self.zombie_speeds = [i * ZOMBIE_HELL_RATIO for i in ZOMBIE_SPEEDS]
            self.damage = ZOMBIE_DMG * ZOMBIE_HELL_RATIO

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        self.update_mini_map()
        self._collide_player_with_items()
        self._collide_player_with_bonus()
        self._collide_player_with_zombie()
        self._collide_bullet_with_zombie()
        self._collide_bullet_with_door()
        if not self.player.has_key or not self.player.has_id:
            self.locked_room_reaction()
        if self.player.has_key:
            self.locked_room_key.kill()
        if self.player.has_id:
            self._destroy_locked_door()
        if len(self.zombies) <= 0:
            self.update_scoreboard(self.player.total_accuracy)
            self.menu.game_over(self.score_list, 'Congratulations')

    def _collide_player_with_bonus(self):
        hits = pg.sprite.spritecollide(self.player, self.bonus_items, False)
        delete = False
        for hit in hits:
            if hit.type == 'coffee':
                delete = self.get_bonus("EXTRA SPEED")
                self.player.speed = 300
            if hit.type == 'water':
                if self.player.shield < PLAYER_SHIELD:
                    delete = self.get_bonus()
                    self.player.shield = PLAYER_SHIELD
            if hit.type == 'beer':
                delete = self.get_bonus("EXTRA STRENGTH")
                self.damage /= 2
            if delete:
                for i in self.bonus_items:
                    i.kill()

    def _collide_player_with_zombie(self):
        hits = pg.sprite.spritecollide(self.player, self.zombies, False, collide_hit_rect)
        for hit in hits:
            self.player.shield -= self.damage
            hit.vel = vector(0, 0)
            if random() < 0.5:
                choice(self.player_pain_sounds).play()
            if self.player.shield <= 0:
                pg.time.wait(500)
                choice(self.player_die_sounds).play()
                if self.player.lives > 0:
                    self.player.lives -= 1
                    self.player.vel = vector(0, 0)
                    self.player.position = vector(self.player_start_pos[0], self.player_start_pos[1])
                    self.player.shield = PLAYER_SHIELD
                else:
                    self.playing = False
                    self.menu.game_over(self.score_list, 'GAME OVER')
        if hits:
            get_hit(self.player)
            self.player.position += vector(KICKBACK, 0).rotate(-hits[0].rotation)

    def _collide_bullet_with_zombie(self):
        hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
        for hit in hits:
            hit.shield -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            self.player.accurate_shot += len(hits[hit])
            hit.vel = vector(0, 0)
            get_hit(hit)
            if random() < 0.7:
                choice(self.zombie_pain_sounds).play()

    def _destroy_locked_door(self):
        for i in self.locked_room_card:
            i.kill()

    def _collide_bullet_with_door(self):
        hits = pg.sprite.groupcollide(self.locked_rooms, self.bullets, False, False)
        for hit in hits:
            if not self.destroyed and self.player.rect.centery < 1500:
                hit.kill()
                busy = pg.mixer.get_busy()
                if busy:
                    pg.mixer.stop()
                    self.sound_effects['broken_door'].play()
                    self.destroyed = True

    def _collide_player_with_items(self):
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.shield < PLAYER_SHIELD:
                self.get_health(hit, BIG_HEALTH_PACK)
            if hit.type == 'mini_health' and self.player.shield < PLAYER_SHIELD:
                self.get_health(hit, MINI_HEALTH_PACK)
            if hit.type == 'shotgun':
                self.get_weapon(hit, 'shotgun')
            if hit.type == 'pistol':
                self.get_weapon(hit, 'pistol')
            if hit.type == 'uzi':
                self.get_weapon(hit, 'uzi')
            if hit.type == 'rifle':
                self.get_weapon(hit, 'rifle')
            if hit.type == 'ammo_small':
                self.get_ammo(hit, 'small')
            if hit.type == 'ammo_big':
                self.get_ammo(hit, 'big')
            if hit.type == 'key':
                hit.kill()
                self.player.has_key = True
            if hit.type == 'id_card':
                hit.kill()
                self.player.has_id = True
            if hit.type == 'money':
                hit.kill()
                self.player.money = True

    def get_bonus(self, bonus=None):
        self.sound_effects['heal'].play()
        self.player.bonus = bonus
        return True

    def get_ammo(self, hit, pack):
        hit.kill()
        self.sound_effects['pistol'].play()
        for weapon in WEAPONS.keys():
            if weapon in self.player.all_weapons:
                self.check_ammo_limit(weapon, pack)

    def check_ammo_limit(self, weapon, pack):
        type_of_pack = {'small': 0.8, 'big': 1.2}
        AMMO = {
            'pistol': 60,
            'shotgun': 228,
            'uzi': 200,
            'rifle': 10
        }
        if self.player.ammo[weapon] < WEAPONS[weapon]['ammo_limit']:
            self.player.ammo[weapon] += int(AMMO[weapon] * type_of_pack[pack])
        if self.player.ammo[weapon] > WEAPONS[weapon]['ammo_limit']:
            self.player.ammo[weapon] = WEAPONS[weapon]['ammo_limit']

    def get_health(self, hit, pack):
        hit.kill()
        self.sound_effects['heal'].play()
        self.player.add_shield(pack)

    def get_weapon(self, hit, weapon):
        hit.kill()
        self.sound_effects[weapon].play()
        self.player.weapon = weapon
        self.player.all_weapons.append(weapon)
        self.player.actual_ammo = self.player.ammo[weapon]

    def locked_room_reaction(self):
        keys = pg.key.get_pressed()
        hits = pg.sprite.spritecollide(self.player, self.locked_rooms, False)
        if not keys[pg.K_SPACE] and hits:
            self.sound_effects['locked_door'].play()

    def handle_events(self):
        self.player.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit_game()
                if event.key == pg.K_p:
                    self.game_paused = not self.game_paused
                if 50 < self.player.rect.x < 102 and 1735 < self.player.rect.y < 1753:
                    if event.key == pg.K_SPACE:
                        self.night = not self.night

    def new(self):
        self.map = TiledMap(path.join(self.map_folder, 'clab_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            object_center = vector(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, object_center.x, object_center.y)
                self.player_start_pos = (object_center.x, object_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'locked':
                self.locked_room_key = Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.locked_rooms.add(self.locked_room_key)
            if tile_object.name == 'locked_gun':
                self.locked_first_room = Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.locked_rooms.add(self.locked_first_room)
            if tile_object.name == 'locked_card':
                door = Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                self.locked_rooms.add(door)
                self.locked_room_card.append(door)
            if tile_object.name == 'zombie':
                Zombie(self, object_center.x, object_center.y)
            if tile_object.name in ITEM_IMAGES.keys():
                if tile_object.name == 'beer' or tile_object.name == 'water' or tile_object.name == 'coffee':
                    bonus = Item(self, object_center, tile_object.name)
                    self.bonus_items.add(bonus)
                else:
                    Item(self, object_center, tile_object.name)

    def draw(self):
        self.board.surface.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        self._draw_all_shields()
        if self.night:
            self.render_fog()
        draw_player_health(self.board.surface, 20, 10, self.player.shield / PLAYER_SHIELD)
        self.board.draw_zombies_left(len(self.zombies))
        self.board.draw_adds(self.board.surface, 150, 10, self.lives_img, self.player.lives)
        self.board.draw_adds(self.board.surface, self.width-340, self.height-160, self.mini_map)
        if self.player.has_key:
            self.board.draw_adds(self.board.surface, 80, 50, self.items_images['key'])
        if self.player.has_id:
            self.board.draw_adds(self.board.surface, 30, 50, self.items_images['id_card'])
        if self.bonus:
            self.board.draw_bonus(self.player.bonus)
            self._set_params_after_bonus()
        if self.player.weapon is not None:
            self.board.draw_adds(self.board.surface, 250, 7, self.items_images[self.player.weapon])
            self.board.draw_ammo_quantity('Ammo: {}'.format(self.player.ammo[self.player.weapon]))
        if self.game_paused:
            self.board.surface.blit(self.dim_screen, (0, 0))
            self.board.draw_pause()
        if self.player.money:
            self.board.draw_money()

    def render_fog(self):
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.board.surface.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def update_scoreboard(self, player_score):
        self.score_list.append((self.player.name, str(player_score)))
        self.score_list = sorted(self.score_list, key=lambda x: float(x[1]), reverse=True)
        self.score_list.remove(self.score_list[5])
        temp_list = []
        for i in self.score_list:
            temp_list.append(' '.join(i))
        with open(path.join(self.game_folder, SCOREBOARD), 'w') as f:
            for score in temp_list:
                f.write(score + '\n')

    def update_mini_map(self):
        self.mini_map.blit(self.mini_map_img, (0, 0))
        player_map_square = pg.Surface([5, 5], pg.SRCALPHA, 32)
        player_map_square.fill(BLUE)
        self.mini_map.blit(player_map_square, (self.player.rect.x / 15, self.player.rect.y / 15))
        for zombie in self.zombies:
            zombie_map_square = pg.Surface([5, 5], pg.SRCALPHA, 32)
            zombie_map_square.fill(RED)
            self.mini_map.blit(zombie_map_square, (zombie.rect.x / 15, zombie.rect.y / 15))

    def _set_params_after_bonus(self):
        timer_start = pg.time.get_ticks()
        timer_stop = pg.time.get_ticks() + 90
        if timer_stop - timer_start > 90:
            self.bonus = False
            self.player.speed = PLAYER_SPEED
            self.damage = ZOMBIE_DMG

    def _draw_all_shields(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Zombie):
                sprite.draw_shield()
            self.board.surface.blit(sprite.image, self.camera.apply(sprite))


if __name__ == "__main__":
    game = Game()
    game.menu.game_intro()
