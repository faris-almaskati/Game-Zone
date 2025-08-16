import tkinter as tk
import random

class GamePage(tk.Frame):
    def __init__(self, master, switch_page_callback, create_back_button, _, __):
        super().__init__(master)
        self.configure(bg="#5d92c9")

        # Canvas behind everything
        self.canvas = tk.Canvas(self, bg="#5d92c9", highlightthickness=0)
        self.canvas.place(relwidth=1, relheight=1)

        # Title
        label = tk.Label(self, text="Game Zone 🎮", font=("Helvetica", 20, "bold"), bg="#5d92c9")
        label.pack(pady=40)
        label.lift()

        # Hangman Button
        hangman_btn = tk.Button(
            self,
            text="Hangman 🔤",
            font=("Helvetica", 14),
            width=20,
            anchor="center",
            justify="center",
            command=lambda: switch_page_callback("hangman")
        )
        hangman_btn.pack(pady=(20, 10))
        hangman_btn.lift()

        # Tic-Tac-Toe Button
        tictactoe_btn = tk.Button(
            self,
            text="     Tic Tac Toe 🌙☀️",
            font=("Helvetica", 14),
            width=20,
            anchor="center",
            justify="center",
            command=lambda: switch_page_callback("xo")
        )
        tictactoe_btn.pack(pady=(20, 10))
        tictactoe_btn.lift()

        # Start heart animation after layout is ready
        self.after(500, self.animate_hearts)

    def create_heart(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return

        x = random.randint(20, canvas_width - 20)
        y = random.randint(20, canvas_height - 20)
        heart = self.canvas.create_text(x, y, text="⋆", fill="#FFFFFF", font=("Helvetica", 14))
        self.animate_single_heart(heart)

    def animate_single_heart(self, heart, step=0):
        if step < 40:
            self.canvas.move(heart, 0, -2)
            self.after(50, lambda: self.animate_single_heart(heart, step + 1))
        else:
            self.canvas.delete(heart)

    def animate_hearts(self):
        self.create_heart()
        self.after(300, self.animate_hearts)
