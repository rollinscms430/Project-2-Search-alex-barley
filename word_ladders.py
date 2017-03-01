# Barley, Alex
# Dr. Myers
# Artificial Intelligence
# Project 2: Solving Problems by Searching
# Word Ladders
# Due: Sunday, February 26, 2017, 11:59 PM

# For this assignment, I decided to use a bidirectional, A* search.
# The problem gives the problem-solver the start word and the end word, and asks
# him or her to find word ladders between the two words.
# A word ladder is a sequence of words that connects two words. For each word, the subsequent 
# word in the ladder is identical to the current word, except for one letter.
# I chose a bidirectional, A* search because I wanted to find the  
# shortest word ladders quickly. 
# I wanted to determine which state to expand next based on the sum of its cost to get to that state 
# and the estimated cost to get from there to a goal state.
# I also wanted my program to have the option of creating a tree from the start word and create a tree 
# from the end word and for the paths in those trees to expand towards one another, doing so 
# when such a path expansion is estimated to have a cheapest total cost.
# Putting the startword and the endword into your priority queue first is an efficient strategy for finding 
# word ladders between the two words. A depth-first search might start down a path
# that is either fruitless or very long. Also, in the case of a depth-first search, I would
# need to change my global dictionary of visited states to an attribute of state objects. 
#
# The priority queue that I implemented allows me to pop the state with the lowest
# f value. f(n) = g(n) + h(n) for a node n.
# g(n) is the cost required to read that node, or state. And for my g(n) values, I simply
# give the number of words in the word ladder that led to that state.
# h(n) is the optimistic estimate of getting from the last word in the node's current ladder 
# to a goal state. h(n) is simply the number of letter swaps necessary to get from that word
# to a goal word. It will never overestimate the true cost of getting from the current state 
# to a goal state. 
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
import Queue
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
    
def count_differences(word1, word2):
    """Returns the number of letter swaps required to create word1 from word2
       This is a state's h(n) for the state n
    """
    count_difference = 0
    for i in range(6):
        if word1[i] != word2[i]:
            count_difference += 1
    return count_difference
    
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
    queue = Queue.PriorityQueue()
    rungs1 = [start_word]
    rungs2 = [end_word]
    state1_f_value = len(rungs1) + count_differences(start_word, end_word)
    state2_f_value = len(rungs2) + count_differences(end_word, start_word)
    initial_state1 = State(rungs1)
    initial_state2 = State(rungs2)
    queue.put((state1_f_value, initial_state1))
    queue.put((state2_f_value, initial_state2))
    
    while queue.qsize() > 0:
        queue_item = queue.get()
        curr_state = queue_item[1]
        for word in six_letter_words:
            if not already_visited(word):
                if is_rung(word, curr_state.rungs[len(curr_state.rungs) - 1]):
                    new_state = curr_state.generate_rung(word)
                    add_to_visited(word)
                    if new_state.rungs[len(new_state.rungs)-1] == start_word:
                        new_state_f_value = len(new_state.rungs) + count_differences(word, end_word)
                    else:
                        new_state_f_value = len(new_state.rungs) + count_differences(word, start_word)
                    queue.put((new_state_f_value, new_state))
            else:
                if is_rung(word, curr_state.rungs[len(curr_state.rungs) - 1]):
                    new_state = curr_state.generate_rung(word)
                    for node in list(queue.queue):
                        # can two ladders be joined to create a ladder from snakes to brains?
                        if finished(node[1], new_state):
                            if node[1].rungs[0] == start_word:
                                new_state.rungs.remove(node[1].rungs[len(node[1].rungs) - 1])
                                word_ladder = node[1].rungs + new_state.rungs[::-1]
                                with open('word_ladders.txt', 'a') as output:
                                    string = ' '.join(word_ladder)
                                    if string not in word_ladders:
                                        output.write(string)
                                        output.write('\n')
                                        word_ladders.update({string:1})
                                        print string
                            else:
                                node[1].rungs.remove(new_state.rungs[len(new_state.rungs) - 1])
                                word_ladder = new_state.rungs + node[1].rungs[::-1]
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