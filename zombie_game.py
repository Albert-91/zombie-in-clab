import pygame
from random import randint
import math


class Board:

    """Class responsible for drawing window game"""

    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Zombie CLab')
        self.bg = pygame.image.load("images/floor.jpg")

    def draw(self, *args):
        """param args: list of object to draw"""
        background = (255, 255, 255)
        self.surface.fill(background)
        # floor
        floor_width = 223
        for i in range(6):
            x = floor_width * i
            self.surface.blit(self.bg, (x, 0))
            self.surface.blit(self.bg, (x, 226))
            self.surface.blit(self.bg, (x, 452))

        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()


class TheGame:

    counter = 1
    my_width = None
    my_height = None

    """connects all elements"""
    def __init__(self, width, height):
        pygame.init()
        self.get_state = 0
        number_of_zombies = 10
        TheGame.my_width = width
        TheGame.my_height = height
        self.board = Board(width, height)
        # clock to control speed of drawing
        self.fps_clock = pygame.time.Clock()
        self.room = Rooms(0, 0)
        self.player1 = Player(width/2, height/2, 20, 20)
        self.zombie_list = []
        for i in range(number_of_zombies):
            x = randint(Player.my_player_width, int(TheGame.my_width) - Player.my_player_width)
            y = randint(Player.my_player_height, int(TheGame.my_height) - Player.my_player_height)
            self.zombie_person = Zombie(x, y, self.player1, 20, 20)
            self.zombie_list.append(self.zombie_person)

    def run(self):
        """Main loop of game"""
        max_distance = 170
        while True:
            self.handle_events()
            player_rect = pygame.Rect(self.player1)
            """states for moving while each button is pressed"""
            if self.get_state == 1:
                self.player1.move_x(self.player1.max_speed)
            elif self.get_state == 2:
                self.player1.move_x(-self.player1.max_speed)
            elif self.get_state == 3:
                self.player1.move_y(self.player1.max_speed)
            elif self.get_state == 4:
                self.player1.move_y(-self.player1.max_speed)
            for i in range(len(self.zombie_list)):
                zombie_rect = pygame.Rect(self.zombie_list[i])
                room_rect = pygame.Rect(Rooms.wall_lines)
                distance = (self.zombie_list[i].rect.x - self.player1.rect.x)**2 + \
                           (self.zombie_list[i].rect.y - self.player1.rect.y)**2
                distance = math.sqrt(distance)
                if distance > max_distance:
                    self.zombie_list[i].zombie_natural_moves()
                elif distance <= max_distance and not player_rect.colliderect(zombie_rect):
                    self.zombie_list[i].zombie_follows()
                elif player_rect.colliderect(zombie_rect):
                    self.zombie_list[i].zombie_attacks()

                """detection of collisions between zombies"""
                for j in range(len(self.zombie_list)):
                    other_zombie = pygame.Rect(self.zombie_list[j])
                    if i != j and zombie_rect.colliderect(other_zombie):
                        if self.zombie_list[i].rect.x > self.zombie_list[j].rect.x:
                            self.zombie_list[i].move_x(-Zombie.max_speed)
                            self.zombie_list[j].move_x(Zombie.max_speed)
                        else:
                            self.zombie_list[i].move_x(Zombie.max_speed)
                            self.zombie_list[j].move_x(-Zombie.max_speed)
                        if self.zombie_list[i].rect.y > self.zombie_list[j].rect.y:
                            self.zombie_list[i].move_y(-Zombie.max_speed)
                            self.zombie_list[j].move_y(Zombie.max_speed)
                        else:
                            self.zombie_list[i].move_y(Zombie.max_speed)
                            self.zombie_list[j].move_y(-Zombie.max_speed)

            self.board.draw(
                self.room,
                self.player1,
                self.zombie_list[0],
                self.zombie_list[1],
                self.zombie_list[2],
                self.zombie_list[3],
                self.zombie_list[4],
                self.zombie_list[5],
                self.zombie_list[6],
                self.zombie_list[7],
                self.zombie_list[8],
                self.zombie_list[9]

            )
            pygame.display.flip()
            self.fps_clock.tick(100)

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
                    x = self.player1.max_speed
                    self.player1.move_x(x)
                    self.get_state = 1

                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x = self.player1.max_speed
                    self.player1.move_x(-x)
                    self.get_state = 2

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y = self.player1.max_speed
                    self.player1.move_y(y)
                    self.get_state = 3

                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y = self.player1.max_speed
                    self.player1.move_y(-y)
                    self.get_state = 4

            elif event.type == pygame.KEYUP:
                self.get_state = 0

            """uncomment if you want to move by mouse"""
            # if event.type == pygame.MOUSEMOTION:
            #     x, y = event.pos
            #     self.player1.move_x(x)
            #     self.player1.move_y(y)

    def move_cond(self, player, other):
        player_rect = pygame.Rect(player)
        other_rect = pygame.Rect(other)
        if player_rect.colliderect(other_rect):
            pass


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


class Rooms(Drawable):
    wall_lines = None
    def __init__(self, x, y, width=1000, height=600, color=(0, 0, 0)):
        super(Rooms, self).__init__(width, height, x, y, color)
        wall_width = 10
        wall_color = (0, 0, 0)
        wall_corners = [(150, 200), (0, 200), (0, 0), (200, 0), (200, 200), (190, 200), (300, 200), (200, 200),
                        (200, 0), (400, 0), (400, 200), (340, 200), (520, 200), (400, 200), (400, 0), (600, 0),
                        (600, 200), (560, 200), (700, 200), (600, 200), (600, 0), (800, 0), (800, 200), (740, 200),
                        (820, 200), (800, 200), (800, 0), (995, 0), (995, 200), (860, 200), (995, 200), (995, 280)]
        pygame.draw.lines(self.surface, wall_color, False, wall_corners, wall_width)
        Rooms.wall_lines = pygame.draw.lines(self.surface, wall_color, False, wall_corners, wall_width)


class Player(Drawable):

    my_player_width = None
    my_player_height = None
    def __init__(self, x, y, width=20, height=20, color=(0, 0, 255), max_speed=5):
        super(Player, self).__init__(width, height, x, y, color)
        self.max_speed = max_speed
        self.surface.fill(color)
        Player.my_player_width = self.width
        Player.my_player_height = self.height

    def move_x(self, x):
        delta_x = x - self.rect.x
        if abs(delta_x) <= TheGame.my_width - Player.my_player_width and delta_x <= 0:
            delta_x = -self.max_speed
            if x > 0:
                self.rect.x += delta_x
            else:
                self.rect.x -= delta_x

    def move_y(self, y):
        delta_y = y - self.rect.y
        if abs(delta_y) <= TheGame.my_height - Player.my_player_height and delta_y <= 0:
            delta_y = -self.max_speed
            if y > 0:
                self.rect.y += delta_y
            else:
                self.rect.y -= delta_y


class Zombie(Player):
    max_speed = None
    def __init__(self, x, y, victim, width=Player.my_player_width, height=Player.my_player_height,
                 color=(255, 0, 0), max_speed=1):
        super(Player, self).__init__(width, height, x, y, color)
        self.max_speed = max_speed
        self.surface.fill(color)
        self.victim = victim
        Zombie.max_speed = max_speed

    def zombie_natural_moves(self):
        a = randint(0, 1)
        self.move_x(a)
        a = randint(0, 1)
        self.move_y(a)

    def zombie_follows(self):
        if self.rect.x > self.victim.rect.x:
            x = self.max_speed
        else:
            x = - self.max_speed
        self.move_x(x)
        if self.rect.y > self.victim.rect.y:
            y = self.max_speed
        else:
            y = - self.max_speed
        self.move_y(y)

    def zombie_attacks(self):
        pass


if __name__ == "__main__":
    game = TheGame(1000, 600)
    game.run()
