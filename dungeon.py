# Dungeon Play Mechanics
import math
import random
import pygame

import textimage

import common
import dungeontiles
import player
import gemstones
import monsters
import soundeffects
import fireball
import effects
import cursor
import items

displayonly_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
teleporter_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_avatar = None

monster_group = pygame.sprite.Group()
gem_group = pygame.sprite.Group()

cursor = cursor.PlayerCursor()
cursor_group = pygame.sprite.Group()
cursor_group.add(cursor)

fireball_group = pygame.sprite.Group()
effects_group = pygame.sprite.Group()

class StatusScore(pygame.sprite.Sprite):

    font_50 = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    score = 0

    def __init__(self, position):
        super().__init__()
        self.position = position
        self.update_image()

    def add_score(self, points):
        self.score += points
        self.update_image()

    def reset(self):
        self.score = 0
        self.update_image()

    def update_image(self):
        text = "Score: {}".format(self.score)
        self.image = self.font_50.render(text, True, common.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


status_group = pygame.sprite.Group()
score_sprite = StatusScore([common.SCREEN_WIDTH - 150, 20])
status_group.add(score_sprite)

# Calc random bounce for the first sprite away from the second sprite
def bounce(sprite1, sprite2, distance):
    cx = sprite1.rect.center[0]
    cy = sprite1.rect.center[1]
    dx = cx - sprite2.rect.center[0]
    dy = cy - sprite2.rect.center[1]
    bx = 0
    if dx != 0:
        bx = dx/abs(dx) * distance * random.random()
    by = 0
    if dy != 0:
        by = dy/abs(dy) * distance * random.random()

    return [cx+bx, cy+by]

def create_dungeon(text):
    global player_avatar

    gem_positions = []  # The starting positions of gems
    monster_positions = []  # The starting positions of monsters
    player_start_pos = [0, 0]

    lines = text.split("\n")
    reading_map = False
    reading_key = False
    key_dict = {}
    map_row = 0

    teleporter_sources = []
    teleporter_targets = []

    for line in lines:
        if reading_key is False and line.startswith("KEY START"):
            reading_key = True
            continue  # Go to next line

        if reading_key is True:
            if line.startswith("KEY END"):
                reading_key = False
                continue

            # Split the key from the values
            key = line[0]
            values = line[2:]  # FIXME - to end
            value_pairs = values.split(",")
            values_dict = {}
            for pair in value_pairs:
                pair_list = pair.split(":")
                values_dict[pair_list[0]] = pair_list[1]

            key_dict[key] = values_dict

        if reading_map is False and line.startswith("MAP START"):
            reading_map = True
            continue  # Go to next line

        if reading_map is True:
            if line.startswith("MAP END"):
                reading_map = False
                continue

            map_col = 0
            for curr_char in line:

                x = map_col * dungeontiles.tile_size + dungeontiles.tile_size/2
                y = map_row * dungeontiles.tile_size + dungeontiles.tile_size/2

                # Lookup char in key_dict
                if curr_char in key_dict:
                    values_dict = key_dict[curr_char]
                    if values_dict is not None:
                        name = values_dict["name"]
                        if name == "wall":
                            wall_group.add(dungeontiles.WallTile([x, y]))
                        elif name == "exit":
                            items_group.add(items.ExitDoor([x, y]))
                        elif name == "key":
                            items_group.add(items.TreasureChest([x, y]))
                        elif name == "boots":
                            items_group.add(items.MagicBoots([x, y]))
                        elif name == "armour":
                            items_group.add(items.Armour([x, y]))
                        elif name == "player":
                            player_start_pos = x, y
                        elif name == "monster":
                            monster_positions.append([x, y])
                            m = None
                            if "type" in values_dict:
                                monstertype = values_dict["type"]
                                if monstertype == "zombie":
                                    m = monsters.GreenZombie([x, y])
                            else:
                                m = monsters.random_monster([x, y])
                            if m is not None:
                                monster_group.add(m)
                        elif name == "gem":
                            gem_positions.append([x, y])
                        elif name == "teleporter":
                            values_dict["x"] = x
                            values_dict["y"] = y
                            if values_dict["direction"] == "source":
                                teleporter_sources.append(values_dict)
                            elif values_dict["direction"] == "target":
                                teleporter_targets.append(values_dict)

                map_col += 1

            map_row += 1

    player_avatar = player.Player(player_start_pos)
    player_group.add(player_avatar)

    for pos in gem_positions:
        gem_group.add(gemstones.random_gem(pos))

    for m in monster_group:
        m.set_player(player_avatar)

    # Match teleporter sources to destinations
    for source in teleporter_sources:
        # id = source["id"]
        for target in teleporter_targets:
            if target["id"] == source["id"]:
                sx = source["x"]
                sy = source["y"]
                tx = target["x"]
                ty = target["y"]
                dx = tx - sx
                dy = ty - sy
                ts = dungeontiles.TeleportSourceTile([sx, sy], dx, dy)
                teleporter_group.add(ts)
                tt = dungeontiles.TeleportTargetTile([tx, ty])
                displayonly_group.add(tt)

def scroll_dungeon(dx, dy):
    '''Adjust all the dungeon sprite positions relative to the screen'''

    if dx == 0 and dy == 0:
        return  # Exit because there is no adjustment

    for sprite in displayonly_group:
        sprite.scroll_position(dx, dy)
    for sprite in items_group:
        sprite.scroll_position(dx, dy)
    for sprite in player_group:
        sprite.scroll_position(dx, dy)
    for sprite in wall_group:
        sprite.scroll_position(dx, dy)
    for sprite in gem_group:
        sprite.scroll_position(dx, dy)
    for sprite in monster_group:
        sprite.scroll_position(dx, dy)
    for sprite in fireball_group:
        sprite.scroll_position(dx, dy)
    for sprite in effects_group:
        sprite.scroll_position(dx, dy)
    for sprite in teleporter_group:
        sprite.scroll_position(dx, dy)

def center_player():
    '''Ajust the map so that the player sits in the middle of the screen'''

    dx = common.SCREEN_WIDTH/2 - player_avatar.rect.center[0]
    dy = common.SCREEN_HEIGHT/2 - player_avatar.rect.center[1]
    scroll_dungeon(dx, dy)

def start_level():
    global final_effect, score, player_death, level_complete, curr_map, \
        screen_snapshot, have_key

    score_sprite.reset()

    displayonly_group.empty()
    items_group.empty()
    teleporter_group.empty()
    player_group.empty()
    monster_group.empty()
    gem_group.empty()
    fireball_group.empty()
    effects_group.empty()
    wall_group.empty()

    # with open(common.maps_folder+"map_amelie.txt") as f:
    with open(common.maps_folder+curr_map) as f:
        mapdata = f.read()

    create_dungeon(mapdata)
    center_player()

    score = 0
    have_key = False
    screen_snapshot = None
    final_effect = None
    player_death = False
    level_complete = False

# This is a special high-speed function for collision detection
# It is much faster than radius collision detection.
# It makes a block from the radius of each sprite to check distance.
def collide_block_radius(sprite1, sprite2):
    dist_check = sprite1.radius + sprite2.radius
    if abs(sprite1.rect.centerx - sprite2.rect.centerx) > dist_check or \
       abs(sprite1.rect.centery - sprite2.rect.centery) > dist_check:
        return False
    else:
        return True


debug_mode = False
wall = None  # For debugging wall collisions

command_mode = "MOVE"
screen_snapshot = None
final_effect = None  # The effect that displays the cause of the end
player_death = False
level_complete = False
score = 0

# curr_map = "map05a.txt"
curr_map = "map_amelie.txt"
start_level()

def play(events, screen):
    global command_mode, screen_snapshot, debug_mode, wall, final_effect, \
        player_death, level_complete

    game_mode = "DUNGEON"

    scroll_trigger = 280  # Pixel distance from edge that triggers autoscroll

    # Check for mouse and keyboard events
    for event in events:
        if final_effect is None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                    debug_mode = not debug_mode  # Toggle debug mode
                elif event.key == pygame.K_LSHIFT or \
                        event.key == pygame.K_RSHIFT:
                    command_mode = "FIREBALL"
                    cursor.set_mode(command_mode)
                elif event.key == pygame.K_p:
                    game_mode = "PAUSED"
                elif event.key == pygame.K_RIGHT:
                    # Calculate the distance to the left-hand scroll border
                    dx = scroll_trigger - player_avatar.rect.center[0]
                    scroll_dungeon(dx, 0)
                elif event.key == pygame.K_LEFT:
                    # Calculate the distance to the right-hand scroll border
                    left_border = common.SCREEN_WIDTH - scroll_trigger
                    dx = left_border - player_avatar.rect.center[0]
                    scroll_dungeon(dx, 0)
                elif event.key == pygame.K_UP:
                    # Calculate the distance to the bottom scroll border
                    bottom_border = common.SCREEN_HEIGHT - scroll_trigger
                    dy = bottom_border - player_avatar.rect.center[1]
                    scroll_dungeon(0, dy)
                elif event.key == pygame.K_DOWN:
                    # Calculate the distance to the top scroll border
                    dy = scroll_trigger - player_avatar.rect.center[1]
                    scroll_dungeon(0, dy)
                elif event.key == pygame.K_SPACE:
                    center_player()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT or\
                        event.key == pygame.K_RSHIFT:
                    command_mode = "MOVE"
                    cursor.set_mode(command_mode)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dx = event.pos[0] - player_avatar.rect.center[0]
                dy = event.pos[1] - player_avatar.rect.center[1]
                angle = math.atan2(dy, dx)
                if command_mode == "FIREBALL":
                    soundeffects.fireball.play()
                    fb = fireball.FireballRed(
                        player_avatar.rect.center, 600, angle)
                    fireball_group.add(fb)
                elif command_mode == "MOVE":
                    if abs(dx) <= player_avatar.radius and \
                       abs(dy) <= player_avatar.radius:
                        # Clicking on the player means stop
                        player_avatar.do_action("STOP")
                    else:
                        player_avatar.walk(angle)

    # Position the cursor at the mouse pointer
    cursor.set_pos(pygame.mouse.get_pos())

    # Autoscroll the map if required
    scroll_delta = 1
    # X adjust
    if player_avatar.rect.center[0] < scroll_trigger:
        scroll_dungeon(scroll_delta, 0)
    elif player_avatar.rect.center[0] > common.SCREEN_WIDTH - scroll_trigger:
        scroll_dungeon(-scroll_delta, 0)
    # Y adjust
    if player_avatar.rect.center[1] < scroll_trigger:
        scroll_dungeon(0, scroll_delta)
    elif player_avatar.rect.center[1] > common.SCREEN_HEIGHT - scroll_trigger:
        scroll_dungeon(0, -scroll_delta)

    # Update animation
    displayonly_group.update()
    items_group.update()
    player_group.update()
    monster_group.update()
    gem_group.update()
    fireball_group.update()
    effects_group.update()
    cursor_group.update()
    teleporter_group.update()
    status_group.update()

    if final_effect is None:
        # Collisions: player to monster
        player_monster_coll = pygame.sprite.spritecollide(
            player_avatar, monster_group, False,
            collided=pygame.sprite.collide_circle)
        if len(player_monster_coll) > 0:
            final_effect = effects.Vanish(player_avatar.rect.center)
            effects_group.add(final_effect)
            player_death = True
            player_avatar.do_action("STOP")

        # Collisions: player to items
        player_items_coll = pygame.sprite.spritecollide(
            player_avatar, items_group, False,
            collided=pygame.sprite.collide_circle)
        for item in player_items_coll:
            if isinstance(item, items.TreasureChest) and \
                    player_avatar.has_item("KEY") is False:
                effect = effects.SparkleWhite(item.rect.center)
                effects_group.add(effect)
                soundeffects.pickup_5.play()
                item.open()
                player_avatar.add_item("KEY")
            elif isinstance(item, items.MagicBoots):
                effect = effects.Vanish(item.rect.center)
                effects_group.add(effect)
                soundeffects.pickup_4.play()
                items_group.remove(item)
                player_avatar.add_item("BOOTS")
            elif isinstance(item, items.Armour):
                effect = effects.Vanish(item.rect.center)
                effects_group.add(effect)
                soundeffects.pickup_5.play()
                items_group.remove(item)
                player_avatar.add_item("ARMOUR")
            elif isinstance(item, items.ExitDoor):
                if player_avatar.has_item("KEY"):
                    effect = effects.Vanish(item.rect.center)
                    effects_group.add(effect)
                    soundeffects.pickup_1.play()
                    level_complete = True
                    final_effect = effect

    # Collisions: player to gem
    player_gem_coll = pygame.sprite.spritecollide(
        player_avatar, gem_group, True,
        collided=pygame.sprite.collide_circle)
    for gem in player_gem_coll:
        score_sprite.add_score(50)
        gem.play_sound()
        effect = effects.Vanish(gem.rect.center)
        effects_group.add(effect)

    # Collisions: player to teleporter
    player_tele_coll = pygame.sprite.spritecollide(
        player_avatar, teleporter_group, False,
        collided=collide_block_radius)
    for t in player_tele_coll:
        effects_group.add(effects.SparkleBlue(t.rect.center))
        target_x = t.rect.center[0] + t.teleportx
        target_y = t.rect.center[1] + t.teleporty
        target_pos = [target_x, target_y]

        player_avatar.set_position(target_pos)
        effects_group.add(effects.SparkleBlue(target_pos))
        center_player()

    # Collisions: fireball to gem
    fb_gem_coll = pygame.sprite.groupcollide(
        fireball_group, gem_group, True, True,
        collided=pygame.sprite.collide_circle)
    for fb in fb_gem_coll:
        soundeffects.explosion.play()
        effects_group.add(effects.ExplosionRed(fb.rect.center))
        for gem in fb_gem_coll[fb]:
            effects_group.add(effects.Vanish(gem.rect.center))

    # Collisions: fireball to teleporter
    fb_tel_coll = pygame.sprite.groupcollide(
        fireball_group, teleporter_group, False, False,
        collided=collide_block_radius)
    for fb in fb_tel_coll:
        t = fb_tel_coll[fb][0]
        effects_group.add(effects.SparkleBlue(t.rect.center))
        target_x = t.rect.center[0] + t.teleportx
        target_y = t.rect.center[1] + t.teleporty
        target_pos = [target_x, target_y]

        fb.set_position(target_pos)
        effects_group.add(effects.SparkleBlue(target_pos))

    # Collisions: fireball to monster
    fb_monster_coll = pygame.sprite.groupcollide(
        fireball_group, monster_group, True, True,
        collided=pygame.sprite.collide_circle)
    for fb in fb_monster_coll:
        score_sprite.add_score(10)
        soundeffects.explosion.play()
        effects_group.add(effects.ExplosionRed(fb.rect.center))
        for monster in fb_monster_coll[fb]:
            effects_group.add(effects.Vanish(monster.rect.center))

    # Collisions: fireball to walls
    fb_wall_coll = pygame.sprite.groupcollide(
        fireball_group, wall_group, True, False,
        collided=collide_block_radius)
    for fb in fb_wall_coll:
        soundeffects.explosion.play()
        effects_group.add(effects.ExplosionRed(fb.rect.center))

    # Collisions: player to wall
    player_wall_coll = pygame.sprite.spritecollide(
        player_avatar, wall_group, False,
        collided=collide_block_radius)
    if len(player_wall_coll) > 0:
        player_avatar.do_action("STOP")
        wall = player_wall_coll[0]
        newpos = bounce(player_avatar, wall, 3)
        player_avatar.set_position(newpos)

    # Collisions: monster to wall
    monster_wall_coll = pygame.sprite.groupcollide(
        monster_group, wall_group, False, False,
        collided=collide_block_radius)
    for monster in monster_wall_coll:
        wall = monster_wall_coll[monster][0]
        monster.stop()
        newpos = bounce(monster, wall, 3)
        monster.set_position(newpos)

    # Remove completed fireballs
    for sprite in fireball_group:
        if sprite.done is True:
            fireball_group.remove(sprite)
            soundeffects.explosion.play()
            effects_group.add(effects.ExplosionRed(sprite.rect.center))

    # End the game after the final effect
    if final_effect is not None:
        if final_effect.done is True:
            if level_complete is True:
                game_mode = "LEVELCOMPLETE"
            elif player_death is True:
                game_mode = "GAMEOVER"

    # Draw
    screen.fill(common.BLACK)

    # TODO - set dungeon clip
    displayonly_group.draw(screen)
    items_group.draw(screen)
    teleporter_group.draw(screen)
    gem_group.draw(screen)
    player_group.draw(screen)
    monster_group.draw(screen)
    fireball_group.draw(screen)
    effects_group.draw(screen)
    wall_group.draw(screen)

    # TODO - Set status clip and draw status incl. score
    status_group.draw(screen)

    if game_mode != "DUNGEON":
        screen_snapshot = screen.copy()

    # TODO - Remove clip
    cursor_group.draw(screen)

    if debug_mode is True:
        common.debug_sprites_draw(screen, player_group)
        common.debug_sprites_draw(screen, gem_group)
        common.debug_sprites_draw(screen, fireball_group)
        common.debug_sprites_draw(screen, monster_group)
        if wall is not None:
            common.debug_sprite_draw(screen, wall)

    return game_mode

def paused(events, screen):
    global screen_snapshot

    game_mode = "PAUSED"

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            game_mode = "DUNGEON"
            return game_mode
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game_mode = "EXIT"
            return game_mode

    # Update animation
    # Nothing to animate yet ...

    # Draw
    screen.fill(common.BLACK)
    if screen_snapshot is not None:
        screen.blit(screen_snapshot, [0, 0])
    textimage.draw(screen, textimage.pause)

    return game_mode

def levelcomplete(events, screen):
    global screen_snapshot, score

    game_mode = "LEVELCOMPLETE"

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            start_level()
            game_mode = "DUNGEON"
            return game_mode
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game_mode = "EXIT"
            return game_mode

    # Update animation
    # Nothing to animate yet ...

    # Draw
    screen.fill(common.BLACK)
    if screen_snapshot is not None:
        screen.blit(screen_snapshot, [0, 0])

    textimage.draw(screen, textimage.levelcomplete)

    return game_mode

def gameover(events, screen):
    global screen_snapshot

    game_mode = "GAMEOVER"

    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            start_level()
            game_mode = "DUNGEON"
            return game_mode
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            game_mode = "EXIT"
            return game_mode

    # Update animation
    # Nothing to animate yet ...

    # Draw
    screen.fill(common.BLACK)
    if screen_snapshot is not None:
        screen.blit(screen_snapshot, [0, 0])
    textimage.draw(screen, textimage.gameover)

    return game_mode