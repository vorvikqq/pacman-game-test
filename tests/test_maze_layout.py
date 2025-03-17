import pytest
from constants import UP, LEFT, RIGHT
from mazedata import MazeBase, Maze1, Maze2


@pytest.fixture
def maze1():
    return Maze1()


@pytest.fixture
def maze2():
    return Maze2()


class TestMaze1:
    def test_init(self, maze1):
        assert maze1.name == "maze1"
        assert maze1.portal_pairs == {0: ((0, 17), (27, 17))}
        assert maze1.home_offset == (11.5, 14)
        assert maze1.home_node_connect_left == (12, 14)
        assert maze1.home_node_connect_right == (15, 14)
        assert maze1.pacman_start == (15, 26)
        assert maze1.fruit_start == (9, 20)

        assert (12, 14) in maze1.ghost_node_deny[UP]
        assert (15, 14) in maze1.ghost_node_deny[UP]
        assert (12, 26) in maze1.ghost_node_deny[UP]
        assert (15, 26) in maze1.ghost_node_deny[UP]
        assert maze1.add_offset(2, 3) in maze1.ghost_node_deny[LEFT]
        assert maze1.add_offset(2, 3) in maze1.ghost_node_deny[RIGHT]


class TestMaze2:
    def test_init(self, maze2):
        assert maze2.name == "maze2"
        assert maze2.portal_pairs == {0: ((0, 4), (27, 4)), 1: ((0, 26), (27, 26))}
        assert maze2.home_offset == (11.5, 14)
        assert maze2.home_node_connect_left == (9, 14)
        assert maze2.home_node_connect_right == (18, 14)
        assert maze2.pacman_start == (16, 26)
        assert maze2.fruit_start == (11, 20)

        assert (9, 14) in maze2.ghost_node_deny[UP]
        assert (18, 14) in maze2.ghost_node_deny[UP]
        assert (11, 23) in maze2.ghost_node_deny[UP]
        assert (16, 23) in maze2.ghost_node_deny[UP]
        assert maze2.add_offset(2, 3) in maze2.ghost_node_deny[LEFT]
        assert maze2.add_offset(2, 3) in maze2.ghost_node_deny[RIGHT]


@pytest.mark.parametrize("maze_class", [Maze1, Maze2])
def test_inheritance(maze_class):
    maze = maze_class()
    assert isinstance(maze, MazeBase)
    assert hasattr(maze, 'set_portal_pairs')
    assert hasattr(maze, 'connect_home_nodes')
    assert hasattr(maze, 'add_offset')
    assert hasattr(maze, 'deny_ghosts_access')
