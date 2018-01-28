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
