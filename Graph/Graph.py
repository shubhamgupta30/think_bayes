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
    return tuple.__new__(self, (v1, v2))

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
      if w in self[v]:
        del self[v][w]
      if v in self[w]:
        del self[w][v]

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
      edges = self[v].viewvalues()
      for e in edges:
        remove_edge(e)

      # The adjacency list should be empty now.
      assert self[v] == {}
      del self[v]
    else:
      logging.warning("Attempt to remove a non-existent vertex " + str(v))

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

  def __eq__(self, other):
    return self.__str__() == other.__str__()

  def __hash__(self):
    return hash_string(self.__str__())


