from typing import List, Optional, Tuple, Dict
import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import random
import math
from Game.Board import Board, GameState
from Game.Player import Player
from Game.Move import Move

# Color scheme
COLORS = {
    'bg': '#2c3e50',
    'board_bg': '#34495e',
    'button_bg': '#ecf0f1',
    'button_active': '#bdc3c7',
    'button_hover': '#d5dbdb',
    'text': '#2c3e50',
    'x_color': '#e74c3c',
    'o_color': '#3498db',
    'win_highlight': '#2ecc71',
    'score_bg': '#34495e',
    'score_text': '#ecf0f1'
}

# Fonts
FONTS = {
    'title': ('Helvetica', 24, 'bold'),
    'score': ('Helvetica', 14),
    'button': ('Helvetica', 32, 'bold'),
    'status': ('Helvetica', 12, 'bold')
}

class TicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure main window
        self.title("Tic-Tac-Toe Pro")
        self.geometry("500x650")
        self.configure(bg=COLORS['bg'])
        self.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure fonts
        self.option_add('*Font', 'Helvetica 12')
        
        # Game state
        self.game_active = True
        self.animation_ids = []
        
        # Players
        self.player_x = Player("X", "Player X")
        self.player_o = Player("O", "Player O")
        self.current_player = self.player_x
        
        # Game statistics
        self.stats = {
            'total_games': 0,
            'x_wins': 0,
            'o_wins': 0,
            'draws': 0,
            'win_streak': 0,
            'max_win_streak': 0
        }
        
        # Board
        self.board = Board()
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        self.main_frame = ttk.Frame(self, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame,
            text="Tic-Tac-Toe Pro",
            font=FONTS['title'],
            foreground='white',
            background=COLORS['bg']
        )
        self.title_label.pack(pady=(0, 20))
        
        # Score frame
        self.score_frame = ttk.Frame(self.main_frame, style='Score.TFrame')
        self.score_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Score labels
        self.score_x = ttk.Label(
            self.score_frame,
            text="X: 0",
            font=FONTS['score'],
            foreground=COLORS['x_color'],
            background=COLORS['score_bg'],
            padding=10
        )
        self.score_x.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.score_ties = ttk.Label(
            self.score_frame,
            text=f"Ties: {self.stats['draws']}",
            font=FONTS['score'],
            foreground='white',
            background=COLORS['score_bg'],
            padding=10
        )
        self.score_ties.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.score_o = ttk.Label(
            self.score_frame,
            text="O: 0",
            font=FONTS['score'],
            foreground=COLORS['o_color'],
            background=COLORS['score_bg'],
            padding=10
        )
        self.score_o.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text=f"{self.current_player.getName()}'s Turn ({self.current_player.getSymbol()})",
            font=FONTS['status'],
            foreground='white',
            background=COLORS['bg']
        )
        self.status_label.pack(pady=(0, 20))
        
        # Game board
        self.board_frame = ttk.Frame(self.main_frame, style='Board.TFrame')
        self.board_frame.pack(pady=10)
        
        # Create game board buttons
        self.buttons = [[None]*3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=FONTS['button'],
                    width=3,
                    height=1,
                    bg=COLORS['button_bg'],
                    fg=COLORS['text'],
                    relief='ridge',
                    borderwidth=2,
                    command=lambda row=r, col=c: self.make_move(row, col)
                )
                btn.grid(row=r, column=c, padx=2, pady=2, ipadx=10, ipady=10)
                
                # Add hover effects
                btn.bind('<Enter>', lambda e, b=btn: self.on_enter(e, b))
                btn.bind('<Leave>', lambda e, b=btn: self.on_leave(e, b))
                
                self.buttons[r][c] = btn
        
        # Control buttons frame
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(pady=(20, 0))
        
        # Restart button
        self.restart_btn = ttk.Button(
            self.control_frame,
            text="New Game",
            command=self.restart_game,
            style='Accent.TButton'
        )
        self.restart_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats button
        self.stats_btn = ttk.Button(
            self.control_frame,
            text="Statistics",
            command=self.show_stats,
            style='TButton'
        )
        self.stats_btn.pack(side=tk.LEFT, padx=5)
        
        # Configure styles
        self.configure_styles()
        
    def configure_styles(self):
        # Configure frame styles
        self.style.configure('TFrame', background=COLORS['bg'])
        self.style.configure('Board.TFrame', background=COLORS['board_bg'])
        self.style.configure('Score.TFrame', background=COLORS['score_bg'])
        
        # Configure button styles
        self.style.configure('TButton',
                           font=FONTS['status'],
                           padding=10)
                           
        self.style.configure('Accent.TButton',
                           font=FONTS['status'],
                           padding=10,
                           foreground='white',
                           background='#27ae60')
        
        # Configure label styles
        self.style.configure('TLabel',
                           background=COLORS['bg'],
                           foreground='white')
        
        # Configure button hover effects
        self.style.map('TButton',
                      foreground=[('active', 'white')],
                      background=[('active', COLORS['button_active'])])
        
        self.style.map('Accent.TButton',
                      background=[('active', '#2ecc71')])

    # -------------------
    # Event Handlers
    # -------------------
    
    def on_enter(self, e, button):
        if button['state'] == 'normal' and button['text'] == '':
            button['bg'] = COLORS['button_hover']
            symbol = self.current_player.getSymbol()
            button['text'] = symbol
            # Use a lighter shade for the hover effect instead of transparency
            if symbol == 'X':
                button['fg'] = '#ff6b6b'  # Lighter red for X
            else:
                button['fg'] = '#6bb9ff'  # Lighter blue for O
    
    def on_leave(self, e, button):
        if button['state'] == 'normal' and button['text'] == self.current_player.getSymbol():
            button['bg'] = COLORS['button_bg']
            button['text'] = ''
            
    def animate_win(self, buttons, step=0):
        if not buttons or not self.game_active:
            return
            
        # Calculate pulse intensity (0.5 to 1.0)
        intensity = 0.75 + 0.25 * (1 + math.sin(step * 0.2))
        
        # Convert base color to RGB
        r, g, b = [int(x * intensity) for x in (46, 204, 113)]  # Base color: #2ecc71
        color = f'#{r:02x}{g:02x}{b:02x}'
        
        # Apply to all winning buttons
        for btn in buttons:
            btn.config(bg=color, fg='white')
        
        # Schedule next animation frame
        self.after(50, lambda: self.animate_win(buttons, step + 1))
            
    def stop_animations(self):
        self.game_active = False  # This will stop the animation loop
    
    # -------------------
    # Game Logic
    # -------------------

    # -------------------
    # Game logic
    # -------------------

    def update_status(self):
        player_name = self.current_player.getName()
        symbol = self.current_player.getSymbol()
        self.status_label.config(text=f"{player_name}'s Turn ({symbol})")
        
        # Update score display
        self.score_x.config(text=f"X: {self.stats['x_wins']}")
        self.score_o.config(text=f"O: {self.stats['o_wins']}")
        self.score_ties.config(text=f"Ties: {self.stats['draws']}")
        
        # Update button hover effects
        for row in self.buttons:
            for btn in row:
                if btn['text'] == '':
                    btn.bind('<Enter>', lambda e, b=btn: self.on_enter(e, b))
                    btn.bind('<Leave>', lambda e, b=btn: self.on_leave(e, b))

    def make_move(self, row: int, col: int) -> None:
        if not self.game_active or self.board.board_matrix[row][col] != "":
            return
            
        # Make the move
        move = Move(row, col, self.current_player)
        self.board.update_board(move)
        
        # Update the button
        btn = self.buttons[row][col]
        symbol = self.current_player.getSymbol()
        btn.config(
            text=symbol,
            fg=COLORS['x_color'] if symbol == 'X' else COLORS['o_color'],
            state='disabled'
        )
        
        # Check game state
        if self.board.state == GameState.WIN:
            self.handle_win()
        elif self.board.state == GameState.DRAW:
            self.handle_draw()
        else:
            self.switch_player()
            self.update_status()

    def highlight_win_line(self) -> None:
        if not self.board.win_line:
            return
            
        win_buttons = []
        for r, c in self.board.win_line:
            btn = self.buttons[r][c]
            win_buttons.append(btn)
            
        # Start smooth win animation
        self.game_active = True  # Ensure animation runs
        self.animate_win(win_buttons)
        
    def handle_win(self):
        # Update stats
        self.stats['total_games'] += 1
        winner = self.current_player.getSymbol()
        
        if winner == 'X':
            self.stats['x_wins'] += 1
            self.stats['win_streak'] = self.stats['win_streak'] + 1 if self.stats['win_streak'] >= 0 else 1
        else:
            self.stats['o_wins'] += 1
            self.stats['win_streak'] = self.stats['win_streak'] - 1 if self.stats['win_streak'] <= 0 else -1
            
        self.stats['max_win_streak'] = max(
            self.stats['max_win_streak'],
            abs(self.stats['win_streak'])
        )
        
        # Highlight winning line
        self.highlight_win_line()
        
        # Disable all buttons
        self.game_active = False
        
        # Show win message
        winner_name = self.current_player.getName()
        messagebox.showinfo(
            "Game Over",
            f"🎉 {winner_name} wins! 🎉\n\n"
            f"{self.stats['x_wins']} - {self.stats['o_wins']} - {self.stats['draws']}"
        )
        
    def handle_draw(self):
        # Update stats
        self.stats['total_games'] += 1
        self.stats['draws'] += 1
        
        # Show draw message
        messagebox.showinfo(
            "Game Over",
            "It's a draw! 🤝\n\n"
            f"{self.stats['x_wins']} - {self.stats['o_wins']} - {self.stats['draws']}"
        )
    
    def switch_player(self):
        self.current_player = self.player_o if self.current_player == self.player_x else self.player_x

    def reset_buttons(self) -> None:
        for row in self.buttons:
            for btn in row:
                btn.config(
                    text="",
                    bg=COLORS['button_bg'],
                    fg=COLORS['text'],
                    state='normal'
                )

    def restart_game(self) -> None:
        # Stop any running animations
        self.stop_animations()
        
        # Reset game state
        self.game_active = True
        self.board.reset()
        self.reset_buttons()
        
        # Randomize starting player for variety
        if random.choice([True, False]):
            self.current_player = self.player_x
        else:
            self.current_player = self.player_o
            
        # Update UI
        self.update_status()
        
    def show_stats(self):
        win_percentage = (
            (self.stats['x_wins'] + self.stats['o_wins']) / 
            max(1, self.stats['total_games']) * 100
        ) if self.stats['total_games'] > 0 else 0
        
        stats_text = (
            f"📊 Game Statistics\n\n"
            f"Total Games: {self.stats['total_games']}\n"
            f"X Wins: {self.stats['x_wins']}\n"
            f"O Wins: {self.stats['o_wins']}\n"
            f"Draws: {self.stats['draws']}\n"
            f"Win Rate: {win_percentage:.1f}%\n"
            f"Current Streak: {abs(self.stats['win_streak'])} "
            f"({'X' if self.stats['win_streak'] > 0 else 'O' if self.stats['win_streak'] < 0 else ''})\n"
            f"Max Win Streak: {self.stats['max_win_streak']}"
        )
        
        messagebox.showinfo("Game Statistics", stats_text)
        
    def on_closing(self):
        # Clean up resources
        self.stop_animations()
        self.destroy()
