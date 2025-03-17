from pygame.locals import *
from vector import Vector
from constants import *
from random import randint
from entity import Entity
from modes import ModeController
from sprites import GhostSprites


class Ghost(Entity):
    """
    Base class for all ghost entities in the game. Handles movement, modes, and interactions with Pacman
    """

    def __init__(self, node, pacman):
        super().__init__(node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector()
        self.pacman = pacman
        self.mode = ModeController(self)
        self.update_move_method()

    def update_move_method(self):
        """
        Updates the movement method based on the ghost's current mode
        """
        if self.mode.current_mode is SCATTER:
            self.set_speed(110)
            self.move_method = self.scatter_movement

        elif self.mode.current_mode is CHASE:
            self.set_speed(110)
            self.move_method = self.goal_movement

        elif self.mode.current_mode is WAIT:
            self.set_speed(110)
            self.move_method = self.wait_movement

        elif self.mode.current_mode is RANDOM:
            self.set_speed(110)
            self.move_method = self.random_movement

        elif self.mode.current_mode is FREIGHT:
            self.set_speed(50)
            self.move_method = self.freight_movement

        elif self.mode.current_mode is SPAWN:
            self.set_speed(200)
            self.move_method = self.spawn_movement

    def update_goal(self):
        """
        Updates the goal position of the ghost based on its current mode
        """
        if self.mode.current_mode is CHASE:
            self.goal = self.pacman.node.position

        elif self.mode.current_mode is SCATTER:
            self.goal = self.scatter_goal

    def update(self, dt):
        """
        Updates ghost movement and mode control
        """
        self.position += self.directions[self.direction] * self.speed * dt
        self.sprites.update()
        self.mode.update(dt)

        if self.overshot_target():
            self.node = self.target
            directions_list = self.valid_directions_list()

            new_direction = self.move_method(directions_list)

            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]

            self.target = self.get_new_target(new_direction)

            if self.target != self.node:
                self.direction = new_direction

            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

        self.update_goal()

    def valid_directions_list(self):
        """
        Method for getting all avaliable directions for ghost to move

        Returns: a list of all possible directions to go
        """
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.valid_direction(key):
                if key != self.direction * -1:
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1)
        return directions

    def random_movement(self, directions):
        """
        Method for getting a random direction from list

        Returns: random element from given directions list
        """

        return directions[randint(0, len(directions) - 1)]

    def goal_movement(self, directions):
        """
        Method for getting the best direction from list to chase Pacman

        Returns the direction that minimizes the distance to the goal
        """
        distances = []

        for direction in directions:
            distance = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            distances.append(distance.magnitudeSquared())

        index = distances.index(min(distances))
        return directions[index]

    def wait_movement(self, directions):
        """
        Returns opposite direction
        """
        return self.direction * -1

    def scatter_movement(self, directions):
        """
        Returns goal_movement method with directions list
        """
        return self.goal_movement(directions)

    def freight_movement(self, directions):
        """
        Returns random_movement method with directions list
        """
        return self.random_movement(directions)

    def spawn_movement(self, directions):
        """
        Returns random_movement method with directions list
        """
        return self.goal_movement(directions)

    def start_freight(self):
        """
        Puts the ghost into freight mode
        """
        self.mode.set_freight_mode()
        if self.mode.current_mode == FREIGHT:
            self.set_speed(50)
            self.move_method = self.random_movement

    def normal_mode(self):
        """
        Puts the ghost into normal mode
        """
        self.set_speed(100)
        self.move_method = self.goal_movement
        self.spawn_node.denyAccess(DOWN, self)

    def spawn(self):
        """
        Sets ghosts home goal
        """
        self.goal = self.home_goal

    def start_spawn(self):
        """
        Starts spawn mode for ghost
        """
        self.mode.set_spawn_mode()
        if self.mode.current_mode == SPAWN:
            self.set_speed(150)
            self.move_method = self.goal_movement
            self.spawn()

    def reset(self):
        """
        Resets the ghost to its initial state
        """
        Entity.reset(self)
        self.points = 200
        self.move_method = self.goal_movement


class Blinky(Ghost):
    """
    Blinky is the red ghost that directly chases Pacman
    """

    def __init__(self, node, pacman):
        super().__init__(node, pacman)
        self.mode = ModeController(self, SCATTER)
        self.color = PURPLE
        self.name = BLINKY
        self.sprites = GhostSprites(self)

    def update_goal(self):
        if self.mode.current_mode is CHASE:
            self.goal = self.pacman.node.position

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(0, 0)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal


class Pinky(Ghost):
    """
    Pinky predicts Pacman's movement and moves 4 tiles ahead
    """

    def __init__(self, node, pacman):
        super().__init__(node, pacman)
        self.color = PINK
        self.name = PINKY
        self.sprites = GhostSprites(self)

    def update_goal(self):
        if self.mode.current_mode is CHASE:
            self.goal = self.pacman.node.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(520, 80)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal


class Inky(Ghost):
    """
    Inky's behavior depends on both Pacman and Blinky's positions
    """

    def __init__(self, node, pacman, blinky=None):
        super().__init__(node, pacman)
        self.color = CYAN
        self.blinky = blinky
        self.name = INKY
        self.sprites = GhostSprites(self)

    def update_goal(self):
        if self.mode.current_mode is CHASE:
            pacman_plus_two = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
            self.goal = (pacman_plus_two - self.blinky.position) * 2 + self.blinky.position

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(520, 640)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal


class Clyde(Ghost):
    """
    Clyde moves towards Pacman but runs away if he's 8 tiles close to him
    """

    def __init__(self, node, pacman):
        super().__init__(node, pacman)
        self.color = ORANGE
        self.name = CLYDE
        self.sprites = GhostSprites(self)

    def update_goal(self):
        if self.mode.current_mode is CHASE:
            d = self.pacman.position - self.position

            d_squared = d.magnitudeSquared()

            if d_squared <= (TILEWIDTH * 8) ** 2:
                self.mode.current_mode = SCATTER
                self.goal = Vector(0, TILEHEIGHT * NROWS)

            else:
                self.goal = self.pacman.node.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

        elif self.mode.current_mode is SCATTER:
            self.goal = Vector(0, TILEHEIGHT * NROWS)

        elif self.mode.current_mode is SPAWN:
            self.goal = self.home_goal


class GhostsGroup():
    """
    Manages all ghost entities in the game
    """

    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman, self.blinky)
        self.clyde = Clyde(node, pacman)

        self.ghosts_list = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts_list)

    def update(self, dt):
        for ghost in self.ghosts_list:
            ghost.update(dt)

    def set_spawn_node(self, node):
        for ghost in self:
            ghost.set_spawn_node(node)

    def start_freight(self):
        for ghost in self:
            ghost.start_freight()
        self.resetPoints()

    def render(self, screen):
        for ghost in self.ghosts_list:
            ghost.render(screen)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()
