#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""

from automaton import Automaton, EPSILON, error, warn
import sys
import pdb # for debugging

##################

def is_deterministic(a:'Automaton')->bool:
  #TODO implement!
  return True
  
##################
  
def recognizes(a:'Automaton', word:str)->bool:
  #TODO implement!
  return True 

##################

if __name__ == "__main__" :
  # First, checks that the script has 2 arguments
  if len(sys.argv) != 3: # If not, show error message and exit
    usagestring = """This script requires two arguments: <automaton-file.af> and <word>
  * <automaton-file.af> is a text file containing an automaton description.
  * <word> is a string, the word to recognize.
Don't forget to specify the command-line options"""
    error(usagestring)

  automatonfile = sys.argv[1]  # First command-line argument: file to read automaton from
  word = sys.argv[2]           # Second command-line argument: word to recognise

  a = Automaton("dummy")
  a.from_txtfile(automatonfile) # Creates Automaton object, loads it from file

  if not is_deterministic(a) :  # Pass created automaton to `is_deterministic` function
    print("ERROR")
  elif recognizes(a, word):     # Pass automaton and word to `recognizes` function
    print("YES")
  else:
    print("NO")

