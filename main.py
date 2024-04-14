#!/usr/bin/env python3
#Created by PepeBigotes

def try_input(msg) -> str:
    try: x = input(msg)
    except KeyboardInterrupt: print("\nKeyboardInterrupt"); exit()
    return x

import os

try:
	try: import curses
	except ImportError:
		print("[!] Module 'curses' is not installed")
		try_input("  Press ENTER to install it (or CTRL+C to exit)")
		os.system('pip3 install windows-curses')
		try: import curses
		except ImportError: print("\n[!] Curses couldn't be installed"); exit(1)
		try_input("\n  Curses installed, press ENTER to continue")
except KeyboardInterrupt: print("\nKeyboardInterrupt"); exit()

import curses
from curses import wrapper
from time import time
from random import choice


# GET WORDS
all_words = []
with open(__file__[:-7] + "words.txt", "r") as file:
    for line in file:
        all_words.append(line)

words = []
for i in range(10):
    word = choice(all_words).strip()
    words += list(word + ' ')
words.pop(-1)  # Delete last space



# VARS
index = 0
words_progress = []  # List of tupples (char, True/False)
words_left = [i for i in words]  # List of chars
start_time = 0
now_time = time()
elapsed_time = 0
precision = 0.0
cpm = 0
wpm = cpm * 5



# FUNCS
def append_char(inp: bool):
    global index, words_progress, words_left
    char = words_left.pop(0)
    words_progress.append((char, inp))
    index += 1

def delete_char():
    global index, words_progress, words_left
    if len(words_progress) == 0: return
    char = words_progress.pop()[0]
    words_left.insert(0, char)
    index -= 1

def check_char(ch, char):
    global index
    if ch == ord('\b'):
        delete_char()
        return
    if ch == curses.KEY_RESIZE: return
    append_char(char == words[index])


def print_typer(stdscr, neu, cor, wro, wrospa):
    stdscr.addstr(3,6, "")
    try:
        for tup in words_progress:
            if tup[1]: stdscr.addstr(tup[0], cor)
            else:
                if tup[0] == " ": stdscr.addstr(tup[0], wrospa)
                else: stdscr.addstr(tup[0], wro)
        pos_y, pos_x = stdscr.getyx()
        for char in words_left: stdscr.addstr(char, neu)
    except curses.error as error: stdscr.addstr(10, 6, error)
    stdscr.move(pos_y, pos_x)
    stdscr.refresh()


def print_header(stdscr, hea):
    stdscr.clear()
    height,width = stdscr.getmaxyx()
    stdscr.addstr(0,0, str.center("Typer-Practice", width), hea)
    stdscr.addstr(1,0, str.center(f"wpm={wpm} pre={int(precision * 100)}%", width), hea)

def print_result(stdscr, neu, cor, wro, exc):
    height,width = stdscr.getmaxyx()
    if wpm >= 100: wpm_col = exc
    elif wpm >= 60: wpm_col = cor
    elif wpm >= 40: wpm_col = neu
    else: wpm_col = wro
    if precision == 1: prec_col = exc
    elif precision >= 0.95: prec_col = cor
    elif precision >= 0.85: prec_col = neu
    else: prec_col = wro
    

    stdscr.addstr(3,0, str.center("RESULTS:", width), curses.A_BOLD)
    stdscr.addstr(5,int(width/2)-4, "Time: ", neu)
    stdscr.addstr(str(round(elapsed_time, 3)), neu)
    stdscr.addstr(6,int(width/2)-16, "Words Per Minute: ", neu)
    stdscr.addstr(str(wpm), wpm_col)
    stdscr.addstr(7,int(width/2)-21, "Characters Per Minute: ", neu)
    stdscr.addstr(str(cpm), wpm_col)
    stdscr.addstr(8,int(width/2)-9, "Precision: ", neu)
    stdscr.addstr(str(int(precision*100)) + "%", prec_col)
    stdscr.addstr(height-3,0, str.center(f"Press CTRL+X to exit", width), neu)
    curses.curs_set(False)
    stdscr.refresh()


def do_exit(code = 0):
    curses.endwin()
    exit(code)


def main(stdscr):
    global start_time, now_time, elapsed_time, precision, cpm, wpm
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(30, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    NEUTRAL = curses.color_pair(1)
    CORRECT = curses.color_pair(2)
    WRONG = curses.color_pair(3)
    WRONG_SPACE = curses.color_pair(30)
    HEADER = curses.color_pair(4)
    EXCELENT = curses.color_pair(5)

    curses.cbreak()
    curses.noecho()

    print_header(stdscr, HEADER)    
    print_typer(stdscr, NEUTRAL, CORRECT, WRONG, WRONG_SPACE)

    while len(words_left) > 0:  # MAIN LOOP
        if len(words_progress) > 0 and start_time == 0: start_time = time()
        ch = stdscr.getch()
        char = curses.keyname(ch).decode()
        if char == "^X": do_exit()
        check_char(ch, char)
        print_header(stdscr, HEADER)
        print_typer(stdscr, NEUTRAL, CORRECT, WRONG, WRONG_SPACE)
        now_time = time()
        elapsed_time = now_time - start_time
        stdscr.refresh()
        cpm = int(len(words_progress) / elapsed_time) * 60
        wpm = int(cpm / 5)
        prec_score = 0
        for tup in words_progress:
            if tup[1]: prec_score +=1
        if not len(words_progress) == 0: precision = prec_score / len(words_progress)
        else: precision = 0.0

    while char != "^X":
        print_header(stdscr, HEADER)
        print_result(stdscr, NEUTRAL, CORRECT, WRONG, EXCELENT)
        ch = stdscr.getch()
        char = curses.keyname(ch).decode()
        if char == "^X": do_exit()



try: wrapper(main)
except KeyboardInterrupt: do_exit()