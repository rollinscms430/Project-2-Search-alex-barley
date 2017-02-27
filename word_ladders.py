# Barley, Alex
# Dr. Myers
# Artificial Intelligence
# Project 2: Solving Problems by Searching
# Word Ladders
# Due: Sunday, February 26, 2017, 11:59 PM

# For this assignment, I decided to use a bidirectional, breadth-first search.
# The problem gives the problem-solver the start word and the end word, and asks
# him or her to find word ladders between the two words.
# I chose a bidirectional, breadth-first search, because I wanted to find a  
# shortest word ladder first, and I wanted to find it quickly. 
# Expanding the startword and the endword first is an efficient strategy for finding 
# word ladders between the two words. A depth-first search might start down a path
# that is either fruitless or very long. Also, in the case of a depth-first search, I would
# need to change my global dictionary of visited states to an attribute of state objects. 
#
# I also decided that I did not want to find an exhaustive list of word ladders
# from snakes to brains, and for this reason, I used a global dictionary of visited words.
# Consider the following two valid word ladders from snakes to brains:
#   (1) snakes SHAKES shares sharks shacks thacks tracks traiks trains brains
#   (2) snakes stakes SHAKES shares sharks shacks thacks tracks traiks trains brains
# My search strategy first finds a faster solution through "shakes"--see (1), 
# and therefore, it will not generate a solution through "snakes stakes shakes." 
# The project description did not ask for an exhaustive list, 
# and I made the decision to find the shortest, unique ladders through a given state.
# That being said, if I were asked to generate an exhaustive list of all word ladders
# from snakes to brains, I would simply change my global dictionary of visited words 
# to an attribute of each state object.

from copy import deepcopy
from collections import OrderedDict

start_word = "snakes"
end_word = "brains"
frontier_queue = []
visited = {}
word_ladders = OrderedDict()
six_letter_words = {}
            
class State(object):
    """Represents a state in the solution of a word ladder
       Attributes:
          rungs: a sequence of words representing a ladder
    """
    
    def __init__(self, rungs):
        """Constructor for a state"""
        self.rungs = rungs
        
    def generate_rung(self, word):
        """Generate a new state by adding a word to the ladder
           Input: a 6 letter word that is identical to the last rung excepting one letter
        """
        new_rungs = deepcopy(self.rungs)
        new_rungs.append(word)
        return State(new_rungs)
        
def create_dictionary_of_words(filename):
    """Adds all of the 6-letter words from a file to the dictionary six_letter_words"""
    with open(filename) as wordsFile:
        for line in wordsFile:
            line = line.strip()
            if len(line) == 6:
                six_letter_words[line] = 1
        
def already_visited(word):
    """Returns true if the input word has already been visited, false otherwise"""
    if word in visited:
        return True
    return False
    
def add_to_visited(word):
    """Adds the input word to the dictionary of visited words"""
    visited[word] = True
    
def is_rung(word1, word2):
    """Returns true if the input words are identical except for one letter, false otherwise"""
    count_differences = 0
    for i in range(6):
        if word1[i] != word2[i]:
            count_differences += 1
    if count_differences == 1:
        return True
    return False
    
def finished(state1, state2):
    """Returns true if the two input states can be joined to form a ladder from startword to endword, false otherwise"""
    if state1.rungs[0] == start_word:
        if state2.rungs[0] == end_word:
            if state1.rungs[len(state1.rungs) - 1] == state2.rungs[len(state2.rungs) - 1]:
                return True
    if state1.rungs[0] == end_word:
        if state2.rungs[0] == start_word:
            if state1.rungs[len(state1.rungs) - 1] == state2.rungs[len(state2.rungs) - 1]:
                return True
    return False
    
def solve(start_word, end_word):
    """Solves the puzze using a bidirectional, breadth-first search,
       putting a state for the start_word and a state for the end_word
       as the first two states in the frontier queue
    """
    rungs1 = [start_word]
    initial_state1 = State(rungs1)
    rungs2 = [end_word]
    initial_state2 = State(rungs2)
    frontier_queue.append(initial_state1)
    frontier_queue.append(initial_state2)
    
    while len(frontier_queue) > 0:
        curr_state = frontier_queue.pop(0)
        for word in six_letter_words:
            if not already_visited(word):
                if is_rung(word, curr_state.rungs[len(curr_state.rungs) - 1]):
                    new_state = curr_state.generate_rung(word)
                    add_to_visited(word)
                    frontier_queue.append(new_state)
            else:
                if is_rung(word, curr_state.rungs[len(curr_state.rungs) - 1]):
                    new_state = curr_state.generate_rung(word)
                    for node in frontier_queue:
                        if finished(node, new_state):
                            if node.rungs[0] == start_word:
                                new_state.rungs.remove(node.rungs[len(node.rungs) - 1])
                                word_ladder = node.rungs + new_state.rungs[::-1]
                                with open('word_ladders.txt', 'a') as output:
                                    string = ' '.join(word_ladder)
                                    if string not in word_ladders:
                                        output.write(string)
                                        output.write('\n')
                                        word_ladders.update({string:1})
                                        print string
                            else:
                                node.rungs.remove(new_state.rungs[len(new_state.rungs) - 1])
                                word_ladder = new_state.rungs + node.rungs[::-1]
                                with open('word_ladders.txt', 'a') as output:
                                    string = ' '.join(word_ladder)
                                    if string not in word_ladders:
                                        output.write(string)
                                        output.write('\n')
                                        word_ladders.update({string:1})
                                        print string
                        
if __name__ == '__main__':
    with open("word_ladders.txt", 'w') as out:
        out.write("Word Ladders--Connecting snakes with brains\n")
    create_dictionary_of_words("words.txt")
    solve(start_word, end_word)