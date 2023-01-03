import curses
from curses import wrapper	#C95757#B411116
import time
import random


rand = random.randint(1, 3)


def start_screen(stdscr):
	stdscr.clear()
	stdscr.addstr('Welcome to the Typing Speed Test!')
	stdscr.addstr('\nPress any key to begin')
	stdscr.refresh()
	stdscr.getkey()
	
	
def display_text(stdscr, target_text, current, wpm):
	stdscr.addstr(target_text)
	stdscr.addstr(1, 0, f'WPM: {wpm}')
	
	for i, char in enumerate(current):
		correct_char = target_text[i]
		color = curses.color_pair(1)
		if char != correct_char:
			color = curses.color_pair(2)
		stdscr.addstr(0, i, char, color)
	
	
def load_text():	
	with open('text.txt', 'r') as f:
		lines = f.readlines()
		return random.choice(lines).strip()


def avg_letters(phrase):
	characters = 0
	words = phrase.split(' ')
	for char in phrase:
		if char == ' ':
			characters += 0
		else:
			characters += 1

	return characters / len(words)


def wpm_test(stdscr):
	global wpm
	target_text = load_text()
	words = target_text.split(' ')
	current_text = []
	wpm = 0
	start_time = time.time()
	stdscr.nodelay(True)
	
	
	while True:
		time_elapsed = max(time.time() - start_time, 1)
		wpm = round((len(current_text) / (time_elapsed / 60)) /
			  round(avg_letters(target_text)))
				
		stdscr.clear()
		display_text(stdscr, target_text, current_text, wpm)		
		stdscr.refresh()
		
		if ''.join(current_text) == target_text:
			stdscr.nodelay(False)
			break
		
		try:
			key = stdscr.getkey()
		except: 
			continue
		
		if ord(key) == 27:
			break
		if key in ('KEY_BACKSPACE', '\b', '\x7f'):
			if len(current_text) > 0:
				current_text.pop()
		elif len(current_text) < len(target_text):
			current_text.append(key)
		

def main(stdscr):

	if rand == 1: 
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	if rand == 2: 
		curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	if rand == 3: 
		curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
	
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
	GREEN = curses.color_pair(1)
	RED = curses.color_pair(2)
	WHITE = curses.color_pair(3)
	
	start_screen(stdscr)
	while True:
		wpm_test(stdscr)
		stdscr.addstr(2, 0, 'You completed the test, press any key to continue...')
		stdscr.addstr(1, 0, f'WPM: {wpm}')
		key = stdscr.getkey()
		if ord(key) == 27:
			break


wrapper(main)
