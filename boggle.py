# Barley, Alex
# Dr. Myers
# Artificial Intelligence
# Project 2: Solving Problems by Searching
# Boggle
# Due: Sunday, February 26, 2017, 11:59 PM

# I decided to use a recursive, depth-first search strategy for this problem, 
# because it mimics the way that I play Boggle. I start with a letter, and I 
# try to find a path through the letters to valid words, backing up and exploring
# alternative adjacencies as I fail.
#
# The project description did not specify what the board should look like, 
# except that it be a 4x4 grid of letters. In the project description, 
# there was an example of one such grid. My program, when run using only 
# the executable as an argument, solves that example grid. 
# If the user wants to generate a random configuration of the board,
# using the letters of the Boggle cubes, he or she can run the following command:
# python boggle.py -s shuffle

# If the user wants to specify the configuration of the letters on the board, 
# he or she can include as an argument, a 16-character, alphabetic string.
# Ex. python boggle.py -i abcdefghijklmnop

# The user can type python boggle.py -h into the command line to get helpful usage instructions.


import sys
import argparse
from copy import deepcopy
from collections import defaultdict
import random

# this is the sample board from the project description
# typing python boggle.py into the command line will solve this board
the_board = [['u', 'n', 't', 'h'], 
             ['g', 'a', 'e', 's'],
             ['s', 'r', 't', 'r'],
             ['h', 'm', 'i', 'a']]

# These are all of the letters on all of the dice of the actual Boggle game, post 2008
dice = ['aaeegn', 'abbjoo', 'achops', 'affkps', 'aoottw', 'cimotu', 'deilrx', 'delvry',
        'distty', 'eeghnw', 'eeinsu', 'ehrtvw', 'eiosst', 'elrtty', 'himnuq', 'hlnnrz']

words = {}
prefixes = defaultdict(list)
solutions = {}

class State(object):
    """Represents a state in a solution of boggle
       Attributes:
         position_sequence: A sequence of tuples, where each subsequent tuple represents a position on 
           the board and a subsequent node along this solution path
         letter_sequence: The sequence of letters up to this point in this solution path
         visited_postions: A dictionary of tuples, where each tuple represents a position on the board
           that has already been visited in this solution path
    """
    
    # constructor for state objects
    def __init__(self, position_sequence, letter_sequence, visited_positions):
        """Constructor for states"""
        self.position_sequence = position_sequence
        self.letter_sequence = letter_sequence
        self.visited_positions = visited_positions
        
    def generate_word(self, position):
        """Returns a new state with a position added to this solution path"""
        new_position_sequence = deepcopy(self.position_sequence)
        new_letter_sequence = deepcopy(self.letter_sequence)
        new_visited_positions = deepcopy(self.visited_positions)
        new_position_sequence.append(position)
        new_letter_sequence += the_board[position[0]][position[1]]
        new_visited_positions[position] = True
        return State(new_position_sequence, new_letter_sequence, new_visited_positions)
  
def create_dictionaries_of_words_and_prefixes(filename):
    """Populates the dictionary words with all of the words from words.txt
       Populates the dictionary prefixes with all of the prefixes of all of the words from words.txt
    """
    with open(filename) as wordsFile:
        for line in wordsFile:
            line = line.strip()
            words[line] = 1
            first_letter = line[0]
            if first_letter not in prefixes:
                prefixes[first_letter] = 1
            for i in range(len(line) - 1):
                if i > 0:
                    first_letter = first_letter + line[i]
                    if first_letter not in prefixes:
                        prefixes[first_letter] = 1
        
def get_adjacencies(position):
    """Returns a list of tuples, specifying positions on the board that are neighbors of the input position"""
    row = position[0]
    column = position[1]
    adjacencies = [(i, j) for i in range(max(0, row - 1), min(len(the_board), row + 1 + 1)) 
    for j in range(max(0, column - 1), min(len(the_board[row]), column + 1 + 1)) if position[0] is not i or position[1] is not j]
    return adjacencies
    
def is_prefix(state):
    """Returns true if the input state's sequence of letters is a prefix of a word in words.txt, false otherwise"""
    if state.letter_sequence in prefixes:
        return True
    return False
        
def is_word(state):
    """Returns true if the input state's sequence of letters is a word in words.txt, false otherwise"""
    if state.letter_sequence in words:
        return True
    return False
        
def recursive_search(state):
    """Solution by recursive depth-first search
       state: the current state in the depth-first search
    """
    # first, determine whether the state is a solution. If it is, print it.
    if is_word(state):
        # In the example grid from the project description--see board above--,
        # there are two ts. This allows the player to form, for example, the word
        # 'seat' twice. This next line ensures that the same solution is printed only once.
        if state.letter_sequence not in solutions:
            solutions[state.letter_sequence] = True
            print state.letter_sequence
            with open('boggle_solutions.txt', 'a') as output:
                output.write(state.letter_sequence)
                output.write('\n')
    # If the current state's sequence of letters is a prefix, create new states for all adjacent postions of
    # this state's last position. Then, recursively serach the new states.
    for position in get_adjacencies(state.position_sequence[len(state.position_sequence)-1]):
        if position not in state.visited_positions:
            if is_prefix(state):
                recursive_search(state.generate_word(position))

def solve(board):
    """Creates a new state for each of the 16 letters/positions on the board,
       then recursively searches from each state to the solutions
    """
    for i in range(len(board)):
        for j in range(len(board[i])):
            position_sequence = [(i, j)]
            letter_sequence = board[i][j]
            visited_positions = {(i, j):True}
            initial_state = State(position_sequence, letter_sequence, visited_positions)
            recursive_search(initial_state)

def shuffle(board):
    """Uses the letters of the actual Boggle dice--post 2008--and places
       a random letter from each die in a random place on the board
    """
    placed = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            which_cube = random.randint(0, len(dice) - 1)
            word = dice[which_cube]
            while which_cube in placed:
                which_cube = random.randint(0, len(dice) - 1)
                word = dice[which_cube]
            letter = word[random.randint(0, len(word) - 1)]
            if letter == 'q':
                letter = 'qu'
            board[i][j] = letter
            placed[which_cube] = 1

def create_board(string):
    """Sets the values of the board, using a 16 character, alphabetic string"""
    letters_used = 0
    for i in range(len(the_board)):
        for j in range(len(the_board[i])):
            if string[letters_used] == 'q':
                the_board[i][j] = 'qu'
            else:
                the_board[i][j] = string[letters_used]
            letters_used += 1

def print_the_board(board):
    """Prints the board to the console"""
    for i in range(len(board)):
        for j in range(len(board[i])):
            print board[i][j],
            print ' ',
        print '\n'

def valid_command(command):
    """This is called if the user includes the -s argument on the command line.
       If -s is followed by the word "shuffle", the dice get shuffled, the board
       gets printed, and the solutions get printed.
    """
    if command is not None:
        if command == "shuffle":
            shuffle(the_board)
            print_the_board(the_board)
            solve(the_board)
        else:
            msg = "Not a valid command: " + command + "\nTry python boggle.py -s shuffle"
            raise argparse.ArgumentTypeError(msg)

def board_config(input_string):
    """This is called if the user includes the -i argument on the command line.
       If -i is followed by a 16 character, alphabetic string, the values on 
       the board take on the letters specified by that string.
       The board and the solutions get printed.
    """
    if input_string is not None:
        if len(input_string) == 16:
            if input_string.isalpha():
                create_board(input_string)
                print_the_board(the_board)
                solve(the_board)
            else:
                msg = "Not a 16-character, alphabetic input string: " + input_string + "\nTry: python boggle.py -i abcdefghijklmnop"
                raise argparse.ArgumentTypeError(msg)
        else:
            msg = "Not a 16-character, alphabetic input string: " + input_string + "\nTry: python boggle.py -i abcdefghijklmnop"
            raise argparse.ArgumentTypeError(msg)

if __name__ == '__main__':
    with open("boggle_solutions.txt", "w") as out:
        out.write("solutions\n")
    create_dictionaries_of_words_and_prefixes("words.txt")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-s', action="store", help='type shuffle to shake the board', dest='action', type=valid_command)
    group.add_argument('-i', action="store", help='type a 16 character string to specify a board configuration', dest='dice', type=board_config)
    args = parser.parse_args()
    
    # If the user enters python boggle.py, print and solve the board given in the project description.
    if len(sys.argv) == 1:
        print_the_board(the_board)
        solve(the_board)