import pygame


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two)


def collide_with_object(self, direction, object_to_collide):
    hits = pygame.sprite.spritecollide(self, object_to_collide, False, collide_hit_rect)
    if direction == 'x':
        if hits:
            if self.vel.x > 0:
                self.position.x = hits[0].rect.left - self.hit_rect.width / 2
            if self.vel.x < 0:
                self.position.x = hits[0].rect.right + self.hit_rect.width / 2
            self.vel.x = 0
            self.hit_rect.centerx = self.position.x
    if direction == 'y':
        if hits:
            if self.vel.y > 0:
                self.position.y = hits[0].rect.top - self.hit_rect.height / 2
            if self.vel.y < 0:
                self.position.y = hits[0].rect.bottom + self.hit_rect.height / 2
            self.vel.y = 0
            self.hit_rect.centery = self.position.y
