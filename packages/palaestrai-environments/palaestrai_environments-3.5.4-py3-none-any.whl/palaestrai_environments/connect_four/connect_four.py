import enum

import random
from typing import Dict, List, Union

ROWS: int = 6
COLS: int = 7


class Player(enum.Enum):
    NOBODY = 0
    P1 = 1
    P2 = 2


class ConnectFour:
    """Connect Four game logic.

    This class contains all the logic of the game as well as a function
    to print the current state to console.
    """

    def __init__(self):
        self.board: List[int] = [0] * ROWS * COLS
        self.player_on_turn: Player = Player.P1
        self.winner: Player = Player.NOBODY
        self.score: Dict[Player, int] = {Player.P1: 0, Player.P2: 0}
        self.total_score: Dict[Player, int] = {Player.P1: 0, Player.P2: 0}
        self.game_over: bool = False

    def start(self) -> Player:
        """Reset the board to its initial state.

        Returns the player that should start.
        """
        self.board = [0] * ROWS * COLS
        self.player_on_turn = random.choice([Player.P1, Player.P2])
        self.winner = Player.NOBODY
        self.score = {Player.P1: 0, Player.P2: 0}
        self.total_score = {Player.P1: 0, Player.P2: 0}
        self.game_over = False

        return self.player_on_turn

    def act_on_column(self, col: int, player: Union[Player, int]) -> bool:
        if isinstance(player, int):
            player = Player(player)

        assert player in (
            Player.P1,
            Player.P2,
        ), f"Invalid player {player}. Must be 1 or 2"

        self.player_on_turn = player

        valid = False

        # Update Board
        for row in range(ROWS - 1, -1, -1):
            if self.board[row * COLS + col] == 0:
                self.board[row * COLS + col] = self.player_on_turn.value
                valid = True
                break

        return valid

    def update(self):
        """Evaluate board state and update scores."""
        self._evaluate_board()
        self.total_score[Player.P1] += self.score[Player.P1]
        self.total_score[Player.P2] += self.score[Player.P2]
        if self.winner != Player.NOBODY:
            self.game_over = True

    def _evaluate_board(self):
        self.score = {Player.P1: 0, Player.P2: 0}
        self.winner: int = Player.NOBODY

        # Check horizontal cells
        for row in range(ROWS):
            for col in range(COLS):
                cell_value = self.board[row * COLS + col]
                if cell_value == 0:
                    continue
                match: int = 0
                for idx in range(1, 4):
                    if col + idx >= COLS:
                        break
                    elif cell_value == self.board[row * COLS + col + idx]:
                        match += 1
                    else:
                        break
                if match >= 3:
                    self.winner = Player(cell_value)
                self.score[Player(cell_value)] += match

        # Check vertical cells
        for row in range(ROWS):
            for col in range(COLS):
                cell_value = self.board[row * COLS + col]
                if cell_value == 0:
                    continue
                match: int = 0
                for idx in range(1, 4):
                    if row + idx >= ROWS:
                        break
                    elif cell_value == self.board[(row + idx) * COLS + col]:
                        match += 1
                    else:
                        break
                if match >= 3:
                    self.winner = Player(cell_value)
                self.score[Player(cell_value)] += match

        # Check diagonally down cells
        for row in range(ROWS):
            for col in range(COLS):
                cell_value = self.board[row * COLS + col]
                if cell_value == 0:
                    continue
                match: int = 0
                for idx in range(1, 4):
                    if row + idx >= ROWS or col + idx >= COLS:
                        break
                    elif (
                        cell_value
                        == self.board[(row + idx) * COLS + col + idx]
                    ):
                        match += 1
                    else:
                        break
                if match >= 3:
                    self.winner = Player(cell_value)
                self.score[Player(cell_value)] += match

        # Check diagonally up cells
        for row in range(ROWS):
            for col in range(COLS):
                cell_value = self.board[row * COLS + col]
                if cell_value == 0:
                    continue
                match: int = 0
                for idx in range(1, 4):
                    if row - idx < 0 or col + idx >= COLS:
                        break
                    elif (
                        cell_value
                        == self.board[(row - idx) * COLS + col + idx]
                    ):
                        match += 1
                    else:
                        break
                if match >= 3:
                    self.winner = Player(cell_value)
                self.score[Player(cell_value)] += match

    def draw_console(self):
        print()
        for row in range(ROWS):
            for col in range(COLS):
                print(self.board[row * COLS + col], end=" ")

            print()

        print("Score/Total: ")
        print(
            f"P1: {self.score[Player.P1]}/{self.total_score[Player.P1]} - "
            f"P2: {self.score[Player.P2]}/{self.total_score[Player.P2]}"
        )
        print("# ===================")
        if self.winner != Player.NOBODY:
            print(f"Player {self.winner.value} wins!")


def main():
    game = ConnectFour()
    game.start()
    player = Player.P1
    game.draw_console()
    while not game.game_over:
        action = 0
        while action == 0:
            action = int(input("Col [1,2,3,4,5,6,7]?:"))
        if not game.act_on_column(action - 1, player):
            raise ValueError("Invalid Turn")
        game.update()
        game.draw_console()

        if player == Player.P1:
            player = Player.P2
        else:
            player = Player.P1


if __name__ == "__main__":
    main()
