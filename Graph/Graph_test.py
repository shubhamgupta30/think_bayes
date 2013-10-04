"""
Test file for Graph.py
"""
import unittest
from Graph import Graph
from Graph import Edge
from Graph import Vertex
from sets import Set

class GraphTest(unittest.TestCase):

  def equal(self, g1, g2):
    """ Tests if two graphs are same
    """
    return g1.__dict__ == g2.__dict__

  def test_add_vertex(self):
    g = Graph()
    g.add_vertex(Vertex('label1'))
    g.add_vertex(Vertex('label2'))
    g.add_vertex(Vertex('label2'))

    self.assertEqual(Vertex('l'), Vertex('l'))
    self.assertEqual(g.vertex_labels, Set(['label1', 'label2']))
    self.assertEqual(sorted(g.keys()), [Vertex('label1'), Vertex('label2')])
    self.assertEqual(g[Vertex('label1')], {})
    self.assertEqual(g[Vertex('label2')], {})

if __name__ == "__main__":
  unittest.main()

