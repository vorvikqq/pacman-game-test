import pytest
import pygame
from pygame.locals import *
from unittest.mock import Mock, patch
from pacman import Pacman
from nodes import Node
from vector import Vector
from constants import *

pygame.init()


@pytest.fixture
def node():
    node = Mock(spec=Node)
    node.position = Vector(0, 0)
    node.neighbors = {LEFT: None, RIGHT: None, UP: None, DOWN: None, PORTAL: None}
    return node


@pytest.fixture
def pacman(node):
    with patch('pacman.PacmanSprites'):
        return Pacman(node)


@pytest.fixture
def pellet():
    pellet = Mock()
    pellet.position = Vector(0, 0)
    pellet.collide_radius = 5
    return pellet


@pytest.fixture
def ghost():
    ghost = Mock()
    ghost.position = Vector(0, 0)
    ghost.collide_radius = 5
    return ghost


class TestPacman:
    def test_init(self, pacman, node):
        assert pacman.name == PACMAN
        assert pacman.direction == LEFT
        assert pacman.speed == 100 * TILEWIDTH / 16
        assert pacman.radius == 10
        assert pacman.color == YELLOW
        assert pacman.node == node
        assert pacman.target == node
        assert pacman.alive
        assert pacman.sprites is not None

    def test_reset(self, pacman):
        pacman.alive = False
        pacman.direction = STOP
        with patch.object(pacman.sprites, 'reset') as mock_reset:
            pacman.reset()
            assert pacman.direction == LEFT
            assert pacman.alive
            mock_reset.assert_called_once()

    def test_die(self, pacman):
        pacman.alive = True
        pacman.direction = RIGHT
        pacman.die()
        assert pacman.alive == False
        assert pacman.direction == STOP

    def test_get_valid_key(self, pacman):
        with patch('pygame.key.get_pressed') as mock_key_pressed:
            mock_key_pressed.return_value = {K_UP: True, K_DOWN: False, K_LEFT: False, K_RIGHT: False}
            assert pacman.getValidKey() == UP

            mock_key_pressed.return_value = {K_UP: False, K_DOWN: True, K_LEFT: False, K_RIGHT: False}
            assert pacman.getValidKey() == DOWN

            mock_key_pressed.return_value = {K_UP: False, K_DOWN: False, K_LEFT: False, K_RIGHT: False}
            assert pacman.getValidKey() == STOP

    def test_update_no_overshot(self, pacman):
        pacman.direction = RIGHT
        pacman.position = Vector(0, 0)
        with patch.object(pacman.sprites, 'update') as mock_update:
            with patch.object(pacman, 'overshot_target', return_value=False):
                with patch.object(pacman, 'getValidKey', return_value=LEFT):
                    pacman.update(0.1)
                    assert pacman.position.x > 0  # Рух вправо
                    assert pacman.direction == LEFT  # Зміна напрямку на протилежний
                    mock_update.assert_called_once_with(0.1)

    def test_update_overshot(self, pacman, node):
        pacman.direction = RIGHT
        pacman.position = Vector(0, 0)
        next_node = Mock(spec=Node)
        next_node.position = Vector(TILEWIDTH, 0)
        next_node.neighbors = {LEFT: None, RIGHT: None, UP: None, DOWN: None, PORTAL: None}
        node.neighbors[RIGHT] = next_node
        pacman.target = next_node
        with patch.object(pacman.sprites, 'update') as mock_sprites_update:
            with patch.object(pacman, 'overshot_target', return_value=True):
                with patch.object(pacman, 'getValidKey', return_value=RIGHT):
                    with patch.object(pacman, 'get_new_target', return_value=next_node):
                        with patch.object(pacman, 'set_position'):
                            pacman.update(0.1)
                            assert pacman.node == next_node
                            assert pacman.target == next_node
                            assert pacman.direction == STOP
                            mock_sprites_update.assert_called_once_with(0.1)

    def test_eat_pellets_collision(self, pacman, pellet):
        pacman.position = Vector(0, 0)
        pacman.collide_radius = 10
        pellet_list = [pellet]
        result = pacman.eatPellets(pellet_list)
        assert result == pellet

    def test_eat_pellets_no_collision(self, pacman, pellet):
        pacman.position = Vector(20, 20)  # Далеко від pellet
        pacman.collide_radius = 10
        pellet_list = [pellet]
        result = pacman.eatPellets(pellet_list)
        assert result is None

    def test_collide_ghost(self, pacman, ghost):
        pacman.position = Vector(0, 0)
        pacman.collide_radius = 10
        result = pacman.collide_ghost(ghost)
        assert result

    def test_collide_check(self, pacman, pellet):
        pacman.position = Vector(0, 0)
        pacman.collide_radius = 10
        assert pacman.collideCheck(pellet)

        pacman.position = Vector(20, 20)  # Далеко
        assert pacman.collideCheck(pellet) == False
