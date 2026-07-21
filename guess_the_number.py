import random
import tkinter as tk


class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess The Number")
        self.root.geometry("380x620")
        self.root.resizable(False, False)


        # UI Color Palette (Modern Dark Mode)
        self.BG_COLOR = "#0f172a"        # Slate Dark
        self.CARD_BG = "#1e293b"         # Dark Blue-Gray
        self.TEXT_COLOR = "#f8fafc"      # Near White
        self.ACCENT_CYAN = "#06b6d4"    # Neon Cyan
        self.ACCENT_PURPLE = "#8b5cf6"  # Bright Purple
        self.BTN_BG = "#334155"         # Soft Slate
        self.BTN_HOVER = "#475569"      # Hover Slate
        self.SUCCESS_COLOR = "#10b981"   # Emerald Green
        self.DANGER_COLOR = "#ef4444"    # Soft Red
        self.WARNING_COLOR = "#f59e0b"   # Amber Yellow


        self.root.configure(bg=self.BG_COLOR)


        # Game Logic State
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.best_score = None
        self.current_input = ""
        self.is_over = False


        self.build_ui()


    def build_ui(self):
        # Header Title
        title_label = tk.Label(
            self.root,
            text="Guess The Number",
            font=("Segoe UI", 18, "bold"),
            bg=self.BG_COLOR,
            fg=self.ACCENT_CYAN
        )
        title_label.pack(pady=(20, 2))


        subtitle = tk.Label(
            self.root,
            text="Pick a number between 1 and 100",
            font=("Segoe UI", 9),
            bg=self.BG_COLOR,
            fg="#94a3b8"
        )
        subtitle.pack(pady=(0, 15))


        # Stats Bar (Attempts & Best Score)
        stats_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        stats_frame.pack(fill="x", padx=30, pady=5)


        self.attempts_label = tk.Label(
            stats_frame,
            text="Attempts: 0",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        )
        self.attempts_label.pack(side="left")


        self.best_score_label = tk.Label(
            stats_frame,
            text="Best Score: -",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_COLOR,
            fg=self.ACCENT_CYAN
        )
        self.best_score_label.pack(side="right")


        # Feedback Banner Box
        self.feedback_box = tk.Label(
            self.root,
            text="Start guessing below!",
            font=("Segoe UI", 11, "bold"),
            bg=self.CARD_BG,
            fg=self.TEXT_COLOR,
            height=2,
            width=32,
            relief="flat"
        )
        self.feedback_box.pack(pady=15)


        # Keypad Input Display
        self.display_label = tk.Label(
            self.root,
            text="_",
            font=("Segoe UI", 24, "bold"),
            bg=self.BG_COLOR,
            fg=self.ACCENT_CYAN
        )
        self.display_label.pack(pady=(0, 15))


        # Custom Keypad Grid Construction
        keypad_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        keypad_frame.pack(pady=10)


        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('⌫', 3, 0), ('0', 3, 1)
        ]


        for text, row, col in buttons:
            if text == '⌫':
                btn = tk.Button(
                    keypad_frame, text=text, font=("Segoe UI", 14, "bold"),
                    bg="#451a1a", fg=self.DANGER_COLOR, activebackground=self.DANGER_COLOR,
                    width=4, height=1, relief="flat", command=self.press_clear
                )
            else:
                btn = tk.Button(
                    keypad_frame, text=text, font=("Segoe UI", 14, "bold"),
                    bg=self.BTN_BG, fg=self.TEXT_COLOR, activebackground=self.BTN_HOVER,
                    width=4, height=1, relief="flat", command=lambda t=text: self.press_num(t)
                )
            btn.grid(row=row, column=col, padx=6, pady=6)


        # Submit / Guess Button
        guess_btn = tk.Button(
            keypad_frame,
            text="GUESS",
            font=("Segoe UI", 12, "bold"),
            bg=self.ACCENT_CYAN,
            fg="#0f172a",
            activebackground="#0284c7",
            width=4,
            height=1,
            relief="flat",
            command=self.submit_guess
        )
        guess_btn.grid(row=3, column=2, padx=6, pady=6)


        # Reset Game Button
        reset_btn = tk.Button(
            self.root,
            text="New Game",
            font=("Segoe UI", 10, "bold"),
            bg=self.BG_COLOR,
            fg=self.ACCENT_PURPLE,
            activebackground=self.ACCENT_PURPLE,
            activeforeground="#ffffff",
            bd=1,
            relief="solid",
            command=self.reset_game
        )
        reset_btn.pack(fill="x", padx=65, pady=(15, 0))


    # Button Handler Methods
    def press_num(self, digit):
        if self.is_over:
            return
        if len(self.current_input) < 3:
            self.current_input += digit
            self.update_display()


    def press_clear(self):
        if self.is_over:
            return
        self.current_input = self.current_input[:-1]
        self.update_display()


    def update_display(self):
        self.display_label.config(text=self.current_input if self.current_input else "_")


    def submit_guess(self):
        if self.is_over or not self.current_input:
            return


        guess = int(self.current_input)
        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")


        if guess < 1 or guess > 100:
            self.feedback_box.config(text="Enter a number between 1 & 100!", fg=self.TEXT_COLOR)
        elif guess < self.secret_number:
            self.feedback_box.config(text="Too Low! Try higher 📈", fg=self.WARNING_COLOR)
        elif guess > self.secret_number:
            self.feedback_box.config(text="Too High! Try lower 📉", fg=self.DANGER_COLOR)
        else:
            self.feedback_box.config(text=f"🎉 Correct! Won in {self.attempts} tries!", fg=self.SUCCESS_COLOR)
            self.is_over = True
            if self.best_score is None or self.attempts < self.best_score:
                self.best_score = self.attempts
                self.best_score_label.config(text=f"Best Score: {self.best_score}")


        self.current_input = ""
        self.update_display()


    def reset_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.current_input = ""
        self.is_over = False
        self.attempts_label.config(text="Attempts: 0")
        self.feedback_box.config(text="Game reset! Start guessing.", fg=self.TEXT_COLOR)
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()