import pygame
from pygame.locals import *
from vector import Vector
from constants import *
from entity import Entity
from sprites import PacmanSprites


class Pacman(Entity):
    """
    Represents the Pacman character in the game, handling movement, collisions,
    and interactions with pellets and ghosts.
    """

    def __init__(self, node):
        """
        Initializes the Pacman entity.

        :param node: The starting node for Pacman.
        """
        super().__init__(node)
        self.name = PACMAN
        self.directions = {
            STOP: Vector(),
            UP: Vector(0, -1),
            DOWN: Vector(0, 1),
            LEFT: Vector(-1, 0),
            RIGHT: Vector(1, 0)
        }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.set_position()
        self.target = node
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)

    def reset(self):
        """
        Resets Pacman to its initial state.
        """
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.get_start_Image()
        self.sprites.reset()

    def die(self):
        """
        Handles Pacman's death by stopping movement and setting alive to False.
        """
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        """
        Updates Pacman's position and handles movement logic.

        :param dt: Time delta for frame updates.
        """
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.getValidKey()
        if self.overshot_target():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.set_position()
        else:
            if self.opposite_direction(direction):
                self.reverse_direction()

    def getValidKey(self):
        """
        Gets the current valid movement key pressed by the player.

        :return: The direction of movement.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        """
        Checks if Pacman collides with any pellet in the pellet list.

        :param pelletList: List of pellets in the game.
        :return: The pellet that was eaten, or None if no collision.
        """
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    def collide_ghost(self, ghost):
        """
        Checks if Pacman collides with a ghost.

        :param ghost: The ghost entity.
        :return: True if Pacman collides with the ghost, False otherwise.
        """
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        """
        Checks collision with another object based on distance.

        :param other: The other entity to check collision with.
        :return: True if collides, False otherwise.
        """
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collide_radius + other.collide_radius) ** 2
        return dSquared <= rSquared
