# Player sprite
import math
import pygame
import spritesheet
import common
from common import image_folder

class Player(pygame.sprite.Sprite):
    sheet = spritesheet.Spritesheet(
        13, 21, filename=image_folder+"Player-01.png")
    frames_walk_up = sheet.get_frames_in_row(8, end_frame=8)
    frames_walk_left = sheet.get_frames_in_row(9, end_frame=8)
    frames_walk_down = sheet.get_frames_in_row(10, end_frame=8)
    frames_walk_right = sheet.get_frames_in_row(11, end_frame=8)
    walking_speed_normal = 120.0/common.frames_per_second
    walking_speed_fast = 210.0/common.frames_per_second
    walking_speed = walking_speed_normal
    radius = 16  # Collsion radius
    items_set = set()

    def __init__(self, position):
        super().__init__()

        self.action = "STOP"
        self.frame_list = self.frames_walk_down
        self.frame_curr = 0
        self.image = self.frame_list[self.frame_curr]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.frame_change = int(common.frames_per_second / 10)
        self.frame_change_counter = 0
        # Track position as float values for better accuracy
        self.position_x = float(position[0])
        self.position_y = float(position[1])
        self.delta_x = 0
        self.delta_y = 0

    def update(self):
        if self.action != "STOP":
            self.frame_change_counter += 1
            if self.frame_change_counter >= self.frame_change:
                self.frame_change_counter = 0
                self.frame_curr += 1  # Change frame
                if self.frame_curr >= len(self.frame_list):
                    self.frame_curr = 0

                # Update float postion values for better accuracy
                self.position_x += self.delta_x
                self.position_y += self.delta_y
                self.rect.center = [int(self.position_x), int(self.position_y)]
                # self.rect.x += self.delta_x
                # self.rect.y += self.delta_y

        self.image = self.frame_list[self.frame_curr]

    def speed_normal(self):
        if self.walking_speed != self.walking_speed_normal:
            self.walking_speed = self.walking_speed_normal
            # Adjust the current speed deltas
            ratio = self.walking_speed_fast/self.walking_speed_normal
            self.delta_x /= ratio
            self.delta_y /= ratio

    def speed_fast(self):
        if self.walking_speed != self.walking_speed_fast:
            self.walking_speed = self.walking_speed_fast
            # Adjust the current speed deltas
            ratio = self.walking_speed_fast/self.walking_speed_normal
            self.delta_x *= ratio
            self.delta_y *= ratio

    def walk(self, angle):
        self.action = "WALK"
        self.delta_x = math.cos(angle) * self.walking_speed
        self.delta_y = math.sin(angle) * self.walking_speed

        # Determine the best frame set
        self.frame_curr = 0
        if abs(self.delta_x) > abs(self.delta_y):
            if self.delta_x > 0:
                self.frame_list = self.frames_walk_right
            else:
                self.frame_list = self.frames_walk_left
        else:
            if self.delta_y > 0:
                self.frame_list = self.frames_walk_down
            else:
                self.frame_list = self.frames_walk_up

    def do_action(self, action_name):
        if self.action == action_name:
            action_name = "STOP"

        self.action = action_name
        if self.action == "STOP":
            self.frame_curr = 0
            self.delta_x = 0
            self.delta_y = 0
        elif self.action == "RIGHT":
            self.frame_list = self.frames_walk_right
            self.frame_curr = 0
            self.delta_x = self.walking_speed
            self.delta_y = 0
        elif self.action == "LEFT":
            self.frame_list = self.frames_walk_left
            self.frame_curr = 0
            self.delta_x = -self.walking_speed
            self.delta_y = 0
        elif self.action == "DOWN":
            self.frame_list = self.frames_walk_down
            self.frame_curr = 0
            self.delta_x = 0
            self.delta_y = self.walking_speed
        elif self.action == "UP":
            self.frame_list = self.frames_walk_up
            self.frame_curr = 0
            self.delta_x = 0
            self.delta_y = -self.walking_speed
        else:  # Any unknown action forces a STOP
            self.action = "STOP"
            self.frame_curr = 0
            self.delta_x = 0
            self.delta_y = 0

    def has_item(self, name):
        return name in self.items_set

    def add_item(self, name):
        if name in self.items_set:
            return

        self.items_set.add(name)

        if name == "BOOTS":
            self.speed_fast()

    def remove_item(self, name):
        if name not in self.items_set:
            return

        self.items_set.discard(name)

        if name == "BOOTS":
            self.speed_fast()

    def set_position(self, position):
        self.position_x = position[0]
        self.position_y = position[1]
        self.rect.center = [int(self.position_x), int(self.position_y)]

    def scroll_position(self, dx, dy):
        self.position_x += dx
        self.position_y += dy
        self.rect.center = [int(self.position_x), int(self.position_y)]