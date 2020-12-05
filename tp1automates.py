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
  return False
  
##################
  
def recognizes(a:'Automaton', word:str)->bool:
  #TODO implement!
  return False

##################

if __name__ == "__main__" :
  if len(sys.argv) != 3:
    usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
    error(usagestring.format(sys.argv[0]))

  automatonfile = sys.argv[1]  
  word = sys.argv[2]

  a = Automaton("dummy")
  a.from_txtfile(automatonfile)

  if not is_deterministic(a) :
    print("ERROR")
  elif recognizes(a, word):
    print("YES")
  else:
    print("NO")

