import pygame
from random import randint
import math


class Board:
    """Class responsible for drawing window game"""

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Zombie in CLab')
        self.bg = pygame.image.load("images/terrain_atlas.png")
        self.intro_bg = pygame.image.load("images/floor.jpg")
        menu_font_path = pygame.font.match_font('arial', bold=1)
        self.menu_font = pygame.font.Font(menu_font_path, 45)
        self.options_font = pygame.font.Font(menu_font_path, 65)
        self.title_font = pygame.font.Font(menu_font_path, 90)

    def draw(self, *args):
        """param args: list of object to draw"""
        background = (255, 255, 255)
        self.surface.fill(background)
        self.surface.blit(self.bg, (200, 200), (0, 0, 90, 150))

        for drawable in args:
            drawable.draw_on(self.surface)


    def draw_menu(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)

        self.surface.blit(self.intro_bg, (0, 0), (0, 0, 200, 200))
        self.draw_text(self.surface, "Zombie in CLab", TheGame.game_width / 2, TheGame.game_height * 0.3,
                       self.title_font)
        self.draw_text(self.surface, "Play", TheGame.game_width / 2, TheGame.game_height * 0.6, self.menu_font)
        self.draw_text(self.surface, "Options", TheGame.game_width / 2, TheGame.game_height * 0.7, self.menu_font)
        self.draw_text(self.surface, "Quit", TheGame.game_width / 2, TheGame.game_height * 0.8, self.menu_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()

    def draw_options(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        self.surface.blit(self.intro_bg, (0, 0), (0, 0, 200, 200))
        self.draw_text(self.surface, "Controls", TheGame.game_width / 2, TheGame.game_height * 0.35, self.options_font)
        self.draw_text(self.surface, "Audio", TheGame.game_width / 2, TheGame.game_height * 0.5, self.options_font)
        self.draw_text(self.surface, "Return", TheGame.game_width / 2, TheGame.game_height * 0.65, self.options_font)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()

    @staticmethod
    def draw_text(surface, text, x, y, font):
        text = font.render(text, True, (255, 0, 0))
        rect = text.get_rect()
        rect.center = x, y
        surface.blit(text, rect)


class TheGame:

    game_width = None
    game_height = None

    """connecting all elements"""

    def __init__(self, width, height):
        pygame.init()
        pygame.key.set_repeat(50, 25)
        self.set_bullet_angle = 180
        self.turn_to_shoot = "down"
        TheGame.game_width = width
        TheGame.game_height = height
        self.number_of_zombies = 20
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.room = Rooms(0, 0)
        self.player = Player(width / 2, height / 2, 26, 26)
        self.zombie_group = pygame.sprite.Group()
        self.all_sprites_group = pygame.sprite.Group()
        self.other_group = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites_group.add(self.player)
        for i in range(self.number_of_zombies):
            x = randint(self.player.get_width, TheGame.game_width - self.player.get_width)
            y = randint(self.player.get_height, TheGame.game_height - self.player.get_height)
            self.zombie_person = Zombie(x, y, self.player, self.player.get_width - 6, self.player.get_height - 6)
            self.zombie_group.add(self.zombie_person)
            self.other_group.add(self.zombie_person)
            self.all_sprites_group.add(self.zombie_person)


    def game_intro(self):
        intro = True
        i = 0.58
        while intro:
            mark_play_pos = 0.58
            mark_quit_pos = 0.77
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.38
            color = (255, 0, 0)
            intro_object = Player(mark_pos_x, mark_pos_y, 26, 26, color)
            intro_object.filling(color)
            self.board.draw_menu(intro_object)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if i > mark_play_pos:
                            i -= 0.1

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_play_pos <= i <= mark_quit_pos:
                            i += 0.1

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if i <= mark_play_pos:
                            intro = False
                            game.run()
                        elif i >= mark_quit_pos:
                            pygame.quit()
                        else:
                            game.game_options()

            pygame.display.flip()
            self.fps_clock.tick(100)

    def game_options(self):
        option = True
        i = 0.325
        while option:
            mark_up_opt_pos = 0.325
            mark_down_opt_pos = 0.625
            mark_pos_y = TheGame.game_height * i
            mark_pos_x = TheGame.game_width * 0.32
            color = (255, 0, 0)
            intro_object = Player(mark_pos_x, mark_pos_y, 30, 30, color)
            intro_object.filling(color)
            self.board.draw_options(intro_object)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        option = False
                        game.game_intro()
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if i > mark_up_opt_pos:
                            """without multiplying and dividing by 1000, i in top position has 0.324(9)"""
                            i *= 1000
                            i -= 0.15 * 1000
                            i /= 1000

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if mark_up_opt_pos <= i < mark_down_opt_pos:
                            i += 0.15

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if i == mark_up_opt_pos:
                            """controlls"""
                            pass
                        elif i >= mark_down_opt_pos:
                            game.game_intro()
                        else:
                            """audio"""
                            pass

            pygame.display.flip()
            self.fps_clock.tick(100)

    def run(self):
        """Main loop of game"""
        max_distance = 170
        a = 0
        while True:
            self.handle_events()
            for self.zombie_person in self.zombie_group:
                distance = (self.zombie_person.rect.x - self.player.rect.x) ** 2 + \
                           (self.zombie_person.rect.y - self.player.rect.y) ** 2
                distance = math.sqrt(distance)
                if distance > max_distance:
                    self.zombie_person.zombie_natural_moves()
                elif distance <= max_distance and not pygame.sprite.collide_rect(self.zombie_person, self.player):
                    self.zombie_person.zombie_follows()
                else:
                    self.zombie_person.zombie_attacks()

                for other_zombie in self.other_group:
                    if other_zombie != self.zombie_person and \
                            pygame.sprite.collide_rect(self.zombie_person, other_zombie):
                        if other_zombie.rect.x > self.zombie_person.rect.x:
                            other_zombie.move_x(-self.zombie_person.max_speed)
                            self.zombie_person.move_x(self.zombie_person.max_speed)
                        else:
                            other_zombie.move_x(self.zombie_person.max_speed)
                            self.zombie_person.move_x(-self.zombie_person.max_speed)
                        if other_zombie.rect.y > self.zombie_person.rect.y:
                            other_zombie.move_y(-self.zombie_person.max_speed)
                            self.zombie_person.move_y(self.zombie_person.max_speed)
                        else:
                            other_zombie.move_y(self.zombie_person.max_speed)
                            self.zombie_person.move_y(-self.zombie_person.max_speed)

            self.board.draw(self.room)
            self.player.animation()
            self.all_sprites_group.update(self.turn_to_shoot)
            self.all_sprites_group.draw(self.board.surface)
            self.bullets.update(self.turn_to_shoot)
            pygame.sprite.groupcollide(self.zombie_group, self.bullets, True, True)
            pygame.display.flip()
            self.fps_clock.tick(50)

    @property
    def get_zombie(self):
        return self.zombie_group

    def handle_events(self):
        """handling the system events, like keyboard buttons or quit the game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return True

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.player.move_x(self.player.get_speed)
                    self.set_bullet_angle = 90

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.player.move_x(-self.player.get_speed)
                    self.set_bullet_angle = 270

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.player.move_y(self.player.get_speed)
                    self.set_bullet_angle = 0

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.player.move_y(-self.player.get_speed)
                    self.set_bullet_angle = 180

                if event.key == pygame.K_SPACE:
                    self.all_sprites_group.add(self.player.shoot(self.set_bullet_angle))
                    self.bullets.add(self.player.shoot(self.set_bullet_angle))


class Drawable:

    def __init__(self, width, height, x, y, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self.surface = pygame.Surface.convert_alpha(self.surface)
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Rooms(Drawable, pygame.sprite.Sprite):
    wall_lines = None

    def __init__(self, x, y, width=1000, height=600, color=(0, 0, 0)):
        super(Rooms, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        wall_width = 10
        wall_color = (0, 0, 0)
        wall_corners = [(150, 200), (0, 200), (0, 0), (200, 0), (200, 200), (190, 200), (300, 200), (200, 200),
                        (200, 0), (400, 0), (400, 200), (340, 200), (520, 200), (400, 200), (400, 0), (600, 0),
                        (600, 200), (560, 200), (700, 200), (600, 200), (600, 0), (800, 0), (800, 200), (740, 200),
                        (820, 200), (800, 200), (800, 0), (995, 0), (995, 200), (860, 200), (995, 200), (995, 280)]
        pygame.draw.lines(self.surface, wall_color, False, wall_corners, wall_width)
        Rooms.wall_lines = pygame.draw.lines(self.surface, wall_color, False, wall_corners, wall_width)


class Player(Drawable, pygame.sprite.Sprite):

    def __init__(self, x, y, width=20, height=20, color=(0, 0, 255), max_speed=4, angle=180):
        super(Player, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.angle = angle
        self.image = self.surface
        self.width = width
        self.height = height
        self.rect = self.image.get_rect(x=x, y=y)
    
    def filling(self, color):
        self.image.fill(color)

    def animation(self, angle=0):
        self.image_im = pygame.image.load('images/character.png').convert_alpha(self.image)
        self.image.blit(self.image_im, (0, 0), (14, 9, 33, 39))
        self.image_im = pygame.transform.scale(self.image_im, (self.width, self.height))
    
    @property
    def get_speed(self):
        return self.max_speed

    @property
    def get_width(self):
        return self.width

    @property
    def get_height(self):
        return self.height

    @property
    def get_angle(self):
        return self.angle

    def move_x(self, x):
        if x != 0:
            delta_x = x - self.rect.x
            if abs(delta_x) <= TheGame.game_width - self.width and delta_x <= 0:
                delta_x = -self.max_speed
                if x > 0:
                    self.rect.x += delta_x
                else:
                    self.rect.x -= delta_x

    def move_y(self, y):
        if y != 0:
            delta_y = y - self.rect.y
            if abs(delta_y) <= TheGame.game_height - self.height and delta_y <= 0:
                delta_y = -self.max_speed
                if y > 0:
                    self.rect.y += delta_y
                else:
                    self.rect.y -= delta_y

    def shoot(self, angle):
        bullet = Bullet(self.rect.centerx, self.rect.centery, angle)
        return bullet


class Bullet(Player, pygame.sprite.Sprite):

    bullet_img = pygame.image.load("images/bullet.png")

    def __init__(self, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.width = 5
        self.height = 10
        self.angle = angle
        self.image = pygame.Surface((self.width, self.height))
        self.image = Bullet.bullet_img
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.max_speed = 5

    def update(self, direction):
        if self.angle == 180:
            self.rect.y += self.max_speed
        elif self.angle == 0:
            self.rect.y -= self.max_speed
        elif self.angle == 270:
            self.rect.x += self.max_speed
        elif self.angle == 90:
            self.rect.x -= self.max_speed
        # kill if it moves off the top of the screen
        if self.rect.top < 0 or\
           self.rect.bottom > TheGame.game_height or \
           self.rect.right > TheGame.game_width or\
           self.rect.left < 0:
            self.kill()


class Zombie(Player, pygame.sprite.Sprite):

    def __init__(self, x, y, victim, width, height, color=(255, 0, 0), max_speed=1):
        super(Player, self).__init__(width, height, x, y, color)
        pygame.sprite.Sprite.__init__(self)
        self.max_speed = max_speed
        self.image = self.surface
        self.image.fill(color)
        self.rect = self.image.get_rect(x=x, y=y)
        self.victim = victim

    def zombie_natural_moves(self):
        moves_list = [0, 0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, 0, 0]
        a = randint(0, len(moves_list) - 1)
        self.move_x(moves_list[a])
        a = randint(0, len(moves_list) - 1)
        self.move_y(moves_list[a])

    def zombie_follows(self):
        if self.rect.x > self.victim.rect.x:
            x = self.max_speed
        else:
            x = -self.max_speed
        self.move_x(x)
        if self.rect.y > self.victim.rect.y:
            y = self.max_speed
        else:
            y = -self.max_speed
        self.move_y(y)

    def zombie_attacks(self):
        pass


if __name__ == "__main__":
    game = TheGame(1000, 600)
    game.game_intro()
    #game.run()

