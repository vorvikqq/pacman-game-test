import pytest
import pygame
import numpy as np
from unittest.mock import Mock, patch
from nodes import Node, NodeGroup
from vector import Vector
from constants import *

pygame.init()


@pytest.fixture
def screen():
    return pygame.display.set_mode((800, 600))


@pytest.fixture
def node():
    return Node(10, 20)


@pytest.fixture
def entity():
    mock_entity = Mock()
    mock_entity.name = PACMAN
    return mock_entity


@pytest.fixture
def node_group(tmp_path):
    level_data = "X X X X\nX + . X\nX P - X\nX X X X"
    p = tmp_path / "test_level.txt"
    p.write_text(level_data)
    return NodeGroup(str(p))


class TestNode:
    def test_init(self, node):
        assert isinstance(node.position, Vector)
        assert node.position.x == 10
        assert node.position.y == 20
        assert len(node.neighbors) == 5  # LEFT, RIGHT, UP, DOWN, PORTAL
        assert all(v is None for v in node.neighbors.values())
        assert len(node.access) == 4  # UP, DOWN, LEFT, RIGHT
        assert PACMAN in node.access[UP]

    def test_deny_access(self, node, entity):
        node.denyAccess(UP, entity)
        assert entity.name not in node.access[UP]
        assert entity.name in node.access[DOWN]

    def test_allow_access(self, node, entity):
        node.denyAccess(UP, entity)
        node.allowAccess(UP, entity)
        assert entity.name in node.access[UP]

    def test_render(self, node, screen):
        neighbor_node = Node(20, 20)
        node.neighbors[RIGHT] = neighbor_node
        with patch.object(pygame, 'draw') as mock_draw:
            node.render(screen)
            mock_draw.line.assert_called_once()
            mock_draw.circle.assert_called_once()


class TestNodeGroup:
    def test_init(self, node_group):
        assert isinstance(node_group.nodesLUT, dict)
        assert node_group.nodeSymbols == ['+', 'P', 'n']
        assert node_group.pathSymbols == ['.', '-', '|', 'p']
        assert len(node_group.nodesLUT) > 0

    def test_read_maze_file(self, node_group, tmp_path):
        data = "X + .\nP - X"
        p = tmp_path / "test.txt"
        p.write_text(data)
        result = node_group.readMazeFile(str(p))
        assert isinstance(result, np.ndarray)
        assert result.shape == (2, 3)

    def test_create_node_table(self, node_group):
        data = np.array([['X', '+', '.'], ['P', '-', 'X']])
        node_group.nodesLUT.clear()
        node_group.createNodeTable(data)
        assert (TILEWIDTH, 0) in node_group.nodesLUT  # '+' на (1, 0)
        assert (0, TILEHEIGHT) in node_group.nodesLUT  # 'P' на (0, 1)
        assert len(node_group.nodesLUT) == 2

    def test_connect_horizontally(self, node_group):
        data = np.array([['+', '.', '+']])
        node_group.nodesLUT.clear()
        node_group.createNodeTable(data)
        node_group.connectHorizontally(data)
        key1 = (0, 0)
        key2 = (2 * TILEWIDTH, 0)
        assert node_group.nodesLUT[key1].neighbors[RIGHT] == node_group.nodesLUT[key2]
        assert node_group.nodesLUT[key2].neighbors[LEFT] == node_group.nodesLUT[key1]

    def test_connect_vertically(self, node_group):
        data = np.array([['+'], ['.'], ['+']])
        node_group.nodesLUT.clear()
        node_group.createNodeTable(data)
        node_group.connectVertically(data)
        key1 = (0, 0)
        key2 = (0, 2 * TILEHEIGHT)
        assert node_group.nodesLUT[key1].neighbors[DOWN] == node_group.nodesLUT[key2]
        assert node_group.nodesLUT[key2].neighbors[UP] == node_group.nodesLUT[key1]

    def test_create_home_nodes(self, node_group):
        homekey = node_group.createHomeNodes(5, 5)
        assert homekey == (7 * TILEWIDTH, 5 * TILEHEIGHT)  # (5+2, 5)
        assert len(node_group.nodesLUT) >= 7

    def test_set_portal_pair(self, node_group):
        node_group.nodesLUT.clear()
        data = np.array([['+', 'X'], ['X', '+']])
        node_group.createNodeTable(data)
        node_group.setPortalPair((0, 0), (1, 1))
        key1 = (0, 0)
        key2 = (TILEWIDTH, TILEHEIGHT)
        assert node_group.nodesLUT[key1].neighbors[PORTAL] == node_group.nodesLUT[key2]
        assert node_group.nodesLUT[key2].neighbors[PORTAL] == node_group.nodesLUT[key1]

    def test_get_node_from_tiles(self, node_group):
        node = node_group.getNodeFromTiles(1, 1)
        assert node is not None
        assert node.position.x == TILEWIDTH
        assert node.position.y == TILEHEIGHT

    def test_deny_access(self, node_group, entity):
        node_group.denyAccess(1, 1, UP, entity)
        node = node_group.getNodeFromTiles(1, 1)
        assert entity.name not in node.access[UP]

    def test_allow_access_list(self, node_group, entity):
        entities = [entity]
        node_group.denyAccess(1, 1, UP, entity)
        node_group.allowAccessList(1, 1, UP, entities)
        node = node_group.getNodeFromTiles(1, 1)
        assert entity.name in node.access[UP]
