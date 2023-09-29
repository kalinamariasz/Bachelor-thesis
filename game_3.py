from tkinter import *
from PIL import Image, ImageTk
import time
from tkinter import simpledialog
import csv
from participant_info import Participant


class Game_3:
    def __init__(self, root):
        self.root = root
        self.player_frame = Frame(root, bg='darkseagreen')
        self.player_frame.pack(side="bottom")
        self.computer_frame = Frame(root, bg='darkseagreen')
        self.computer_frame.pack(side="top")
        self.current_frame = Frame(root, bg='darkseagreen')
        self.current_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.computer_numbers = [20, 50, 100]
        self.player_numbers = [44, 72, 98]
        self.player_hand = []
        self.computer_hand = []
        self.current_card = 0
        self.previous_card = 0
        self.photos_cards_computer = []
        self.photos_cards_player = []
        self.index_computer_photos = 0
        self.root = root
        self.time_computer_played = 0
        self.game_end = False
        self.time_perception_array = []
        self.actual_time_array = []
        self.time_current_changed = 0
        self.wait = None
        self.participant_info = Participant()


    # Make a button 'Start game' that deals cards after clicking it
    def start_game(self):
        # Start the timer for the current card
        self.time_current_changed = time.time()
        self.start_game_button = Button(self.root, text="Start game", font=("system", 20), command=lambda:self.deal_cards(), 
                                        bg="white", bd=1, activebackground="darkseagreen")
        self.start_game_button.place(relx=0.5, rely=0.5, anchor=CENTER)


    def deal_cards(self):
        # Make a headline for the new game
        with open('Experiment_data_' + str(self.participant_info.id) + '.txt', 'a') as f:
                f.write('\n')
                f.write('GAME 3\n')
        # Append computer's and player's numbers to their hands
        for i in self.computer_numbers:
            self.computer_hand.append("{}_card".format(i))
        for i in self.player_numbers:
            self.player_hand.append("{}_card".format(i))
        # Remove the start button
        self.start_game_button.place_forget()

        # For every card in the hand, append the picture representation of it to an array
        for card in self.player_hand:
            resized_card = self.resize_cards(f'card_images/{card}.jpg')
            self.photos_cards_player.append(resized_card)
        for card in self.computer_hand:
            resized_card_r = self.resize_cards(f'card_images/{card}.jpg')
            self.photos_cards_computer.append(resized_card_r)
        # Show cards and make the computer wait to play its card
        self.show_cards_player()
        self.show_cards_computer()
        self.computer_wait()
        # Start the timer for the current card
        self.time_current_changed = time.time()

    
    def computer_wait(self):
        # The card that the computer will play is its first (lowest) card
        card = self.computer_numbers[0]
        # EXCEPTION: Computer waits for the player to play 98 to play 100
        if card == 100:
            if self.current_card == 98:
                self.wait = self.current_frame.after(1000, lambda: self.play_card_computer())
        # If it's higher than the current card, start waiting to play your card
        elif card > self.current_card:
            # If you have already been in the process of waiting, stop counting that waiting time
            if self.wait is not None:
                self.current_frame.after_cancel(self.wait)
            # If the player played all their cards, computer waits just 1 second with playing its card
            if len(self.player_numbers) == 0:
                self.wait = self.current_frame.after(1000, lambda: self.play_card_computer())
            else:
                # The new waiting time is the gap between the computer's card and the current card
                waiting_time = (card-self.current_card)*1000
                # After the waiting time elapses, the computer plays its card
                self.wait = self.current_frame.after(waiting_time, lambda: self.play_card_computer())
    

    def play_card_computer(self):
        # Start the timers of when the computer played its card and when the card in the middle changed
        self.time_computer_played = time.time()
        self.time_current_changed = time.time()
        # Put the computer's card in the middle and remove it from its hand
        self.cards_in_the_middle(self.photos_cards_computer[self.index_computer_photos])
        self.panel_0.grid(row=0, column= 0)
        self.computer_hand.remove("{}_card".format(self.computer_numbers[0]))
        self.index_computer_photos += 1
        self.order_check_computer()


    # For each player's card, make a button. Once clicked, order_check_player fires
    def show_cards_player(self):
        self.panel_1 = Button(self.player_frame, image=self.photos_cards_player[0], bg='darkseagreen',
                        command= lambda: self.order_check_player(0), state= NORMAL)
        self.panel_1.grid(row=0, column=1)
            
        self.panel_2 = Button(self.player_frame, image=self.photos_cards_player[1], bg='darkseagreen',
                        command= lambda: self.order_check_player(1), state= NORMAL)
        self.panel_2.grid(row=0, column=2)

        self.panel_3 = Button(self.player_frame, image=self.photos_cards_player[2], bg='darkseagreen',
                        command= lambda: self.order_check_player(2), state= NORMAL)
        self.panel_3.grid(row=0, column=3)


    def show_cards_computer(self):
        self.resized_card_computer = self.resize_cards(f'card_images/comp_card.jpg')
        # Put computer's cards with the back picture in grids, forget the grids for the cards that have been removed from the hand
        self.panel_4 = Label(self.computer_frame, image=self.resized_card_computer, bg="darkseagreen")
        self.panel_4.grid(row=0, column=1)
        if len(self.computer_hand)<3:
            self.panel_4.grid_forget()  
        self.panel_5 = Label(self.computer_frame, image=self.resized_card_computer, bg="darkseagreen")
        self.panel_5.grid(row=0, column=2)
        if len(self.computer_hand)<2:
            self.panel_5.grid_forget()
        self.panel_6 = Label(self.computer_frame, image=self.resized_card_computer, bg="darkseagreen")
        self.panel_6.grid(row=0, column=3)
        if len(self.computer_hand)<1:
            self.panel_6.grid_forget()


    def order_check_player(self, x):
        if self.game_end is False:
            # The chosen card x is the card that the player pressed on
            card_number = int(self.player_hand[x].split("_", 1)[0])
            # If it is higher than the smallest card the player still has:
            if card_number > min(self.player_numbers):
                # Display the textbox
                mistake_label = Label(self.root, text="Play the lowest card", height = 2, width = 25, font=("system", 20),
                                    borderwidth=2, relief="solid")
                mistake_label.place(relx=0.5, rely=0.1, anchor=CENTER)
                mistake_label.after(1700, mistake_label.destroy)
            # If it is higher than the smallest card the computer still has:
            elif len(self.computer_numbers)>0 and card_number > min(self.computer_numbers):
                # Display the textbox
                lower_card_label = Label(self.root, text="Computer had the lower card", height = 2, width = 30, font=("system", 20),
                                    borderwidth=2, relief="solid")
                lower_card_label.place(relx=0.5, rely=0.1, anchor=CENTER)
                lower_card_label.after(1500, lower_card_label.destroy)
                # If some time passed since the computer played its last card (so it did not play it while the textbox was displayed), play the card
                if time.time() > self.time_computer_played:
                    self.current_frame.after(1000, self.play_card_computer)
            else:
                # Forget the grid of the card that was played
                if x == 0:
                    self.panel_1.grid_forget()
                if x == 1:
                    self.panel_2.grid_forget()
                if x == 2:
                    self.panel_3.grid_forget()
                # Put the card in the middle and save the previous card
                self.cards_in_the_middle(self.photos_cards_player[x])
                self.previous_card = self.current_card
                self.current_card = min(self.player_numbers)
                # Remove it from the player's numbers
                self.player_numbers.remove(min(self.player_numbers))
                # Stop counting the waiting time so that the computer will not play its card while the participant is answering the question
                if self.wait is not None:
                    self.current_frame.after_cancel(self.wait)
                # Ask about time perception
                self.ask_question()
                # Check if the game ended
                self.root.after(2000, self.check_if_end)
                 # If the computer still has cards, start waiting
                if len(self.computer_numbers)>0:
                    self.computer_wait()


    # Ask the player about time perception
    def ask_question(self):
        # Save the situation on the screen
        with open('Experiment_data_' + str(self.participant_info.id) + '.txt', 'a') as f:
                f.write('Previous card: ' + str(self.previous_card) + "\n")
                f.write('Played card: ' + str(self.current_card) + "\n")
                f.write('Player\'s cards: ' + str(self.player_numbers) + "\n")
                f.write('Computer\'s cards: ' + str(self.computer_numbers) + "\n")
        # The actual elapsed time is the difference between the current time and when the last card was played
        elapsed_time = time.time() - self.time_current_changed
        with open('Experiment_data_' + str(self.participant_info.id) + '.txt', 'a') as f:
            f.write('Actual elapsed time: ' + str(elapsed_time) + "\n")
        # Ask the question and record the answer
        answer = 0
        answer = simpledialog.askstring("Experiment", "How much time [in seconds] has passed before you played your card, since the previous card was played?", parent=self.root)
        with open('Experiment_data_' + str(self.participant_info.id) + '.txt', 'a') as f:
            f.write('Perceived elapsed time: ' + str(answer) + "\n")
            f.write('\n')
        # Save in the csv file
        with open('Experiment_data_' + str(self.participant_info.id) + '.csv', 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.participant_info.fieldnames)
            writer.writerow({"ID": '-', "Age": '-', "Game number": 3, "Previous card": self.previous_card, "Played card": self.current_card, "Time elapsed": elapsed_time, "Time estimated": answer, "Cards participant": self.player_numbers, "Number of cards participant": len(self.player_numbers), "Cards computer": self.computer_numbers, "Number of cards computer": len(self.computer_numbers)})
        # Update the time since the player played their card
        self.time_current_changed = time.time()


    def check_if_end(self):
        # The game ends if the computer and player have no cards left and game has not ended yet
        if (len(self.computer_numbers) == 0 and len(self.player_numbers) == 0) and self.game_end is False:
            self.current_frame.place_forget()
            self.player_frame.pack_forget()
            self.computer_frame.pack_forget()
            # Stop counting the waiting time
            self.current_frame.after_cancel(self.wait)
            # End the game
            self.root.quit()
            self.game_end = True
    

    def lower_card_player(self):
        # If the player had a lower card than what the computer played:
        if len(self.player_numbers)>0:
            if self.current_card > min(self.player_numbers):
                # Stop counting the waiting time so that the computer will not play its card while the mistakes are corrected
                if self.wait is not None:
                    self.current_frame.after_cancel(self.wait)
                # Display the textbox
                mistake_label = Label(self.root, text="You had the lower card", height = 2, width = 35, font=("system", 20),
                                        borderwidth=2, relief="solid")
                mistake_label.place(relx=0.5, rely=0.1, anchor=CENTER)
                mistake_label.after(3000, mistake_label.destroy)
                # Remove the card from the player's numbers and from the screen
                self.player_numbers.remove(min(self.player_numbers))
                if len(self.player_numbers)<3:
                    self.current_frame.after(2000, self.panel_1.grid_forget)
                if len(self.player_numbers)<2:
                    self.current_frame.after(2000, self.panel_2.grid_forget)
                if len(self.player_numbers)<1:
                    self.current_frame.after(2000, self.panel_3.grid_forget)
                # Record the mistake in the text and in the csv file
                with open('Experiment_data_' + str(self.participant_info.id) + '.txt', 'a') as f:
                    f.write("Mistake\n")
                    f.write("\n")
                with open('Experiment_data_' + str(self.participant_info.id) + '.csv', 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.participant_info.fieldnames)
                    writer.writerow({"ID": '-', "Age": '-', "Game number": 3, "Previous card": self.previous_card, "Played card": self.current_card, "Time elapsed": 'mistake', "Time estimated": 'mistake', "Cards participant": self.player_numbers, "Number of cards participant": len(self.player_numbers), "Cards computer": self.computer_numbers, "Number of cards computer": len(self.computer_numbers)})
                # Check if that ended the game, if not, make the computer wait
                self.root.after_cancel(self.end_game)
                self.end_game = self.root.after(3800, self.check_if_end)
                if len(self.computer_numbers)>0:
                    self.root.after(4000, self.computer_wait)
                # Check if there are still lower cards in the player's numbers
                self.root.after(4000, self.lower_card_player)


    def order_check_computer(self):
        # Put computer's card in the middle and remove it from its numbers. Save the previous card
        self.previous_card = self.current_card
        self.current_card = min(self.computer_numbers)
        self.computer_numbers.remove(min(self.computer_numbers))
        # Update computer's cards and start waiting
        self.show_cards_computer()
        # Check if the game ended
        self.end_game = self.root.after(2000, self.check_if_end)
        if self.game_end is False:
            # If the computer still has cards, start waiting
            if len(self.computer_numbers)>0:
                self.computer_wait()
            # Check if the player had a lower card than what the computer played
            self.lower_card_player()


    # Resize cards
    def resize_cards(self, card):
        entry_card = Image.open(card)
        resized_image = entry_card.resize((160,230))
        final_card = ImageTk.PhotoImage(resized_image)
        return final_card


    # Update the photo of the card in the middle
    def cards_in_the_middle(self, card):
        self.panel_0 = Label(self.current_frame, image=card, bg="darkseagreen")
        self.panel_0.grid(row=0, column=0)