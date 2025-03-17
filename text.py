import pygame
from vector import Vector
from constants import *


class Text():
    """
    Represents a text object to be displayed on the screen.

    Attributes:
        id (int or None): Unique identifier for the text object.
        text (str): The text content to be displayed.
        color (tuple): RGB color of the text.
        size (int): Font size of the text.
        showtime (float or None): Duration (in seconds) before the text disappears.
        visible (bool): Whether the text is currently visible.
        destroy (bool): Flag indicating if the text should be removed.
        position (Vector): The (x, y) position of the text.
        timer (float): Timer tracking how long the text has been displayed.
    """

    def __init__(self, text, color, x, y, size, time=None, visible=True, id=None):
        """
        Initializes a Text object.

        Args:
            text (str): The text to be displayed.
            color (tuple): RGB color of the text.
            x (int): X-coordinate of the text position.
            y (int): Y-coordinate of the text position.
            size (int): Font size.
            time (float): Duration before the text disappears. Defaults to None.
            visible (bool): Whether the text is initially visible. Defaults to True.
            id (int): Unique identifier for the text. Defaults to None.
        """
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.showtime = time
        self.visible = visible
        self.destroy = False
        self.position = Vector(x, y)
        self.timer = 0
        self.label = None
        self.setup_font("fonts/PressStart2P-Regular.ttf")
        self.create_label()

    def setup_font(self, font_name):
        """
        Sets up the font for rendering text.

        Args:
            font_name: The font file path.
        """
        self.font = pygame.font.Font(font_name, self.size)

    def create_label(self):
        """
        Renders the text into a surface.
        """
        self.label = self.font.render(self.text, 1, self.color)

    def change_text(self, new_text):
        """
        Updates the text content and re-renders it.

        Args:
            new_text (str): The new text to display.
        """
        self.text = str(new_text)
        self.create_label()

    def update(self, dt):
        """
        Updates the text visibility based on its display duration.

        Args:
            dt (float): Time since the last update.
        """
        if self.showtime is not None:
            self.timer += dt

            if self.timer >= self.showtime:
                self.timer = 0
                self.showtime = None
                self.destroy = True

    def render(self, screen):
        """
        Renders the text onto the screen if it is visible.

        Args:
            screen: The game screen surface.
        """
        if self.visible:
            coords = self.position.asTuple()
            screen.blit(self.label, coords)


class TextGroup():
    """
    Manages multiple Text objects for display.

    Attributes:
        nextid (int): Next available unique identifier for text objects.
        alltext (dict): Dictionary storing all active Text objects.
    """

    def __init__(self):
        """
        Initializes the TextGroup and sets up default text elements.
        """
        self.nextid = 5
        self.alltext = {}
        self.setup_text()
        self.show_text(READYTXT)

    def add_text(self, text, color, x, y, size, time=None, id=None):
        """
        Adds a new text object to the group.

        Args:
            text (str): The text to be displayed.
            color (tuple): RGB color of the text.
            x (int): X-coordinate position.
            y (int): Y-coordinate position.
            size (int): Font size.
            time (float): Duration before the text disappears. Defaults to None.
            id (int): Unique identifier for the text. Defaults to None.

        Returns:
            int: The unique identifier of the added text.
        """
        if id is not None:
            self.alltext[id] = Text(text, color, x, y, size, time=time, id=id)
            added_id = id
        else:
            self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
            added_id = self.nextid
            self.nextid += 1
        return added_id

    def remove_text(self, id):
        """
        Removes a text object from the group by its ID.

        Args:
            id (int): The identifier of the text to be removed.
        """
        self.alltext.pop(id)

    def setup_text(self):
        """
        Initializes the default text elements for the game.
        """
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, TILEHEIGHT)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23 * TILEWIDTH, TILEHEIGHT, TILEHEIGHT)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25 * TILEWIDTH, 20 * TILEHEIGHT, TILEHEIGHT, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625 * TILEWIDTH, 20 * TILEHEIGHT, TILEHEIGHT, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10 * TILEWIDTH, 20 * TILEHEIGHT, TILEHEIGHT, visible=False)
        self.add_text("SCORE", WHITE, 0, 0, TILEHEIGHT)
        self.add_text("LEVEL", WHITE, 23 * TILEWIDTH, 0, TILEHEIGHT)

    def update(self, dt):
        """
        Updates all text objects, removing expired ones.

        Args:
            dt (float): Time since the last update.
        """
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.remove_text(tkey)

    def show_text(self, id):
        """
        Shows a specific text object by its ID.

        Args:
            id (int): The identifier of the text to show.
        """
        self.hide_text()
        self.alltext[id].visible = True

    def hide_text(self):
        """
        Hides specific game text elements.
        """
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def update_score(self, score):
        """
        Updates the displayed score.

        Args:
            score (int): The new score value.
        """
        self.update_text(SCORETXT, str(score).zfill(8))

    def update_level(self, level):
        """
        Updates the displayed level.

        Args:
            level (int): The new level value.
        """
        self.update_text(LEVELTXT, str(level + 1).zfill(3))

    def update_text(self, id, value):
        """
        Updates a specific text element.
        """
        if id in self.alltext.keys():
            self.alltext[id].change_text(value)

    def render(self, screen):
        """
        Renders all visible text objects on the screen.
        """
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
