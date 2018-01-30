#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
handle entity.

inherit from Sprite
"""

import pygame


class Entity(pygame.sprite.Sprite):
    """
    This class describe a moving entity.

    a moving entity will be an ennemy, a block or a controlled entity.
    """

    def __init__(self):
        """
        Constructor.

        Pass in the color of the block, and its x and y position.
        """
        super().__init__()
        self.rect = self.image.get_rect()
        self.x_speed = 0
        self.y_speed = 0
        self.forced = False
        self.journey = 9999
        self.old_angle = None
        self.pushing_entity = False

    def rotate(self, angle):
        if self.forced or self.old_angle is None:
            return
        self.image = pygame.transform.rotate(self.image,- self.old_angle)
        self.old_angle = angle
        self.image = pygame.transform.rotate(self.image, angle)

    def update_speed(self, speed):
        x_speed = speed[0]
        y_speed = speed[1]
        if x_speed is not None:
            self.x_speed += x_speed
        if y_speed is not None:
            self.y_speed += y_speed

    def set_speed(self, speed):
        x_speed = speed[0]
        y_speed = speed[1]
        if x_speed is None:
            x_speed = self.x_speed
        if y_speed is None:
            y_speed = self.y_speed
        if not self.forced:
            self.x_speed = x_speed
            self.y_speed = y_speed

    def update(self):
        if self.forced:
            self.image = pygame.transform.rotate(self.image, 90)
            if self.old_angle is not None:
                self.old_angle += 90
            self.journey += 1
            return True
        if self.old_angle is None or self.old_angle in [90,270]:
            self.rect.x += self.x_speed
        if self.old_angle is None or self.old_angle in [0,180]:
            self.rect.y += self.y_speed
        return True

    def force_move(self, x_speed, y_speed):
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.forced = True
        self.journey = 0

    def align(self):
        self.rect.x = round((self.rect.x-self.x_speed)/32)*32
        self.rect.y = round((self.rect.y-self.y_speed)/32)*32

    def get_move(angle, value):
        x = y = 0
        direction = int(angle / 90)
        if direction is 0:
            y -= value
        elif direction is 1:
            x -= value
        elif direction is 2:
            y += value
        elif direction is 3:
            x += value
        return x, y

    def apply_move(self, angle, value):
        x, y = Entity.get_move(angle, value)
        self.rect.x += x
        self.rect.y += y
