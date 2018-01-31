#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines a moving entity controlled by the user.

Will handle movement, score, lifes and powerup
"""

import pygame
from greebles.entity import Entity
from random import shuffle,randrange
BLACK = (0, 0, 0, 0)


class Enemy(Entity):
    """
    This class represents a ennemy, a moving entity controlled by the user.

    inherit from entity
    """
    def __init__(self):
        """
        Default constructor.

        build an image with a ennemy
        """
        self.image.set_colorkey(BLACK)
        super().__init__()
        self.old_angle = 0
        self.available_path = []

    def pick_direction(self):
        if self.old_angle in self.available_path:
            if randrange(0,10) > 1:
                return self.old_angle
        shuffle(self.available_path)
        return self.available_path[0]

    def update(self):
        if len(self.available_path) == 0:
            self.rotate(self.old_angle+90)
            return False
        self.rotate(self.pick_direction())
        if self.old_angle == 0:
            self.y_speed = -2
        if self.old_angle == 180:
            self.y_speed = 2
        if self.old_angle == 90:
            self.x_speed = -2
        if self.old_angle == 270:
            self.x_speed = 2

        return super().update()
