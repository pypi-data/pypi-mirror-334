import pygame as pg
from palaestrai_connect_four.pygame_engine import Players

from .config import CELL_SIZE, BOARD_COLOR, RED, YELLOW


class Cell(pg.sprite.Sprite):
    """Representation of a cell in connect four.

    Parameters
    ----------
    gen: ConnectFour
        A reference to the game engine instance.
    pos: pygame.math.Vector2
        Topleft position of this cell.

    Attributes
    ----------
    value: Players
        The player who owns this cell. Players.NONE if no player
        owns this cell.
    """

    def __init__(self, gen, pos):
        self._layer = 1
        super().__init__(gen.sprites)

        self.value = Players.NONE

        self._cell_image = pg.Surface((CELL_SIZE, CELL_SIZE))
        pg.draw.rect(
            self._cell_image,
            BOARD_COLOR,
            self._cell_image.get_rect(topleft=(0, 0)),
            1,
        )

        self._chip_red_image = pg.Surface((CELL_SIZE - 10, CELL_SIZE - 10))
        self._chip_red_image.fill(RED)
        self._chip_yellow_image = pg.Surface((CELL_SIZE - 10, CELL_SIZE - 10))
        self._chip_yellow_image.fill(YELLOW)

        self._image = None
        self._rect = pg.Rect(pos, (CELL_SIZE, CELL_SIZE))

    def update(self, delta_time):
        """Update the cell depending of the current value.

        Parameters
        ----------
        delta_time: float
            Elapsed time since last update in seconds.

        """
        self._image = self._cell_image.copy()
        if self.value == Players.P1:
            self._image.blit(
                self._chip_red_image,
                self._chip_red_image.get_rect(
                    center=self._image.get_rect().center
                ),
            )
        elif self.value == Players.P2:
            self._image.blit(
                self._chip_yellow_image,
                self._chip_yellow_image.get_rect(
                    center=self._image.get_rect().center
                ),
            )

    def draw(self, display):
        """Draw the cells image to the display.

        Parameters
        ----------
        display: pg.Surface
            The display surface to draw to.

        """
        display.blit(self._image, self._rect)
