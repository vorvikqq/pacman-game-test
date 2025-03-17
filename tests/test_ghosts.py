import pygame
import pytest
from unittest.mock import Mock
from ghosts import *
from constants import *
from sprites import GhostSprites
from vector import Vector
from modes import ModeController

pygame.init()

pygame.display.set_mode((1, 1))

spritesheet = pygame.image.load("images/spritesheet.png").convert()


@pytest.fixture
def mock_pacman():
    pacman = Mock()
    pacman.node = Mock()
    pacman.node.position = Vector(100, 100)
    pacman.direction = RIGHT
    pacman.position = Vector(100, 100)
    pacman.directions = {
        UP: Vector(0, -1),
        DOWN: Vector(0, 1),
        LEFT: Vector(-1, 0),
        RIGHT: Vector(1, 0)
    }
    return pacman


@pytest.fixture
def mock_node():
    node = Mock()
    node.position = Vector(50, 50)
    node.neighbors = {UP: Mock(), DOWN: Mock(), LEFT: Mock(), RIGHT: Mock(), PORTAL: None}
    node.access = {UP: [GHOST], DOWN: [GHOST], LEFT: [GHOST], RIGHT: [GHOST]}
    return node


@pytest.fixture
def ghost(mock_node, mock_pacman):
    ghost = Ghost(mock_node, mock_pacman)
    ghost.direction = RIGHT
    ghost.directions = {UP: Vector(0, -1), DOWN: Vector(0, 1), LEFT: Vector(-1, 0), RIGHT: Vector(1, 0)}
    ghost.name = GHOST
    return ghost


class TestGhost:
    def test_update_move_method_scatter(self, ghost):
        ghost.mode.current_mode = SCATTER
        ghost.update_move_method()
        assert ghost.move_method == ghost.scatter_movement
        assert ghost.speed == 110 * TILEWIDTH / 16

    def test_update_move_method_chase(self, ghost):
        ghost.mode.current_mode = CHASE
        ghost.update_move_method()
        assert ghost.move_method == ghost.goal_movement
        assert ghost.speed == 110 * TILEWIDTH / 16

    def test_update_move_method_freight(self, ghost):
        ghost.mode.current_mode = FREIGHT
        ghost.update_move_method()
        assert ghost.move_method == ghost.freight_movement
        assert ghost.speed == 50 * TILEWIDTH / 16

    def test_update_goal_chase(self, ghost, mock_pacman):
        ghost.mode.current_mode = CHASE
        ghost.update_goal()
        assert ghost.goal == mock_pacman.node.position

    def test_valid_directions_list(self, ghost):
        ghost.direction = LEFT
        directions = ghost.valid_directions_list()

        assert RIGHT not in directions
        assert LEFT in directions
        assert UP in directions
        assert DOWN in directions

    def test_random_movement(self, ghost):
        directions = [UP, DOWN, LEFT, RIGHT]
        direction = ghost.random_movement(directions)
        assert direction in directions

    def test_goal_movement(self, ghost):
        ghost.goal = Vector(200, 200)
        directions = [UP, DOWN, LEFT, RIGHT]
        direction = ghost.goal_movement(directions)
        assert direction in directions

    def test_wait_movement(self, ghost):
        ghost.direction = UP
        direction = ghost.wait_movement([])
        assert direction == DOWN

    def test_normal_mode(self, ghost):
        ghost.normal_mode()
        assert ghost.speed == 100 * TILEWIDTH / 16
        assert ghost.move_method == ghost.goal_movement

    def test_reset(self, ghost):
        ghost.points = 400
        ghost.reset()
        assert ghost.points == 200
        assert ghost.move_method == ghost.goal_movement


class TestBlinky:
    def test_update_goal_chase(self, mock_node, mock_pacman):
        blinky = Blinky(mock_node, mock_pacman)
        blinky.sprites = GhostSprites(blinky)
        blinky.mode.current_mode = CHASE
        blinky.update_goal()
        assert blinky.goal == mock_pacman.node.position

    def test_update_goal_scatter(self, mock_node, mock_pacman):
        blinky = Blinky(mock_node, mock_pacman)
        blinky.sprites = GhostSprites(blinky)
        blinky.mode.current_mode = SCATTER
        blinky.update_goal()
        assert blinky.goal == Vector(0, 0)

    def test_update_goal_spawn(self, mock_node, mock_pacman):
        blinky = Blinky(mock_node, mock_pacman)
        blinky.sprites = GhostSprites(blinky)
        blinky.mode.current_mode = SPAWN
        blinky.update_goal()
        assert blinky.goal == blinky.home_goal


class TestPinky:
    def test_update_goal_chase(self, mock_node, mock_pacman):
        pinky = Pinky(mock_node, mock_pacman)
        pinky.sprites = GhostSprites(pinky)
        pinky.mode.current_mode = CHASE
        pinky.update_goal()
        expected_goal = mock_pacman.node.position + mock_pacman.directions[mock_pacman.direction] * TILEWIDTH * 4
        assert pinky.goal == expected_goal

    def test_update_goal_scatter(self, mock_node, mock_pacman):
        pinky = Pinky(mock_node, mock_pacman)
        pinky.sprites = GhostSprites(pinky)
        pinky.mode.current_mode = SCATTER
        pinky.update_goal()
        assert pinky.goal == Vector(520, 80)

    def test_update_goal_spawn(self, mock_node, mock_pacman):
        pinky = Pinky(mock_node, mock_pacman)
        pinky.sprites = GhostSprites(pinky)
        pinky.mode.current_mode = SPAWN
        pinky.update_goal()
        assert pinky.goal == pinky.home_goal


class TestInky:
    def test_update_goal_chase(self, mock_node, mock_pacman):
        blinky = Blinky(mock_node, mock_pacman)
        blinky.sprites = GhostSprites(blinky)

        inky = Inky(mock_node, mock_pacman, blinky)
        inky.sprites = GhostSprites(inky)
        inky.mode.current_mode = CHASE
        inky.update_goal()

        pacman_plus_two = mock_pacman.position + mock_pacman.directions[mock_pacman.direction] * TILEWIDTH * 2
        expected_goal = (pacman_plus_two - blinky.position) * 2 + blinky.position
        assert inky.goal == expected_goal

    def test_update_goal_scatter(self, mock_node, mock_pacman):
        blinky = Blinky(mock_node, mock_pacman)
        blinky.sprites = GhostSprites(blinky)

        inky = Inky(mock_node, mock_pacman, blinky)
        inky.sprites = GhostSprites(inky)
        inky.mode.current_mode = SCATTER
        inky.update_goal()

        assert inky.goal == Vector(520, 640)

    def test_update_goal_spawn(self, mock_node, mock_pacman):
        blinky = Blinky(mock_node, mock_pacman)
        blinky.sprites = GhostSprites(blinky)

        inky = Inky(mock_node, mock_pacman, blinky)
        inky.sprites = GhostSprites(inky)
        inky.mode.current_mode = SPAWN
        inky.update_goal()

        assert inky.goal == inky.home_goal


class TestClyde:
    def test_update_goal_chase_far(self, mock_node, mock_pacman):
        clyde = Clyde(mock_node, mock_pacman)
        clyde.sprites = GhostSprites(clyde)
        clyde.position = Vector(500, 500)
        clyde.mode.current_mode = CHASE
        clyde.update_goal()

        expected_goal = mock_pacman.node.position + mock_pacman.directions[mock_pacman.direction] * TILEWIDTH * 4
        assert clyde.goal == expected_goal

    def test_update_goal_chase_close(self, mock_node, mock_pacman):
        clyde = Clyde(mock_node, mock_pacman)
        clyde.sprites = GhostSprites(clyde)
        clyde.position = Vector(110, 110)
        clyde.mode.current_mode = CHASE
        clyde.update_goal()

        assert clyde.mode.current_mode == SCATTER
        assert clyde.goal == Vector(0, TILEHEIGHT * NROWS)

    def test_update_goal_scatter(self, mock_node, mock_pacman):
        clyde = Clyde(mock_node, mock_pacman)
        clyde.sprites = GhostSprites(clyde)
        clyde.mode.current_mode = SCATTER
        clyde.update_goal()

        assert clyde.goal == Vector(0, TILEHEIGHT * NROWS)

    def test_update_goal_spawn(self, mock_node, mock_pacman):
        clyde = Clyde(mock_node, mock_pacman)
        clyde.sprites = GhostSprites(clyde)
        clyde.mode.current_mode = SPAWN
        clyde.update_goal()

        assert clyde.goal == clyde.home_goal


class TestGhostsGroup:
    def test_init(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        assert isinstance(ghosts_group.blinky, Blinky)
        assert isinstance(ghosts_group.pinky, Pinky)
        assert isinstance(ghosts_group.inky, Inky)
        assert isinstance(ghosts_group.clyde, Clyde)

        assert len(ghosts_group.ghosts_list) == 4
        assert ghosts_group.blinky in ghosts_group.ghosts_list
        assert ghosts_group.pinky in ghosts_group.ghosts_list
        assert ghosts_group.inky in ghosts_group.ghosts_list
        assert ghosts_group.clyde in ghosts_group.ghosts_list

    def test_iter(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        ghosts = list(ghosts_group)
        assert len(ghosts) == 4
        assert ghosts_group.blinky in ghosts
        assert ghosts_group.pinky in ghosts
        assert ghosts_group.inky in ghosts
        assert ghosts_group.clyde in ghosts

    def test_update(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.update = Mock()

        dt = 0.1
        ghosts_group.update(dt)

        for ghost in ghosts_group.ghosts_list:
            ghost.update.assert_called_once_with(dt)

    def test_set_spawn_node(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.set_spawn_node = Mock()

        new_node = Mock()
        ghosts_group.set_spawn_node(new_node)

        for ghost in ghosts_group.ghosts_list:
            ghost.set_spawn_node.assert_called_once_with(new_node)

    def test_start_freight(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.start_freight = Mock()

        ghosts_group.start_freight()

        for ghost in ghosts_group.ghosts_list:
            ghost.start_freight.assert_called_once()

        for ghost in ghosts_group.ghosts_list:
            assert ghost.points == 200

    def test_render(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.render = Mock()

        screen = Mock()

        ghosts_group.render(screen)

        for ghost in ghosts_group.ghosts_list:
            ghost.render.assert_called_once_with(screen)

    def test_updatePoints(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.points = 100

        ghosts_group.updatePoints()

        for ghost in ghosts_group.ghosts_list:
            assert ghost.points == 200

    def test_resetPoints(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.points = 400

        ghosts_group.resetPoints()

        for ghost in ghosts_group.ghosts_list:
            assert ghost.points == 200

    def test_hide(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.visible = True

        ghosts_group.hide()

        for ghost in ghosts_group.ghosts_list:
            assert ghost.visible is False

    def test_show(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.visible = False

        ghosts_group.show()

        for ghost in ghosts_group.ghosts_list:
            assert ghost.visible is True

    def test_reset(self, mock_node, mock_pacman):
        ghosts_group = GhostsGroup(mock_node, mock_pacman)

        for ghost in ghosts_group.ghosts_list:
            ghost.reset = Mock()

        ghosts_group.reset()

        for ghost in ghosts_group.ghosts_list:
            ghost.reset.assert_called_once()
