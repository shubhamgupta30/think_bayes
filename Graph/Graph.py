"""A way of representing Simple Undirected graphs.

A simple representation of graph as dictioanry of sets.
Every vertex has a label, which is used to access it in the graph.
Graph is a dictionary with keys as vertex labels, and the values as the
adjacency list of these vertices.
An adjacency list is itself a dictionary with keys as vertex labels and values
are the corresponding edge objects.
Storing the edge objects is useful as they may store additional information
about the edge, like weights, labels, etc.
An edge is represented as a pair of vertex labels.

Inspired largely by implementation in
http://greenteapress.com/complexity/thinkcomplexity.pdf
"""

from sets import Set
from collections import deque
from numpy.random import binomial
import hashlib
import logging

"""A hash function
"""
def hash_string(s):
  return int(hashlib.md5(s).hexdigest(), 16)

"""
A class representing a vertex. It has a label.
"""
class Vertex:
  def __init__ (self, label):
    """ Creates a new vertex.

    Args:
      label: Label of the vertex to be created
    """
    self.label = label

  def __repr__(self):
    """ Crete a string representation of the vertex
    """
    return '%s' % repr(self.label)

  __str__ = __repr__

  def __eq__(self, other):
    return self.__str__() == other.__str__()

  def __hash__(self):
    return hash_string(self.__str__())


""" A class representing an edge.
It inherits from Tuple, and hence the objects created are immutable.
When a new object is created, first __new__ is called, followed by __init__.
Thus we have overridden __new__ in this instead of __init__.
"""

class Edge(tuple):
  def __new__ (self, v1, v2):
    """ Creates a new undirected edge.

    Args:
      v1: First Vertex
      v2: Second Vertex
    """
    if v1.label < v2.label:
      return tuple.__new__(self, (v1, v2))
    return tuple.__new__(self, (v2, v1))

  def __repr__(self):
    """ Crete a string representation of the edge
    """
    return '(%s, %s)' % (repr(self[0]), repr(self[1]))

  __str__ = __repr__

  def __eq__(self, other):
    return self.__str__() == other.__str__()

  def __hash__(self):
    return hash_string(self.__str__())


class Graph(dict):
  def __init__ (self, vs = [], es = []):
    """Create a new graph.

    Args:
      vs: list of vertices
      es: list of edges
    """
    for v in vs:
      self.add_vertex(v)

    for e in es:
      self.add_edge(e)

  def add_vertex(self, v) :
    """ Adds a vertex to the Graph's vertices.

    Args:
      v: The vertex to be added
    """
    # Property: Every vertex of a graph has a unique label.
    # If a vertex exists in the graph with this label, then do not insert
    #this vertex.
    if v in self:
      logging.warning('Vertex not inserted as there is another vertex in graph'
                      + ' with label ' + v.label)
      return
    self[v] = {}

  def add_edge(self, e):
    """ Adds an edge to the set of vertices.

    Args:
      e: the edge to be added
    """
    (v,w) = e
    if not self.has_key(v):
      logging.warning('Attempt to insert edge ' + str(e) + ' while vertex ' +
                      str(v) + ' is not in graph yet. This resulted in '+
                      'addition of ' + str(v) + ' to the graph.')
      self.add_vertex(v)
    if not self.has_key(w):
      logging.warning('Attempt to insert edge ' + str(e) + ' while vertex ' +
                      str(w) + ' is not in graph yet. This resulted in '+
                      'addition of ' + str(w) + ' to the graph.')
      self.add_vertex(w)
    self[v][w] = e
    self[w][v] = e


  def remove_edge(self, e):
    """ Removes an edge from the graph if the edge is present.
    Otherwise, it does nothing. Note that it does not throw an error
    if the edge is not present.

    Args:
      e: The edge to be removed
    """
    (v,w) = e
    if self.has_key(v) and self.has_key(w):
      edge_present = w in self[v] and v in self[w]
      edge_not_present = w not in self[v] and v not in self[w]
      assert edge_present or edge_not_present
      if edge_present:
        del self[w][v]
        del self[v][w]
      else:
        logging.warning('The edge ' + str(e) + ' is not present in the graph.')
    else:
      logging.warning('One of the vertices for the edge ' + str(e) + ' is ' +
                      'not present in the graph. Edge deletion unsuccessful.')

  def remove_vertex(self, v):
    """ Removes a vertex from the graph if it is present. Otherwise, it does
    nothing. Note that it does not throw an error in case a vertex is not
    present.

    Args:
      v: The vertex to be removed
    """
    # Is the vertex present in the graph?
    if self.has_key(v):
      # Remove all the neighbouring edges
      edges = self[v].values()
      for e in edges:
        self.remove_edge(e)

      # The adjacency list should be empty now.
      assert self[v] == {}
      del self[v]
    else:
      logging.warning("Attempt to remove a non-existent vertex " + str(v))

  def get_edge(self, v1, v2):
    """ Returns the edge between vertices v1 and v2 if it exists.

    Args:
      v1: The first vertex
      v2: The second vertex
    Returns:
      The edge between v1 and v2, and None otherwise
    """
    if v1 not in self.viewkeys():
      logging.warning('Vertex ' + str(v1) + ' is not present in graph.' +
                      'Edge query unsuccessful.')
      return None
    if v2 not in self.viewkeys():
      logging.warning('Vertex ' + str(v2) + ' is not present in graph.' +
                      'Edge query unsuccessful.')
      return None
    edge_present = v1 in self[v2] and v2 in self[v1]
    edge_not_present = v1 not in self[v2] and v2 not in self[v1]
    assert edge_present or edge_not_present
    if edge_present:
      assert self[v2][v1] == self[v1][v2]
      return self[v2][v1]
    return None

  def vertices(self):
    """ Returns a list of vertices of the graph

    Returns:
      A list of vertices of the graph
    """
    return self.keys()

  def edges(self):
    """ Returns a list of edges of the graph

    Returns:
      A list of edges of the graph
    """
    edges = Set()
    for v in self.viewkeys():
      for e in self[v].viewvalues():
        edges.add(e)
    return list(edges)

  def out_vertices(self, v):
    """ Returns a list of vertices adjacent to v

    Args:
      v :  the vertex
    Returns:
      List of neighbors of the vertex v
    """
    if v not in self:
      logging.warning('out_vertices fails, because ' + str(v) + ' is not in ' +
                      'the graph')
      return []
    return self[v].keys()

  def out_edges(self, v):
    """ Returns a list of edges adjacent to v

    Args:
      v :  the vertex
    Returns:
      List of edges incident on the vertex v
    """
    if v not in self:
      logging.warning('out_edges fails, because ' + str(v) + ' is not in ' +
                      'the graph')
      return []
    return self[v].values()

  def add_all_edges(self):
    """ Starts from an edgeless graph and adds all edges
    """
    if self.edges() != []:
      logging.warning('Graph ' + str(self) + ' is not edgeless. Aborting add_all_edges.')
      return
    vertices = self.vertices()
    for v in vertices:
      for w in vertices:
        if v == w:
          continue
        self[v][w] = self[w][v] if v in self[w] else Edge(v, w)


  def is_graph_sane(self):
    """ Performs basic sanity checks on the graph

    Returns:
      true: if graph is sane
      false: if graph has some error
    """

    for (v, neighbours) in self.iteritems():
      for w in neighbours:
        if v not in self[w]:
          print "Undirectedness violated"
          return false
        if self[v][w] != self[w][v]:
          print "Wrong Edge representation"
          return false

    return true

  def bfs(self, start):
    """ Takes a start node and performs a bfs.
    Args:
      start: the start node
    Returns:
      A set of discovered nodes in the graph
    """
    queue = deque([start])
    visited = Set()
    while queue:
      v = queue.popleft()
      for w in self.out_vertices(v):
        if w not in visited:
          queue.append(w)
      visited.add(v)
    return visited

  def is_connected(self):
    """ Determines if the graph is connected
    Returns:
      true if the graph is connected, false otherwise
    """
    if len(self) == 0:
      # An empty graph is vacuosly connected
      return True
    visited = self.bfs(next(self.iterkeys()))
    if len(visited) == len(self):
      return True
    return False

  def __eq__(self, other):
    return self.__str__() == other.__str__()

  def __hash__(self):
    return hash_string(self.__str__())

def getRandomCoinFlip(p):
  max_flips = 10000
  coin_flips = binomial(1, p, max_flips)
  position = 0
  while True:
    if position == max_flips:
      coin_flips = binomial(1, p, max_flips)
      position = 0
    else:
      yield coin_flips[position]
      position += 1

class RandomGraph(Graph):
  def __init__(self, n, p):
    """ Creates a random graph with the parameters n,p
    Args:
      n : number of vertices
      p: Probability that an edge is present in the graph
    """
    coin = getRandomCoinFlip(p)
    vertices = [Vertex('v' + str(i)) for i in xrange(n)]
    edges = [Edge(v,w) for v in vertices for w in vertices if v != w and next(coin) == 1]
    Graph.__init__(self, vertices, edges)

