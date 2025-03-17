class Animation(object):
    """
    Represents an animation consisting of multiple frames.

    Attributes:
        name (str): The type of entity (FRUIT).
        color (tuple): The color of the fruit.
        lifespan (int): The time (in seconds) before the fruit disappears.
        timer (float): Tracks the elapsed time since the fruit appeared.
        destroy (bool): Indicates whether the fruit should be removed.
        points (int): The score awarded when the fruit is collected.
        sprites (FruitSprites): The sprite representation of the fruit.
    """

    def __init__(self, frames=[], speed=30, loop=True):
        """
         Initializes an animation instance.

         Args:
            frames (list): List of frames in the animation.
            speed (int): Number of frames per second.
            loop (bool): Whether the animation should repeat when finished.
        """
        self.frames = frames
        self.current_frame = 0
        self.speed = speed
        self.loop = loop  # repeat animation
        self.d_time = 0
        self.is_finished = False

    def reset(self):
        """
         Resets the animation to the first frame.
        """
        self.current_frame = 0
        self.is_finished = False

    def update(self, dt):
        """
        Updates the animation state based on elapsed time.

        Args:
            dt (float): Time elapsed since the last update.

        Returns:
            object: The current frame of the animation.
        """
        if not self.is_finished:
            self.next_frame(dt)
        if self.current_frame == len(self.frames):  # якщо досягається останнього кадру
            if self.loop:
                self.current_frame = 0  # починаємо спочтку
            else:
                self.is_finished = True
                self.current_frame -= 1

        return self.frames[self.current_frame]

    def next_frame(self, d_time):
        """
        Advances the animation to the next frame based on elapsed time.

        Args:
            d_time (float): Time elapsed since the last frame update.
        """
        self.d_time += d_time
        if self.d_time >= (1.0 / self.speed):
            self.current_frame += 1
            self.d_time = 0
