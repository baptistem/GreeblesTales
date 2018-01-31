#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines a moving entity controlled by the user.

Will handle movement, score, lifes and powerup
"""
import pygame
from greebles.entity import Entity

BLACK = (0, 0, 0, 0)


class Tank(Entity):
    """
    This class represents a tank, a moving entity controlled by the user.

    inherit from entity
    """

    def __init__(self):
        """
        Default constructor.

        build an image with a tank
        """
        self.image = pygame.image.load("assets/tank.png")
        self.image.set_colorkey(BLACK)
        super().__init__()
        self.old_angle = 0
        self.input = []
        self.index = -1
        self.old_index = -1

    def blocked(self):
        self.old_index = self.index
        self.index -= 1

    def unblocked(self):
        self.index = -1

    def update(self):
        if len(self.input) == 0:
            return False
        if abs(self.index) > len(self.input):
            self.rotate(self.input[-1])
            return False
        print("updaaaate")
        self.rotate(self.input[self.index])
        if self.old_angle == 0:
            self.y_speed = -2
        if self.old_angle == 180:
            self.y_speed = 2
        if self.old_angle == 90:
            self.x_speed = -2
        if self.old_angle == 270:
            self.x_speed = 2

        return super().update()

    def get_angle(self):
        if abs(self.index) <= len(self.input):
            return self.input[self.index]
        else:
            return None
