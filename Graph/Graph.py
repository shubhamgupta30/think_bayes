"""A way of representing Simple Undirected graphs.

A simple representation of graph as dictioanry of sets.
Every vertex has a label, which is used to access it in the graph.
Graph is a dictionary with keys as vertex labels, and the values as the
adjacency list of these vertices.
An adjacency list is a set of labels corresponding to the neighbouring vertices
An edge is represented as a pair of vertex labels.

Inspired largely by implementation in
http://greenteapress.com/complexity/thinkcomplexity.pdf
"""

from sets import Set

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


class Graph(dict):
  def __init__ (self, vs = [], es = []):
    """Create a new graph.

    Args:
      vs: list of vertices
      es: list of edges
    """
    self.vertex_labels = Set()
    for v in vs:
      self.add_vertex(v)

    for e in es:
      self.add_edge(e)

  def add_vertex(self, v) :
    """ Adds a vertex to the set of vertices.

    Args:
      v: The vertex to be added
    """
    # Property: Every vertex of a graph has a unique label.
    # If a vertex exists in the graph with this label, then do not insert
    # this vertex.
    if v.label not in self.vertex_labels:
      self.vertex_labels.add(v.label)
      self[v] = Set()

  def add_edge(self, e):
    """ Adds an edge to the set of vertices.

    Args:
      e: the edge to be added
    """
    (v,w) = e
    assert self.has_key(v)
    assert self.has_key(w)
    self[v].add(w)
    self[w].add(v)

  def remove_edge(self, e):
    """ Removes an edge from the graph

    Args:
      e: The edge to be removed
    """
    (v,w) = e
    if self.has_key(v) and self.has_key(w):
      if w in self[v]:
        self[v].remove(w)
      if v in self[w]:
        self[w].remove(v)

  def remove_vertex(self, v):
    """ Removes a vertex from the graph

    Args:
      v: The vertex to be removed
    """
    # Assumption of a 'sane' graph
    if self.has_key(v):
      for vertex in self[v]:
        self[vertex].remove(v)
      del self[v]
      # The label is freed only if the vertex present in the graph is deleted.
      self.vertex_labels.remove(v.label)

  def is_graph_sane(self):
    """ Performs basic sanity checks on the graph

    Returns:
      true: if graph is sane
      false: if graph has some error
    """
    if self.vertex_labels != Set([v.label for v in self.keys()]):
      print "Label List Mismatch"
      return false

    for (v, neighbours) in self.iteritems():
      for w in neighbours:
        if v not in self[w]:
          print "Undirectedness violated"
          return false

    return true


