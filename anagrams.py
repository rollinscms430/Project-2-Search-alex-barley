# Barley, Alex
# Dr. Myers
# Artificial Intelligence
# Project 2: Solving Problems by Searching
# Anagrams
# Due: Sunday, February 26, 2017, 11:59 PM

anagrams = {}
with open('anagrams.txt', 'w') as output:
    output.write('Anagrams:\n')
with open("words.txt") as wordsFile:
    for line in wordsFile:
        line = line.strip()
        tup = tuple(sorted(line))
        # If the set of letters is not in the dictionary called anagrams, add it, 
        # giving its value as a list of one item, a string--the string being the first
        # word encountered that is composed of that set of letters.
        # Otherwise, add the word the the list of words associated with that key set.
        if tup not in anagrams:
            anagrams[tup] = [line]
        else:
            anagrams[tup].append(line)
for key in anagrams:
    if len(anagrams[key]) > 1:
        with open('anagrams.txt', 'a') as out:
            out.write(' '.join(sorted(anagrams[key])))
            out.write('\n')
        print ' '.join(sorted(anagrams[key]))