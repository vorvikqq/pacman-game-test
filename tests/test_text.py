import pytest
import pygame
from constants import *
from unittest.mock import Mock
from text import Text, TextGroup
from vector import Vector

pygame.init()


@pytest.fixture
def screen():
    return pygame.Surface((800, 600))


@pytest.fixture
def text_instance():
    return Text("Hello", (255, 255, 255), 100, 100, 20, time=2)


@pytest.fixture
def text_group_instance():
    return TextGroup()


class TestText:
    def test_init(self, text_instance):
        assert text_instance.text == "Hello"
        assert text_instance.color == (255, 255, 255)
        assert text_instance.position == Vector(100, 100)
        assert text_instance.size == 20
        assert text_instance.showtime == 2
        assert text_instance.visible is True
        assert text_instance.destroy is False
        assert text_instance.timer == 0
        assert text_instance.label is not None

    def test_change_text(self, text_instance):
        text_instance.change_text("New Text")
        assert text_instance.text == "New Text"
        assert text_instance.label is not None

    def test_update(self, text_instance):
        text_instance.update(1)
        assert text_instance.timer == 1
        text_instance.update(1.1)
        assert text_instance.destroy is True

    def test_render(self, text_instance, screen):
        mock_screen = Mock(wraps=screen)
        text_instance.render(mock_screen)
        mock_screen.blit.assert_called_once_with(text_instance.label, (100, 100))


class TestTextGroup:
    def test_init(self, text_group_instance):
        assert text_group_instance.nextid == 7
        assert isinstance(text_group_instance.alltext, dict)

    def test_add_text(self, text_group_instance):
        text_id = text_group_instance.add_text("Test", (255, 255, 255), 50, 50, 15)
        # print(f"Assigned text_id: {text_id}")
        assert text_id == 7
        assert text_group_instance.alltext[7] is not None
        assert text_group_instance.alltext[7].text == "Test"

    def test_remove_text(self, text_group_instance):
        assert 10 not in text_group_instance.alltext

        text_id = text_group_instance.add_text("RemoveMe", (255, 255, 255), 50, 50, 15, id=10)
        print(f"Assigned text_id: {text_id}")
        assert text_group_instance.alltext[10].text == "RemoveMe"

        text_group_instance.remove_text(10)

        assert 10 not in text_group_instance.alltext

    def test_update_text(self, text_group_instance):
        text_group_instance.add_text("Test", (255, 255, 255), 50, 50, 15, id=5)
        text_group_instance.update_text(5, "Updated Text")
        assert text_group_instance.alltext[5].text == "Updated Text"

    def test_show_text(self, text_group_instance):
        text_group_instance.show_text(READYTXT)
        assert text_group_instance.alltext[READYTXT].visible is True

    def test_hide_text(self, text_group_instance):
        text_group_instance.hide_text()
        assert text_group_instance.alltext[READYTXT].visible is False
        assert text_group_instance.alltext[PAUSETXT].visible is False
        assert text_group_instance.alltext[GAMEOVERTXT].visible is False

    def test_render(self, text_group_instance, screen):
        mock_screen = Mock(wraps=screen)
        text_group_instance.render(mock_screen)
        assert all(mock_screen.blit.called for text in text_group_instance.alltext.values())
