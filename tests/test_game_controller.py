import unittest
from unittest.mock import MagicMock, patch
from constants import *
from pacman import Pacman
from ghosts import GhostsGroup
from pellets import PelletGroup
from fruit import Fruit
from nodes import NodeGroup
from text import TextGroup
from music import MusicController
from sprites import LifeSprites, MazeSprites
from mazedata import MazeData
from main import GameController


class TestGameController(unittest.TestCase):
    @patch('pygame.display.set_mode')
    def setUp(self, mock_set_mode):
        mock_set_mode.return_value = MagicMock()

        with patch('pygame.init'), \
                patch('pygame.time.Clock', return_value=MagicMock()):
            self.game = GameController()

        self.mock_pacman = MagicMock(spec=Pacman)
        self.mock_ghosts = MagicMock(spec=GhostsGroup)
        self.mock_pellet_group = MagicMock(spec=PelletGroup)
        self.mock_pellet_group.num_eaten = None
        self.mock_pellet_group.pellets = None
        self.mock_text_group = MagicMock(spec=TextGroup)
        self.mock_music_controller = MagicMock(spec=MusicController)
        self.mock_nodes = MagicMock(spec=NodeGroup)
        self.mock_maze_sprites = MagicMock(spec=MazeSprites)
        self.mock_maze_data = MagicMock(spec=MazeData)

        self.game.pacman = self.mock_pacman
        self.game.ghosts = self.mock_ghosts
        self.game.pelletGroup = self.mock_pellet_group
        self.game.textGroup = self.mock_text_group
        self.game.musicController = self.mock_music_controller
        self.game.nodes = self.mock_nodes
        self.game.mazesprites = self.mock_maze_sprites
        self.game.mazedata = self.mock_maze_data

        self.game.screen = MagicMock()

        self.mock_pacman.alive = True
        self.mock_pacman.visible = True

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(self.game.level, 0)
        self.assertEqual(self.game.lives, 5)
        self.assertEqual(self.game.score, 0)
        self.assertTrue(self.game.pause.paused)
        self.assertIsNone(self.game.fruit)
        self.assertFalse(self.game.finishBG)
        self.assertEqual(self.game.difficulty, 1)
        self.assertEqual(self.game.bg_color, 0)

    def test_set_difficulty(self):
        self.game.lifesprites = MagicMock(spec=LifeSprites)

        # Тест Легкого рівня
        self.game.set_difficulty(0)
        self.assertEqual(self.game.difficulty, 0)
        self.assertEqual(self.game.lives, 6)
        self.game.lifesprites.reset_lives.assert_called_with(6)

        # Тест Середнього рівня
        self.game.set_difficulty(1)
        self.assertEqual(self.game.difficulty, 1)
        self.assertEqual(self.game.lives, 4)
        self.game.lifesprites.reset_lives.assert_called_with(4)

        # Тест Складного рівня
        self.game.set_difficulty(2)
        self.assertEqual(self.game.difficulty, 2)
        self.assertEqual(self.game.lives, 3)
        self.game.lifesprites.reset_lives.assert_called_with(3)

    def test_set_background_color(self):
        for i in range(len(self.game.background_colors)):
            self.game.set_background_color(i)
            self.assertEqual(self.game.bg_color, i)

    def test_update_score(self):
        initial_score = self.game.score
        self.game.update_score(100)
        self.assertEqual(self.game.score, initial_score + 100)
        self.game.textGroup.update_score.assert_called_with(self.game.score)

    def test_restart_game(self):
        self.game.lives = 2
        self.game.level = 3
        self.game.score = 500

        self.game.lifesprites = MagicMock(spec=LifeSprites)
        self.game.startGame = MagicMock()
        self.game.restart_game()

        # Перевіряємо, що значення повернулися до початкових
        self.assertEqual(self.game.lives, 5)
        self.assertEqual(self.game.level, 0)
        self.assertEqual(self.game.score, 0)
        self.assertTrue(self.game.pause.paused)
        self.assertIsNone(self.game.fruit)
        self.game.startGame.assert_called_once()
        self.game.textGroup.show_text.assert_called_with(READYTXT)

    def test_next_level(self):
        initial_level = self.game.level

        self.game.startGame = MagicMock()
        self.game.show_entities = MagicMock()
        self.game.next_level()

        self.assertEqual(self.game.level, initial_level + 1)
        self.assertTrue(self.game.pause.paused)
        self.game.show_entities.assert_called_once()
        self.game.startGame.assert_called_once()
        self.game.textGroup.update_level.assert_called_with(self.game.level)

    def test_reset_level(self):
        self.game.reset_level()

        self.assertTrue(self.game.pause.paused)
        self.game.textGroup.show_text.assert_called_with(READYTXT)
        self.mock_pacman.reset.assert_called_once()
        self.mock_ghosts.reset.assert_called_once()
        self.assertIsNone(self.game.fruit)

    def test_check_pellet_events_empty(self):
        self.mock_pacman.eatPellets.return_value = None
        self.game.checkPelletEvents()

        self.mock_pacman.eatPellets.assert_called_once()
        self.game.musicController.play_pacman_eat_music.assert_not_called()

    def test_set_background(self):
        with patch('pygame.surface.Surface', return_value=MagicMock()):
            self.game.background_norm = MagicMock()
            self.game.background_finish = MagicMock()
            self.mock_maze_sprites.construct_background.side_effect = lambda bg, level: bg

            self.game.level = 3
            self.game.setBackground()

            self.assertEqual(self.mock_maze_sprites.construct_background.call_count, 2)
            self.assertFalse(self.game.finishBG)
            self.assertEqual(self.game.background, self.game.background_norm)

    def test_show_and_hide_entities(self):
        self.game.hide_entities()
        self.assertFalse(self.mock_pacman.visible)
        self.mock_ghosts.hide.assert_called_once()

        self.game.show_entities()
        self.assertTrue(self.mock_pacman.visible)
        self.mock_ghosts.show.assert_called_once()

    def test_check_ghost_events_pacman_eats_ghost(self):
        mock_ghost = MagicMock()
        mock_ghost.mode.current_mode = FREIGHT
        mock_ghost.points = 200
        mock_ghost.position = MagicMock(x=100, y=100)

        self.mock_ghosts.__iter__.return_value = [mock_ghost]
        self.mock_pacman.collide_ghost.return_value = True

        self.game.update_score = MagicMock()
        self.game.show_entities = MagicMock()
        self.game.pause = MagicMock()

        self.game.checkGhostEvents()

        self.mock_pacman.collide_ghost.assert_called_with(mock_ghost)
        self.game.musicController.play_pacman_eat_ghost.assert_called_once()
        self.assertFalse(self.mock_pacman.visible)
        self.assertFalse(mock_ghost.visible)
        self.game.update_score.assert_called_with(200)
        mock_ghost.start_spawn.assert_called_once()

    def test_check_ghost_events_ghost_kills_pacman(self):
        mock_ghost = MagicMock()
        mock_ghost.mode.current_mode = "CHASE"

        self.mock_ghosts.__iter__.return_value = [mock_ghost]

        self.mock_pacman.collide_ghost.return_value = True
        self.mock_pacman.alive = True

        initial_lives = self.game.lives

        self.game.lifesprites = MagicMock(spec=LifeSprites)

        self.game.reset_level = MagicMock()
        self.game.restart_game = MagicMock()
        self.game.pause = MagicMock()

        self.game.checkGhostEvents()

        self.mock_pacman.collide_ghost.assert_called_with(mock_ghost)
        self.game.musicController.play_pacman_die.assert_called_once()
        self.assertEqual(self.game.lives, initial_lives - 1)
        self.mock_pacman.die.assert_called_once()
        self.mock_ghosts.hide.assert_called_once()

    def test_check_fruit_events(self):
        mock_fruit = MagicMock(spec=Fruit)
        mock_fruit.points = 100
        mock_fruit.position = MagicMock(x=100, y=100)
        mock_fruit.image = MagicMock()
        mock_fruit.image.get_offset.return_value = (0, 0)
        self.game.fruit = mock_fruit

        self.mock_pacman.collideCheck.return_value = True

        self.game.update_score = MagicMock()
        self.game.textGroup = MagicMock(spec=TextGroup)

        self.game.checkFruitEvents()

        self.mock_pacman.collideCheck.assert_called_with(mock_fruit)
        self.game.musicController.play_pacman_eat_music.assert_called_once()
        self.game.update_score.assert_called_with(100)
        self.assertIsNone(self.game.fruit)
        self.assertEqual(len(self.game.fruit_captured), 1)
