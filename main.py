from os import path
from board import Board
from menu import Menu
from player import Player
from screen import Camera, Map
from walls import Wall
from zombie import Zombie
from settings import *
from functions import quit


class TheGame:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.zombies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.map = None
        self.player_img = None
        self.intro_img = None
        self.zombie_img = None
        self.bullet_img = None
        self.player = None
        self.load_data()
        self.map_data = self.map.get_map()
        self.new()
        self.camera = Camera(self.map.width, self.map.height)
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.dt = None
        self.all_sprites.add(self.player)
        self.menu = Menu(self)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.intro_img = pygame.image.load(path.join(img_folder, INTRO_IMG))
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMAGE))
        self.zombie_img = pygame.image.load(path.join(img_folder, ZOMBIE_IMAGE))
        self.bullet_img = pygame.image.load(path.join(img_folder, BULLET_IMG))
        self.bullet_img = pygame.transform.scale(self.bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))

    def run(self, difficulty):
        max_distance = 300
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
            pygame.display.flip()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
        hits = pygame.sprite.groupcollide(self.bullets, self.zombies, True, False)
        for hit in hits:
            hit.kill()

    def handle_events(self):
        self.player.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quit()

    def new(self):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'Z':
                    Zombie(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

    def draw(self):
        self.board.surface.fill((128, 128, 128))
        for sprite in self.all_sprites:
            self.board.surface.blit(sprite.image, self.camera.apply(sprite))


if __name__ == "__main__":
    game = TheGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    # game.menu.game_intro()
    game.run("easy")
