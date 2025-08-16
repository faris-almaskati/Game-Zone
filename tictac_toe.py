import tkinter as tk
from tkinter import messagebox
import random

class XandO(tk.Frame):
    def __init__(self, master, switch_page_callback, create_back_button):
        super().__init__(master)
        self.configure(bg="#a0e4fa")

        self.grans_symbol = "🌙"
        self.bot_symbol = "☀️"
        self.current_player = self.grans_symbol
        self.stop_game = False
        self.grans_wins = 0
        self.bot_wins = 0

        # Title
        title = tk.Label(self, text="  Tic Tac Toe ✨", font=("Helvetica", 18, "bold"), bg="#a0e4fa", anchor="center")
        title.pack(fill="x", pady=10)
        
        # Win Counter
        self.counter_label = tk.Label(self, text="You: 0 | Bugs: 0", font=("Helvetica", 14), bg="#a0e4fa")
        self.counter_label.pack(pady=5)

        # Game board container
        board_frame = tk.Frame(self, bg="#a0e4fa")
        board_frame.pack(pady=10)

        self.b = [[None for _ in range(3)] for _ in range(3)]
        self.states = [[0 for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.b[i][j] = tk.Button(
                    board_frame,
                    height=2,
                    width=4,
                    font=("Segoe UI Emoji", 20),
                    command=lambda r=i, c=j: self.clicked(r, c)
                )
                self.b[i][j].grid(row=i, column=j, padx=4, pady=4)

        # Restart Button
        restart_btn = tk.Button(
            self,
            text="Play Again",
            font=("Helvetica", 12),
            cursor="hand2",
            command=self.restart_game
        )
        restart_btn.pack(pady=5)

        # Back button to GameZone
        back_btn = create_back_button(self, lambda: switch_page_callback("game"))
        back_btn.place(x=10, y=10)

        # Intro Message
        self.after(500, lambda: messagebox.showinfo("Welcome!", "You are 🌙 \nBot is ☀️"))

    def clicked(self, r, c):
        if self.states[r][c] == 0 and not self.stop_game and self.current_player == self.grans_symbol:
            self.b[r][c].configure(text=self.grans_symbol)
            self.states[r][c] = self.grans_symbol
            self.check_if_win()

            if not self.stop_game:
                self.current_player = self.bot_symbol
                self.after(500, self.bot_move)

    def bot_move(self):
        if self.stop_game:
            return

        move = self.find_best_move(self.bot_symbol) or self.find_best_move(self.grans_symbol)

        if not move:
            empty_cells = [(i, j) for i in range(3) for j in range(3) if self.states[i][j] == 0]
            move = random.choice(empty_cells) if empty_cells else None

        if move:
            r, c = move
            self.b[r][c].configure(text=self.bot_symbol)
            self.states[r][c] = self.bot_symbol
            self.check_if_win()

            if not self.stop_game:
                self.current_player = self.grans_symbol

    def find_best_move(self, symbol):
        for i in range(3):
            row = self.states[i]
            if row.count(symbol) == 2 and row.count(0) == 1:
                return (i, row.index(0))

            col = [self.states[0][i], self.states[1][i], self.states[2][i]]
            if col.count(symbol) == 2 and col.count(0) == 1:
                return (col.index(0), i)

        diag1 = [self.states[i][i] for i in range(3)]
        if diag1.count(symbol) == 2 and diag1.count(0) == 1:
            idx = diag1.index(0)
            return (idx, idx)

        diag2 = [self.states[i][2 - i] for i in range(3)]
        if diag2.count(symbol) == 2 and diag2.count(0) == 1:
            idx = diag2.index(0)
            return (idx, 2 - idx)

        return None

    def check_if_win(self):
        s = self.states
        lines = []

        for i in range(3):
            lines.append([s[i][0], s[i][1], s[i][2]])
            lines.append([s[0][i], s[1][i], s[2][i]])

        lines.append([s[0][0], s[1][1], s[2][2]])
        lines.append([s[0][2], s[1][1], s[2][0]])

        for line in lines:
            if line[0] == line[1] == line[2] != 0:
                self.stop_game = True
                winner = line[0]
                messagebox.showinfo("Winner!", f"{winner} Won! 🥳")

                if winner == self.grans_symbol:
                    self.grans_wins += 1
                elif winner == self.bot_symbol:
                    self.bot_wins += 1

                self.update_counter()
                return

        if all(cell != 0 for row in s for cell in row) and not self.stop_game:
            self.stop_game = True
            messagebox.showinfo("Tie", "It's a tie! 😑")

    def restart_game(self):
        self.states = [[0 for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.b[i][j].configure(text="")
        self.stop_game = False
        self.current_player = self.grans_symbol

    def update_counter(self):
        self.counter_label.config(text=f"You: {self.grans_wins} | Bot: {self.bot_wins}")
