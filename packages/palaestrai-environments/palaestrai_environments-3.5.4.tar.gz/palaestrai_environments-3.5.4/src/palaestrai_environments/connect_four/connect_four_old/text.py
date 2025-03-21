import pygame as pg

from .config import WHITE


class Text(pg.sprite.Sprite):
    """Represents an object to display a text.

    Parameters
    ----------
    gen: :class:`.ConnectFour`
        A reference to the game engine instance.
    pos: pygame.math.Vector2
        The topleft position of the text.
    text: str
        The text to be displayed.
    size: int
        The size of the text to be displayed.
    color: tuple, optional
        The color of the text. Defaults to (255, 255, 255) (white).
    """

    def __init__(self, gen, pos, text, size, color=WHITE):
        self._layer = 2
        super().__init__(gen.sprites)

        self.text = text
        self.size = size
        self.color = color
        self._image = pg.font.Font(None, size).render(text, True, color)
        self._rect = self._image.get_rect(topleft=pos)

    def update(self, delta_time):
        """Update the text displayed depending of the current values.

        Text, size, and color could be changed externally.

        Parameters
        ----------
        delta_time: float
            Elapsed time since last update in seconds.

        """
        self._image = pg.font.Font(None, self.size).render(
            self.text, True, self.color
        )
        self._rect = self._image.get_rect(topleft=self._rect.topleft)

    def draw(self, display):
        """Draw the text image to the display.

        Parameters
        ----------
        display: pg.Surface
            The display surface to draw to.

        """
        display.blit(self._image, self._rect)
