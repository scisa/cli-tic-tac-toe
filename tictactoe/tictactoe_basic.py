#!/usr/bin/env python

import re
import argparse
from operator import itemgetter

# TODO argparse verbose
# schiffe versenken



GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
WHITE = '\033[0m'
BOLD = '\033[1m'

FLF = 11 #field length factor
TRYS = 3
VERBOSE = False


def print_error(msg):
	print(BOLD + RED + '[ERROR] ' + msg + WHITE)


def print_warning(msg):
	print(BOLD + YELLOW + '[WARNING] ' + msg + WHITE)


def print_banner():
	print('\n' + ' '*FLF + '-- Tic Tac Toe --')


def game_field(liste):

	feld =  "\t0,1,2\t" + liste[0] + "|" + liste[1] + "|" + liste[2] + "\n" + \
			"\t     \t" + "-"*FLF + "\n" +\
			"\t3,4,5\t" + liste[3] + "|" + liste[4] + "|" + liste[5] + "\n" + \
			"\t     \t" + "-"*FLF + "\n" + \
            "\t6,7,8\t" + liste[6] + "|" + liste[7] + "|" + liste[8] + "\n"
	print('\n')
	print(feld)


def choose_stone(is_x):
	if is_x:
		stone = ' x '
	else:
		stone = ' o '
	
	return stone


def trys_left(game_try):
	print_warning("Only " + str(TRYS - game_try + 1) + " trys left before exiting!")


def wrong_type_error(game_try):
	print_error("You have to insert a number. Nothing else!")
	trys_left(game_try)


def invalid_index_error(game_try):
	print_error("This is not a valid index!")
	trys_left(game_try)


def double_index_warning(game_try):
	print_warning("another stone is at this position. Please try again!")
	trys_left(game_try)
	

def is_exiting(game_try):
	if game_try > TRYS:
		print_error("Number of trys exceeded. exiting...")
		exit(1)


def index_input():
	index = int(input("\nThrow a stone at an index. Don't hit an Index twice: "))
	if index < 0 or index > 8:
		raise IndexError 
	
	return index


def calc_index():
	game_try = 1
	while True:
		is_exiting(game_try)
		game_try += 1

		try:
			index = index_input()
			break
		except (NameError, TypeError, SyntaxError) as e:
			wrong_type_error(game_try)
		except IndexError as e:
			invalid_index_error(game_try)
	
	return index


def calc_new_field(field, index, game_try):
	if re.match('^\s*$',field[index]):
		field[index] = stone
		is_changed = True
	else:
		double_index_warning(game_try)
		is_changed = False

	return field, is_changed


def new_stone(field, stone):
	game_try = 1
	while True:
		is_exiting(game_try)
		game_try += 1		
		
		index = calc_index()
		field, is_changed = calc_new_field(field, index, game_try)
		
		if is_changed:
			break

	return field
	

def color_field(field, situation):
	for index in situation:
		field[index] = GREEN + field[index] + WHITE

	return field


def winning(field, stone, situation):
	field = color_field(field, situation)
	game_field(field)
	print(BOLD + GREEN + "Player " + str(stone).strip() + " wins :)" + WHITE)
	exit(0)


def get_winning_situations():
	return [
	    [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [6, 4, 2]
     ]


def verbose_win_checker(situation, field):
	if VERBOSE:
		match_field_sit = itemgetter(*situation)(field)
		print("")
		print(match_field_sit)


def is_winning(field, stone, situation):
	verbose_win_checker(situation, field)	

	for i in range(3):
		if field[situation[i]] != stone:
			return

	winning(field, stone, situation)
			


def check_for_winner(field, stone):
	winning_situations = get_winning_situations()
	for situation in winning_situations:
		is_winning(field, stone, situation)


def field_full(field):
	game_field(field)
	print(BOLD + BLUE + "Patt. No one wins :|" + WHITE)
	exit(0)


def check_if_field_full(field):
	for index in field:
		if not re.match('.*x.*', index) and not re.match('.*o.*', index):
			return
	
	field_full(field)	
			

def change_x(is_x):
	result = True
	if is_x:
		result = False
	
	return result


def define_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    arguments = parser.parse_args()
    return arguments


if __name__ == "__main__":
	args = define_argument_parser()
	VERBOSE = args.verbose
	print_banner()
	
	field = [" "*3, " "*3, " "*3, " "*3, " "*3, " "*3, " "*3, " "*3, " "*3]
	is_x = True	

	while True:
		game_field(field)
		stone = choose_stone(is_x)		
		field = new_stone(field, stone)
		check_for_winner(field, stone)
		check_if_field_full(field)
		is_x = change_x(is_x)
	
