import pygame

from support import import_animations, draw_message


class NonPlayableCharacter(pygame.sprite.Sprite):
    def __init__(self, *groups, pos=(0, 250), player=pygame.sprite.Sprite(), message='Do not trust the platforms!'):
        super().__init__(*groups)
        self.sprite_type = 'entity'
        self.image = pygame.transform.scale(pygame.image.load('graphics/npc/0.png'), (32, 32))
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        self.groups = groups
        self.gravity_speed = 0.8
        self.speed = 4





        self.on_ground = False
        self.on_ceiling = False
        self.status = 'idle'
        self.flip = False
        self.player = player
        self.message = message
        self.health = 1000

        # animations
        self.frame = 0
        self.animation_speed = 0.075
        self.animations = import_animations('graphics/npc')

    def apply_gravity(self):
        self.direction.y += self.gravity_speed
        self.rect.y += self.direction.y

    def die(self):
        print(self.health)
        if self.health <= 0:
            self.kill()

    def jump(self):
        self.direction.y = -16

    def interact(self, player):
        if player.rect.colliderect(self.rect):
            draw_message(self.message)

    def animate(self):
        if self.status == 'run':
            self.frame += self.animation_speed
            if self.frame > len(self.animations) - 1:
                self.frame = 0

            surface = self.animations[str(int(self.frame))]
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

            self.status = 'idle'

    def update(self):
        self.die()
        self.interact(self.player)
        self.get_status()
        self.animate()
