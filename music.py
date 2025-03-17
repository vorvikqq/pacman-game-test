import pygame


class MusicController():
    """
    Class that controlles all sounds in game(music, eating pellets etc.)
    sound_status (bool): Status for either playing sounds or not.
    pacman_eat_sound (pygame.mixer.Sound): sound of eating pellet downloaded by pygame.mixer.
    pacman_eat_ghost_sound  (pygame.mixer.Sound): sound of eating ghost downloaded by pygame.mixer.
    pacman_die_sound (pygame.mixer.Sound): sound of pacman dying by ghost downloaded by pygame.mixer.

    """

    def __init__(self):
        pygame.mixer.init()
        self.sound_status = True
        pygame.mixer.music.load("pacman sounds/main menu music.mp3")
        self.pacman_eat_sound = pygame.mixer.Sound("pacman sounds/pacman eating.mp3")
        self.pacman_eat_ghost_sound = pygame.mixer.Sound("pacman sounds/pacman eating ghost.mp3")
        self.pacman_die_sound = pygame.mixer.Sound("pacman sounds/pacman die.mp3")
        pygame.mixer.music.set_volume(0.15)
        self.pacman_eat_sound.set_volume(0.5)
        self.pacman_eat_ghost_sound.set_volume(0.15)
        self.pacman_die_sound.set_volume(0.15)

    """
    Method for playing background music.
    """

    def play_bg_music(self):
        pygame.mixer.music.play()

    """
    Method for playing pacman eating pellet sound.
    """

    def play_pacman_eat_music(self):
        if self.sound_status:
            if self.pacman_eat_sound.get_num_channels() == 0:
                self.pacman_eat_sound.play(maxtime=280)
    """
    Method for playing pacman eating ghost sound.
    """

    def play_pacman_eat_ghost(self):
        if self.sound_status:
            self.pacman_eat_ghost_sound.play()
    """
    Method for playing pacman dying by ghost sound.
    """

    def play_pacman_die(self):
        if self.sound_status:
            pygame.mixer.music.stop()
            self.pacman_eat_sound.stop()
            self.pacman_die_sound.play()

    """
    Method for pausing all sounds in game. Works like a switch.
    """

    def pause_music(self):
        if self.sound_status:
            pygame.mixer.music.pause()
            self.sound_status = False
        else:
            pygame.mixer.music.unpause()
            self.sound_status = True
