import pytest
from unittest.mock import Mock
from constants import UP, DOWN, LEFT, RIGHT
from mazedata import MazeBase


@pytest.fixture
def maze_base():
    return MazeBase()


@pytest.fixture
def mock_nodes():
    nodes = Mock()
    nodes.setPortalPair = Mock()
    nodes.createHomeNodes = Mock(return_value="home_key")
    nodes.connectHomeNodes = Mock()
    nodes.denyAccessList = Mock()
    return nodes


@pytest.fixture
def mock_ghosts():
    return Mock()


class TestMazeBase:
    def test_init(self, maze_base):
        assert maze_base.portal_pairs == {}
        assert maze_base.home_offset == (0, 0)
        assert maze_base.ghost_node_deny == {UP: (), DOWN: (), LEFT: (), RIGHT: ()}

    def test_set_portal_pairs(self, maze_base, mock_nodes):
        maze_base.portal_pairs = {0: ((1, 2), (3, 4)), 1: ((5, 6), (7, 8))}
        maze_base.set_portal_pairs(mock_nodes)

        assert mock_nodes.setPortalPair.call_count == 2
        mock_nodes.setPortalPair.assert_any_call((1, 2), (3, 4))
        mock_nodes.setPortalPair.assert_any_call((5, 6), (7, 8))

    def test_connect_home_nodes(self, maze_base, mock_nodes):
        maze_base.home_offset = (10, 12)
        maze_base.home_node_connect_left = (11, 12)
        maze_base.home_node_connect_right = (14, 12)

        maze_base.connect_home_nodes(mock_nodes)

        mock_nodes.createHomeNodes.assert_called_once_with(10, 12)
        mock_nodes.connectHomeNodes.assert_any_call("home_key", (11, 12), LEFT)
        mock_nodes.connectHomeNodes.assert_any_call("home_key", (14, 12), RIGHT)

    def test_add_offset(self, maze_base):
        maze_base.home_offset = (5, 10)
        result = maze_base.add_offset(3, 4)
        assert result == (8, 14)

    def test_deny_ghosts_access(self, maze_base, mock_nodes, mock_ghosts):
        maze_base.home_offset = (10, 10)

        maze_base.ghost_node_deny = {
            UP: ((1, 2), (3, 4)),
            DOWN: (),
            LEFT: ((5, 6),),
            RIGHT: ()
        }

        maze_base.deny_ghosts_access(mock_ghosts, mock_nodes)

        mock_nodes.denyAccessList.assert_any_call(12, 13, LEFT, mock_ghosts)
        mock_nodes.denyAccessList.assert_any_call(12, 13, RIGHT, mock_ghosts)

        mock_nodes.denyAccessList.assert_any_call(1, 2, UP, mock_ghosts)
        mock_nodes.denyAccessList.assert_any_call(3, 4, UP, mock_ghosts)
        mock_nodes.denyAccessList.assert_any_call(5, 6, LEFT, mock_ghosts)
