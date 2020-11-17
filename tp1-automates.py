#!/usr/bin/env python3
"""
Read an automaton and a word, returns:
 * ERROR if non deterministic
 * YES if word is recognized
 * NO if word is rejected
"""

import automaton
import sys
import pdb # for debugging

if len(sys.argv) != 3:
  usagestring = "Usage: {} <automaton-file.af> <word-to-recognize>"
  automaton.error(usagestring.format(sys.argv[0]))

automatonfile = sys.argv[1]  
word = sys.argv[2]

print("TODO: faire le TP 1")  

