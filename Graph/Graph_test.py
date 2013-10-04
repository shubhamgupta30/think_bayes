"""
Test file for Graph.py
"""
import unittest
from Graph import Graph
from Graph import Edge
from Graph import Vertex

class GraphTest(unittest.TestCase):

  def equal(self, g1, g2):
    """ Tests if two graphs are same
    """
    return g1.__dict__ == g2.__dict__

  def test_add_vertex(self):
    g1 = Graph()
    g1.add_vertex(Vertex('label1'))
    g1.add_vertex(Vertex('label2'))
    g1.add_vertex(Vertex('label2'))

    g2 = Graph()
    g2.add_vertex(Vertex('label1'))
    g2.add_vertex(Vertex('label2'))
    self.assertTrue(self.equal(g1, g2))

if __name__ == "__main__":
  unittest.main()

