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
    self.assertEqual(g, {v:{w:e}, w:{v:e}})
    g.clear();

    # Without adding one vertex
    g.add_vertex(v)
    g.add_edge(e)
    self.assertEqual(g, {v:{w:e}, w:{v:e}})
    g.clear();

    # After Adding both vertices
    g.add_vertex(v)
    g.add_vertex(w)
    g.add_edge(e)
    self.assertEqual(g, {v:{w:e}, w:{v:e}})

  def test_remove_edge(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e1 = Edge(v,w)
    e2 = Edge(w,x)
    e3 = Edge(v,x)

    # Remove edge from an empty graph
    g.remove_edge(e1)
    self.assertEqual(g, {})

    # Remove a non existent edge with one vertex present
    g.clear()
    g.add_vertex(v)
    g.remove_edge(e1)
    self.assertEqual(g, {v:{}})

    # Remove a non existent edge with both vertices present
    g.clear()
    g.add_vertex(v)
    g.add_vertex(w)
    g.remove_edge(e1)
    self.assertEqual(g, {v:{}, w:{}})

    # Remove an existent edge
    g.clear()
    g.add_edge(e1)
    g.add_edge(e2)
    g.remove_edge(e1)
    self.assertEqual(g, {v:{}, w:{x:e2}, x:{w:e2}})

if __name__ == "__main__":
  unittest.main()

