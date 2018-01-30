#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame as pg
from greebles.tank import Tank
from greebles import level
from greebles.block import Block
from greebles.settings import Settings
from greebles.entity import Entity
from greebles.fly import Fly
from random import randrange
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

settings = Settings(0)


pg.init()

screen_width = 32 * 21
screen_height = 32 * 15
size = (screen_width, screen_height)

screen = pg.display.set_mode(size)

pg.display.set_caption("Greebles Tales!")

sprites = pg.sprite.Group()
blocks = pg.sprite.Group()
players = pg.sprite.Group()
enemies = pg.sprite.Group()

tank = Tank()
tank.rect.x = 33
tank.rect.y = 33

players.add(tank)

fly = Fly()
fly.rect.x = 32*10+1
fly.rect.y = 32*10+1

enemies.add(fly)

sprites = level.make_spiral(int(screen_width/32-2), int(screen_height/32-2), sprites)
#sprites = level.make_maze(int(screen_width/32-2), int(screen_height/32-2), sprites)

for sprite in sprites:
    blocks.add(sprite)

# clean for players
for player in players:
    hits = pg.sprite.spritecollide(player, blocks, False)
    for hit in hits:
        hit.fade()

# clean for enemies
for ennemy in enemies:
    hits = pg.sprite.spritecollide(ennemy, blocks, False)
    for hit in hits:
        hit.fade()


sprites.add(tank)
sprites.add(fly)
# draw border
for i in range(0, screen_width, 32):
    for n in range(0, screen_height, screen_height-32):
        block = Block(True)
        block.rect.y = 0+n
        block.rect.x = i
        blocks.add(block)
        sprites.add(block)
for i in range(0, screen_height, 32):
    for n in range(0, screen_width, screen_width-32):
        block = Block(True)
        block.rect.y = i
        block.rect.x = 0+n
        blocks.add(block)
        sprites.add(block)


pg.display.flip()

done = False
clock = pg.time.Clock()
x_speed = y_speed = 0
slowclock = 0


def is_path_clear(angle, entity):
    if angle is None:
        return True  # no angle, no path
    tank.apply_move(angle, 5)
    hits = pg.sprite.spritecollide(tank, blocks, False)
    result = True
    for hit in hits:
        if blocks.has(hit):
            result = False
    tank.apply_move(angle, -5)
    return result


while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type is pg.QUIT:
            done = True
        if event.type is pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                tank.input.append(90)
            elif event.key == pg.K_RIGHT:
                tank.input.append(270)
            elif event.key == pg.K_UP:
                tank.input.append(0)
            elif event.key == pg.K_DOWN:
                tank.input.append(180)
            elif event.key == pg.K_SPACE:
                # pushing the tank hitbox 5 pixel further for colision check
                tank.apply_move(tank.old_angle, 5)
                hits = pg.sprite.spritecollide(tank, blocks, False)
                if len(hits) > 0:
                    # only take the closest
                    # first compare the hitbox
                    hits[0].journey = 0
                    hits[0].align()
                    block_power = 2
                    hits[0].x_speed, hits[0].y_speed =\
                        Entity.get_move(tank.old_angle, 4+block_power)
                tank.apply_move(tank.old_angle, -5)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                tank.input.remove(90)
            if event.key == pg.K_RIGHT:
                tank.input.remove(270)
            if event.key == pg.K_UP:
                tank.input.remove(0)
            if event.key == pg.K_DOWN:
                tank.input.remove(180)

    screen.fill(NOIR)
    tank.unblocked()
    for block in sprites:
        if players.has(block):
            print(block.get_angle())
            if not is_path_clear(block.get_angle(), block):
                block.blocked()
                while not is_path_clear(block.get_angle(), block):
                    block.blocked()
        if block.update():
            block.remove(sprites)
            hits = pg.sprite.spritecollide(block, sprites, False)
            for hit in hits:
                if enemies.has(block):
                    print("enemy")
                    if block.forced:
                        block.kill()
                    continue
                elif players.has(block):
                    if block.forced:
                        if settings.level > 1:
                            block.kill()
                        print("dead")
                        block.align()
                        block.forced = False
                        block.set_speed((0, 0))
                else:
                    if block.journey is 1:
                        block.fade()
                    elif enemies.has(hit):
                        block.pushing_entity = True
                        hit.force_move(block.x_speed, block.y_speed)
                    elif players.has(hit):
                        # Block is pushing against a player!
                        if not settings.tank_squashable:
                            block.bounce()
                        elif not hit.forced:
                            block.pushing_entity = True
                            hit.force_move(block.x_speed, block.y_speed)
                    else:
                        if not block.pushing_entity:
                            block.bounce()
                        else:
                            block.align()
                            block.pushing_entity = False
            if block.alive():
                block.add(sprites)
    slowclock += 1
    if slowclock == 360:
        slowclock = 0
        x = randrange(len(blocks.sprites()))
        blocks.sprites()[x].fade()
    sprites.draw(screen)
    pg.display.flip()
    if len(players.sprites()) is 0:
        done = True

    clock.tick(60)
