#!/usr/bin/env xython
# -*- coding: utf-8 -*-
""" handle level generation. """
from random import shuffle, randrange
from greebles.block import Block
from itertools import cycle

blocks = []


def add_block(x, y):
    block = Block()
    block.rect.y = 32+y*32
    block.rect.x = 32+x*32
    return block


def add_to_sprites(blocks, sprites):
    for x in blocks:
        for y in x:
            if y is not None:
                sprites.add(y)
    return sprites


def init_blocks(w, h):
    return [[add_block(x, y) for y in range(h)] for x in range(w)]


def make_spiral(w, h, sprites):
    """Make a sxriral"""

    blocks = init_blocks(w, h)
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    directions_loop = cycle(directions)
    count_x = w
    count_y = h
    x = 0
    y = 0

    def walk_inv_hori(x, y, count):
        # print("inv hori", x, y, count, w-count)
        i = x
        for _ in range(count):
            blocks[i][y] = None
            i -= 1
        return i+1, y

    def walk_inv_vert(x, y, count):
        # print("inv vert", x, y, count, h)
        i = y
        for _ in range(count):
            blocks[x][i] = None
            i -= 1
        return x, i+1

    def walk_hori(x, y, count):
        # print("hori", x, y, count)
        i = x
        for _ in range(count):
            blocks[i][y] = None
            i += 1
        return i-1, y

    def walk_vert(x, y, count):
        # print("vert", x, y, count)
        i = y
        for _ in range(count):
            blocks[x][i] = None
            i += 1

        return x, i-1

    count_d = 0
    max_count = 3
    while count_x > 0 and count_y > 0:
        direction = next(directions_loop)
        if direction[0] is not 0:
            if direction[0] < 0:
                x, y = walk_inv_hori(x, y, count_x)
            else:
                x, y = walk_hori(x, y, count_x)
        else:
            if direction[1] < 0:
                x, y = walk_inv_vert(x, y, count_y)
            else:
                x, y = walk_vert(x, y, count_y)

        count_d += 1
        if count_d is max_count:
            count_x -= 2
            count_y -= 2
            count_d = 0
            max_count = 2

    return add_to_sprites(blocks, sprites)


def make_line(w, h, sprites):
    blocks = init_blocks(w, h)
    x = 0
    reverse = True
    while x < len(blocks):
        for y in range(len(blocks[x])):
            blocks[x][y] = None
        x += 1
        if x < len(blocks):
            if reverse:
                y = -1
            else:
                y = 0
            blocks[x][y] = None
        x += 1
        reverse = not reverse

    return add_to_sprites(blocks, sprites)


def make_maze(w, h, sprites):
    """
    Generate a maze with a given height and screen_width.

    shameless stolen from wikipedia.
    """
    blocks = init_blocks(w, h)
    complexity = 0.5
    density = 0.7
    shape = ((w // 2) * 2+1, (h // 2) * 2+1)
    # Adjust complexity and density relative to maze size
    complexity = int(complexity * (5 * (shape[0] + shape[1])))
    density = int(density * ((shape[0] // 2) * (shape[1] // 2)))
    # Make aisles
    for i in range(density):
        x, y = randrange(0, shape[1] // 2) * 2, randrange(0, shape[0] // 2) * 2
        blocks[y][x] = None
        for j in range(complexity):
            neighbours = []
            if x > 0:
                neighbours.append((y, x - 2))
            if x < shape[1] - 2:
                neighbours.append((y, x + 2))
            if y > 0:
                neighbours.append((y - 2, x))
            if y < shape[0] - 2:
                neighbours.append((y + 2, x))
            if len(neighbours):
                shuffle(neighbours)
                y_, x_ = neighbours.pop()
                if blocks[y_][x_] is not None:
                    blocks[y_][x_] = None
                    blocks[y_ + (y - y_) // 2][x_ + (x - x_) // 2] = None
                    x, y = x_, y_

    return add_to_sprites(blocks, sprites)
