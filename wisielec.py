#!/usr/bin/python
# -*- coding: utf-8 -*-
import random, string
from flask import Flask, render_template, url_for, flash, redirect, request

#configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

WORDS = []
game = None

class Hangman:
    def __init__(self):
        self.available_letters = string.ascii_lowercase
        self.used_letters = ''
        self.word_to_guess = self.select_word()
        self.number_of_guesses = 8

    def get_available_letters(self):
        return self.available_letters

    def get_used_letters(self):
        return self.used_letters

    def get_word_to_guess(self):
        return self.word_to_guess

    def select_word(self):
        return WORDS[random.randrange(0, len(WORDS))]

    def update_letters(self, user_guess):
        if user_guess not in self.get_used_letters():
            self.available_letters = self.get_available_letters().replace(user_guess, '')

    def display_word(self):
        word = ''
        for letter in self.get_word_to_guess():
            if letter in self.get_used_letters():
                word += letter + '  '
            else:
                word += '  __  '
        return word



def import_words():
    file = open('words.txt', 'r')
    for line in file:
        WORDS.append(line)
    file.close()

@app.route('/')
def index():
    flash('Zapraszam do nowej gry')
    return render_template('layout.html')

@app.route('/hangman')
def update_game_status():
    global game
    if game == None:
        game = Hangman()
        return render_template('game.html', gra =  game )
    else:
        pass
        #todo logika gry

@app.route('/newgame', methods=['POST'])
def new_game():
    global game
    game = None
    return redirect(url_for('update_game_status'))

@app.route('/guess', methods=['POST'])
def user_guess():
    global game
    if len(request.form['letter']) != 1:
        flash('Wpisz JEDNĄ literę!')
        return redirect(url_for('update_game_status'))
    else:
        game.update_letters(request.form['letter'])
        return redirect(url_for('update_game_status'))

if __name__ == '__main__':
    import_words()
    app.run()