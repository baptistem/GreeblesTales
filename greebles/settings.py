#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Handle settings from game."""


class Settings():
    """Handle game settings."""

    def __init__(self, level=0):
        """Set the default settings."""
        if level == 0:
            self.tank_squashable = False
        self.level = level
