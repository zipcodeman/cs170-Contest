import graph
import sys
import copy
import networkx as nx

debugging = False

def solve(g, heuristic=lambda g, node, touched: len([n for n in
                         g.neighbors(node) if n not in touched]), alg="greedy"):
  return eval(alg)(g, heuristic)

def greedy(g, heuristic):
  if debugging: print "Graph input:",g.nodes()
  g = copy.deepcopy(g)
  nodes = len(g.nodes())
  ans = []
  touched = set()
  bestChoice = -1
  bestScore = -1
  for node in g.nodes():
    h = heuristic(g, node, touched)
    if h > bestScore:
      bestChoice = node
      bestScore = h

  if debugging: print "chosing node:", bestChoice
  possibleNextChoices = set(g.neighbors(bestChoice))
  if bestChoice in possibleNextChoices:
    possibleNextChoices.remove(bestChoice)
  if debugging: print "connected next choices:",possibleNextChoices
  ans.append(bestChoice)
  touched.add(bestChoice)
  touched.update(g.neighbors(bestChoice))
  if debugging: print "Nodes touched so far:",touched

  g.remove_node(bestChoice)
  if debugging: print "Graph after removing choice:",g.nodes()

  while len(touched) < nodes:
    bestChoice = -1
    bestScore = -1
    if len(possibleNextChoices) == 0:
      return None
    for choice in possibleNextChoices:
      h = heuristic(g, choice, touched)
      if h > bestScore and choice not in touched: 
        bestChoice = choice
        bestScore = h
    if bestChoice == -1:
      for choice in possibleNextChoices:
        h = heuristic(g, choice, touched)
        if h > bestScore:
          bestChoice = choice
          bestScore = h

    if debugging: print "chosing node:",bestChoice
    ans.append(bestChoice)
    touched.add(bestChoice)
    touched.update(g.neighbors(bestChoice))
    if debugging: print "Nodes touched so far:",touched
    possibleNextChoices.update(g.neighbors(bestChoice))
    if bestChoice in possibleNextChoices:
      possibleNextChoices.remove(bestChoice)
    if debugging: print "connected next choices:",possibleNextChoices

    g.remove_node(bestChoice)

    if debugging: print "Graph after removing choice:",g.nodes()
  return ans

def greedyold(g, heuristic):
  if debugging: print "Graph input:",g
  g = copy.deepcopy(g)
  ans = []
  bestChoice = -1
  bestScore = -1
  for node in range(len(g)):
    h = heuristic(g, node)
    if h > bestScore:
      bestChoice = node
      bestScore = h

  if debugging: print "chosing node:", bestChoice
  possibleNextChoices = g[bestChoice]
  if debugging: print "connected next choices:",possibleNextChoices
  ans.append(bestChoice)

  g.removeNode(bestChoice)
  if debugging: print "Graph after removing choice:",g

  while not g.graphEmpty():
    bestChoice = -1
    bestScore = -1
    if len(possibleNextChoices) == 0:
      return None
    for choice in possibleNextChoices:
      h = heuristic(g, choice)
      if h > bestScore:
        bestChoice = choice
        bestScore = h

    if debugging: print "chosing node:",bestChoice
    possibleNextChoices.remove(bestChoice)
    ans.append(bestChoice)
    possibleNextChoices.update(g[bestChoice])
    if debugging: print "connected next choices:",possibleNextChoices

    g.removeNode(bestChoice)
    if debugging: print "Graph after removing choice:",g
  return ans
  
if __name__ == "__main__":
  debugging = True
  if len(sys.argv) <= 1:
    print "You must specify an input file"
  else:
    G = nx.read_adjlist('graphs/' + sys.argv[1] + '.adjlist')
    print G.nodes()
    print G.edges()
    print solve(G)
    g = graph.Graph('graphs/' + sys.argv[1] + '.adjlist')
    print solve(g, alg="greedyold", heuristic=lambda g, node: len(g[node]))
