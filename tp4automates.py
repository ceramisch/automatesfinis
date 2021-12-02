#!/usr/bin/env python3
"""
Read a regular expression and returns:
 * YES if word is recognized
 * NO if word is rejected"""

from typing import Set, List
from automaton import Automaton, EPSILON, State, error, warn, RegExpReader
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
  # Copy-paste from previous TPs
  pass  

##################

def kleene(a1:Automaton)->Automaton:
  # Copy-paste from previous TPs
  return a1 

##################

def concat(a1:Automaton, a2:Automaton)->Automaton:
  # Copy-paste from previous TPs
  return a1 

##################

def union(a1:Automaton, a2:Automaton)->Automaton:
  # Copy-paste from previous TPs
  return a1 
  
##################
   
def regexp_to_automaton(re:str)->Automaton:
  """
  Moore's algorithm: regular expression `re` -> non-deterministic automaton
  """
  postfix = RegExpReader(regexp).to_postfix()
  stack:List[Automaton] = []
  #TODO implement!
  return stack[0]
  
##################

if __name__ == "__main__" :
  # First, checks that the script has 2 arguments
  if len(sys.argv) != 3: # If not, show error message and exit
    usagestring = """This script requires two arguments: <regular-expression> and <word>
  * <regular-expression> is a string, representing a regular expression that denotes a language.
  * <word> is a string, the word to recognize (is it in the denoted language?).
Don't forget to specify the command-line options"""
    error(usagestring)

  regexp = sys.argv[1]  
  word = sys.argv[2]

  a = regexp_to_automaton(regexp)
  determinise(a)
  if recognizes(a, word):
    print("YES")
  else:
    print("NO")

