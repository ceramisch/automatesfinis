#!/usr/bin/env python3
"""
Module to represent, build and manipulate finite state automata
"""

from typing import Dict, List, Union, Tuple, Optional
from collections import OrderedDict, Counter # remember order of insertion
import sys
import os.path
import pdb
import re

########################################################################
########################################################################

def warn(message, *, warntype="WARNING", pos="", **format_args):
  """Print warning message."""
  msg_list = message.format(**format_args).split("\n")
  beg, end = ('\x1b[33m', '\x1b[m') if sys.stderr.isatty() else ('', '')
  if pos: pos += ": "
  for i, msg in enumerate(msg_list):
    warn = warntype if i==0 else " "*len(warntype)
    print(beg, pos, warn, ": ", msg, end, sep="", file=sys.stderr)

##################

def error(message, **kwargs):
    """Print error message and quit."""
    warn(message, warntype="ERROR", **kwargs)
    sys.exit(1)
    
########################################################################
########################################################################

try: # Make the library robust
  from graphviz import Source
except ModuleNotFoundError:
  warn("Warning: graphviz not installed, will not draw automaton graphically")
  class Source: # Dummy class for typing only
    def __init__(self,res):
      pass
    def render(self,outfilename):
      warn("Graphviz not installed, cannot draw automaton")

EPSILON = "%" # Constant to represent empty string

########################################################################

class State(object):
  """
  Represents a state in the automaton, with its list of transitions
  """
  transitions: Dict[str,Dict['State',None]]
  name: str
  is_accept: bool
  
##################

  def __init__(self, name:str)->None:
    """
    Create a new state with a given name
    """
    self.name = name
    self.transitions = OrderedDict()  # by default, empty dict
    self.is_accept = False # by default, create non-accept state

##################
    
  def make_accept(self, accepts:bool=True):
    """
    Transform state into accept state, or the opposite, if accepts=False
    """
    self.is_accept = accepts

##################
   
  def add_transition(self, symbol:str, dest:'State'):
    """
    Add a transition on string `symbol` to State `dest`
    """
    destset = self.transitions.get(symbol,OrderedDict())
    if dest in destset:
      warn("Redundant transition: {s} -{a}-> {d}",s=self.name,
                                                  a=symbol,d=dest.name)
    destset[dest]=None
    self.transitions[symbol] = destset

##################

  def __str__(self)->str:
    """
    Standard function to obtain a string representation of a state
    """
    return self.name.replace('"',"&quot;")

########################################################################
########################################################################

class Automaton(object):
  """
  An automaton is a list of states and a pointer to the initial state
  Transitions and acceptance are represented inside states (see above)
  """  
  name:str
  statesdict:Dict[str,State]
  initial:State
  
##################  
  
  def __init__(self,name:str)->None:
    self.reset(name)     

##################

  def reset(self,name:str=None):
    """
    Reinitialize the automaton with empty content
    """
    if name:
      self.name = name
    elif not self.name:
      self.name = "NewAutomaton"
      warn("New automaton has no name")
    self.statesdict = OrderedDict()   
    self.initial = None 

##################

  def deepcopy(self)->'Automaton':
    """
    Make a deep copy of itself, that is a copy of all elements
    """
    a = Automaton(self.name + "_copy")
    a.from_txt(self.to_txtfile())
    a.initial = a.statesdict[self.initial.name]
    return a

##################
      
  def add_transition(self, src:str, symbol:str, dst:str):
    """
    Add a transition from `src` to `dst` on `symbol`
    """    
    src_state = self.statesdict.get(src, State(src)) # create if absent    
    if not self.statesdict and not self.initial: 
      self.initial = src_state # by default first state added is initial
    self.statesdict[src] = src_state # if new, add to dict
    dst_state = self.statesdict.get(dst, State(dst)) # create if absent
    self.statesdict[dst] = dst_state # if new, add to dict
    src_state.add_transition(symbol, dst_state) # add the transition    

##################

  def remove_state(self, delstate:str):
    """
    Remove `delstate` from the automaton as well as all its transitions.
    """
    if delstate not in self.statesdict :     
      warn("State {} does not exist, will not remove".format(delstate))
      return    
    delstateobj = self.statesdict[delstate]
    del(self.statesdict[delstate]) # First, remove from main states list
    for state in self.statesdict.values(): # For all remaining states
      for (symbol,dests) in state.transitions.items() :
        if delstateobj in dests :
          del(dests[delstateobj])
      if state.transitions and not state.transitions[symbol] : 
        del(state.transitions[symbol]) # no transition left on symbol
          
##################

  def remove_transition(self, src:str, symbol:str, dst:str):
    """
    Remove a transition from `src` to `dst` on `symbol`
    """ 
    try:
      del(self.statesdict[src].transitions[symbol][self.statesdict[dst]])
    except KeyError:
      warn("Transition {} -{}-> {} not found".format(src,symbol,dst))

##################

  @property
  def states(self) -> List[str]:
    return list(self.statesdict.keys())

##################

  @property
  def alphabet(self)->List[str]:
    """
    Get the set of symbols used in the current transitions (+ epsilon)
    """
    alphabet:Dict[str,None] = OrderedDict()
    for state in self.statesdict.values():
      for s in state.transitions.keys():       
        alphabet[s] = None
    return list(alphabet.keys())

##################

  @property
  def reachable_states(self) -> List[str]:
    """
    Returns a list of reachable states in the automaton
    """
    result = set([self.initial])
    nbelems = 0
    while nbelems != len(result) :
      nbelems = len(result)
      addtoresult = []
      for state in result :        
        for destlist in state.transitions.values() :
          for dest in destlist :
            addtoresult.append(dest)
      result = result.union(addtoresult)
    return list(map(lambda x:x.name,result))

##################

  def remove_unreachable(self):
    """
    Remove unreachable states from the automaton
    """
    removed = []
    for state in self.states :
      if not state in self.reachable_states :
        removed.append(state)
    for r in removed :
      self.remove_state(r)

##################

  @property
  def acceptstates(self)->List[str]:
    """
    Return a set of accept states in the automaton.
    If the initial state is accepting, then it is the first in the list
    """
    accept = OrderedDict({k:None for (k,v) in self.statesdict.items() \
                                 if v.is_accept})
    if self.initial and self.initial.name in accept :
      result = [self.initial.name]
      del(accept[self.initial.name])
    else :
      result = []
    return result + list(accept.keys())
    
##################

  @property
  def transitions(self)->List[Tuple[str,str,str]]:
    """
    Returns a list of transitions, each represented as a tuple.
    The tuple contains three strings: (source, symbol, destination)
    The first transitions are always from the initial state
    """
    result = []
    # Transitions from initial state    
    for (symbol,dests) in self.initial.transitions.items():
      for destination in dests :
        result.append((self.initial.name,symbol,destination.name))       
    # Transitions from other states      
    for source in self.statesdict.values():
      if source != self.initial :
        for (symbol,dests) in source.transitions.items():
          for destination in dests :
            result.append((source.name,symbol,destination.name))
    return result
          

##################

  def rename_state(self, oldname: str, newname: str):
    """
    Renames a state in the automaton from `oldname` to `newname`
    """
    if newname in self.states :
      warn("New name \"{}\" already exists, try a new one".format(newname))
      return
    try :
      self.statesdict[newname] = self.statesdict[oldname]
      self.statesdict[newname].name = newname
      del self.statesdict[oldname]
    except KeyError:
      warn("Tried to rename not-existent state \"{}\"".format(oldname))

##################

  @property
  def transition_table(self)->str:
    """
    Return a string representing the transition table of the automaton
    """
    res = ""
    rows = [[""]+self.alphabet]
    maxlen = 1
    for s in self.statesdict.values():
      row = [s.name]
      for a in rows[0][1:] : # for every symbol of the alphabet
        dest = s.transitions.get(a, None)
        if dest and len(dest) == 1:
          row.append(list(dest)[0].name)          
        elif dest: # non-deterministic
          row.append("{"+",".join([x.name for x in dest])+"}")
        else:
          row.append(" ")
        maxlen = max(maxlen,len(row[-1])) # maximum length of a cell
      rows.append(row)    
    for row in rows:      
      res += "|"+"|".join([("{:"+str(maxlen)+"}").format(c) for c in row])+"|\n"
      res += "-"*((maxlen+1)*len(row)+1) + "\n"
    return res[:-1]
	  
##################
    
  def make_accept(self, src:Union[str,List[str]], accepts:bool=True, add:bool=False):
    """
    Transform the a state(s) of the automaton into accept state(s)
    """
    if isinstance(src,str):
      src = [src] # transform in list if necessary
    for srci in src:
      if srci not in self.statesdict:
        if add :
          self.statesdict[srci] = State(srci)          
        else :
          error("Accept state {a} inexistent!",a=srci)
      self.statesdict[srci].make_accept(accepts)
    
##################

  def __str__(self)->str:
    """
    Standard function to obtain a string representation of an automaton
    """
    alphabet_no_eps = [ x for x in self.alphabet if x is not EPSILON ]
    tpl = "{A} = <Q={{{Q}}}, S={{{S}}}, D, q0={q0}, F={{{F}}}>\nD =\n{D}"    
    return tpl.format(A=self.name, Q=str(",".join(self.states)),
                      S=",".join(alphabet_no_eps), q0=self.initial, 
                      F=",".join(self.acceptstates),
                      D=self.transition_table)

##################
    
  def to_graphviz(self, outfilename:str=None) -> Source:
    if not self.states:
      tpl = "digraph L{{label=\"{name}\"; node [shape=record]; a [label=\"empty\"]}}"
      res = tpl.format(name=self.name)
    else:
      res = """digraph finite_state_machine {
  rankdir=LR;  
  size=\"8,5\""""
      res += "  label=\"{}\"".format(self.name)
      if self.acceptstates:
        accept = " ".join(map(lambda x : '"'+x+'"', self.acceptstates))
        res += "  node [shape = doublecircle]; {};\n".format(accept)   
      res += "  node [shape = circle];\n"
      res += "  __I__ [label=\"\", style=invis, width=0]\n"
      res += "  __I__ -> \"{}\"\n".format(self.initial)      
      for (s,a,d) in self.transitions:
        sym = a if a != EPSILON else "ε"
        res += "  \"{s}\" -> \"{d}\" [label = {a}];\n".format(s=s,d=d,a=sym)      
      res += "}"    
    output = Source(res)
    if outfilename:      
      output.render(outfilename)
    return output

##################
    
  def to_txtfile(self, outfilename:str=None) -> str:
    """
    Save automaton into txt file.
    """
    res = ""
    for (s,a,d) in self.transitions:
      res += "{} {} {}\n".format(s,a,d)          
    res += "A "
    res += " ".join([s for s in self.acceptstates])      
    if outfilename:
      if os.path.isfile(outfilename):
        warn("File {f} exists, will be overwritten",f=outfilename)
      with open(outfilename,"w") as outfile:
        print(res,file=outfile)
    return res
    
##################   

  def _repr_svg_(self):    
    return self.to_graphviz()._repr_svg_()

##################   

  def from_txt(self, source:str, name:str=None):
    """
    Reads from a txt source string and initializes automaton.
    """
    if self.statesdict :
      warn("Automaton {a} not empty: content will be lost",a=self.name)
    self.reset(name)
    rows = source.strip().split("\n")
    for (i,row) in enumerate(rows[:-1]):
      try:
        (src,symbol,dest) = row.strip().split(" ")
        self.add_transition(src,symbol,dest)
      except ValueError:
        error("Malformed triple {t}",pos=name+":"+str(i+1),t=row.strip())
    if not rows[-1].startswith("A"):
      error("File must end with \"A\" row",pos=name+":"+str(len(rows)))
    self.make_accept(rows[-1].strip().split(" ")[1:], add=True)

##################
    
  def from_txtfile(self, infilename:str):
    """
    Reads from txt file and initializes automaton.
    """    
    try:
      with open(infilename) as infile:
        rows = infile.readlines()
    except FileNotFoundError:
      error("File not found: {f}",f=infilename)
    name = os.path.splitext(os.path.basename(infilename))[0]
    return self.from_txt("".join(rows), name)
    
########################################################################
########################################################################

class RegExpReader(object):
  """
  A reader for regular expressions, mainly used to convert to postfix notation
  """
  
  exp:str
  hd:int
  
  def __init__(self,exp:str)->None:
    """
    re is an infix regular expression (union +, kleene * and concatenation)
    """
    self.exp = exp
    
  def to_postfix(self)->Optional[str]:
    """
    Convert current regexp to postfix notation using a top-down LL parser
    You'll learn about this parser in L3 - Compilation ;-)
    We implement the following context-free grammar (L2 Langages formels ;-)
    E -> C E'; E' -> '+' C E' | epsilon; C -> K C'; C' -> K C' | epsilon
    K -> '(' E ')' K' | a K'; K' -> '*' | epsilon
    """
    def re_error(fct:str, ex: str, found: str):
      error("\"{}\": \"{}\" expected, \"{}\" found".format(fct, ex, found))
    def elem(re:str)->bool:
      return re[self.hd].isalnum() or re[self.hd] == EPSILON
    def forward(re:str, ex: str):
      if re[self.hd] == ex : self.hd += 1
      else: re_error("forward",ex,re[self.hd])
    def e(re:str)->Optional[str]:
      if re[self.hd] == "(" or elem(re): return ebis(re, c(re))
      else: re_error("e","( or symbol", re[self.hd]); return None
    def ebis(re:str, h:str)->Optional[str]:
      if re[self.hd] in "+": forward(re, '+'); return h + ebis(re, c(re)) + "+"
      elif re[self.hd] in ")$": return h
      else: re_error("ebis",")+$ or symbol", re[self.hd]); return None
    def c(re:str)->Optional[str]:
      if re[self.hd] == "(" or elem(re): return cbis(re, k(re))
      else: re_error("c","( or symbol",re[self.hd]); return None
    def cbis(re:str,h:str)->Optional[str]:
      if re[self.hd] == "(" or elem(re): return h + cbis(re, k(re)) + "."
      elif re[self.hd] in "+)$": return h
      else: re_error("cbis","()+$ or symbol", re[self.hd]); return None
    def k(re:str)->Optional[str]:
      if elem(re) : r = re[self.hd]; forward(re, r)
      elif re[self.hd] == '(' : forward(re, '('); r = e(re); forward(re, ')')        
      else: re_error("k","( or symbol", re[self.hd]); return None
      return kbis(re,r)
    def kbis(re:str,h:str)->Optional[str]:
      if self.hd >= len(re): pdb.set_trace()
      if re[self.hd] == '*' : forward(re, '*'); return h + "*"
      elif re[self.hd] in "+()$" or elem(re): return h
      else: re_error("kbis","()+$* or symbol", re[self.hd]); return None
              
    self.hd = 0 # reading head, initialized once and kept during parsing
    result = e(self.exp+"$")
    if self.hd == len(self.exp):
      return result
    else: return error("Stopped at index {} \"{}\"".format(self.hd,self.exp[self.hd]))

########################################################################
########################################################################

if __name__ == "__main__": # If the module is run from command line, test it
  a = Automaton("astarbstar")
  a.add_transition("0","a","1")  
  a.add_transition("1","a","1")
  a.add_transition("0","b","2")
  a.add_transition("2","b","2")  
  a.make_accept(["0","1", "2"])  
  print(a)  
  a.to_graphviz("my-test-automaton.gv")
  b = a.deepcopy()
  a.reset()
  print(b)
  for testfile in ["astarbstar","astarbstar-nfa","astarbstar-epsilon"]:
    a.from_txtfile("test/{}.af".format(testfile))
    a.to_graphviz("test/{}.gv".format(testfile))
    print(a)
    print(a.to_txtfile())
    
