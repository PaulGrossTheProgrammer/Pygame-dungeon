# Fireball sprites
import math
import pygame

import common
import spritesheet
from common import image_folder

class DirectedSprite(pygame.sprite.Sprite):
    speed = 4

    def __init__(self, position, distance, angle, sound=None):
        super().__init__()

        self.angle_frames = self.sheet.get_angled_image_list(angle)

        # Track position as float values for better accuracy
        self.position_x = float(position[0])
        self.position_y = float(position[1])

        self.speed *= 60.0/common.frames_per_second
        self.frame_curr = 0
        self.image = self.angle_frames[self.frame_curr]
        self.rect = self.image.get_rect()
        self.rect.center = position
        # self.frame_change_trigger = 5
        self.frame_change_trigger = int(common.frames_per_second / 12)
        self.frame_change_counter = 0
        self.delta_x = math.cos(angle) * self.speed
        self.delta_y = math.sin(angle) * self.speed
        self.distance_end = distance
        self.distance_acc = 0
        self.done = False

    def update(self):
        if self.done is True:
            return

        self.frame_change_counter += 1
        if self.frame_change_counter >= self.frame_change_trigger:
            self.frame_change_counter = 0
            self.frame_curr += 1  # Change frame
            if self.frame_curr >= len(self.angle_frames):
                self.frame_curr = 0

        # Update float postion values for better accuracy
        self.position_x += self.delta_x
        self.position_y += self.delta_y

        self.rect.center = [int(self.position_x), int(self.position_y)]
        self.distance_acc += self.speed
        if self.distance_acc >= self.distance_end:
            self.done = True

        self.image = self.angle_frames[self.frame_curr]

    def set_position(self, position):
        self.position_x = position[0]
        self.position_y = position[1]
        self.rect.center = position

    def scroll_position(self, dx, dy):
        self.position_x += dx
        self.position_y += dy
        self.rect.center = [int(self.position_x), int(self.position_y)]


class FireballRed(DirectedSprite):
    sheet = spritesheet.Spritesheet(
        3, 2, filename=image_folder+"fireball-red.png")
    image_list = sheet.get_frames()
    sheet.create_angled_image_lists(image_list, 32)
    radius = 16

class FireballGreen(DirectedSprite):
    sheet = spritesheet.Spritesheet(
        3, 2, filename=image_folder+"fireball-green.png")
    image_list = sheet.get_frames()
    sheet.create_angled_image_lists(image_list, 32)
    radius = 16

class FireballBlue(DirectedSprite):
    sheet = spritesheet.Spritesheet(
        3, 2, filename=image_folder+"fireball-blue.png")
    image_list = sheet.get_frames()
    sheet.create_angled_image_lists(image_list, 32)
    radius = 16