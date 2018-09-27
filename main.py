from os import path
from board import Board
from item import Item
from menu import Menu
from player import Player
from screen import Camera, TiledMap
from walls import Obstacle
from zombie import Zombie
from settings import *
from functions import quit, collide_hit_rect, draw_player_health


class TheGame:
    def __init__(self, width, height):
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
        self.bullet_img = None
        self.player = None
        self.gun_smoke = []
        self.zombie_death_smoke = []
        self.items_images = {}
        self.load_data()
        self.map_data = self.map.make_map()
        self.new()
        self.camera = Camera(self.map.width, self.map.height)
        self.fps_clock = pg.time.Clock()
        self.dt = None
        self.menu = Menu(self)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        items_img_folder = path.join(img_folder, 'items')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'clab_map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.intro_img = pg.image.load(path.join(img_folder, INTRO_IMG))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMAGE))
        self.zombie_img = pg.image.load(path.join(img_folder, ZOMBIE_IMAGE))
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG))
        self.bullet_img = pg.transform.scale(self.bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))
        for smoke in FLASH_SMOKE:
            self.gun_smoke.append(pg.image.load(path.join(game_folder, 'images/smokes/Flash/{}'.format(smoke))))
        for smoke in GREEN_SMOKE:
            self.zombie_death_smoke.append(pg.image.load(path.join(game_folder, 'images/smokes/Green smoke/{}'.format(smoke))))
        for item in ITEM_IMAGES:
            self.items_images[item] = pg.image.load(path.join(items_img_folder, ITEM_IMAGES[item]))
            self.items_images[item] = pg.transform.scale(self.items_images[item], (ITEM_SIZE, ITEM_SIZE))

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
            self.draw()
            self.update()
            pg.display.flip()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.shield < PLAYER_SHIELD:
                hit.kill()
                self.player.add_shield(BIG_HEALTH_PACK)
        hits = pg.sprite.spritecollide(self.player, self.zombies, False, collide_hit_rect)
        for hit in hits:
            self.player.shield -= ZOMBIE_DMG
            hit.vel = vector(0, 0)
            if self.player.shield <= 0:
                self.menu.game_over()
        if hits:
            self.player.position += vector(KNOCKBACK, 0).rotate(-hits[0].rotation)
        hits = pg.sprite.groupcollide(self.zombies, self.bullets, False, True)
        for hit in hits:
            hit.shield -= BULLET_DMG
            hit.vel = vector(0, 0)

    def handle_events(self):
        self.player.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    quit()

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
            if tile_object.name in ['health']:
                Item(self, object_center, tile_object.name)

    def draw(self):
        self.board.surface.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Zombie):
                sprite.draw_shield()
            self.board.surface.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.board.surface, 20, 10, self.player.shield / PLAYER_SHIELD)


if __name__ == "__main__":
    game = TheGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    # game.menu.game_intro()
    game.run("easy")
