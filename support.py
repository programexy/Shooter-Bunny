import pygame
import os
import csv


def import_csv_layout(path):
    layouts = {}
    for level in os.listdir(path):
        if level.split('.')[-1] == 'csv':
            layout = []
            with open(path + '/' + level) as file:
                data = csv.reader(file, delimiter=',')
                for row in data:
                    layout.append(row)
                layouts[level.split('_')[-1].split('.')[0]] = layout
    return layouts


def import_animations(path):
    images = {}
    for image in os.listdir(path):
        if image.split('.')[-1] == 'png':
            surface = pygame.image.load(path + '/' + image).convert_alpha()
            images[image.replace('.png', '')] = surface
    return images


def draw_message(message='message', pos=(0, 32 * 14), size=(32 * 20, 32 * 2), name='Pixil'):
    box = pygame.Surface(size)
    box.fill('gray')
    pygame.font.init()
    font = pygame.font.Font('UI/thin.ttf', 15)
    name = font.render(name+':', False, (0,0,0))

    x = pos[0] + 4
    y = pos[1] + 20
    length = 0
    pygame.display.get_surface().blit(box, pos)
    for index, character in enumerate(list(message)):
        surface_per_char = font.render(character, False, (255, 233, 173))
        pygame.display.get_surface().blit(surface_per_char, (x + length, y))
        pygame.display.get_surface().blit(name, (pos[0] + 4, pos[1] + 2))
        length += surface_per_char.get_width() + 1
