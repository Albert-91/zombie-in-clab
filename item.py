from settings import *


class Item(pygame.sprite.Sprite):

    def __init__(self, game, position, type):
        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = game.items_images[type]
        self.game = game
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = position
