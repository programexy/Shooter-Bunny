import pygame
from math import *
from support import import_animations


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups, pos=(0, 250), obstacle_sprites=pygame.sprite.Group()):
        super().__init__(*groups)
        self.sprite_type = 'entity'
        self.image = pygame.transform.scale(pygame.image.load('graphics/player/0.png'), (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.groups = groups
        self.gravity_speed = 0.8
        self.speed = 4
        self.on_ground = False
        self.on_ceiling = False
        self.status = 'idle'
        self.flip = False
        self.dead = False
        self.frame = 0
        self.animation_speed = 0.075
        self.animations = import_animations('graphics/player')
        self.shooting = False
        self.ammo = []
        self.max_ammo = 2
        self.reload = False
        self.reload_time = 0
        self.reload_length = 1000
        self.health = 1000
        self.full_health = 1000
        self.interact = False

    def apply_gravity(self):
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = -16

    def animate(self):
        if self.status == 'run':
            self.frame += self.animation_speed
            if self.frame > len(self.animations) - 1:
                self.frame = 0

            surface = self.animations[str(int(self.frame))]
            image = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        elif self.status == 'shoot':
            surface = self.animations['shoot']
            image = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        else:
            surface = self.animations['0']
            image = pygame.transform.scale(surface, (surface.get_width() * 2, surface.get_height() * 2))
        self.image = pygame.transform.flip(image, self.flip, False)

    def get_status(self):
        if self.direction.x > 0:
            self.flip = False
        elif self.direction.x < 0:
            self.flip = True
        if abs(self.direction.x) > 0:
            # print(True)
            self.status = 'run'
        else:
            if self.shooting:
                self.status = 'shoot'
            else:
                self.status = 'idle'
        if self.health <= 0:
            self.dead = True

    def fire(self):
        current_time = pygame.time.get_ticks()
        if self.max_ammo > 0:
            self.ammo.append(Bullet(self.groups, player=self))
            self.max_ammo -= 1
            print(self.max_ammo)
        elif self.max_ammo <= 0 and not self.reload:
            self.max_ammo = -5
            self.reload_time = pygame.time.get_ticks()
            self.reload = True

        if self.reload and current_time - self.reload_time >= self.reload_length:
            self.max_ammo = 2
            self.reload = False
            print(self.max_ammo)



    def move_bullet(self):
        for bullet in self.ammo:
            bullet.move()

    def update(self):
        self.move_bullet()
        self.get_status()
        self.animate()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, *groups, player=None):
        super().__init__(*groups)
        self.image = pygame.transform.flip(pygame.image.load('graphics/tiles/20.png').convert_alpha(), player.flip,
                                           False)

        self.player = player
        self.angle = 0
        self.fire()

        # print(self.direction)
        self.life_span = 13


    def fire(self):
        self.flip = self.player.flip

        mouse_x, mouse_y = pygame.mouse.get_pos()



        distance_x = mouse_x - pygame.display.get_surface().get_width()//2
        distance_y = mouse_y - pygame.display.get_surface().get_height()//2
        self.angle = atan2(distance_y, distance_x)
        self.image = pygame.transform.rotozoom(self.image, degrees(self.angle)+180, 3)
        if self.flip:
            rect = self.image.get_rect(topright=self.player.rect.midleft)
        else:
            rect = self.image.get_rect(topleft=self.player.rect.midright)

        self.rect = rect

        # speed_x, speed_y can be `float` but I don't convert to `int` to get better position

    def move(self):
        speed = 30
        self.rect.centerx += cos(self.angle)*speed
        self.rect.centery += sin(self.angle)*speed
        if self.life_span > 0:
            self.life_span -= 1
        else:
            self.kill()
