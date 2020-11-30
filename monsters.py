# Monsters
import math
import random
import pygame
import spritesheet
import common
from common import image_folder

class Monster(pygame.sprite.Sprite):

    player = None  # Set this so that the monster can react to the player
    radius = 20
    speed = 1.0
    frame_change_trigger = 18

    def __init__(self, position):
        super().__init__()

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.speed *= 60.0/common.frames_per_second

        # Track position as float values for better accuracy
        self.position_x = float(position[0])
        self.position_y = float(position[1])
        self.delta_x = 0.0
        self.delta_y = 0.0

        # Spritesheet animation
        # Start the monster on a random frame
        self.frame_curr = random.randrange(len(self.frames) - 1)
        self.frame_change_counter = 0

        # The monster makes decsions when triggered
        self.decision_trigger = 60
        self.decision_counter = 0

    def update(self):
        self.frame_change_counter += 1
        if self.frame_change_counter >= self.frame_change_trigger:
            self.frame_change_counter = 0
            self.frame_curr += 1  # Change frame
            if self.frame_curr >= len(self.frames):
                self.frame_curr = 0
        self.image = self.frames[self.frame_curr]

        # Update float postion values for better accuracy
        self.position_x += self.delta_x
        self.position_y += self.delta_y
        self.rect.center = [int(self.position_x), int(self.position_y)]

        # If the player is set, attack the player
        if self.player is not None:
            # Periodically trigger decisions
            self.decision_counter += 1
            if self.decision_counter >= self.decision_trigger:
                self.decision_counter = 0

                # ---MONSTER ARTIFICAL INTELLIGENCE ---
                dx = self.player.rect.center[0] - self.rect.center[0]
                dy = self.player.rect.center[1] - self.rect.center[1]
                action = random.choice(["DIRECT", "XAXIS", "YAXIS"])
                if action == "DIRECT":
                    angle = math.atan2(dy, dx)
                    self.delta_x = math.cos(angle) * self.speed
                    self.delta_y = math.sin(angle) * self.speed
                elif action == "XAXIS":
                    self.delta_x = self.speed
                    self.delta_y = 0
                    if dx < 0:
                        self.delta_x = -self.delta_x
                elif action == "YAXIS":
                    self.delta_x = 0
                    self.delta_y = self.speed
                    if dy < 0:
                        self.delta_y = -self.delta_y

    def set_player(self, player):
        self.player = player

    def stop(self):
        self.delta_x = 0
        self.delta_y = 0

    def set_position(self, position):
        self.position_x = position[0]
        self.position_y = position[1]
        self.rect.center = position

    def scroll_position(self, dx, dy):
        self.position_x += dx
        self.position_y += dy
        self.rect.center = [int(self.position_x), int(self.position_y)]

class PurplePeopleEater(Monster):
    sheet = spritesheet.Spritesheet(
        4, 1, filename=image_folder+"PurplePeopleEater-02.png")
    frames = sheet.get_frames()

    radius = 20
    speed = 1.3

class GreenZombie(Monster):
    sheet = spritesheet.Spritesheet(
        3, 1, filename=image_folder+"Zombie.png")
    frames = sheet.get_frames()

    radius = 12
    speed = 0.5

class BlueGhost(Monster):
    sheet = spritesheet.Spritesheet(
        28, 1, filename=image_folder+"sGhost_strip28.png")
    frames = sheet.get_frames()

    radius = 10
    speed = 1.8
    frame_change_trigger = 3


random_list = [PurplePeopleEater, GreenZombie, BlueGhost]

def random_monster(position):
    return random.choice(random_list)(position)