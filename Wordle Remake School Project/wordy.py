"""
Module: wordy

A completely original word game that will knock your socks off!

Authors:
- Matthew Torno mtorno@sandiego.edu
- Luka Berg lberg@sandiego.edu
"""

import string, json
from typing import Callable
from tkinter import Event

from views import WordyView
from models import WordyModel, NotAWordError

class WordyController:
    """ Controller class for WordyController. """

    WORD_SIZE: int    # number of characters in the correct word
    NUM_GUESSES: int  # number of guesses allowed by the user

    model: WordyModel  # the model used to verify the guess
    view: WordyView    # the GUI view

    current_guess_num: int    # the guess number the user is currently on (starts at 0)
    current_guess: list[str]  # list of characters in the current guess

    def __init__(self, view: WordyView, model: WordyModel, settings: dict) -> None:
        """ Initialize the controller. """

        self.WORD_SIZE = settings['word_size']
        self.NUM_GUESSES = settings['num_guesses']

        self.model = model

        self.current_guess_num = 0
        self.current_guess = []

        # Create the view
        self.view = view

        # TODO: use the set_key_handler method in your view to set up the
        # event handlers for all of the keyboard keys (A-Z, BACK, ENTER)
        for ch in string.ascii_lowercase:
            view.set_key_handler (ch, self.create_letter_handler(ch))
        view.set_key_handler ("back", self.delete_last_letter)
        view.set_key_handler ("enter", self.check_solution)

        # TODO: use create_binding to set Control-H to show the hint

        view.create_binding ("<Control-h>",self.show_hint)
        # Start GUI
        self.view.start_gui()


    def clear_current_guess(self):
        """ Clears the current guess. """
        for _ in range(len(self.current_guess)):
            self.current_guess.pop()


    def show_hint(self, e: Event):
        """ Secret function to display the answer in the messages frame. """
        view.display_message (model.word)
        

    def create_letter_handler(self, letter: str) -> Callable[[], None]:
        """ Creates an event handler function that will.

        (1) Add a letter to the current guess.
        (2) Update the view so that the letter shows up in the appropriate
        spot.

        Note that if the current guess already is already at the WORD_SIZE,
        the handler shouldn't do anything.

        Precondition: letter is a single character.

        Parameters:
            letter (str): The letter to use in the function that is generated.

        Returns:
            Callable[[], None]: A function that will either do the two steps
            above or nothing (if the current guess already has WORD_SIZE
            characters.
        """
        def call ():
            assert len(letter) ==1
            if len(self.current_guess) <= self.WORD_SIZE -1:
                self.current_guess.append(letter)
                view.set_letter (letter, self.current_guess_num, len (self.current_guess)-1)
            return None

        return call

    def delete_last_letter(self) -> None:
        """ An event handler that will delete the last letter from the current
        guess and remove it from the view.

        Note that if the current guess is empty (i.e. doesn't have any
        letters), this handler will do nothing.
        """
        if len(self.current_guess) >= 0:
            self.current_guess = self.current_guess[:-1]
            view.set_letter ("", self.current_guess_num, len (self.current_guess))


    def check_solution(self) -> None:
        """ Checks the current guess using the wordy model, then updates the
        wordy view to display the result of the guess. This function will act
        as the handler for the "ENTER" button.

        If the current guess doesn't have enough letters, this will do nothing
        except display a message in the view that reads, "Word not finished!".

        If the wordy model indicates that the guess is not a word, this
        function should ONLY display a message in the view that reads, "XXX is
        not a valid word." (where XXX is the guess).

        If the guess was correct, in addition to updating the colors of the
        guess, the view should display a message that reads, "Correct!!! Wordy
        Up, y'all!".

        If the guess was incorrect and was the last available guess, the view
        should display a message that reads, "Darn. You are out of guesses.
        Better luck next time!".

        In the case of a correct guess or running out of guesses, the view's
        game_over method should be called to disable the user from further
        interacting with the keyboard.
        """
        if len (self.current_guess) == self.WORD_SIZE:
            word = ''.join(self.current_guess)
            try:
                check = model.check_guess(word)
                view.guess_frame.show_guess_result(self.current_guess_num, check[1])
                view.keyboard_frame.set_key_colors (check[2])
                self.current_guess_num+=1
                self.current_guess=[]
                if check[0]:
                    view.display_message ("Correct!!! Word Up, y'all!")
                    view.game_over()
                else:
                    if self.current_guess_num >= self.NUM_GUESSES:
                        view.display_message ("Darn. You are out of guesses. Better luck next time!")
                        view.game_over()
            except:
                word in model.word_list
                if word not in model.word_list:
                    view.display_message (word + " is not a valid word")
        else:   
            view.display_message("Word Not Finished !!!!!!!!!!")



if __name__ == "__main__":
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)

    # create model, view, then controller
    model = WordyModel(settings['word_size'], settings['word_list_file'])
    view = WordyView(settings)
    controller = WordyController(view, model, settings)

