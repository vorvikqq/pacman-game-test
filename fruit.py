from entity import Entity
from constants import *
from sprites import FruitSprites


class Fruit(Entity):
    """
    Represents a collectible fruit entity in the game.

    Attributes:
            name (str): The type of entity (FRUIT).
            color (tuple): The color of the fruit.
            lifespan (int): The time (in seconds) before the fruit disappears.
            timer (float): Tracks the elapsed time since the fruit appeared.
            destroy (bool): Indicates whether the fruit should be removed.
            points (int): The score awarded when the fruit is collected.
            sprites (FruitSprites): The sprite representation of the fruit.
    """

    def __init__(self, node, level=0):
        """
        Initializes a fruit entity.

        Args:
            node (Node): The initial position of the fruit.
            level (int): The game level, affecting the fruit's point value.
        """
        Entity.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 5
        self.timer = 0
        self.destroy = False
        self.points = 100 + level * 20
        self.setBetweenNodes(RIGHT)
        self.sprites = FruitSprites(self, level)

    def update(self, dt):
        """
        Updates the fruit's state based on elapsed time.

        Args:
            dt (float): Time elapsed since the last update.
        """
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
