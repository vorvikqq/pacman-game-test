class Pause(object):
    """
    Manages game pause functionality, allowing for timed pauses and manual toggling.

    Attributes:
        paused (bool): Indicates whether the game is currently paused.
        timer (float): Tracks the elapsed time during a timed pause.
        pause_time (float or None): Duration for which the game should remain paused.
        func (callable or None): Function to be executed after the pause ends.
    """

    def __init__(self, paused=False):
        """
        Initializes the Pause instance.

        Args:
            paused (bool): Initial pause state. Defaults to False.
        """
        self.paused = paused
        self.timer = 0
        self.pause_time = None
        self.func = None

    def update(self, dt):
        """
        Updates the pause timer and resumes the game when the pause time expires.

        Args:
            dt (float): Time elapsed since the last update.

        Returns:
            callable or None: The stored function if the pause ends, otherwise None.
        """
        if self.pause_time is not None:
            self.timer += dt
            if self.timer >= self.pause_time:
                self.timer = 0
                self.pause_time = None
                self.paused = False
                return self.func
        return None

    def set_pause(self, player_paused=False, pause_time=None, func=None):
        """
        Sets a pause with optional timing and a function to execute upon resumption.

        Args:
            player_paused (bool): Indicates whether the pause was triggered manually.
            pause_time (float or None): Duration of the pause. If None, the pause remains indefinite.
            func (callable or None): Function to execute when the pause ends.
        """
        self.timer = 0
        self.func = func
        self.pause_time = pause_time
        self.flip()

    def flip(self):
        """
        Toggles the pause state.
        """
        self.paused = not self.paused
