import pytest
from unittest.mock import Mock, patch
import pygame
from music import MusicController


@pytest.fixture
def music_controller():
    return MusicController()


def test_initialization(music_controller):
    assert music_controller.sound_status
    assert round(pygame.mixer.music.get_volume(), 2) == 0.15
    assert round(music_controller.pacman_eat_sound.get_volume(), 2) == 0.5
    assert round(music_controller.pacman_eat_ghost_sound.get_volume(), 2) == 0.15
    assert round(music_controller.pacman_die_sound.get_volume(), 2) == 0.15


def test_play_bg_music(music_controller):
    with patch('pygame.mixer.music.play') as mock_play:
        music_controller.play_bg_music()
        mock_play.assert_called_once()


def test_play_pacman_eat_music(music_controller):
    music_controller.pacman_eat_sound = Mock()
    music_controller.pacman_eat_sound.get_num_channels.return_value = 0

    music_controller.play_pacman_eat_music()
    music_controller.pacman_eat_sound.play.assert_called_once()

    music_controller.sound_status = False
    music_controller.play_pacman_eat_music()
    music_controller.pacman_eat_sound.play.assert_called_once()


def test_play_pacman_eat_ghost(music_controller):
    music_controller.pacman_eat_ghost_sound = Mock()

    music_controller.play_pacman_eat_ghost()
    music_controller.pacman_eat_ghost_sound.play.assert_called_once()

    music_controller.sound_status = False
    music_controller.play_pacman_eat_ghost()
    music_controller.pacman_eat_ghost_sound.play.assert_called_once()


def test_play_pacman_die(music_controller):
    music_controller.pacman_die_sound = Mock()
    music_controller.pacman_eat_sound = Mock()

    with patch.object(pygame.mixer.music, 'stop', Mock()) as mock_stop_music:
        music_controller.play_pacman_die()
        mock_stop_music.assert_called_once()
        music_controller.pacman_eat_sound.stop.assert_called_once()
        music_controller.pacman_die_sound.play.assert_called_once()


def test_pause_music_unpause(music_controller):
    with patch('pygame.mixer.music.pause') as mock_pause, \
            patch('pygame.mixer.music.unpause') as mock_unpause:

        music_controller.pause_music()
        mock_pause.assert_called_once()
        assert music_controller.sound_status == False

        music_controller.pause_music()
        mock_unpause.assert_called_once()
        assert music_controller.sound_status
