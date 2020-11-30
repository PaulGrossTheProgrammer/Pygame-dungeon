# Dungeon game

import pygame

import common
import dungeon

screen = pygame.display.get_surface()

# The clock manages how fast the game updates
clock = pygame.time.Clock()

pygame.display.set_caption('Dungeon Game')

pygame.mouse.set_visible(False)

# pygame.mixer.music.play(-1)  # Play background music loop - disabled

game_mode = "DUNGEON"

game_on = True
while game_on:
    # Check for mouse and keyboard events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            print("User closed the game window")
            game_on = False

    if game_mode == "DUNGEON":
        next_game_mode = dungeon.play(events, screen)
    elif game_mode == "PAUSED":
        next_game_mode = dungeon.paused(events, screen)
    elif game_mode == "LEVELCOMPLETE":
        next_game_mode = dungeon.levelcomplete(events, screen)
    elif game_mode == "GAMEOVER":
        next_game_mode = dungeon.gameover(events, screen)

    game_mode = next_game_mode

    if game_mode == "EXIT":
        game_on = False

    pygame.display.flip()

    clock.tick(common.frames_per_second)

pygame.quit()
quit()