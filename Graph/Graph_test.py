"""
Test file for Graph.py
"""
import unittest
from Graph import Graph
from Graph import Edge
from Graph import Vertex
from sets import Set

class GraphTest(unittest.TestCase):

  def isomorphic(self, g1, g2):
    """ Tests if two graphs are same
    """
    return g1.__dict__ == g2.__dict__

  def test_add_vertex(self):
    g = Graph()
    # Tests that a label is used only once.
    g.add_vertex(Vertex('label1'))
    g.add_vertex(Vertex('label2'))
    g.add_vertex(Vertex('label2'))

    self.assertEqual(g, {Vertex('label1'):{}, Vertex('label2'):{}})

  def test_add_edge(self):
    g = Graph()
    v = Vertex('label1')
    w = Vertex('label2')
    e = Edge(v,w)

    # Without adding both vertices
    g.add_edge(e)
    self.assertEqual(g, {})

    # Without adding one vertex
    g.add_vertex(v)
    g.add_edge(e)
    self.assertEqual(g, {v:{}})

    # After Adding both vertices
    g.add_vertex(w)
    g.add_edge(e)
    self.assertEqual(g, {v:{w:e}, w:{v:e}})

if __name__ == "__main__":
  unittest.main()

