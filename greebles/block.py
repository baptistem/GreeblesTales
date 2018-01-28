#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
handle block.

inherit from entity
"""

import pygame
from greebles.entity import Entity
BLACK = (0, 0, 0, 0)


class Block(Entity):
    """
    This class describe a moving entity.

    a moving entity will be an ennemy, a block or a controlled entity.
    """

    def __init__(self, immuable=False):
        """
        Constructor.

        Pass in the color of the block, and its x and y position.
        """
        self.journey = 0
        self.immuable = immuable
        self.to_fade = False
        self.image = pygame.image.load("assets/sandblock.png")
        self.image.set_colorkey(BLACK)

        super().__init__()

    def update(self):
        """Move if needed."""
        if self.immuable or \
           not self.to_fade \
           and \
           (self.x_speed is 0 and self.y_speed is 0):
                return False
        self.journey += 1
        if self.to_fade:
            if self.journey >= 5:
                self.kill()
            else:
                self.image = pygame.image.load("assets/sandblock"+str(self.journey)+".png")

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        return True

    def bounce(self):
        if abs(self.x_speed) >= 0.25 or abs(self.y_speed) >= 0.25:
            if abs(self.x_speed) > abs(self.y_speed):
                self.y_speed = 0
            else:
                self.x_speed = 0
            self.x_speed = - self.x_speed/2
            self.y_speed = - self.y_speed/2
            self.update()
        else:
            self.stop()

    def stop(self):
        self.align()
        self.x_speed = 0
        self.y_speed = 0
        self.journey = 0
    
    def fade(self):
        self.to_fade = True
