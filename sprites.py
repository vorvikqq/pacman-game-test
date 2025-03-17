import pygame
from constants import *
import numpy as np
from animation import Animation


class SpritesSheet(object):
    """
    Represents a sprite sheet containing multiple game sprites.

    Attributes:
        sheet (pygame.Surface): The loaded and processed sprite sheet.
    """

    def __init__(self):
        """
        Loads and processes the sprite sheet, adjusting its size according to the game's tile dimensions.
        """
        self.sheet = pygame.image.load("images/spritesheet.png").convert()
        transcolor = self.sheet.get_at((0, 0))
        self.sheet.set_colorkey(transcolor)  # take color that made that transparent
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        # according to the constants
        # the size of the sprite sheet changes
        # AND! regardless of the value of TILEWIDTH and TILEHEIGHT,
        # sprites will be displayed correctly

    def get_image(self, x, y, width, height):
        """
        Extracts a single sprite from the sprite sheet.
        """
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

# Creating separate classes to store
# all character part sprites to separate them
# from the class class and avoid a sprite table file.


class PacmanSprites(SpritesSheet):
    """
    Manages Pacman's sprite animations.

    Attributes:
        entity: The Pacman entity.
        animations (dict): A dictionary mapping directions to animations.
        stop_image (tuple): Coordinates of the stop image.
    """

    def __init__(self, entity):
        """
        Initializes the sprite manager for Pacman.
        """
        SpritesSheet.__init__(self)
        self.entity = entity
        self.entity.image = self.get_start_Image()
        self.animations = {}
        self.define_ani_for_pacman()
        self.stop_image = (8, 0)

    def get_start_Image(self):
        """
        Returns the initial Pacman image for the starting position.
        """
        return self.get_image(8, 0)

    def get_image(self, x, y):
        """
        Recives a sprite image from the sprite sheet
        """
        return SpritesSheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)

    def define_ani_for_pacman(self):
        """
        Defines animations for Pacman's movement in different directions.
        """
        self.animations[LEFT] = Animation(((8, 0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animation(((10, 0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animation(((10, 2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animation(((8, 2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animation(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    def update(self, d_time):
        """
        Updates Pacman's animation based on its movement direction.
        """
        if self.entity.alive:
            direction_map = {
                LEFT: (self.animations[LEFT], (8, 0)),
                RIGHT: (self.animations[RIGHT], (10, 0)),
                DOWN: (self.animations[DOWN], (8, 2)),
                UP: (self.animations[UP], (10, 2))
            }

            if self.entity.direction in direction_map:
                animation, stop_image = direction_map[self.entity.direction]
                self.entity.image = self.get_image(*animation.update(d_time))
                self.stop_image = stop_image
            elif self.entity.direction == STOP:
                self.entity.image = self.get_image(*self.stop_image)
        else:
            self.entity.image = self.get_image(*self.animations[DEATH].update(d_time))

    def reset(self):
        """
        Reset all animations to their original state
        """
        for key in list(self.animations.keys()):
            self.animations[key].reset()


class GhostSprites(SpritesSheet):
    """
    Manages the sprites and animations for ghosts.

    Attributes:
        entity: The ghost entity.
        x (dict): Mapping of ghost types to sprite sheet positions.
    """

    def __init__(self, entity):
        """
        Loads and processes the sprite sheet, adjusting its size according to the game's tile dimensions.
        """
        SpritesSheet.__init__(self)
        self.x = {BLINKY: 0, PINKY: 2, INKY: 4, CLYDE: 6}
        self.entity = entity
        self.entity.image = self.get_start_Image()

    def get_start_Image(self):
        return self.get_image(self.x[self.entity.name], 4)

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)

    # add ani (ani picture) for ghost
    def update(self):
        x = self.x[self.entity.name]

        if self.entity.mode.current_mode == FREIGHT:
            self.entity.image = self.get_image(10, 4)
            return

        if self.entity.mode.current_mode == SPAWN:
            x = 8

        direction_map = {
            LEFT: (x, 8),
            RIGHT: (x, 10),
            DOWN: (x, 6),
            UP: (x, 4),
        }

        self.entity.image = self.get_image(*direction_map.get(self.entity.direction, (x, 8)))


class FruitSprites(SpritesSheet):
    """
    Manages the sprites for fruits in the game.

    Attributes:
        entity: The fruit entity.
        fruits (dict): Mapping of fruit types to sprite sheet positions.
    """

    def __init__(self, entity, level):
        SpritesSheet.__init__(self)
        self.entity = entity
        self.fruits = {0: (16, 8), 1: (18, 8), 2: (20, 8), 3: (16, 10), 4: (18, 10), 5: (20, 10)}
        self.entity.image = self.get_start_Image(level % len(self.fruits))

    def get_start_Image(self, k):
        return self.get_image(*self.fruits[k])

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


class LifeSprites(SpritesSheet):
    """
    Manages the life indicators displayed on the screen.

    Attributes:
        images (list): List of life images.
    """

    def __init__(self, numlives):
        SpritesSheet.__init__(self)
        self.reset_lives(numlives)

    def remove_image(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def reset_lives(self, numlives):
        """Resets the life display with the given number of lives."""
        self.images = []
        for i in range(numlives):
            self.images.append(self.get_image(0, 0))

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, 2 * TILEWIDTH, 2 * TILEHEIGHT)


class MazeSprites(SpritesSheet):
    """
    Manages the maze sprite rendering.

    Attributes:
        data (ndarray): The structure of the maze.
        rot_data (ndarray): Rotation values for each tile.
    """

    def __init__(self, mazefile, rot_file):
        SpritesSheet.__init__(self)
        self.data = self.read_mazeFile(mazefile)
        self.rot_data = self.read_mazeFile(rot_file)

    def get_image(self, x, y):
        return SpritesSheet.get_image(self, x, y, TILEWIDTH, TILEHEIGHT)

    def read_mazeFile(self, mazefile):
        """Reads the maze layout from a file."""
        return np.loadtxt(mazefile, dtype='<U1')

    def construct_background(self, background, y):
        """Constructs the maze background by placing tiles at the correct positions."""
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.get_image(x, y)
                    rot_val = int(self.rot_data[row][col])  # get val for rotate
                    sprite = self.rotate(sprite, rot_val)  # give it val for out sprite object
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.get_image(10, 8)
                    background.blit(sprite, (col * TILEWIDTH, row * TILEHEIGHT))

        return background

    def rotate(self, sprite, value):
        """Rotates the sprite by a multiple of 90 degrees."""
        return pygame.transform.rotate(sprite, value * 90)  # each time miltiply by 90
