#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines a moving entity controlled by the user.

Will handle movement, score, lifes and powerup
"""

import pygame
from greebles.enemy import Enemy

BLACK = (0, 0, 0, 0)


class Fly(Enemy):
    """
    This class represents a enemy, a moving entity controlled by the user.

    inherit from entity
    """

    def __init__(self):
        """
        Default constructor.

        build an image with a ennemy
        """
        self.image = pygame.image.load("assets/fly.png")
        self.image.set_colorkey(BLACK)
        super().__init__()
