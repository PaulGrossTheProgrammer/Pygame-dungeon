import pygame

import common

pause_text = "Press P to Resume, X to exit"
gameover_text = "GAMEOVER: Press R to Restart, X to exit"
levelcomplete_text = "LEVEL COMPLETE: Press R to Restart, X to exit"

message_font_50 = pygame.font.SysFont(pygame.font.get_default_font(), 50)

pause = message_font_50.render(pause_text, True, common.WHITE)
gameover = message_font_50.render(gameover_text, True, common.WHITE)
levelcomplete = message_font_50.render(levelcomplete_text, True, common.WHITE)

def draw(screen, image, position=None):
    rect = image.get_rect()
    if position is None:
        # TODO: Cetnter on the screen's current dimensions
        # rect.center = [common.SCREEN_WIDTH/2, common.SCREEN_HEIGHT/2]
        rect.center = [screen.get_width()/2, screen.get_height()/2]

    screen.blit(image, rect)

def drawtext(screen, text, size=None, color=None, position=None):
    global message_font_50

    if size is None:
        font = message_font_50
    else:
        font = pygame.font.SysFont(pygame.font.get_default_font(), size)

    if color is None:
        color = common.WHITE

    image = font.render(text, True, color)

    draw(screen, image, position)