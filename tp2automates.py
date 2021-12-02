#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * YES if word is recognized
 * NO if word is rejected
Determinises the automaton if it's non deterministic
"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb # for debugging

##################

def is_deterministic(a:Automaton)->bool:
  # Copy-paste from previous TPs
  return False
  
##################
  
def recognizes(a:Automaton, word:str)->bool:
  # Copy-paste from previous TPs
  return False
  
##################

def determinise(a:Automaton):
  #TODO implement!
  pass
  
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
  a.from_txtfile(automatonfile)
  if not is_deterministic(a) :
    determinise(a)
  if recognizes(a, word):
    print("YES")
  else:
    print("NO")
