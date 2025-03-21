import os
import pygame
from palaestrai_connect_four.connect_four import (
    COLS,
    ROWS,
    ConnectFour,
    Player,
)
from time import time
from typing import Dict

KEY_MAP = {
    1: pygame.K_1,
    2: pygame.K_2,
    3: pygame.K_3,
    4: pygame.K_4,
    5: pygame.K_5,
    6: pygame.K_6,
    7: pygame.K_7,
}
P1_IMG = os.path.abspath(
    os.path.join(__file__, "../../..", "hARL-Logo.svg.png")
)
P2_IMG = os.path.abspath(
    os.path.join(__file__, "../../..", "PalaestrAI_Logo_Brain_final.svg.png")
)


class PalaestrAIConnectFour:
    def __init__(self):
        self.initialized: bool = False
        self.external_input: Dict[int, bool] = {}
        self.last_keys: Dict[int, bool] = {}
        self.keys: Dict[int, bool] = {i: False for i in range(1, 8)}
        self.display: pygame.Surface
        self.player_images: Dict[Player, pygame.Surface] = {}
        self.game: ConnectFour
        self.player_on_turn: Player
        self.timer: float = 0.0

    def start(self):
        if not self.initialized:
            pygame.display.init()
            self.display = pygame.display.set_mode((800, 600))
            self.player_images = {
                Player.P1: pygame.image.load(P1_IMG).convert_alpha(),
                Player.P2: pygame.image.load(P2_IMG).convert_alpha(),
            }
            self.game = ConnectFour()
            self.initialized = True

        self.player_on_turn = self.game.start()
        self.keys: Dict[int, bool] = {i: False for i in range(1, 8)}

    def update(self, elapsed_time: float):
        self.process_inputs()
        if self.game.game_over:
            return

        if self.timer > 0.0:
            self.timer -= elapsed_time
        else:
            col = -1
            for button, pressed in self.keys.items():
                if pressed:
                    col = button
                    break

            if col > 0:
                if not self.game.act_on_column(col - 1, self.player_on_turn):
                    print("Invalid turn")
                else:
                    self.game.update()
                    # self.game.draw_console()
                    if self.player_on_turn == 1:
                        self.player_on_turn = 2
                    else:
                        self.player_on_turn = 1

                self.timer = 1.0

    def draw(self):
        self.display.fill((80, 80, 80))
        board_px = 120
        board_py = 30
        cell_width = 80
        cell_height = 80

        # Draw board
        for row in range(ROWS):
            for col in range(COLS):
                cell_value = self.game.board[row * COLS + col]
                if cell_value == 1:
                    player = Player.P1
                elif cell_value == 2:
                    player = Player.P2
                else:
                    continue
                cell_px = board_px + col * cell_width
                cell_py = board_py + row * cell_height
                self.display.blit(
                    self.player_images[player], (cell_px, cell_py)
                )

        # self.game.draw_console()
        # Flip display
        pygame.display.flip()

    def shutdown(self):
        if self.initialized:
            pygame.display.quit()
            pygame.quit()
            self.initialized = False

    @property
    def game_over(self):
        return self.game.game_over

    def process_inputs(self):
        self.last_keys = self.keys.copy()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.game_over = True
                return
            if self.external_input:
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.game_over = True
                    return
                for but, key in KEY_MAP.items():
                    if event.key == key:
                        self.keys[but] = True
            if event.type == pygame.KEYUP:
                for but, key in KEY_MAP.items():
                    if event.key == key:
                        self.keys[but] = False

        if self.external_input:
            self.keys = self.external_inputs

        # print(self.keys)


def main():
    con4 = PalaestrAIConnectFour()
    con4.start()
    dt = 0.00022
    start = time()
    while not con4.game_over:
        con4.update(dt)
        con4.draw()
        end = time()
        dt = end - start
        start = end

    print("Shutdown")
    con4.shutdown()


if __name__ == "__main__":
    main()
