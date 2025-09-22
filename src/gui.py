class GameGUI:
    def __init__(self, master):
        self.master = master
        master.title("Rock Paper Scissors")

        self.choices = ['rock', 'paper', 'scissors']
        self.player_score = 0
        self.computer_score = 0

        self.label = Label(master, text="Choose rock, paper, or scissors:")
        self.label.pack()

        self.rock_button = Button(master, text="Rock", command=lambda: self.play("rock"))
        self.rock_button.pack()

        self.paper_button = Button(master, text="Paper", command=lambda: self.play("paper"))
        self.paper_button.pack()

        self.scissors_button = Button(master, text="Scissors", command=lambda: self.play("scissors"))
        self.scissors_button.pack()

        self.result_label = Label(master, text="")
        self.result_label.pack()

        self.score_label = Label(master, text="Score - Player: 0, Computer: 0")
        self.score_label.pack()

        self.quit_button = Button(master, text="Quit", command=master.quit)
        self.quit_button.pack()

    def play(self, player_choice):
        computer_choice = random.choice(self.choices)
        self.result_label.config(text=f"Computer chose: {computer_choice}")

        if player_choice == computer_choice:
            self.result_label.config(text=f"{self.result_label['text']} - It's a tie!")
        elif (player_choice == "rock" and computer_choice == "scissors") or \
             (player_choice == "paper" and computer_choice == "rock") or \
             (player_choice == "scissors" and computer_choice == "paper"):
            self.player_score += 1
            self.result_label.config(text=f"{self.result_label['text']} - You win this round!")
        else:
            self.computer_score += 1
            self.result_label.config(text=f"{self.result_label['text']} - Computer wins this round!")

        self.score_label.config(text=f"Score - Player: {self.player_score}, Computer: {self.computer_score}")