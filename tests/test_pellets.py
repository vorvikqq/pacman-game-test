import pytest
import pygame
import numpy as np
from unittest.mock import Mock, patch
from pellets import Pellet, PowerPellet, PelletGroup
from vector import Vector

pygame.init()


@pytest.fixture
def screen():
    return pygame.display.set_mode((800, 600))


@pytest.fixture
def pellet():
    return Pellet(1, 1)


@pytest.fixture
def power_pellet():
    return PowerPellet(1, 1)


@pytest.fixture
def pellet_group(tmp_path):
    pellet_data = """X X X X X X X X X X X X X X X X X X X X X X X X X X X X
X X X X X X X X X X X X X X X X X X X X X X X X X X X X
X X X X X X X X X X X X X X X X X X X X X X X X X X X X
0 1 1 1 1 1 1 1 1 1 1 1 1 7 8 1 1 1 1 1 1 1 1 1 1 1 1 0
1 + . . . . + . . . . . + 3 3 + . . . . . + . . . . + 1
1 . 2 3 3 2 . 2 3 3 3 2 . 3 3 . 2 3 3 3 2 . 2 3 3 2 P 1"""
    p = tmp_path / "test_pellets.txt"
    p.write_text(pellet_data)
    return PelletGroup(str(p))


class TestPellet:
    def test_init(self, pellet):
        assert isinstance(pellet.position, Vector)
        assert pellet.color == (255, 255, 0)
        assert pellet.points == 10
        assert pellet.visible

    def test_render_visible(self, pellet, screen):
        pellet.visible = True
        with patch.object(pygame, 'draw') as mock_draw:
            pellet.render(screen)
            mock_draw.circle.assert_called_once()

    def test_render_not_visible(self, pellet, screen):
        pellet.visible = False
        with patch.object(pygame, 'draw') as mock_draw:
            pellet.render(screen)
            mock_draw.circle.assert_not_called()


class TestPowerPellet:
    def test_init(self, power_pellet):
        assert power_pellet.points == 50
        assert power_pellet.radius > Pellet(1, 1).radius
        assert power_pellet.flash_time == 0.4

    def test_update_blinking(self, power_pellet):
        initial_visible = power_pellet.visible
        power_pellet.update(0.5)
        assert power_pellet.visible != initial_visible
        assert power_pellet.timer == 0

    def test_update_no_blinking(self, power_pellet):
        initial_visible = power_pellet.visible
        power_pellet.update(0.2)
        assert power_pellet.visible == initial_visible
        assert power_pellet.timer == 0.2


class TestPelletGroup:
    def test_init(self, pellet_group):
        assert isinstance(pellet_group.pellets, list)
        assert isinstance(pellet_group.power_pellets, list)
        assert pellet_group.num_eaten == 0
        assert len(pellet_group.pellets) == 30
        assert len(pellet_group.power_pellets) == 1

    def test_update(self, pellet_group):
        with patch.object(PowerPellet, 'update') as mock_update:
            pellet_group.update(0.1)
            assert mock_update.call_count == len(pellet_group.power_pellets)

    def test_read_pellet_file(self, pellet_group, tmp_path):
        data = ". . . .\nP . . .\n. . . ."
        p = tmp_path / "test.txt"
        p.write_text(data)
        result = pellet_group.read_pellet_file(str(p))
        assert isinstance(result, np.ndarray)
        assert result.shape == (3, 4), f"Очікувана форма (3, 4), отримано {result.shape}"

    def test_is_empty(self, pellet_group):
        assert not pellet_group.is_empty()
        pellet_group.pellets.clear()
        assert pellet_group.is_empty()

    def test_render(self, pellet_group, screen):
        with patch.object(Pellet, 'render') as mock_render:
            pellet_group.render(screen)
            assert mock_render.call_count == len(pellet_group.pellets)
