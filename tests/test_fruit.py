import pytest
import pygame
from unittest.mock import Mock, patch
from fruit import Fruit
from constants import *


pygame.init()
pygame.display.set_mode((1, 1))

# Моковий клас для вузла (Node)


class MockNode:
    def __init__(self, x=0, y=0):
        self.position = pygame.math.Vector2(x, y)
        self.neighbors = {RIGHT: None, LEFT: None, UP: None, DOWN: None}


@pytest.fixture
def node():
    return MockNode()


@pytest.fixture
def fruit(node):
    with patch('sprites.FruitSprites') as MockFruitSprites:
        MockFruitSprites.return_value = Mock()
        return Fruit(node, level=1)


class TestFruit:
    def test_init(self, fruit, node):

        assert fruit.name == FRUIT
        assert fruit.color == GREEN
        assert fruit.lifespan == 5
        assert fruit.timer == 0
        assert fruit.destroy is False
        assert fruit.points == 120  # 100 + level*20 (level=1)
        assert fruit.node == node
        assert fruit.sprites is not None

    def test_update_no_destroy(self, fruit):

        fruit.update(3)  # Менше ніж 5 секунд
        assert fruit.destroy is False

    def test_update_destroy(self, fruit):

        fruit.update(6)  # Більше ніж 5 секунд
        assert fruit.destroy is True
