import pytest
from unittest.mock import Mock
from mazedata import MazeData, Maze1, Maze2


@pytest.fixture
def maze_data():
    return MazeData()


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


class TestMazeData:
    def test_init(self, maze_data):
        assert maze_data.obj is None
        assert maze_data.maze_dict == {0: Maze1, 1: Maze2}

    @pytest.mark.parametrize("level,expected_class", [
        (0, Maze1),
        (1, Maze2),
        (2, Maze1),
        (3, Maze2),
    ])
    def test_load_maze(self, maze_data, level, expected_class):
        maze_data.load_maze(level)
        assert isinstance(maze_data.obj, expected_class)


def test_maze_integration(mock_nodes, mock_ghosts):
    maze_data = MazeData()
    maze_data.load_maze(0)

    maze_data.obj.set_portal_pairs(mock_nodes)
    mock_nodes.setPortalPair.assert_called_with((0, 17), (27, 17))

    maze_data.obj.connect_home_nodes(mock_nodes)
    mock_nodes.createHomeNodes.assert_called_with(11.5, 14)

    maze_data.obj.deny_ghosts_access(mock_ghosts, mock_nodes)
    assert mock_nodes.denyAccessList.call_count > 0
