from __future__ import annotations

import enum
import logging
from copy import deepcopy

import numpy as np
from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.reward_information import RewardInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.environment.environment_baseline import EnvironmentBaseline
from palaestrai.environment.environment_state import EnvironmentState
from palaestrai.types import Box, Discrete
from palaestrai.types.simtime import SimTime
from palaestrai.util import seeding
from typing import List

LOG = logging.getLogger("palaestrai.environment.TicTacToe")


class Peg(enum.Enum):
    EMPTY = 0
    ENV = 1
    AGENT = 2

    def __int__(self):
        return self.value


class TicTacToeEnvironment(Environment):
    """The tic tac toe environment.

    The goal is to place symbols on the board and form a three symbol
    row of the own symbol.

    There are three possible states per tile:

        0 = unassigned
        1 = assigned to player 1 (the environment)
        2 = assigned to player 2 (the agent)

    """

    def __init__(
        self,
        uid: str,
        seed: int,
        randomness: float = 0.5,
        invalid_turn_limit: int = 5,
        *args,
        **kwargs,
    ):
        super().__init__(uid=uid, seed=seed, *args, **kwargs)
        self.rng = seeding.np_random(seed)[0]
        self.randomness: float = randomness
        self.invalid_turn_limit: int = invalid_turn_limit
        self.board: List[Peg] = [Peg.EMPTY for i in range(9)]
        self.reward_space: Box = Box(-100, 10, (1,))
        self.invalid_turn_counter: int = 0
        self.turn_counter: int = 0

        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) Parameter loaded: randomness=%f, invalid_turn_limit=%x",
            self.__class__,
            id(self),
            self.uid,
            self.randomness,
            self.invalid_turn_limit,
        )

    def start_environment(self):
        """Start the tic tac toe environment.

        The function sets up the sensors and the actuator used by the
        agent to make turns.

        """
        self.board = [Peg.EMPTY for i in range(9)]
        self.turn_counter: int = 0
        self.invalid_turn_counter = 0
        self.sensors = [
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 1-1"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 1-2"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 1-3"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 2-1"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 2-2"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 2-3"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 3-1"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 3-2"),
            SensorInformation(Peg.EMPTY.value, Discrete(3), "Tile 3-3"),
        ]
        self.actuators = [
            ActuatorInformation(0, Discrete(len(self.board)), "Field selector")
        ]
        if np.random.uniform(0, 1) > 0.5:
            # optimal tic tac toe algorithm starts
            self.board[self._compute_oponent_turn(self.board)] = Peg.ENV
            self._map_board_to_sensors()

        return EnvironmentBaseline(
            sensors_available=self.sensors,
            actuators_available=self.actuators,
            simtime=SimTime(self.turn_counter, None),
        )

    def update(self, actuators):
        """Creates new sensor information

        This method creates new sensor readings. The actuator value
        marks the desired tile of the agent player. Only one actuator
        is allowed.

        Parameters
        ----------
        actuators : List[ActuatorInformation]
            List of actuators, in this case only one actuator is
            allowed.

        Returns
        -------
        Tuple[List[SensorInformation], List[RewardInformation], bool]
            Tuple of List of SensorInformation with new values, reward(s)
            and a flag that sigals if the current state is a terminal
            state.

        """
        LOG.debug("Playing %s...", actuators)
        actuator = actuators[0]
        self.turn_counter += 1

        # Terminate environment if self.invalid_turn_limit is reached
        if self.invalid_turn_counter >= self.invalid_turn_limit:
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Agent made too many invalid turns! Environment terminates now!",
                self.__class__,
                id(self),
                self.uid,
            )
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        np.array([-100.0], dtype=np.float32),
                        self.reward_space,
                        "Tic-Tac-Toe-Reward",
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # Agent makes invalid turn:
        #   High penalty, no change in the env. The agent can try again
        #   until self.invalid_turn_limit is reached
        if not (
            TicTacToeEnvironment.is_valid_move(self.board, actuator.value)
        ):
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Agent made invalid turn: %x",
                self.__class__,
                id(self),
                self.uid,
                actuator.value,
            )
            self.invalid_turn_counter = self.invalid_turn_counter + 1
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        np.array([-100.0], dtype=self.reward_space.dtype),
                        self.reward_space,
                        "Tic-Tac-Toe-Reward",
                    )
                ],
                done=False,
                simtime=SimTime(self.turn_counter, None),
            )

        else:
            self.invalid_turn_counter = 0

        # execute turn of agent
        self.board[actuator.value] = Peg.AGENT
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) Board after agent's turn: %s",
            self.__class__,
            id(self),
            self.uid,
            str(self.board),
        )
        self._map_board_to_sensors()

        # check if the agent won
        if TicTacToeEnvironment.is_game_won(self.board, Peg.AGENT):
            LOG.info(
                "Agent won tic-tac-toe match (worker: %s):\n%s",
                self.uid,
                TicTacToeEnvironment.to_str(self.board),
            )
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        np.array([10.0], dtype=self.reward_space.dtype),
                        self.reward_space,
                        "Tic-Tac-Toe-Reward",
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # check if the game is a draw because of agent move
        if TicTacToeEnvironment.is_draw(self.board):
            LOG.info(
                "Tic-tac-toe match is draw. "
                "This is a strange game: The only winning move "
                "is not to play. (worker: %s)\n%s",
                self.uid,
                TicTacToeEnvironment.to_str(self.board),
            )
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        np.array([0.0], dtype=self.reward_space.dtype),
                        self.reward_space,
                        "Tic-Tac-Toe-Reward",
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # Turn of algorithm within environment.
        #   In order to spice things up, the algorithm can make random,
        #   not optimal turns with a specified probability
        if np.random.uniform(0, 1) > self.randomness:
            # optimal tic tac toe algorithm makes turn
            self.board[self._compute_oponent_turn(self.board)] = Peg.ENV
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Board after environments "
                "optimal turn: %s",
                self.__class__,
                id(self),
                self.uid,
                str(self.board),
            )
        else:
            # random turn
            # sampling from actuator space is currently not possible
            # -> gives same "random" number all the time
            # within one experiment run
            random_move = np.random.randint(0, 9)
            while not TicTacToeEnvironment.is_valid_move(
                self.board, random_move
            ):
                random_move = np.random.randint(0, 9)
            self.board[random_move] = Peg.ENV
            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) Board after environments "
                "random turn: %s.",
                self.__class__,
                id(self),
                self.uid,
                str(self.board),
            )

        self._map_board_to_sensors()

        # check if algorithm won
        if TicTacToeEnvironment.is_game_won(self.board, Peg.ENV):
            LOG.info(
                "WOPR has won (worker: %s):\n%s",
                self.uid,
                TicTacToeEnvironment.to_str(self.board),
            )
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        np.array([-10.0], dtype=self.reward_space.dtype),
                        self.reward_space,
                        "Tic-Tac-Toe-Reward",
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )

        # check if the game is a draw because of algorithm move
        if TicTacToeEnvironment.is_draw(self.board):
            LOG.info(
                "Tic-tac-toe match is draw. "
                "This is a strange game: The only winning move "
                "is not to play. (worker: %s)\n%s",
                self.uid,
                TicTacToeEnvironment.to_str(self.board),
            )
            return EnvironmentState(
                sensor_information=self.sensors,
                rewards=[
                    RewardInformation(
                        np.array([0.0], dtype=self.reward_space.dtype),
                        self.reward_space,
                        "Tic-Tac-Toe-Reward",
                    )
                ],
                done=True,
                simtime=SimTime(self.turn_counter, None),
            )
        return EnvironmentState(
            sensor_information=self.sensors,
            rewards=[
                RewardInformation(
                    np.array([1.0], dtype=self.reward_space.dtype),
                    self.reward_space,
                    "Tic-Tac-Toe-Reward",
                )
            ],
            done=False,
            simtime=SimTime(self.turn_counter, None),
        )

    @staticmethod
    def is_draw(board):
        return TicTacToeEnvironment.board_full(board)

    @staticmethod
    def board_full(board):
        return not any(x == Peg.EMPTY for x in board)

    @staticmethod
    def is_valid_move(board, tile_index):
        return board[tile_index] == Peg.EMPTY

    @staticmethod
    def switch_players(player: Peg) -> Peg:
        return Peg.ENV if player == Peg.AGENT else Peg.ENV

    @staticmethod
    def is_game_won(board: List[Peg], player: Peg) -> bool:
        # horizontal lines
        if board[0] == player and board[1] == player and board[2] == player:
            return True
        elif board[3] == player and board[4] == player and board[5] == player:
            return True
        elif board[6] == player and board[7] == player and board[8] == player:
            return True

        # vertical lines
        elif board[0] == player and board[3] == player and board[6] == player:
            return True
        elif board[1] == player and board[4] == player and board[7] == player:
            return True
        elif board[2] == player and board[5] == player and board[8] == player:
            return True

        # diagonal lines
        elif board[0] == player and board[4] == player and board[8] == player:
            return True
        elif board[2] == player and board[4] == player and board[6] == player:
            return True
        else:
            return False

    def _map_board_to_sensors(self):
        for i in range(len(self.board)):
            self.sensors[i].value = self.board[i].value

    def _compute_oponent_turn(self, board):
        best_score = -123
        best_move = None
        for move in range(len(board)):
            if TicTacToeEnvironment.is_valid_move(board, move):
                board_copy = deepcopy(board)
                board_copy[move] = Peg.ENV
                score = int(
                    self._minimax(
                        board_copy,
                        TicTacToeEnvironment.switch_players(Peg.ENV),
                    )
                )
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move

    @staticmethod
    def pos_to_str(peg: Peg) -> str:
        return (" ", "O", "X")[peg.value]

    @staticmethod
    def to_str(board) -> str:
        return (
            f" ___ ___ ___\n"
            f"|   |   |   |\n"
            f"| {TicTacToeEnvironment.pos_to_str(board[0])} | "
            f"{TicTacToeEnvironment.pos_to_str(board[1])} | "
            f"{TicTacToeEnvironment.pos_to_str(board[2])} |\n"
            f"|   |   |   |\n"
            f" ___ ___ ___\n"
            f"|   |   |   |\n"
            f"| {TicTacToeEnvironment.pos_to_str(board[3])} | "
            f"{TicTacToeEnvironment.pos_to_str(board[4])} | "
            f"{TicTacToeEnvironment.pos_to_str(board[5])} |\n"
            f"|   |   |   |\n"
            f" ___ ___ ___\n"
            f"|   |   |   |\n"
            f"| {TicTacToeEnvironment.pos_to_str(board[6])} | "
            f"{TicTacToeEnvironment.pos_to_str(board[7])} | "
            f"{TicTacToeEnvironment.pos_to_str(board[8])} |\n"
            f"|   |   |   |\n"
            f" ___ ___ ___"
        )

    def _minimax(self, board, player):
        if TicTacToeEnvironment.board_full(board):
            return 0
        # check if previous turn was a winning turn (for the other player)
        if TicTacToeEnvironment.is_game_won(
            board, TicTacToeEnvironment.switch_players(Peg(player))
        ):
            return TicTacToeEnvironment.switch_players(Peg(player))
        scores = []
        for move in range(len(board)):
            if TicTacToeEnvironment.is_valid_move(board, move):
                board_copy = deepcopy(board)
                board_copy[move] = Peg(player)
                score = self._minimax(
                    board_copy,
                    TicTacToeEnvironment.switch_players(Peg(player)),
                )
                scores.append(int(score))
        # maximize from the perspective of the current player
        if player == Peg.AGENT:
            return min(int(x) for x in scores)
        else:
            return max(int(x) for x in scores)
