#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame as pg
from greebles.tank import Tank
from greebles import level
from greebles.block import Block
from greebles.settings import Settings
from greebles.entity import Entity
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

tank = Tank()
tank.rect.x = 33
tank.rect.y = 33

players.add(tank)

#sprites = level.make_spiral(int(screen_width/32-2), int(screen_height/32-2), sprites)
sprites = level.make_maze(int(screen_width/32-2), int(screen_height/32-2), sprites)

for sprite in sprites:
    blocks.add(sprite)

sprites.add(tank)
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


while not done:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type is pg.QUIT:
            done = True
        if event.type is pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                tank.set_speed(x_speed=-2)
                tank.rotate(90)
            elif event.key == pg.K_RIGHT:
                tank.set_speed(x_speed=2)
                tank.rotate(270)
            elif event.key == pg.K_UP:
                tank.set_speed(y_speed=-2)
                tank.rotate(0)
            elif event.key == pg.K_DOWN:
                tank.rotate(180)
                tank.set_speed(y_speed=2)
            elif event.key == pg.K_SPACE:
                # pushing the tank hitbox 5 pixel further for colision check
                tank.apply_move(tank.old_angle, 5)
                hits = pg.sprite.spritecollide(tank, blocks, False)
                if len(hits) > 0:
                    # only take the closest
                    # first compare the hitbox
                    hits[0].journey = 0
                    hits[0].align()
                    speed = hits[0].x_speed + hits[0].y_speed
                    hits[0].x_speed, hits[0].y_speed =\
                        Entity.get_move(tank.old_angle, 4+speed)
                tank.apply_move(tank.old_angle, -5)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                tank.set_speed(0, tank.y_speed)
            elif event.key == pg.K_UP or event.key == pg.K_DOWN:
                tank.set_speed(tank.x_speed, 0)

    if tank.y_speed is 2 and abs(tank.x_speed) is 0:
        tank.rotate(180)
    if tank.y_speed is -2 and abs(tank.x_speed) is 0:
        tank.rotate(0)
    if tank.x_speed is 2 and abs(tank.y_speed) is 0:
        tank.rotate(270)
    if tank.x_speed is -2 and abs(tank.y_speed) is 0:
        tank.rotate(90)

    screen.fill(NOIR)
    for block in sprites:
        if block.update():
            block.remove(sprites)
            hits = pg.sprite.spritecollide(block, sprites, False)
            for hit in hits:
                if players.has(block):
                    if block.forced:
                        if settings.level > 1:
                            block.kill()
                        print("dead")
                        block.align()
                        block.forced = False
                        block.set_speed(0, 0)
                        block.rotate(0)
                    else:
                        print("frame")
                        for angle in range(0, 360, 90):
                            tank.apply_move(angle, 2)
                            angle_hits = pg.sprite.spritecollide(tank, pg.sprite.GroupSingle(hit), False,pg.sprite.collide_rect_ratio(0.9))
                            if len(angle_hits) > 0:
                                print(angle)
                                if angle == 0 or angle == 180:
                                    tank.rect.y -= tank.y_speed
                                else:
                                    tank.rect.x -= tank.x_speed
                                tank.apply_move(angle, -2)
                                break
                            tank.apply_move(angle, -2)

                else:
                    if block.journey is 1:
                        block.fade()
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
