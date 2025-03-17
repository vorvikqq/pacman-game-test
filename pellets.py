import pygame
from vector import Vector
from constants import *
import numpy as np
from typing import List


class Pellet:
    """
    Represents a basic pellet in the game that the player can collect.
    """

    def __init__(self, row: int, column: int):
        """
        Initializes a Pellet object.

        :param row: Row index of the pellet in the grid.
        :param column: Column index of the pellet in the grid.
        """
        self.name = PELLET
        self.position = Vector(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = YELLOW
        self.radius = int(2 * TILEWIDTH / 16)
        self.collide_radius = int(2 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen):
        """
        Renders the pellet on the screen if it is visible.

        :param screen: The Pygame screen where the pellet is drawn.
        """
        if self.visible:
            adjust = Vector(TILEWIDTH, TILEHEIGHT) / 2
            p = (self.position + adjust).asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class PowerPellet(Pellet):
    """
    Represents a Power Pellet in the game, which grants special abilities when eaten.
    """

    def __init__(self, row: int, column: int):
        """
        Initializes a PowerPellet object.

        :param row: Row index of the power pellet in the grid.
        :param column: Column index of the power pellet in the grid.
        """
        super().__init__(row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.4  # Time interval for blinking effect
        self.timer = 0

    def update(self, dt: float) -> None:
        """
        Updates the visibility of the Power Pellet to create a blinking effect.

        :param dt: Time elapsed since the last update.
        """
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0


class PelletGroup:
    """
    Manages a group of pellets and power pellets in the game.
    """

    def __init__(self, pellet_file: str):
        """
        Initializes a PelletGroup object by loading pellet data from a file.

        :param pellet_file: Path to the file containing pellet layout.
        """
        self.pellets: List[Pellet] = []
        self.power_pellets: List[PowerPellet] = []
        self.create_pellet_list(pellet_file)
        self.num_eaten: int = 0

    def update(self, dt: float) -> None:
        """
        Updates the state of all power pellets in the group.

        :param dt: Time elapsed since the last update.
        """
        for power_pellet in self.power_pellets:
            power_pellet.update(dt)

    def create_pellet_list(self, pellet_file: str) -> None:
        """
        Creates a list of pellets and power pellets from a given file.

        :param pellet_file: Path to the file containing pellet layout.
        """
        data = self.read_pellet_file(pellet_file)
        for row_index, row in enumerate(data):
            for col_index, cell in enumerate(row):
                if cell in {'.', '+'}:  # Normal pellet
                    self.pellets.append(Pellet(row_index, col_index))
                elif cell in {'P', 'p'}:  # Power pellet
                    power_pellet = PowerPellet(row_index, col_index)
                    self.pellets.append(power_pellet)
                    self.power_pellets.append(power_pellet)

    def read_pellet_file(self, text_file: str) -> np.ndarray:
        """
        Reads the pellet layout from a text file and returns it as a NumPy array.

        :param text_file: Path to the text file containing pellet layout.
        :return: NumPy array representing the pellet layout.
        """
        return np.loadtxt(text_file, dtype='<U1')

    def is_empty(self) -> bool:
        """
        Checks if all pellets have been eaten.

        :return: True if there are no remaining pellets, False otherwise.
        """
        return not self.pellets

    def render(self, screen):
        """
        Renders all pellets on the screen.

        :param screen: The Pygame screen where pellets are drawn.
        """
        for pellet in self.pellets:
            pellet.render(screen)
