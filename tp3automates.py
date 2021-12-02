#!/usr/bin/env python3
"""
Applies Kleene's star, concatenation and union of automata.
"""

from automaton import Automaton, EPSILON, State, error, warn
import sys
import pdb # for debugging

##################

def kleene(a1:Automaton)->Automaton:
  # TODO: implement Kleene's star
  return a1 

##################

def concat(a1:Automaton, a2:Automaton)->Automaton:
  # TODO: implement concatenation
  return a1 

##################

def union(a1:Automaton, a2:Automaton)->Automaton:
  # TODO: implement union
  return a1 

##################


if __name__ == "__main__" :
  # First, checks that the script has 2 arguments
  if len(sys.argv) != 3: # If not, show error message and exit
    usagestring = """This script requires two arguments: <automaton-file1.af> and <automaton-file2.af>
  * <automaton-file1.af> is a text file containing the first automaton description.
  * <automaton-file2.af> is a text file containing the second automaton description.
Don't forget to specify the command-line options"""
    error(usagestring)
    
  # First automaton, argv[1]
  a1 = Automaton("dummy")
  a1.from_txtfile(sys.argv[1])
  a1.to_graphviz(a1.name+".gv")
  print(a1)

  # Second automaton, argv[2]
  a2 = Automaton("dummy")
  a2.from_txtfile(sys.argv[2])
  a2.to_graphviz(a2.name+".gv")
  print(a2)
    
  a1star = kleene(a1)
  print()
  print(a1star)
  a1star.to_graphviz("a1star.gv")

  a1a2 = concat(a1, a2)
  print()
  print(a1a2)
  a1a2.to_graphviz("a1a2.gv")

  a1ora2 = union(a1, a2)
  print()
  print(a1ora2)
  a1ora2.to_graphviz("a1ora2.gv")

