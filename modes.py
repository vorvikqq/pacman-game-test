from constants import *


class DefaultMode():
    """
    Handles the default behavior of a ghost's movement modes.

    Attributes:
        timer (float): Tracks time elapsed in the current mode.
        mode (str): Current mode of the ghost.
        time (float): Duration of the current mode before switching.
    """

    def __init__(self, start_mode=WAIT):
        """
        Initializes the mode system with a starting mode.

        Args:
            start_mode (str): The initial mode of the ghost.
        """
        self.timer = 0
        self.mode = None
        self.set_mode(start_mode)

    def update(self, dt):
        """
        Updates the mode timer and switches modes when necessary.

        Args:
            dt (float): Time since the last update.
        """
        self.timer += dt

        if self.timer >= self.time:
            if self.mode == WAIT:
                self.scatter()
            elif self.mode == SCATTER:
                self.chase()
            elif self.mode == CHASE:
                self.scatter()
            elif self.mode == RANDOM:
                self.scatter()
            elif self.mode == FREIGHT:
                self.scatter()
            elif self.mode == SPAWN:
                self.wait()

    def reset_mode(self):
        """
        Resets the ghost to either SCATTER or CHASE mode.
        """
        if self.mode == FREIGHT:
            self.set_mode(SCATTER)
        elif self.mode == WAIT:
            self.set_mode(SCATTER)

    def set_mode(self, mode):
        """
        Changes the current mode.

        Args:
            mode (str): The new mode to set.
        """
        if mode == SCATTER:
            self.scatter()
        elif mode == CHASE:
            self.chase()
        elif mode == WAIT:
            self.wait()
        elif mode == RANDOM:
            self.random()
        elif mode == FREIGHT:
            self.freight()
        elif mode == SPAWN:
            self.spawn()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

    def wait(self):
        self.mode = WAIT
        self.time = 3
        self.timer = 0

    def random(self):
        self.mode = RANDOM
        self.time = 10
        self.timer = 0

    def freight(self):
        self.mode = FREIGHT
        self.time = 7
        self.timer = 0

    def spawn(self):
        self.mode = SPAWN
        self.time = 5
        self.timer = 0


class ModeController():
    """
    Manages the mode transitions and updates for a ghost.

    Attributes:
        time (float): Timer tracking duration of current mode.
        timer (float): Secondary timer for tracking FREIGHT mode.
        main_mode (DefaultMode): The main mode handler.
        current_mode (str): The currently active mode.
        ghost (Ghost): The ghost instance associated with this controller.
    """

    def __init__(self, ghost, start_mode=WAIT):
        """
        Initializes the mode controller.

        Args:
            ghost (Ghost): The ghost whose mode is controlled.
            start_mode (str): The initial mode for the ghost.
        """
        self.time = 0
        self.timer = 0
        self.main_mode = DefaultMode(start_mode)
        self.current_mode = self.main_mode.mode
        self.ghost = ghost

    def update(self, dt):
        """
        Updates the ghost's mode and movement behavior.

        Args:
            dt (float): Time since last update.
        """
        self.main_mode.update(dt)
        self.current_mode = self.main_mode.mode
        self.ghost.update_move_method()

        if self.current_mode == SPAWN and self.ghost.node.position == self.ghost.home_goal:
            self.main_mode.set_mode(WAIT)

        if self.current_mode == FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.ghost.normal_mode()
                self.current_mode = self.main_mode.mode
        elif self.current_mode in [SCATTER, CHASE]:
            self.current_mode = self.main_mode.mode

        if self.current_mode == SPAWN and self.ghost.node == self.ghost.spawn_node:
            self.ghost.normal_mode()
            self.current_mode = self.main_mode.mode

    def set_mode(self, mode):
        """
        Changes the mode dynamically.

        Args:
            mode (str): The new mode to set.
        """
        self.main_mode.set_mode(mode)
        self.current_mode = self.main_mode.mode
        self.ghost.update_move_method()

    def set_freight_mode(self):
        """
        Activates the frightened (FREIGHT) mode if the ghost is in SCATTER or CHASE.
        """
        if self.current_mode in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.set_mode(FREIGHT)
        elif self.current_mode == FREIGHT:
            self.timer = 0

    def set_spawn_mode(self):
        """
        Switches the ghost to SPAWN mode if currently in FREIGHT mode.
        """
        if self.current_mode == FREIGHT:
            self.set_mode(SPAWN)
