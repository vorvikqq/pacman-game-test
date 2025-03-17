import pytest
import pygame
from unittest.mock import Mock
from entity import Entity
from vector import Vector
from constants import *


@pytest.fixture
def mock_node():
    node = Mock()
    node.position = Vector(0, 0)
    node.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
    node.access = {UP: [], DOWN: [], LEFT: [], RIGHT: []}
    return node


@pytest.fixture
def entity(mock_node):
    return Entity(mock_node)


def test_initialization(entity, mock_node):
    assert entity.node == mock_node
    assert entity.target == mock_node
    assert entity.home_goal == mock_node.position
    assert entity.position == mock_node.position
    assert entity.speed == 100 * TILEWIDTH / 16
    assert entity.direction == UP


def test_set_position(entity):
    entity.node.position = Vector(5, 5)
    entity.set_position()
    assert entity.position == Vector(5, 5)


def test_set_spawn_node(entity, mock_node):
    entity.set_spawn_node(mock_node)
    assert entity.node == mock_node
    assert entity.target == mock_node
    assert entity.home_goal == mock_node.position
    assert entity.spawn_node == mock_node
    assert entity.position == mock_node.position
    assert entity.direction == UP


def test_valid_direction(entity, mock_node):
    mock_node.neighbors[UP] = Mock()
    mock_node.access[UP] = [entity.name]
    assert entity.valid_direction(UP) is True
    assert entity.valid_direction(DOWN) is False


def test_reverse_direction():
    node_mock = Mock()
    target_mock = Mock()

    entity = Entity(node_mock)
    entity.target = target_mock

    entity.reverse_direction()

    assert entity.node == target_mock
    assert entity.target == node_mock


def test_set_speed(entity):
    entity.set_speed(2.0)
    assert entity.speed == 2.0 * TILEWIDTH / 16


def test_reset(entity):
    entity.direction = RIGHT
    entity.visible = False
    entity.set_speed(5.0)
    entity.reset()
    assert entity.direction == STOP
    assert entity.visible is True
    assert entity.speed == 100 * TILEWIDTH / 16


def test_overshot_target():
    node_mock = Mock()
    node_mock.position = Vector(0, 0)

    target_mock = Mock()
    target_mock.position = Vector(10, 0)

    entity = Entity(node_mock)
    entity.target = target_mock

    entity.position = Vector(5, 0)
    assert not entity.overshot_target()

    entity.position = Vector(15, 0)
    assert entity.overshot_target()

    entity.target = None
    assert not entity.overshot_target()
