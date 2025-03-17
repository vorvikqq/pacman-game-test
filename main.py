import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from fruit import Fruit
from ghosts import GhostsGroup
from pauser import Pause
from text import TextGroup
from music import MusicController
from sprites import LifeSprites
from sprites import MazeSprites
from mazedata import MazeData
from settings_menu import SettingsMenu


class GameController(object):
    """
    Main controller for the Pac-Man game.

    Attributes:
        screen (pygame.Surface): Main game screen.
        background (pygame.Surface): Current background surface.
        clock (pygame.time.Clock): Game clock.
        fruit (Fruit or None): Current fruit in the game.
        pause (Pause): Pause controller.
        level (int): Current game level.
        lives (int): Number of player lives.
        score (int): Player score.
        textGroup (TextGroup): Handles on-screen text.
        musicController (MusicController): Controls game music.
        lifesprites (LifeSprites): Handles life indicator sprites.
        finishBG (bool): Flag for background animation at level end.
        finishTime (float): Time between background swaps.
        finishTimer (float): Timer for background swap.
        fruit_captured (list): List of captured fruit sprites.
        mazedata (MazeData): Handles maze data.
        difficulty_levels (list): Available difficulty levels.
        background_colors (list): Available background colors.
        difficulty (int): Selected difficulty level.
        bg_color (int): Selected background color.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        pygame.display.set_caption("Pac-Man Game")
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.background_norm = None
        self.background_finish = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textGroup = TextGroup()
        self.musicController = MusicController()
        self.lifesprites = LifeSprites(self.lives)
        self.finishBG = False
        self.finishTime = 0.2
        self.finishTimer = 0
        self.fruit_captured = []
        self.mazedata = MazeData()
        self.difficulty_levels = ["Easy", "Medium", "Hard"]
        self.background_colors = [BLACK, GRAY, NAVY]
        self.difficulty = 1
        self.bg_color = 0

    def set_difficulty(self, difficulty_level):
        """
        Sets the game difficulty and adjusts lives accordingly.

        Args:
            difficulty_level (int): Difficulty index (0 = Easy, 1 = Medium, 2 = Hard).
        """
        self.difficulty = difficulty_level

        if self.difficulty == 0:
            self.lives = 6
        elif self.difficulty == 1:
            self.lives = 4
        elif self.difficulty == 2:
            self.lives = 3

        self.lifesprites.reset_lives(self.lives)

    def set_background_color(self, color):
        """
        Sets the background color of the game.

        Args:
            color (int): Index of background color in background_colors list.
        """
        self.bg_color = color

    def restart_game(self):
        """
        Restarts the game, resetting all attributes to initial values.
        """
        self.lives = 5
        self.level = 0
        self.score = 0
        self.textGroup.update_score(self.score)
        self.textGroup.update_level(self.level)
        self.textGroup.show_text(READYTXT)
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.lifesprites.reset_lives(self.lives)
        self.fruit_captured = []

    def reset_level(self):
        """
        Resets the current level without restarting the game.
        """
        self.pause.paused = True
        self.textGroup.show_text(READYTXT)
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None

    def next_level(self):
        """
        Advances to the next level.
        """
        self.show_entities()
        self.level += 1
        self.textGroup.update_level(self.level)
        self.pause.paused = True
        self.startGame()

    def setBackground(self):
        """
        Sets the background surfaces for the game.

        This method creates two background surfaces: one for normal gameplay and one for
        the finishing sequence. Both are filled with the selected background color and then
        updated using the maze sprites to add level-specific visual elements.
        """
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(self.bg_color)
        self.background_finish = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_finish.fill(self.bg_color)
        self.background_norm = self.mazesprites.construct_background(self.background_norm, self.level % 5)
        self.background_finish = self.mazesprites.construct_background(self.background_finish, 5)
        self.finishBG = False
        self.background = self.background_norm

    def startGame(self):
        """
        Initializes and starts a new game level.

        This method sets up the maze, loads necessary game objects such as Pac-Man, ghosts,
        pellets, and nodes, and applies various constraints to regulate ghost behavior.
        """
        self.mazedata.load_maze(self.level)
        self.mazesprites = MazeSprites('mazes/' + self.mazedata.obj.name + ".txt", 'mazes/' + self.mazedata.obj.name + "_rotation.txt")
        self.setBackground()
        self.musicController.play_bg_music()
        self.nodes = NodeGroup('mazes/' + self.mazedata.obj.name + ".txt")
        self.mazedata.obj.set_portal_pairs(self.nodes)
        self.mazedata.obj.connect_home_nodes(self.nodes)

        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacman_start))
        self.pelletGroup = PelletGroup('mazes/' + self.mazedata.obj.name + ".txt")
        self.ghosts = GhostsGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.pinky.set_spawn_node(self.nodes.getNodeFromTiles(*self.mazedata.obj.add_offset(2, 3)))
        self.ghosts.inky.set_spawn_node(self.nodes.getNodeFromTiles(*self.mazedata.obj.add_offset(0, 3)))
        self.ghosts.clyde.set_spawn_node(self.nodes.getNodeFromTiles(*self.mazedata.obj.add_offset(4, 3)))
        self.ghosts.blinky.set_spawn_node(self.nodes.getNodeFromTiles(*self.mazedata.obj.add_offset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.spawn_node.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.spawn_node.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.deny_ghosts_access(self.ghosts, self.nodes)

    def update(self):
        """
        Updates all game objects and handles game logic per frame.
        """
        dt = self.clock.tick(60) / 1000.0
        self.textGroup.update(dt)
        self.pelletGroup.update(dt)

        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkFruitEvents()
            self.checkGhostEvents()
        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)
        if self.finishBG:
            self.finishTimer += dt
            if self.finishTimer >= self.finishTime:
                self.finishTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_finish
                else:
                    self.background = self.background_norm
        after_pause_method = self.pause.update(dt)
        if after_pause_method is not None:
            after_pause_method()
        self.checkEvents()
        self.render()

    def update_score(self, points):
        """
        Updates the player's score.

        Args:
            points (int): Points to add to the score.
        """
        self.score += points
        self.textGroup.update_score(self.score)

    def checkFruitEvents(self):
        """
        Handles fruit spawning and collection events.
        """
        if self.pelletGroup.num_eaten == 50 or self.pelletGroup.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.musicController.play_pacman_eat_music()
                self.update_score(self.fruit.points)
                self.textGroup.add_text(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)

                # Ensure the captured fruit is stored only if it is unique
                fruit_captured = False
                for fruit in self.fruit_captured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruit_captured = True
                        break
                if not fruit_captured:
                    self.fruit_captured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkPelletEvents(self):
        """
        Handles pellet consumption and power-up activation.
        """
        pellet = self.pacman.eatPellets(self.pelletGroup.pellets)
        if pellet:
            self.pelletGroup.num_eaten += 1
            self.musicController.play_pacman_eat_music()
            self.update_score(pellet.points)

            if self.pelletGroup.num_eaten == 30:
                self.ghosts.inky.spawn_node.allowAccess(RIGHT, self.ghosts.inky)
            if self.pelletGroup.num_eaten == 70:
                self.ghosts.clyde.spawn_node.allowAccess(LEFT, self.ghosts.clyde)

            self.pelletGroup.pellets.remove(pellet)

            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()

            if self.pelletGroup.is_empty():
                self.finishBG = True
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    def checkEvents(self):
        """
        Handles player input and general game events.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.textGroup.hide_text()
                            self.show_entities()
                        else:
                            self.textGroup.show_text(PAUSETXT)
                            self.hide_entities()

                if event.key == K_m:
                    self.musicController.pause_music()

    def checkGhostEvents(self):
        """
        Handles interactions between Pac-Man and ghosts.
        """
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current_mode is FREIGHT:
                    self.musicController.play_pacman_eat_ghost()
                    self.pacman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.textGroup.add_text(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current_mode is not SPAWN:
                    if self.pacman.alive:
                        self.musicController.play_pacman_die()
                        self.lives -= 1
                        self.lifesprites.remove_image()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textGroup.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pause_time=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=3, func=self.reset_level)

    def show_entities(self):
        """
        Makes Pac-Man and ghosts visible.
        """
        self.pacman.visible = True
        self.ghosts.show()

    def hide_entities(self):
        """
        Hides Pac-Man and ghosts from the screen.
        """
        self.pacman.visible = False
        self.ghosts.hide()

    def render(self):
        """
        Renders all game objects onto the screen.
        """
        self.screen.blit(self.background, (0, 0))
        self.pelletGroup.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textGroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        for i in range(len(self.fruit_captured)):
            x = SCREENWIDTH - self.fruit_captured[i].get_width() * (i + 1)
            y = SCREENHEIGHT - self.fruit_captured[i].get_height()
            self.screen.blit(self.fruit_captured[i], (x, y))

        pygame.display.update()


if __name__ == "__main__":
    game = GameController()
    settings_menu = SettingsMenu(game)

    running = True
    in_settings_menu = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            if in_settings_menu:
                if settings_menu.handle_input(event):
                    in_settings_menu = False

        if in_settings_menu:
            settings_menu.render()
        else:
            game.update()

    pygame.quit()
