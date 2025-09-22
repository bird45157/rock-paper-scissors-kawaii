from tkinter import Tk, Button, Label, Frame, Toplevel
import random
import winsound
import os
import threading

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = Label(tw, text=self.text, bg="#fff0f6", fg="#d72660", font=("Courier New", 10, "bold"), bd=1, relief="solid")
        label.pack(ipadx=6, ipady=2)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class Game:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")
        master.configure(bg="#ffe4ec")  # Light pink background

        self.sound_path = os.path.join(os.path.dirname(__file__), "..", "assets", "kawaii.wav")

        # Start screen
        self.splash = Frame(master, bg="#ffe4ec")
        self.splash.pack(fill="both", expand=True)
        splash_font = ("Courier New", 24, "bold")
        self.splash_label = Label(self.splash, text="♥ Start Game? ♥", font=splash_font, bg="#ffe4ec", fg="#d72660")
        self.splash_label.pack(pady=60)
        self.splash_button = Button(self.splash, text="Start ♥", font=splash_font, bg="#ffb6c1", fg="#d72660", bd=2, relief="solid", padx=20, pady=10, command=self.start_game)
        self.splash_button.pack(pady=20)
        Tooltip(self.splash_button, "Click to begin your kawaii adventure!")

    def start_game(self):
        self.splash.pack_forget()
        self.setup_game()

    def setup_game(self):
        # Outer retro window frame
        self.window_frame = Frame(self.master, bg="#ffe4ec", bd=6, relief="solid", highlightbackground="#ffb6c1", highlightcolor="#ffb6c1", highlightthickness=6)
        self.window_frame.pack(padx=40, pady=40)

        # Pixel-art heart in window corner
        self.corner_heart = Label(self.window_frame, text="♥", font=("Courier New", 18, "bold"), bg="#ffe4ec", fg="#d72660")
        self.corner_heart.place(x=0, y=0)

        self.choices = [
            ("rock", "🪨"),
            ("paper", "📄"),
            ("scissors", "✂️")
        ]
        self.player_score = 0
        self.computer_score = 0
        self.tie_count = 0  # Track number of ties
        self.high_player_score = 0  # Track highest player score
        self.high_computer_score = 0  # Track highest computer score

        self.cute_messages = [
            "Yay! So cute!",
            "Kawaii win!",
            "So close!",
            "Heart power!",
            "You got this!",
            "UwU!",
            "Nice try!",
            "Super cute!"
        ]

        label_font = ("Courier New", 16, "bold")
        button_font = ("Courier New", 13, "bold")
        button_style = {
            "bg": "#ffb6c1",  # Soft pink
            "fg": "#d72660",
            "activebackground": "#ffe4ec",
            "activeforeground": "#d72660",
            "font": button_font,
            "bd": 2,
            "relief": "solid",
            "padx": 12,
            "pady": 8
        }

        self.title_label = Label(self.window_frame, text="rock paper scissors", font=label_font, bg="#ffe4ec", fg="#d72660", bd=0)
        self.title_label.pack(pady=(10, 8))

        self.score_label = Label(self.window_frame, text="Score - Player: 0, Computer: 0, Ties: 0", font=label_font, bg="#ffe4ec", fg="#222")
        self.score_label.pack(pady=4)

        self.high_score_label = Label(self.window_frame, text="♥ High Scores - Player: 0, Computer: 0", font=label_font, bg="#ffe4ec", fg="#d72660")
        self.high_score_label.pack(pady=4)

        self.result_label = Label(self.window_frame, text="", font=label_font, bg="#ffe4ec", fg="#222")
        self.result_label.pack(pady=8)

        # Emoji buttons for choices
        self.rock_button = Button(self.window_frame, text="Rock 🪨 ♥", command=lambda: self.button_click(lambda: self.play("rock"), self.rock_button), **button_style)
        self.rock_button.pack(pady=4)
        Tooltip(self.rock_button, "Pick rock! So strong!")

        self.paper_button = Button(self.window_frame, text="Paper 📄 ♥", command=lambda: self.button_click(lambda: self.play("paper"), self.paper_button), **button_style)
        self.paper_button.pack(pady=4)
        Tooltip(self.paper_button, "Pick paper! So soft!")

        self.scissors_button = Button(self.window_frame, text="Scissors ✂️ ♥", command=lambda: self.button_click(lambda: self.play("scissors"), self.scissors_button), **button_style)
        self.scissors_button.pack(pady=4)
        Tooltip(self.scissors_button, "Pick scissors! So sharp!")

        self.reset_button = Button(self.window_frame, text="Reset Scores ♥", command=lambda: self.button_click(self.reset_scores, self.reset_button), bg="#ffb6c1", fg="#d72660", font=button_font, bd=2, relief="solid", padx=12, pady=8)
        self.reset_button.pack(pady=(8, 4))
        Tooltip(self.reset_button, "Reset your kawaii scores!")

        self.quit_button = Button(self.window_frame, text="Quit", command=lambda: self.button_click(self.master.quit, self.quit_button), bg="#d72660", fg="white", font=button_font, bd=2, relief="solid", padx=12, pady=8)
        self.quit_button.pack(pady=(8, 8))
        Tooltip(self.quit_button, "Leave the kawaii world :(")

    def button_click(self, action, button):
        # Play kawaii sound if file exists
        if os.path.exists(self.sound_path):
            winsound.PlaySound(self.sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            winsound.Beep(880, 120)  # fallback beep
        self.animate_button(button)
        action()

    def animate_button(self, button):
        # Bounce effect
        orig_padx = button.cget("padx")
        orig_pady = button.cget("pady")
        button.config(padx=orig_padx+8, pady=orig_pady+4)
        button.after(120, lambda: button.config(padx=orig_padx, pady=orig_pady))

    def play(self, player_choice):
        computer_choice, computer_emoji = random.choice(self.choices)
        cute_message = random.choice(self.cute_messages)
        self.result_label.config(text=f"Computer chose: {computer_choice} {computer_emoji}\n{cute_message}")
        self.animate_result()

        if player_choice == computer_choice:
            self.tie_count += 1
            self.result_label.config(text=f"{self.result_label['text']}\nIt's a tie!")
            self.heart_rain()
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissors" and computer_choice == "paper"):
            self.player_score += 1
            self.result_label.config(text=f"{self.result_label['text']}\nYou win this round!")
            self.heart_rain()
        else:
            self.computer_score += 1
            self.result_label.config(text=f"{self.result_label['text']}\nComputer wins this round!")

        # Update high scores if needed
        if self.player_score > self.high_player_score:
            self.high_player_score = self.player_score
        if self.computer_score > self.high_computer_score:
            self.high_computer_score = self.computer_score

        self.score_label.config(text=f"Score - Player: {self.player_score}, Computer: {self.computer_score}, Ties: {self.tie_count}")
        self.high_score_label.config(text=f"♥ High Scores - Player: {self.high_player_score}, Computer: {self.high_computer_score}")

    def heart_rain(self):
        # Show falling hearts animation
        for i in range(8):
            heart = Label(self.window_frame, text="♥", font=("Courier New", 16, "bold"), bg="#ffe4ec", fg="#d72660")
            heart.place(x=random.randint(10, 300), y=0)
            self.animate_heart(heart, 0)

    def animate_heart(self, heart, y):
        if y < 120:
            heart.place(y=y)
            heart.after(30, lambda: self.animate_heart(heart, y+12))
        else:
            heart.destroy()

    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.tie_count = 0
        self.score_label.config(text="Score - Player: 0, Computer: 0, Ties: 0")
        self.result_label.config(text="Scores reset! UwU!")

    def animate_result(self):
        # Flash the result label color for cuteness
        original_color = self.result_label.cget("fg")
        self.result_label.config(fg="#d72660")
        self.result_label.after(200, lambda: self.result_label.config(fg=original_color))

if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    root.mainloop()