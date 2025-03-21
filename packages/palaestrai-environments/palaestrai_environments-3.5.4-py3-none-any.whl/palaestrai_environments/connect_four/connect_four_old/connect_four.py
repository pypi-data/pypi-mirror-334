import logging
from palaestrai.agent import ActuatorInformation, SensorInformation
from palaestrai.types import MultiBinary
from palaestrai_connect_four.pygame_engine import PalaestrAIBoardgame, Players

from .board import Board
from .config import (
    BUTTONS,
    CELL_SIZE,
    COLS,
    GREY,
    ROWS,
    SCORE1_X,
    SCORE2_X,
    SCORE_Y1,
    SCORE_Y2,
    WHITE,
)
from .text import Text

LOG = logging.getLogger(__name__)


class ConnectFour(PalaestrAIBoardgame):
    """The palaestrAI boardgame of connect four."""

    def __init__(self, params):
        params.setdefault("key_map", BUTTONS)
        super().__init__(params)

        self.board = None
        self.acted = False
        self.text_p1 = None
        self.reward_p1 = None
        self.text_p2 = None
        self.reward_p2 = None

    def load(self):
        """Load a new board game."""
        super().load()

        self.scores = {
            Players.P1: 0,
            Players.P2: 0,
        }

        self.board = Board(self)
        self.player_on_turn = self.rng.choice([Players.P1, Players.P2])

        self._controls = [Text(self, (5, 5), "Use keys:", 30)]
        offset = 120 + CELL_SIZE // 2
        for idx, button in enumerate(BUTTONS):
            self._controls.append(
                Text(self, (1 + (offset + idx * CELL_SIZE), 5), button, 30)
            )

        self.text_p1 = Text(self, (SCORE1_X, SCORE_Y1), "Player 1", 30)
        self.reward_p1 = Text(self, (SCORE1_X, SCORE_Y2), "Score: 0", 30)
        self.text_p2 = Text(self, (SCORE2_X, SCORE_Y1), "Player 2", 30)
        self.reward_p2 = Text(self, (SCORE2_X, SCORE_Y2), "Score: 0", 30)

    def next_turn(self, is_agent_turn=False):
        """Next iteration of the game's main loop.

        To allow agents a frame perfect control of the game, the loop
        is only progressed once for each agent. For human players, the
        loop will continue until the player has acted.

        Parameters
        ----------
        is_agent_turn: bool, optional
            Indicates if an agent is the current acting player.

        Returns
        -------
        Players
            The winner of this match or Players.NONE.

        """
        self.acted = False
        self.is_agent_turn = is_agent_turn

        for text in self._controls:
            text.color = GREY if self.is_agent_turn else WHITE

        while not self.acted:
            self.tick()
            self.board.is_invalid_move = not self.events()
            if self.game_over:
                break
            self.update()
            self.draw()

        self._keys.reset()

        if self.game_over:
            return Players.NONE

        return self._evaluate_board()

    def next_player(self):
        """Determine the next acting player.

        No change if the last move was invalid.

        """
        if self.board.is_invalid_move:
            return
        if self.player_on_turn == Players.P1:
            self.player_on_turn = Players.P2
        else:
            self.player_on_turn = Players.P1

    def _evaluate_board(self):
        """Evaluate the board state and update displayed texts.

        Returns
        -------
        Players
            The winner if any, Players.NONE otherwise.

        """
        scores, winner = self.board.evaluate()

        for pl, score in scores.items():
            self.scores[pl] += score

        self.reward_p1.text = f"Score: {self.scores[Players.P1]}"
        self.reward_p2.text = f"Score: {self.scores[Players.P2]}"

        if winner != Players.NONE:
            LOG.info(
                "Player %s wins the game with score %.3f",
                winner.name,
                self.scores[winner],
            )
        return winner

    def get_board_controls(self):
        """Return the board controls.

        The board controls are defined by actuators.

        Returns
        -------
        list[ActuatorInformation]
            A list of actuators that define the board controls.

        """
        actuators = list()

        players = [pl for pl, is_agent in self.agent_map.items() if is_agent]
        for player in players:
            actuators.append(
                ActuatorInformation(
                    uid=player.uid,
                    value=[0 for _ in range(COLS)],
                    space=MultiBinary(COLS),
                )
            )

        return actuators

    def get_board_state(self):
        """Return the board state.

        The board state is defined by a sensors for each cell.

        Returns
        -------
        list[SensorInformation]
            A list of sensors with one sensor for each cell.

        """
        value2sensor = {
            Players.NONE: [0, 0],
            Players.P1: [1, 0],
            Players.P2: [0, 1],
        }
        sensors = list()
        for col in range(COLS):
            for row in range(ROWS):
                sensors.append(
                    SensorInformation(
                        uid=f"cell-{col}-{row}",
                        value=value2sensor[
                            self.board.get_cell_value(col, row)
                        ],
                        space=MultiBinary(2),
                    )
                )
        return sensors

    def get_reward(self):
        """Return the current scores of the players."""
        return self.scores

    def was_valid_move(self):
        """Returns whether the last move was valid."""
        return not self.board.is_invalid_move
