import pygame
import sys
from level import Level
import asyncio
from ui import UI


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((32 * 20, 32 * 16))
        self.clock = pygame.time.Clock()

        self.level = Level()
        pygame.display.set_caption('THIS IS A RAGE GAME')
        pygame.display.set_icon(pygame.image.load('graphics/player/0.png').convert_alpha())

    async def run(self):
        while True:
            self.screen.fill((252, 223, 205))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            self.level.run()
            self.clock.tick(60)
            pygame.display.flip()
            await asyncio.sleep(0)


if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
