import pytmx

from zombie_game.settings import *


class Camera:

    def __init__(self, game, width, height):
        self.width = width
        self.height = height
        self.game = game
        self.screen = pg.Rect(0, 0, self.width, self.height)

    def apply(self, entity):
        return entity.rect.move(self.screen.topleft)

    def apply_rect(self, rect):
        return rect.move(self.screen.topleft)

    def update(self, target):
        x, y = self._get_target_coordinates(target)
        self.screen = pg.Rect(x, y, self.width, self.height)

    def _get_target_coordinates(self, target):
        x = -target.rect.centerx + int(self.game.width / 2)
        y = -target.rect.centery + int(self.game.height / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - self.game.width), x)
        y = max(-(self.height - self.game.height), y)
        return x, y


class TiledMap:

    def __init__(self, filename):
        self.tmxdata = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
