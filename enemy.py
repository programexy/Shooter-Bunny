from math import dist

import pygame

from support import import_animations


class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups, pos=(0, 0), gravity=0, mob='bee'):
        super().__init__(*groups)
        self.image = pygame.Surface((32, 32))
        self.sprite_type = 'entity'
        self.mob = mob
        self.rect = self.image.get_rect(topleft=pos)
        self.gravity_speed = gravity
        self.direction = pygame.math.Vector2()
        self.frame = 0
        self.animation_speed = 0.075
        self.flip = False
        self.animations = import_animations(f'graphics/{mob}')
        self.speed = 1
        self.health = 10
        self.on_ground = False
        self.on_ceiling = False

    def animate(self):
        self.frame += self.animation_speed
        if self.frame > len(self.animations):
            self.frame = 0

        surface = self.animations[str(int(self.frame))]
        image = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        self.image = pygame.transform.flip(image, self.flip, False)

    def apply_gravity(self):
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y

    def update(self):
        self.animate()

    def ai(self, player):
        if dist(player.rect.center, self.rect.center) < 200:
            if player.rect.centerx > self.rect.centerx:
                self.rect.centerx += self.speed
                self.flip = False
            elif player.rect.centerx < self.rect.centerx:
                self.rect.centerx -= self.speed
                self.flip = True

            if player.rect.centery > self.rect.centery:
                self.rect.centery += self.speed
            elif player.rect.centery < self.rect.centery:
                self.rect.centery -= self.speed

        if self.health <= 0:
            self.kill()

class Explosives(pygame.sprite.Sprite):
    def __init__(self, *groups, pos=(0,0)):
        super().__init__(*groups)
        self.image = pygame.image.load('graphics/explosion/0.png')
        self.rect = self.image.get_rect(center=pos)
        self.frame = 0
        self.animation_speed = 0.15
        self.animations = import_animations('graphics/explosion')

    def animate(self):
        self.frame += self.animation_speed
        if self.frame > len(self.animations):
            self.kill()
            self.frame = 0

        surface = self.animations[str(int(self.frame))]
        self.image = pygame.transform.scale(surface, (surface.get_width()*3/4, surface.get_height()*3/4))
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.animate()