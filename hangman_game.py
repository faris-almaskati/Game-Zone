import tkinter as tk
from random import choice

class HangMan(tk.Frame):
    def __init__(self, master, switch_page_callback, create_back_button):
        super().__init__(master)
        self.configure(bg="#a0e4fa")

        self.word_list = ["avocado", "sausage", "sushi", "baguette", "matcha", "lasagna"]
        self.max_tries = 6
        self.player_score = 0
        self.computer_score = 0

        # Title
        self.title_label = tk.Label(self, text="Hangman 🔤", font=("Helvetica", 18, "bold"), bg="#a0e4fa")
        self.title_label.pack(pady=10)

        # Hangman graphic
        self.hangman_label = tk.Label(self, text="", font=("Courier", 12), bg="#a0e4fa", justify="left")
        self.hangman_label.pack()

        # Clue display
        self.clue_label = tk.Label(self, text="", font=("Helvetica", 16), bg="#a0e4fa")
        self.clue_label.pack(pady=10)

        # Entry for guessing
        self.entry = tk.Entry(self, font=("Helvetica", 14))
        self.entry.pack()

        # Submit button
        self.submit_btn = tk.Button(self, text="Guess", font=("Helvetica", 12), command=self.process_guess)
        self.submit_btn.pack(pady=5)

        # Feedback
        self.feedback_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#a0e4fa")
        self.feedback_label.pack()

        # Guessed letters
        self.guessed_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#a0e4fa")
        self.guessed_label.pack()

        # Score
        self.score_label = tk.Label(self, text="", font=("Helvetica", 12), bg="#a0e4fa")
        self.score_label.pack(pady=10)

        # Restart button
        self.restart_btn = tk.Button(self, text="Play Again", font=("Helvetica", 12),
            cursor="hand2", command=self.start_game)
        self.restart_btn.pack(pady=5)

        # Back button to GameZone
        back_btn = create_back_button(self, lambda: switch_page_callback("game"))
        back_btn.place(x=10, y=10)

        self.start_game()

    def start_game(self):
        self.word = choice(self.word_list)
        self.clue = ["_"] * len(self.word)
        self.letters_tried = []
        self.letters_wrong = 0
        self.entry.config(state="normal")
        self.feedback_label.config(text="Try and guess the mystery word 🤔 Food category!")
        self.update_display()

    def process_guess(self):
        letter = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)

        if len(letter) != 1 or not letter.isalpha():
            self.feedback_label.config(text="Invalid input, choose another.")
            return

        if letter in self.letters_tried:
            self.feedback_label.config(text=f"You've already picked '{letter}'")
            return

        self.letters_tried.append(letter)

        if letter in self.word:
            self.feedback_label.config(text=f"Congrats! '{letter}' is correct!")
            for i, char in enumerate(self.word):
                if char == letter:
                    self.clue[i] = letter
        else:
            self.letters_wrong += 1
            self.feedback_label.config(text=f"Sorry, '{letter}' is incorrect.")

        self.update_display()
        self.check_game_over()

    def update_display(self):
        self.hangman_label.config(text=self.hangedman(self.letters_wrong))
        self.clue_label.config(text=" ".join(self.clue))
        self.guessed_label.config(text=f"Guesses: {', '.join(self.letters_tried)}")
        self.score_label.config(text=f"You: {self.player_score} | Bot: {self.computer_score}")

    def check_game_over(self):
        if self.letters_wrong >= self.max_tries:
            self.feedback_label.config(text=f"Game Over 😓 The word was '{self.word}'")
            self.computer_score += 1
            self.entry.config(state="disabled")
        elif "".join(self.clue) == self.word:
            self.feedback_label.config(text=f"Winner winner chicken dinner! 🥳 The word was '{self.word}'")
            self.player_score += 1
            self.entry.config(state="disabled")

    def hangedman(self, stage):
        graphic = [
            """
+-------+
|
|
| 
|
|
==============
""",
            """
+-------+
|       |
|       0
| 
|
|
==============
""",
            """
+-------+
|       |
|       0
|       |
|
|
==============
""",
            """
+-------+
|       |
|       0
|      -|
|
|
==============
""",
            """
+-------+
|       |
|       0
|      -|-
|
|
==============
""",
            """
+-------+
|       |
|       0
|      -|-
|      /
|
==============
""",
            """
+-------+
|       |
|       0
|      -|-
|      / \\
|
==============
"""
        ]
        return graphic[min(stage, self.max_tries)]
