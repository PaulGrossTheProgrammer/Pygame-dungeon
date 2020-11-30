# Item Tiles
import pygame

import common

class ItemSprite(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()

        self.rect.center = position

    def scroll_position(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

class ExitDoor(ItemSprite):
    image = pygame.image.load(common.image_folder+"dngn_exit.png")
    rect = image.get_rect()
    radius = 16

class TreasureChest(ItemSprite):
    image_closed = pygame.image.load(common.image_folder+"chest2_closed.png")
    image_open = pygame.image.load(common.image_folder+"chest2_open.png")
    image = image_closed
    rect = image.get_rect()
    radius = 16

    def open(self):
        self.image = self.image_open

class MagicBoots(ItemSprite):
    image = pygame.image.load(common.image_folder+"boots2_jackboots.png")
    rect = image.get_rect()
    radius = 16

class Armour(ItemSprite):
    image = pygame.image.load(common.image_folder+"ring_mail1.png")
    rect = image.get_rect()
    radius = 16