import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, *groups, pos=(0,0), image=pygame.Surface((32,32))):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)