import tkinter as tk
from gamezone import GamePage
from hangman_game import HangMan
from tictac_toe import XandO
import os

print("Running from:", os.path.abspath(__file__))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Zone")
        self.geometry("500x500")
        self.resizable(False, False)

        self.frames = {}

        # Load GamePage as the main hub
        self.frames["game"] = GamePage(
            self,
            self.switch_page,
            self.create_back_button,
            self.frames.get("game"),
            self.show_frame
        )

        self.current_frame = None
        self.switch_page("game")

    def switch_page(self, page_name):
        if self.current_frame:
            self.current_frame.pack_forget()

        if page_name in self.frames:
            self.current_frame = self.frames[page_name]
        else:
            if page_name == "hangman":
                self.frames["hangman"] = HangMan(
                    self,
                    self.switch_page,
                    self.create_back_button
                )
                self.current_frame = self.frames["hangman"]

            elif page_name == "xo":
                self.frames["xo"] = XandO(
                    self,
                    self.switch_page,
                    self.create_back_button
                )
                self.current_frame = self.frames["xo"]

        self.current_frame.pack(fill="both", expand=True)

    def create_back_button(self, parent, command):
        return tk.Button(
            parent,
            text="← Back",
            font=("Helvetica", 12),
            bg="#f0f0f0",
            fg="#333",
            relief="flat",
            cursor="hand2",
            command=command
        )

    def show_frame(self, frame):
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
