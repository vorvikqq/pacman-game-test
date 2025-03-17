import pytest
from unittest.mock import Mock, patch
import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RETURN
from settings_menu import SettingsMenu

pygame.init()


@pytest.fixture(autouse=True)
def mock_pygame_font():
    with patch('pygame.font.Font') as mock_font:
        mock_font.return_value = Mock()
        yield mock_font


@pytest.fixture(autouse=True)
def mock_pygame_display():
    with patch('pygame.display.update') as mock_update:
        yield mock_update


@pytest.fixture
def game_controller():
    controller = Mock()
    controller.difficulty = 0
    controller.bg_color = 0
    controller.screen = Mock()
    return controller


@pytest.fixture
def settings_menu(game_controller):
    return SettingsMenu(game_controller)


class TestSettingsMenu:
    def test_initialization(self, settings_menu):
        assert settings_menu.selected_option == 0
        assert settings_menu.difficulty == 0
        assert settings_menu.bg_color == 0
        assert settings_menu.difficulty_levels == ["Easy", "Medium", "Hard"]
        assert settings_menu.background_colors == ['Black', 'Gray', 'Navy']
        assert len(settings_menu.options) == 2

    def test_render(self, settings_menu):
        settings_menu.render()

        settings_menu.game_controller.screen.fill.assert_called_with((0, 0, 0))
        assert settings_menu.game_controller.screen.blit.call_count == len(settings_menu.options)

    def test_handle_input_up(self, settings_menu):
        initial_selected_option = settings_menu.selected_option
        event = Mock(type=pygame.KEYDOWN, key=K_UP)

        settings_menu.handle_input(event)
        assert settings_menu.selected_option == (initial_selected_option - 1) % len(settings_menu.options)

    def test_handle_input_down(self, settings_menu):
        initial_selected_option = settings_menu.selected_option
        event = Mock(type=pygame.KEYDOWN, key=K_DOWN)

        settings_menu.handle_input(event)
        assert settings_menu.selected_option == (initial_selected_option + 1) % len(settings_menu.options)

    def test_handle_input_left(self, settings_menu):
        event = Mock(type=pygame.KEYDOWN, key=K_LEFT)

        # Рівень складності
        settings_menu.selected_option = 0
        initial_difficulty = settings_menu.difficulty
        settings_menu.handle_input(event)
        assert settings_menu.difficulty == (initial_difficulty - 1) % len(settings_menu.difficulty_levels)

        # Колір фону
        settings_menu.selected_option = 1
        initial_bg_color = settings_menu.bg_color
        settings_menu.handle_input(event)
        assert settings_menu.bg_color == (initial_bg_color - 1) % len(settings_menu.background_colors)

    def test_handle_input_right(self, settings_menu):
        event = Mock(type=pygame.KEYDOWN, key=K_RIGHT)

        # Рівень складності
        settings_menu.selected_option = 0
        initial_difficulty = settings_menu.difficulty
        settings_menu.handle_input(event)
        assert settings_menu.difficulty == (initial_difficulty + 1) % len(settings_menu.difficulty_levels)

        # Колір фону
        settings_menu.selected_option = 1
        initial_bg_color = settings_menu.bg_color
        settings_menu.handle_input(event)
        assert settings_menu.bg_color == (initial_bg_color + 1) % len(settings_menu.background_colors)

    def test_handle_input_confirm(self, settings_menu):
        event = Mock(type=pygame.KEYDOWN, key=K_RETURN)

        settings_menu.handle_input(event)

        settings_menu.game_controller.set_difficulty.assert_called_with(settings_menu.difficulty)
        settings_menu.game_controller.set_background_color.assert_called_with(
            settings_menu.background_colors[settings_menu.bg_color])
        settings_menu.game_controller.startGame.assert_called_once()
