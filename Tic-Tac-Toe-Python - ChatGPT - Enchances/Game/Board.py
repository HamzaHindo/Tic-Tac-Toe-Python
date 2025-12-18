from enum import Enum
from typing import List, Optional, Tuple
from .Player import Player
from .Move import Move

class GameState(Enum):
    WIN = 0
    DRAW = 1
    RUNNING = 2

class Board:
    board_matrix: List[List[str]]
    win_line: Optional[List[Tuple[int,int]]]

    def __init__(self):
        self.win_line: Optional[List[Tuple[int,int]]] = None
        self.n_moves: int = 0
        self.state: GameState = GameState.RUNNING
        self.blank_sym: str = ''
        self.board_matrix: List[List[str]] = [[self.blank_sym]*3 for _ in range(3)]
        self.WIN_CONDITIONS: List[List[Tuple[int,int]]] = [
            # rows
            [(0,0),(0,1),(0,2)], [(1,0),(1,1),(1,2)], [(2,0),(2,1),(2,2)],
            # cols
            [(0,0),(1,0),(2,0)], [(0,1),(1,1),(2,1)], [(0,2),(1,2),(2,2)],
            # diagonals
            [(0,0),(1,1),(2,2)], [(0,2),(1,1),(2,0)]
        ]

    def update_board(self, move: Move) -> None:
        x, y, sym = move.getMove()
        if self.board_matrix[x][y] == self.blank_sym:
            self.board_matrix[x][y] = sym
            self.n_moves += 1

        if self.is_win(move.getPlayer()):
            self.state = GameState.WIN
        elif self.is_draw():
            self.state = GameState.DRAW
        else:
            self.state = GameState.RUNNING

    def is_win(self, player: Player) -> bool:
        for line in self.WIN_CONDITIONS:
            if all(self.board_matrix[r][c].upper() == player.getSymbol().upper() for r,c in line):
                self.win_line = line
                return True
        self.win_line = None
        return False

    def is_draw(self) -> bool:
        return self.n_moves == 9 and self.win_line is None

    def reset(self) -> None:
        self.board_matrix = [[self.blank_sym]*3 for _ in range(3)]
        self.n_moves = 0
        self.win_line = None
        self.state = GameState.RUNNING
