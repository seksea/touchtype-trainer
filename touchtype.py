import time
import sys
import random
import os
import curses

letters = "abcdefghijklmnopqrstuvwxyz"
symbols = "1234567890!£$%^&*;:()[]{}|\\\"\'#"

# clearscreen func that works on unix and win
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def generate_word(letters_used : str) -> str:
    letters_not_used = []
    for letter in letters:
        if letter not in letters_used:
            letters_not_used += letter
    words_to_use = []
    with open("dictionary.txt") as f:
        lines = f.readlines()
        for word in lines:
            word_is_good = True
            for letter in letters_not_used:
                if letter in word:
                    word_is_good = False
                    break
                else:
                    word_is_good = True
            if word_is_good:
                words_to_use.append(word.rstrip("\n"))
    return random.choice(words_to_use)


def generate_sentence(number_of_words : int, letters_used : str) -> str:
    sentence = ""
    sentence += generate_word(letters_used)
    for i in range(1, number_of_words):
        sentence += " "
        sentence += generate_word(letters_used)
    sentence += "."
    return sentence

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.clear()
    stdscr.addstr(0, 0, "Generating sentences...")
    stdscr.refresh()
    #create sentence list
    sentences = []
    for i in range(0, 5):
        sentences.append(generate_sentence(10, sys.argv[1]))
    #begin timer
    start_time = time.time()
    correct_letters = 0
    incorrect_letters = 0
    for i in range(0, 5):
        stdscr.clear()
        stdscr.addstr(0, 3, "== Touchtype Trainer ==")
        stdscr.addstr(2, 1, sentences[i])
        for j in range(0, len(sentences[i])):
            stdscr.move(3, 1+j)
            stdscr.refresh()
            try:
                key = stdscr.getkey()
                stdscr.addstr(3, 1+j, key, curses.color_pair(1 if key == sentences[i][j] else 2))
                if (key == sentences[i][j]):
                    correct_letters += 1
                else:
                    incorrect_letters += 1
            except:
                pass
    time_took = time.time() - start_time
    print(f"""
=============
    STATS
=============
Using letters {sys.argv[1]}
Time: {time_took}
WPM: {50/(time_took/60)}
WPS: {50/(time_took)}
Accuracy: {(correct_letters/(incorrect_letters+correct_letters))*100}%""")
curses.wrapper(main)