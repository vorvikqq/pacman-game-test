from constants import *


class MazeBase:
    """
    Base class for maze structures in the game.

    Attributes:
        portal_pairs (dict): Dictionary storing portal pair positions.
        home_offset (tuple): Offset coordinates for the ghost home.
        ghost_node_deny (dict): Dictionary specifying restricted ghost movement.
    """

    def __init__(self) -> None:
        """
        Initializes the base maze structure.
        """
        self.portal_pairs = {}
        self.home_offset = (0, 0)
        self.ghost_node_deny = {UP: (), DOWN: (), LEFT: (), RIGHT: ()}

    def set_portal_pairs(self, nodes):
        """
        Sets portal connections between nodes.

        Args:
            nodes (Nodes): Node manager that handles maze connectivity.
        """
        for pair in list(self.portal_pairs.values()):
            nodes.setPortalPair(*pair)

    def connect_home_nodes(self, nodes):
        """
        Connects the home nodes for ghosts.

        Args:
            nodes (Nodes): Node manager handling maze connectivity.
        """
        key = nodes.createHomeNodes(*self.home_offset)
        nodes.connectHomeNodes(key, self.home_node_connect_left, LEFT)
        nodes.connectHomeNodes(key, self.home_node_connect_right, RIGHT)

    def add_offset(self, x, y):
        """
        Adds the home offset to given coordinates.

        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.

        Returns:
            tuple: Adjusted coordinates with the home offset.
        """
        return x + self.home_offset[0], y + self.home_offset[1]

    def deny_ghosts_access(self, ghosts, nodes):
        """
        Restricts ghosts from entering specific nodes.

        Args:
            ghosts (Ghosts): Ghost objects.
            nodes (Nodes): Node manager controlling movement permissions.
        """
        nodes.denyAccessList(*(self.add_offset(2, 3) + (LEFT, ghosts)))
        nodes.denyAccessList(*(self.add_offset(2, 3) + (RIGHT, ghosts)))

        for direction in list(self.ghost_node_deny.keys()):
            for values in self.ghost_node_deny[direction]:
                nodes.denyAccessList(*(values + (direction, ghosts)))


class Maze1(MazeBase):
    """
    Represents the first maze layout.

    Attributes:
        name (str): Name of the maze.
        portal_pairs (dict): Portal pair locations.
        home_offset (tuple): Offset for the ghost home.
        home_node_connect_left (tuple): Left connection point for ghost home.
        home_node_connect_right (tuple): Right connection point for ghost home.
        pacman_start (tuple): Starting position of Pac-Man.
        fruit_start (tuple): Position where the fruit appears.
        ghost_node_deny (dict): Restricted areas for ghost movement.
    """

    def __init__(self) -> None:
        """
        Initializes Maze1 with predefined structure.
        """
        MazeBase.__init__(self)
        self.name = "maze1"
        self.portal_pairs = {0: ((0, 17), (27, 17))}
        self.home_offset = (11.5, 14)
        self.home_node_connect_left = (12, 14)
        self.home_node_connect_right = (15, 14)
        self.pacman_start = (15, 26)
        self.fruit_start = (9, 20)
        self.ghost_node_deny = {
            UP: ((12, 14), (15, 14), (12, 26), (15, 26)),
            LEFT: (self.add_offset(2, 3),),
            RIGHT: (self.add_offset(2, 3),)
        }


class Maze2(MazeBase):
    """
    Represents the second maze layout.

    Attributes:
        name (str): Name of the maze.
        portal_pairs (dict): Portal pair locations.
        home_offset (tuple): Offset for the ghost home.
        home_node_connect_left (tuple): Left connection point for ghost home.
        home_node_connect_right (tuple): Right connection point for ghost home.
        pacman_start (tuple): Starting position of Pac-Man.
        fruit_start (tuple): Position where the fruit appears.
        ghost_node_deny (dict): Restricted areas for ghost movement.
    """

    def __init__(self):
        """
        Initializes Maze2 with predefined structure.
        """
        MazeBase.__init__(self)
        self.name = "maze2"
        self.portal_pairs = {0: ((0, 4), (27, 4)), 1: ((0, 26), (27, 26))}
        self.home_offset = (11.5, 14)
        self.home_node_connect_left = (9, 14)
        self.home_node_connect_right = (18, 14)
        self.pacman_start = (16, 26)
        self.fruit_start = (11, 20)
        self.ghost_node_deny = {
            UP: ((9, 14), (18, 14), (11, 23), (16, 23)),
            LEFT: (self.add_offset(2, 3),),
            RIGHT: (self.add_offset(2, 3),)
        }


class MazeData:
    """
    Handles maze selection and loading.

    Attributes:
        obj (MazeBase or None): Current maze instance.
        maze_dict (dict): Mapping of level numbers to maze classes.
    """

    def __init__(self) -> None:
        """
        Initializes the MazeData class.
        """
        self.obj = None
        self.maze_dict = {0: Maze1, 1: Maze2}

    def load_maze(self, level):
        """
        Loads the maze corresponding to the given level.

        Args:
            level (int): Current game level.
        """
        self.obj = self.maze_dict[level % len(self.maze_dict)]()
