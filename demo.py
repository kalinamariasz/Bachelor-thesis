from tkinter import *
from PIL import Image, ImageTk


class Demo:
    def __init__(self, root):
        self.root = root
        self.player_frame = Frame(root, bg='darkseagreen')
        self.player_frame.pack(side="bottom")
        self.computer_frame = Frame(root, bg='darkseagreen')
        self.computer_frame.pack(side="top")
        self.current_frame = Frame(root, bg='darkseagreen')
        self.current_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.computer_numbers = [20]
        self.player_numbers = [5]
        self.player_hand = []
        self.computer_hand = []
        self.current_card = 0
        self.photos_cards_computer = []
        self.photos_cards_player = []
        self.index_computer_photos = 0
        self.root = root
        self.time_computer_played = 0
        self.game_end = False
        self.wait = None

    
    # Make a button 'Trial game' that starts the demo after clicking it
    def start_game(self):
        self.start_game_button = Button(self.root, text="Trial game", font=("system", 20), command=lambda:self.deal_cards(), 
                                        bg="white", bd=1, activebackground="darkseagreen")
        self.start_game_button.place(relx=0.5, rely=0.5, anchor=CENTER)


    def deal_cards(self):
        # Append computer's and player's numbers to their hands
        for i in self.computer_numbers:
            self.computer_hand.append("{}_card".format(i))
        for i in self.player_numbers:
            self.player_hand.append("{}_card".format(i))
        # Remove the trial game button
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

    
    def computer_wait(self):
        # The card that the computer will play is its first (lowest, and in this case, only) card
        card = self.computer_numbers[0]
        # If it's higher than the current card, start waiting to play your card
        if card > self.current_card:
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


    def show_cards_computer(self):
        self.resized_card_computer = self.resize_cards(f'card_images/comp_card.jpg')
        # Put computer's cards with the back picture in grids, forget the grids for the cards that have been removed from the hand
        self.panel_4 = Label(self.computer_frame, image=self.resized_card_computer, bg="darkseagreen")
        self.panel_4.grid(row=0, column=1)
        if len(self.computer_hand)<1:
            self.panel_4.grid_forget()


    def order_check_player(self, x):
        if self.game_end is False:
            # Forget the grid of the card that was played
            if x == 0:
                self.panel_1.grid_forget()
            # Put the card in the middle
            self.cards_in_the_middle(self.photos_cards_player[x])
            self.current_card = min(self.player_numbers)
            # Remove it from the player's numbers
            self.player_numbers.remove(min(self.player_numbers))
            # Check if the game ended
            self.root.after(2000, self.check_if_end)
            # If the computer still has cards, start waiting
            if len(self.computer_numbers)>0:
                self.computer_wait()


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
                if len(self.player_numbers)<1:
                    self.current_frame.after(2000, self.panel_1.grid_forget)
                # Check if that ended the game, if not, make the computer wait
                self.root.after_cancel(self.end_game)
                self.end_game = self.root.after(3800, self.check_if_end)
                if len(self.computer_numbers)>0:
                    self.root.after(4000, self.computer_wait)
                # Check if there are still lower cards in the player's numbers
                self.root.after(4000, self.lower_card_player)


    def order_check_computer(self):
        # Put computer's card in the middle and remove it from its numbers
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