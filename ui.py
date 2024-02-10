import pygame
import os

pygame.font.init()


class UI:
    def __init__(self, player=pygame.sprite.Sprite()):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.display_map = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]
        self.level_buttons = {}
        self.offset = pygame.math.Vector2(248, 184)
        self.lv_bt_group = pygame.sprite.Group()

        self.get_levels()

    def draw_finish_you_win(self):
        pygame.font.init()
        font = pygame.font.Font('UI/normal.ttf', 25)
        img = font.render('You finished the game!', True, 'black')
        center_x = self.display_surface.get_size()[0] // 2
        center_y = self.display_surface.get_size()[1] // 2
        rect = img.get_rect(center=(center_x, center_y))
        self.display_surface.blit(img, rect)

    def draw_title(self):
        self.draw_text(text='Shooter Bunny Rage Game', pos=(230, 50), size=30, color=(111, 203, 198))
        self.draw_text(text='RAGE GAME', pos=(100, 95), size=30, color=(203, 175, 111))
        self.draw_text(text='WSAD/Space to move/jump, Click/E to shoot, Esc to go to Level Select, Space to continue',
                       size=12, pos=(self.display_surface.get_size()[0] // 2, 380))
        self.draw_text(text='Credits to Kenney and jobromedia from opengameart.org',
                       size=12, pos=(self.display_surface.get_size()[0] // 2, 400))

    def draw_text(self, size=50, color=(0, 0, 0), text='Level select', pos=(0, 0), font='thin'):
        pygame.font.init()
        font = pygame.font.Font(f'UI/{font}.ttf', size)
        img = font.render(text, True, color)
        rect = img.get_rect(center=pos)
        self.display_surface.blit(img, rect)

    def get_levels(self):
        for level in os.listdir('Tilemap'):
            if level.split('.') == [level]:
                button = Button(level[-1])
                self.level_buttons[int(level[-1])] = button
                self.lv_bt_group.add(button)
        button_space = 36 * 2
        for row_index, row in enumerate(self.display_map):
            for col_index, col in enumerate(row):
                x = col_index * button_space + self.offset.x
                y = row_index * button_space + self.offset.y
                self.level_buttons[col].rect.center = (x, y)

    def draw_level_button(self):
        self.draw_text(pos=(320, 100))
        self.lv_bt_group.draw(self.display_surface)
        # self.level_buttons.draw(self.display_surface)

    def draw_story_start(self):
        story = """Once upon a time, there were two rabbits.
        One had a gun, the other had knowledge. 
        They were stuck in a strange land full of critters and obstacles.
        They need to past the levels to get out.
        """.split('\n')
        for index, line in enumerate(story):
            x = self.display_surface.get_width() // 2
            y = index * 20 + 25
            self.draw_text(text=line, pos=(x, y), size=15)

    def draw_story_end(self):
        story = """They fought and fought.
        They went through many obstacles and holes.
        However, they found the ship.
        The ship to freedom, the ship to home.
        And they were gone, coming back only for memories.
        
        THE END
        """.split('\n')
        for index, line in enumerate(story):
            x = self.display_surface.get_width() // 2
            y = index * 20 + 50
            self.draw_text(text=line, pos=(x, y), size=15)


class Button(pygame.sprite.Sprite):
    def __init__(self, level, pos=(100, 100)):
        super().__init__()
        self.image = pygame.image.load('UI/circle.png').convert_alpha()
        font = pygame.font.Font('UI/thin.ttf', 15)
        level_number_img = font.render(level, True, (0, 0, 0))
        self.image.blit(level_number_img, level_number_img.get_rect(center=(18, 18)))
        self.rect = self.image.get_rect(center=pos)
        self.level = level
        self.unlocked = False

    def return_clicked(self):
        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
            else:

                return False
