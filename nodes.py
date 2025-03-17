import pygame
from vector import Vector
from constants import *
import numpy as np


class Node:
    """
    Class representing a node in the maze graph.
    """

    def __init__(self, x, y):
        """
        Initializes a node with given coordinates.

        :param x: X coordinate
        :param y: Y coordinate
        """
        self.position = Vector(x, y)
        self.neighbors = {LEFT: None, RIGHT: None, UP: None, DOWN: None, PORTAL: None}
        self.access = {UP: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       DOWN: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       LEFT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       RIGHT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def denyAccess(self, direction, entity):
        """
        Denies movement in a given direction for an entity.

        :param direction: Movement direction (UP, DOWN, LEFT, RIGHT)
        :param entity: Entity for which access is denied
        """
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allowAccess(self, direction, entity):
        """
        Allows movement in a given direction for an entity.

        :param direction: Movement direction
        :param entity: Entity for which access is allowed
        """
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def render(self, screen):
        """
        Renders the node and its connections.

        :param screen: Screen to render on
        """
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)


class NodeGroup(object):
    """
       Class representing a group of nodes in the game maze.
    """

    def __init__(self, level):
        """
        Initializes the node group based on the game level.

        :param level: Path to the level file
        """
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    def readMazeFile(self, textfile):
        """
        Reads the level file and returns an array of characters.

        :param textfile: Path to the level file
        :return: Array of level characters
        """
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        """
        Creates a table of nodes from the level character array.

        :param data: 2D array of level characters
        :param xoffset: X offset
        :param yoffset: Y offset
        """
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                # Якщо символ є вузлом, додаємо його в таблицю
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col + xoffset, row + yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def createHomeNodes(self, xoffset, yoffset):
        """
        Creates a home area for ghosts within the game grid.

        :param xoffset: X-coordinate offset for positioning the home.
        :param yoffset: Y-coordinate offset for positioning the home.
        :return: Key representing the home node.
        """
        homedata = np.array([['X', 'X', '+', 'X', 'X'],
                             ['X', 'X', '.', 'X', 'X'],
                             ['+', 'X', '.', 'X', '+'],
                             ['+', '.', '+', '.', '+'],
                             ['+', 'X', 'X', 'X', '+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset + 2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):
        """
        Connects the home node to another node in the given direction.

        :param homekey: Key of the home node.
        :param otherkey: Coordinates (col, row) of the node to connect.
        :param direction: Direction of the connection.
        """
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction * -1] = self.nodesLUT[homekey]

    def constructKey(self, x, y):
        """
        Constructs a unique key for a node based on its coordinates.

        :param x: X coordinate
        :param y: Y coordinate
        :return: Unique node key
        """
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectNodes(self, key1, key2, direction1, direction2):
        """
        Connects two nodes in a specified direction.

        :param key1: Key of the first node
        :param key2: Key of the second node
        :param direction1: Direction for the first node
        :param direction2: Direction for the second node
        """
        self.nodesLUT[key1].neighbors[direction1] = self.nodesLUT[key2]
        self.nodesLUT[key2].neighbors[direction2] = self.nodesLUT[key1]

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        """
        Connects nodes horizontally within the given data grid.

        :param data: 2D array representing the game map.
        :param xoffset: X-coordinate offset for node positioning.
        :param yoffset: Y-coordinate offset for node positioning.
        """
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        currentKey = self.constructKey(col + xoffset, row + yoffset)
                        self.connectNodes(key, currentKey, RIGHT, LEFT)
                        key = currentKey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        """
        Connects nodes vertically within the given data grid.

        :param data: 2D array representing the game map.
        :param xoffset: X-coordinate offset for node positioning.
        :param yoffset: Y-coordinate offset for node positioning.
        """
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        currentKey = self.constructKey(col + xoffset, row + yoffset)
                        self.connectNodes(key, currentKey, DOWN, UP)
                        key = currentKey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        """
        Retrieves a node from pixel coordinates.

        :param xpixel: X-coordinate in pixels.
        :param ypixel: Y-coordinate in pixels.
        :return: Node object or None if not found.
        """
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        """
        Retrieves a node based on tile coordinates.

        :param col: Column index.
        :param row: Row index.
        :return: Node object or None if not found.
        """
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNode(self):
        """
        Returns the first node in the lookup table.

        :return: First Node object.
        """
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    def setPortalPair(self, pair1, pair2):
        """
        Creates a portal connection between two nodes.

        :param pair1: Coordinates (col, row) of the first portal node.
        :param pair2: Coordinates (col, row) of the second portal node.
        """
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def denyAccess(self, col, row, direction, entity):
        """
        Denies access to a specific direction for an entity at a given tile.

        :param col: Column index.
        :param row: Row index.
        :param direction: Direction to deny access.
        :param entity: Entity being restricted.
        """
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        """
        Allows access to a specific direction for an entity at a given tile.

        :param col: Column index.
        :param row: Row index.
        :param direction: Direction to allow access.
        :param entity: Entity being allowed.
        """
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    def denyAccessList(self, col, row, direction, entities):
        """
        Denies access to multiple entities at a given tile and direction.

        :param col: Column index.
        :param row: Row index.
        :param direction: Direction to deny access.
        :param entities: List of entities to restrict.
        """
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    def allowAccessList(self, col, row, direction, entities):
        """
        Allows access to multiple entities at a given tile and direction.

        :param col: Column index.
        :param row: Row index.
        :param direction: Direction to allow access.
        :param entities: List of entities to allow.
        """
        for entity in entities:
            self.allowAccess(col, row, direction, entity)

    def denyHomeAccess(self, entity):
        """
        Denies access to the home node for a specific entity.

        :param entity: Entity being restricted.
        """
        self.nodesLUT[self.homekey].denyAccess(DOWN, entity)

    def allowHomeAccess(self, entity):
        """
        Allows access to the home node for a specific entity.

        :param entity: Entity being allowed.
        """
        self.nodesLUT[self.homekey].allowAccess(DOWN, entity)

    def denyHomeAccessList(self, entities):
        """
        Denies access to the home node for multiple entities.

        :param entities: List of entities to restrict.
        """
        for entity in entities:
            self.denyHomeAccess(entity)

    def allowHomeAccessList(self, entities):
        """
        Allows access to the home node for multiple entities.

        :param entities: List of entities to allow.
        """
        for entity in entities:
            self.allowHomeAccess(entity)
