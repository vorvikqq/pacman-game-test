import pytest
from unittest.mock import Mock
from constants import *
from modes import ModeController, DefaultMode
from vector import Vector


class TestDefaultMode:
    def test_init(self):
        mode = DefaultMode(start_mode=WAIT)
        assert mode.mode == WAIT
        assert mode.timer == 0
        assert mode.time == 3

    def test_set_mode(self):
        mode = DefaultMode()

        mode.set_mode(SCATTER)
        assert mode.mode == SCATTER
        assert mode.time == 7
        assert mode.timer == 0

        mode.set_mode(CHASE)
        assert mode.mode == CHASE
        assert mode.time == 20
        assert mode.timer == 0

        mode.set_mode(FREIGHT)
        assert mode.mode == FREIGHT
        assert mode.time == 7
        assert mode.timer == 0

    def test_update(self):
        mode = DefaultMode(start_mode=WAIT)

        mode.update(1.5)
        assert mode.timer == 1.5
        assert mode.mode == WAIT

        mode.update(2.0)
        assert mode.mode == SCATTER
        assert mode.timer == 0

    def test_reset_mode(self):
        mode = DefaultMode(start_mode=FREIGHT)

        mode.reset_mode()
        assert mode.mode == SCATTER

        mode.set_mode(WAIT)
        mode.reset_mode()
        assert mode.mode == SCATTER


@pytest.fixture
def mock_ghost():
    ghost = Mock()
    ghost.update_move_method = Mock()
    ghost.normal_mode = Mock()
    ghost.node = Mock()
    ghost.node.position = Vector(0, 0)
    ghost.home_goal = Vector(100, 100)
    ghost.spawn_node = Mock()
    return ghost


class TestModeController:
    def test_init(self, mock_ghost):
        controller = ModeController(mock_ghost, start_mode=WAIT)

        assert isinstance(controller.main_mode, DefaultMode)
        assert controller.current_mode == WAIT
        assert controller.ghost == mock_ghost

    def test_update(self, mock_ghost):
        controller = ModeController(mock_ghost, start_mode=WAIT)

        controller.update(1.5)
        assert controller.main_mode.timer == 1.5
        assert controller.current_mode == WAIT

        controller.update(2.0)
        assert controller.current_mode == SCATTER
        assert controller.main_mode.timer == 0

    def test_set_mode(self, mock_ghost):
        controller = ModeController(mock_ghost)

        controller.set_mode(CHASE)
        assert controller.current_mode == CHASE
        mock_ghost.update_move_method.assert_called_once()

    def test_set_freight_mode(self, mock_ghost):
        controller = ModeController(mock_ghost, start_mode=CHASE)

        controller.set_freight_mode()
        assert controller.current_mode == FREIGHT
        assert controller.timer == 0
        assert controller.time == 7

        controller.set_mode(SPAWN)
        controller.set_freight_mode()
        assert controller.current_mode == SPAWN

    def test_set_spawn_mode(self, mock_ghost):
        controller = ModeController(mock_ghost, start_mode=FREIGHT)

        controller.set_spawn_mode()
        assert controller.current_mode == SPAWN

        controller.set_mode(CHASE)
        controller.set_spawn_mode()
        assert controller.current_mode == CHASE
