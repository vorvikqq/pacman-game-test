import pygame
from pygame.constants import *
from constants import *


class SettingsMenu:
    """
    Represents the settings menu where the player can adjust game difficulty
    and background color.

    Attributes:
        game_controller (GameController): Reference to the main game controller.
        selected_option (int): Index of the currently selected menu option.
        font (pygame.font.Font): Font used for rendering menu text.
        difficulty_levels (list): List of available difficulty levels.
        background_colors (list): List of available background colors.
        options (list): Current menu options displayed to the player.
        difficulty (int): Currently selected difficulty level.
        bg_color (int): Currently selected background color index.
    """

    def __init__(self, game_controller):
        """
        Initializes the SettingsMenu.

        Args:
            game_controller (GameController): The main game controller.
        """
        self.game_controller = game_controller
        self.selected_option = 0
        self.font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 15)
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.background_colors = ['Black', 'Gray', 'Navy']
        self.options = [
            f"Difficulty: {self.difficulty_levels[self.game_controller.difficulty]}",
            f"Background Color: {self.background_colors[self.game_controller.bg_color]}"
        ]
        self.difficulty = self.game_controller.difficulty
        self.bg_color = self.game_controller.bg_color

    def render(self):
        """
        Renders the settings menu on the screen.
        Highlights the selected option in red while others remain white.
        """
        self.game_controller.screen.fill((0, 0, 0))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected_option else (255, 0, 0)
            option_text = self.font.render(option, True, color)
            self.game_controller.screen.blit(option_text, (100, 100 + i * 50))

        pygame.display.update()

    def handle_input(self, event):
        """
        Handles user input to navigate the settings menu and adjust values.

        Args:
            event (pygame.event.Event): The event to process.

        Returns:
            bool: True if the player confirms settings and exits the menu, otherwise False.
        """
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)

            if event.key == K_LEFT:
                if self.selected_option == 0:
                    self.difficulty = (self.difficulty - 1) % len(self.difficulty_levels)
                elif self.selected_option == 1:
                    self.bg_color = (self.bg_color - 1) % len(self.background_colors)

            if event.key == K_RIGHT:
                if self.selected_option == 0:
                    self.difficulty = (self.difficulty + 1) % len(self.difficulty_levels)
                elif self.selected_option == 1:
                    self.bg_color = (self.bg_color + 1) % len(self.background_colors)

            # Update the displayed text after changes
            self.options[0] = f"Difficulty: {self.difficulty_levels[self.difficulty]}"
            self.options[1] = f"Background Color: {self.background_colors[self.bg_color]}"

            if event.key == K_RETURN:
                # Save the selected settings and start the game
                self.game_controller.set_difficulty(self.difficulty)
                self.game_controller.set_background_color(self.background_colors[self.bg_color])
                self.game_controller.startGame()
                return True  # Exit settings menu
        return False
