import pytest
from unittest.mock import Mock
from pauser import Pause


@pytest.fixture
def pause():
    return Pause()


@pytest.fixture
def mock_func():
    return Mock()


class TestPause:

    def test_initialization(self, pause):
        assert pause.paused == False
        assert pause.timer == 0
        assert pause.pause_time is None
        assert pause.func is None

    def test_set_pause(self, pause, mock_func):
        pause.set_pause(player_paused=True, pause_time=5, func=mock_func)

        assert pause.paused
        assert pause.pause_time == 5
        assert pause.func == mock_func
        assert pause.timer == 0

    def test_toggle_pause(self, pause):
        assert pause.paused == False
        pause.flip()
        assert pause.paused
        pause.flip()
        assert pause.paused == False

    def test_update_no_pause(self, pause):
        result = pause.update(1)
        assert result is None
        assert pause.paused == False

    def test_update_with_pause(self, pause, mock_func):
        pause.set_pause(player_paused=True, pause_time=5, func=mock_func)

        result = pause.update(3)
        assert result is None
        assert pause.paused
        assert pause.timer == 3

        result = pause.update(2)
        assert result is mock_func
        assert pause.paused == False
        assert pause.timer == 0

    def test_set_pause_with_no_time(self, pause, mock_func):
        pause.set_pause(player_paused=True, pause_time=None, func=mock_func)

        assert pause.paused
        assert pause.func == mock_func
        assert pause.pause_time is None

    def test_update_during_no_time_pause(self, pause):
        pause.set_pause(player_paused=True, pause_time=None, func=None)

        result = pause.update(1)
        assert result is None
        assert pause.paused
        assert pause.timer == 0
