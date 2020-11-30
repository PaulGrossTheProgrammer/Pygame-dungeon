# Dungeon Tiles
import random
import pygame

import common
import spritesheet

# Load the dungeon tiles spritesheets
frames = []
ss_names = "hyptosis_tile-art-batch-{}.png"
for number in range(1, 5):
    ss = spritesheet.Spritesheet(
        30, 30, filename=common.image_folder+ss_names.format(number))
    frames.append(ss.get_frames())

def get_tile_image(sheet, row, col):
    frame_list = frames[sheet-1]
    image = frame_list[row*30+col]
    return image

# determine tile size from first tile
tile_size = get_tile_image(1, 0, 0).get_rect().width

wall_images = []
wall_images.append(get_tile_image(1, 7, 0))
wall_images.append(get_tile_image(1, 7, 1))
wall_images.append(get_tile_image(1, 7, 2))
wall_images.append(get_tile_image(1, 7, 3))
wall_images.append(get_tile_image(1, 7, 4))
wall_images.append(get_tile_image(1, 8, 3))

class WallTile(pygame.sprite.Sprite):
    radius = 16

    def __init__(self, position):
        super().__init__()
        self.image = random.choice(wall_images)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def scroll_position(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

teleport_source_image = get_tile_image(4, 5, 6)
teleport_target_image = get_tile_image(4, 6, 6)

class TeleportSourceTile(pygame.sprite.Sprite):
    radius = 16

    def __init__(self, position, teleportx, teleporty):
        super().__init__()
        self.image = teleport_source_image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.teleportx = teleportx
        self.teleporty = teleporty

    def scroll_position(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class TeleportTargetTile(pygame.sprite.Sprite):
    radius = 16

    def __init__(self, position):
        super().__init__()
        self.image = teleport_target_image
        self.rect = self.image.get_rect()
        self.rect.center = position

    def scroll_position(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy