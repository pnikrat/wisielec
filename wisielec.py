# -*- coding: utf-8 -*-
import random
import string
import sys
import logging
from flask import Flask, render_template, url_for, flash, redirect, request

DEBUG = False  # configuration
SECRET_KEY = 'l55Vsm2ZJ5q1U518PlxfM5IE2T42oULB'

app = Flask(__name__)
app.config.from_object(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

WORDS = []
game = None


class Hangman:
    def __init__(self):
        self.available_letters = string.ascii_lowercase
        self.used_letters = ''
        self.word_to_guess = self.select_word()
        self.number_of_guesses = 8
        self.win = False

    def get_available_letters(self):
        return self.available_letters

    def get_used_letters(self):
        return self.used_letters

    def get_used_letters_sorted(self):
        return ''.join(sorted(self.get_used_letters()))

    def get_word_to_guess(self):
        return self.word_to_guess

    def get_number_of_guesses(self):
        return self.number_of_guesses

    def select_word(self):
        return WORDS[random.randrange(0, len(WORDS))]

    def update_letters(self, user_guess):
        if user_guess in self.get_used_letters():
            return 'You\'ve already used that letter!'
        elif user_guess not in self.get_used_letters():
            self.available_letters = self.get_available_letters().replace(user_guess, '')
            self.used_letters += user_guess
            if user_guess in self.get_word_to_guess():
                return 'Good guess!'
            else:
                self.number_of_guesses -= 1
                return 'Wrong guess!'

    def check_win(self):
        self.win = True
        for letter in self.get_word_to_guess():
            if letter not in self.get_used_letters():
                self.win = False

        return self.win


    def display_word(self):
        word = ''
        for letter in self.get_word_to_guess():
            if letter in self.get_used_letters():
                word += letter + '  '
            else:
                word += '  __  '
        return word


def import_words():
    file = open('tmp/words.txt', 'r')
    for line in file:
        WORDS.append(line.rstrip())
    file.close()


@app.route('/')
def index():
    flash('Have fun!')
    return render_template('layout.html')


@app.route('/hangman')
def update_game_status():
    global game
    if game is None:
        game = Hangman()
        flash('Tries left: ' + str(game.get_number_of_guesses()))
        return render_template('game.html', gra=game)
    else:
        if game.check_win():
            flash('You won!')
        elif not game.check_win() and game.number_of_guesses == 0:
            flash('You lost! The word was: ' + game.get_word_to_guess())
        flash('Tries left: ' + str(game.get_number_of_guesses()))
        return render_template('game.html', gra=game)


@app.route('/newgame', methods=['POST'])
def new_game():
    global game
    game = None
    return redirect(url_for('update_game_status'))


@app.route('/guess', methods=['POST'])
def user_guess():
    global game
    if len(request.form['letter']) != 1:
        flash('Enter ONLY ONE letter!')
        return redirect(url_for('update_game_status'))
    else:
        flash(game.update_letters(request.form['letter']))
        return redirect(url_for('update_game_status'))


if __name__ == '__main__':
    import_words()
    app.run()
