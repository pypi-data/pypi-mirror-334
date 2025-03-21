import logging
import pygame as pg
from palaestrai_connect_four.pygame_engine import Players
from pygame.math import Vector2 as Vec

from .cell import Cell
from .config import BUTTONS, CELL_SIZE, COLS, ROWS, BOARD_POS

LOG = logging.getLogger(__name__)


class Board(pg.sprite.Sprite):
    """The board of connect four.

    Holds all the cells and an image of the board

    """

    def __init__(self, gen):
        self._layer = 0
        super().__init__(gen.sprites)

        self.gen = gen
        self.image = pg.Surface((CELL_SIZE * COLS, CELL_SIZE * ROWS))
        self.rect = pg.Rect(BOARD_POS, (CELL_SIZE * COLS, CELL_SIZE * ROWS))
        self.is_invalid_move = False
        self.cells = list()
        for col in range(COLS):
            x_pos = (col * CELL_SIZE) + self.rect.x
            self.cells.append(list())
            for row in range(ROWS - 1, -1, -1):
                y_pos = (row * CELL_SIZE) + self.rect.y
                self.cells[col].append(Cell(gen, Vec(x_pos, y_pos)))

    def get_cell_value(self, col, row):
        """Return the value of a given cell.

        Parameters
        ----------
        col: int
            Column index of the requested cell.
        row: int
            Row index of the requested cell.

        Returns
        -------
        Players
            The cell's assignment to a player (NONE, P1, or P2)
        """
        return self.cells[col][row].value

    def act_on_column(self, col, player):
        """Let the player act on a column.

        Parameters
        ----------
        col: int
            Index of the column to act on.
        player: Players
            The player who is acting.

        Returns
        -------
        bool
            True, if the action was valid, false otherwise.

        Raises
        ------
        ValueError
            if player has an invalid value.

        """
        col_idx = min(ROWS, max(0, col))
        if player == Players.NONE:
            raise ValueError()

        for cell in self.cells[col_idx]:
            if cell.value == Players.NONE:
                cell.value = player
                return True

        return False

    def update(self, delta_time):
        """Update the board with input from the players.

        Parameters
        ----------
        delta_time: float
            Elapsed time since last update in seconds.

        """
        self.is_invalid_move = False
        for idx, button in enumerate(BUTTONS):
            if self.gen.is_new_key_press(button):
                if self.act_on_column(idx, self.gen.player_on_turn):
                    LOG.debug(
                        "Player %s acted on column %s",
                        self.gen.player_on_turn,
                        button,
                    )
                else:
                    LOG.debug(
                        "Illegal move by player %s: %s",
                        self.gen.player_on_turn,
                        button,
                    )
                    self.is_invalid_move = True

                self.gen.acted = True

    def draw(self, display):
        """Draw the boards image to the display.

        Parameters
        ----------
        display: pg.Surface
            The display surface to draw to.

        """
        display.blit(self.image, self.rect)

    def evaluate(self):
        """Evaluate the current board state.

        Players get a negative reward on an invalid move. Players get
        a positive reward for each two or more adjacently owned cells.
        E.g., two cells give 1 point, three cells give 2 + 1 points.

        Returns
        -------
        dict
            Current rewards
        Players
            The player who wins or Players.NONE if there is no winner,
            yet.
        """
        rewards = {
            Players.P1: 0,
            Players.P2: 0,
        }
        winner = Players.NONE

        # Check for invalid move
        if self.is_invalid_move:
            rewards[self.gen.player_on_turn] = -15
            if self.gen.player_on_turn == Players.P1:
                return rewards, winner
            else:
                return rewards, winner

        # Check horizontal cells
        for c in range(COLS - 3):
            for r in range(ROWS):
                if self.cells[c][r].value == Players.NONE:
                    continue
                value = self.cells[c][r].value
                reward = 0
                for i in range(1, 4):
                    if value == self.cells[c + i][r].value:
                        reward += 1
                    else:
                        break
                if reward >= 3:
                    winner = self.cells[c][r].value
                rewards[self.cells[c][r].value] += reward

        # Check vertical cells
        for c in range(COLS):
            for r in range(ROWS - 3):
                if self.cells[c][r].value == Players.NONE:
                    continue
                value = self.cells[c][r].value
                reward = 0
                for i in range(1, 4):
                    if value == self.cells[c][r + i].value:
                        reward += 1
                    else:
                        break
                if reward >= 3:
                    winner = value
                rewards[value] += reward

        # Check diagonally up cells
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if self.cells[c][r].value == Players.NONE:
                    continue
                value = self.cells[c][r].value
                reward = 0
                for i in range(1, 4):
                    if value == self.cells[c + 1][r + 1].value:
                        reward += 1
                    else:
                        break
                if reward >= 3:
                    winner = value
                rewards[value] += reward

        # Check diagonally down cells
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if self.cells[c][r].value == Players.NONE:
                    continue
                value = self.cells[c][r].value
                reward = 0
                for i in range(1, 4):
                    if value == self.cells[c + 1][r - 1].value:
                        reward += 1
                    else:
                        break
                if reward >= 3:
                    winner = value
                rewards[value] += reward

        return rewards, winner
