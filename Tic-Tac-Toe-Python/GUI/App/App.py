from typing import List, Optional
import tkinter as tk
from tkinter import messagebox
from Game.Board import Board, GameState
from Game.Player import Player
from Game.Move import Move

class TicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tic-Tac-Toe")
        self.geometry("300x400")
        self.resizable(False, False)

        # Players
        self.player_x = Player("X", "Player X")
        self.player_o = Player("O", "Player O")
        self.current_player: Player = self.player_x

        # Board
        self.board: Board = Board()

        # Score
        self.score = {"X":0, "O":0}

        # Scoreboard
        self.score_label = tk.Label(self, text=self.get_score_text(), font=("Arial",14))
        self.score_label.pack(pady=10)

        # Board buttons
        self.board_frame = tk.Frame(self)
        self.board_frame.pack()
        self.buttons: List[List[Optional[tk.Button]]] = [[None]*3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.board_frame, text="", font=("Arial",24), width=4, height=2,
                    command=lambda row=r, col=c: self.make_move(row,col)
                )
                btn.grid(row=r,column=c)
                self.buttons[r][c] = btn

        # Default button background (platform-independent)
        self.default_btn_bg = tk.Button(self).cget("bg")

        # Restart button
        self.restart_btn = tk.Button(self, text="Restart", font=("Arial",12), command=self.restart_game)
        self.restart_btn.pack(pady=10)

    # -------------------
    # Utility functions
    # -------------------

    def get_score_text(self) -> str:
        return f"Score - X: {self.score['X']} | O: {self.score['O']}"

    # -------------------
    # Game logic
    # -------------------

    def update_status(self):
        self.status_label.config(text=f"{self.current_player.getName()}'s turn ({self.current_player.getSymbol()})")
        # Highlight X button only if current player is X
        if self.current_player.getSymbol() == "X":
            self.x_btn.config(bg="red")
        else:
            self.x_btn.config(bg="gray")

    def make_move(self, row: int, col: int) -> None:
        if self.board.board_matrix[row][col] != "":
            return

        move = Move(row, col, self.current_player)
        self.board.update_board(move)

        # Update button text
        btn = self.buttons[row][col]
        assert btn is not None
        btn.config(text=self.current_player.getSymbol())

        # Check for win/draw
        if self.board.state == GameState.WIN:
            self.score[self.current_player.getSymbol()] += 1
            self.highlight_win_line()
            self.score_label.config(text=self.get_score_text())
            messagebox.showinfo("Winner", f"{self.current_player.getName()} wins!")
            self.board.reset()
            self.reset_buttons()
        elif self.board.state == GameState.DRAW:
            messagebox.showinfo("Draw", "It's a draw!")
            self.board.reset()
            self.reset_buttons()
        else:
            self.current_player = self.player_o if self.current_player == self.player_x else self.player_x

    def highlight_win_line(self) -> None:
        for r, c in (self.board.win_line or []):
            btn = self.buttons[r][c]
            assert btn is not None
            btn.config(bg="lightgreen")

    def reset_buttons(self) -> None:
        for r in range(3):
            for c in range(3):
                btn = self.buttons[r][c]
                assert btn is not None
                btn.config(text="", bg=self.default_btn_bg)

    def restart_game(self) -> None:
        self.score = {"X":0,"O":0}
        self.score_label.config(text=self.get_score_text())
        self.board.reset()
        self.reset_buttons()
        self.current_player = self.player_x
