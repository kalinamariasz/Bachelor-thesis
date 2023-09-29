from tkinter import *
from demo import Demo
from game_1 import Game_1
from game_2 import Game_2
from game_3 import Game_3
from game_4 import Game_4
from game_5 import Game_5
from game_6 import Game_6
from tkinter import simpledialog
from tkinter import messagebox
import random
import csv
from participant_info import Participant


# Display instructions
def show_info():
    messagebox.showinfo("Instructions", """In this experiment, you will be playing 6 games of 'The Mind' in cooperation with the computer imitating human game play. In every game, \
both you and the computer will receive 3 cards with a number between 1 and 100. Only your cards are visible to you.

The goal of the game is to cooperate with the computer so that all 6 cards are played in ascending order. You can play your card at any time.  Once you play your card, it will appear \
in the centre of the screen, on the discard pile. You should estimate how long you should wait before playing your lowest card so that if your card is lower, you play it first, but if \
the computer’s card is lower, its card is played first.""")
    
    messagebox.showinfo("Instructions", """Throughout the game, you will be asked about how long you waited before you played your card. Type your answer in seconds, using the keyboard.

Note that the question means how long you waited since the previous card was played to the discard pile. That means the previous card could have been either played by you or by the computer.""")
    
    messagebox.showinfo("Instructions", """The first game is a trial game. In this game, both you and the computer receive only one card. After you have played your card, \
the trial game ends, and the first game will start. Start the trial game by pressing the button \"Trial game\".""")


if __name__ == '__main__':
    root = Tk()
    root.title('The Mind')
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
    root.configure(background='darkseagreen')
    # Ask for informed consent
    consent_answer = messagebox.askyesno("Informed consent", """This experiment is about the game 'The Mind'. The aim of this experiment is to examine how humans play the game. You will be \
asked to play that game using a computer interface. The data about your gameplay and your age will be recorded. All information will remain confidential and anonymous.

Your participation is voluntary. You can terminate your participation at any moment by exiting the experiment; your information will be discarded then. Your participation in the study \
will require around 5-10 minutes. The researcher will answer any questions you might have during and after the experiment.

Have you read the agreement and consent to the collection and processing of your data?""")

    participant_info = Participant()

    # All games, except for game (1), are played in random order
    games = [2, 3, 4, 5, 6]
    random.shuffle(games)
    if consent_answer is True:
        age_answer = simpledialog.askstring("Survey", "How old are you?", parent=root)
        # Save the data to the files
        with open('Experiment_data_' + str(participant_info.id) + '.txt', 'w') as f:
            f.write('Age: ' + str(age_answer) + '\n')
        with open('Experiment_data_' + str(participant_info.id) + '.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=participant_info.fieldnames)
            writer.writeheader()
            writer.writerow({"ID": participant_info.id, "Age": age_answer})
        if age_answer!="" and age_answer is not None:
            show_info()
            # Show demo and play all games
            trial = Demo(root)
            trial.start_game()
            root.mainloop()
            game = Game_1(root)
            game.start_game()
            root.mainloop()
            for g in games:
                if g==2:
                    game = Game_2(root)
                if g==3:
                    game = Game_3(root)
                if g==4:
                    game = Game_4(root)
                if g==5:
                    game = Game_5(root)
                if g==6:
                    game = Game_6(root)
                game.start_game()
                root.mainloop()
            # Display the end message
            end_message = Label(root, background='darkseagreen', font=("system", 20), text='This is the end of the experiment.\n\nThank you for your participation.')
            end_message.place(relx=0.5, rely=0.5, anchor=CENTER)
            root.mainloop()
    else:
        root.quit()