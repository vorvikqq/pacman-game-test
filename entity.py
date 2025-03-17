import pygame
from pygame.locals import *
from vector import Vector
from constants import *


class Entity():
    """
    Represents a game entity that moves within the game world.

    Attributes:
        name (str): The name of the entity.
        directions (dict): Mapping of movement directions to vector values.
        direction (Vector): Current movement direction.
        speed (float): Movement speed of the entity.
        collide_radius (int): Radius for collision detection.
        radius (int): Radius of the entity for rendering.
        color (tuple): RGB color for rendering.
        node (Node): Current node in the game grid.
        position (Vector): Current position of the entity.
        target (Node): Target node for movement.
        home_goal (Vector): Home position for the entity.
        visible (bool): Whether the entity is visible.
        spawn_node (Node): Initial node where the entity spawns.
        image (pygame.Surface): Image used to render the entity.
    """

    def __init__(self, node):
        """
        Initializes an Entity object with a starting node.

        Args:
            node (Node): The starting node of the entity.
        """
        self.name = ""
        self.directions = {
            STOP: Vector(),
            UP: Vector(0, -1),
            DOWN: Vector(0, 1),
            LEFT: Vector(-1, 0),
            RIGHT: Vector(1, 0)
        }
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.collide_radius = 5
        self.radius = 10
        self.color = WHITE
        self.node = node
        self.set_position()
        self.target = node
        self.home_goal = node
        self.visible = True
        self.set_spawn_node(node)
        self.image = None

    def set_position(self):
        """
        Sets the position of the entity to the current node's position.
        """
        self.position = self.node.position.copy()

    def set_spawn_node(self, given_node):
        """
        Sets the spawn node and resets the entity's position.

        Args:
            given_node (Node): The node where the entity spawns.
        """
        self.node = given_node
        self.target = given_node
        self.home_goal = given_node.position
        self.spawn_node = given_node
        self.set_position()
        self.direction = UP

    def valid_direction(self, direction):
        """
        Checks if a given direction is valid for movement.

        Args:
            direction (Vector): The direction to check.

        Returns:
            bool: True if the direction is valid, False if its not.
        """
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def valid_directions_list(self):
        """
        Returns a list of valid movement directions.

        Returns:
            list: A list of valid movement directions.
        """
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)

        if len(directions) == 0:
            directions.append(self.direction * -1)

        return directions

    def get_new_target(self, direction):
        """
        Returns the next node in the given direction if valid.

        Args:
            direction (Vector): The direction to move.

        Returns:
            Node: The next node in the given direction or the current node.
        """
        if self.valid_direction(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshot_target(self):
        """
        Checks if the entity has overshot its target node.

        Returns:
            bool: True if the target has been overshot, False otherwise.
        """
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2_target = vec1.magnitudeSquared()
            node2_self = vec2.magnitudeSquared()
            return node2_self >= node2_target
        return False

    def reverse_direction(self):
        """
        Reverses the movement direction of the entity.
        """
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def opposite_direction(self, direction):
        """
        Checks if the given direction is the opposite of the current direction.

        Args:
            direction (Vector): The direction to check.

        Returns:
            bool: True if the direction is opposite, False otherwise.
        """
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def render(self, screen):
        """
        Renders the entity on the screen.

        Args:
            screen: The game screen surface.
        """
        if self.visible:
            if self.image is not None:
                adjust = Vector(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt()
                pygame.draw.circle(screen, self.color, p, self.radius)

    def setBetweenNodes(self, direction):
        """
        Moves the entity to a position between two nodes.

        Args:
            direction (Vector): The movement direction.
        """
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def set_speed(self, speed):
        """
        Sets the entity's movement speed.

        Args:
            speed (float): The new speed value.
        """
        self.speed = speed * TILEWIDTH / 16

    def reset(self):
        """
        Resets the entity to its spawn node with default values.
        """
        self.set_spawn_node(self.spawn_node)
        self.direction = STOP
        self.speed = 100 * TILEWIDTH / 16
        self.visible = True
