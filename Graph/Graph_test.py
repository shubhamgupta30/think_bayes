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

  def verify_list_equal_unordered(self, l1, l2):
    """ Tests if two lists are equal unordered

    Args:
      l1, l2: lists to be compared
    """
    self.assertEqual(sorted(l1), sorted(l2))

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

  def test_remove_vertex(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e1 = Edge(v,w)
    e2 = Edge(w,x)
    e3 = Edge(v,x)

    # Test removal of only vertex
    g.add_vertex(v)
    g.remove_vertex(v)
    self.assertEqual(g, {})

    # Test removal of vertex with no edges incident on it
    g.clear()
    g.add_vertex(v)
    g.add_edge(e2)
    g.remove_vertex(v)
    self.assertEqual(g, {w:{x:e2}, x:{w:e2}})

    # Test removal of vertex with edges incident on it.
    g.clear()
    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)
    g.remove_vertex(v)
    self.assertEqual(g, {w:{x:e2}, x:{w:e2}})

  def test_get_edge(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e1 = Edge(v,w)
    e2 = Edge(w,x)
    e3 = Edge(v,x)

    # Query for edge from an empty graph
    self.assertEqual(g.get_edge(v, w), None)

    # Query for a non existent edge with one vertex present
    g.clear()
    g.add_vertex(v)
    self.assertEqual(g.get_edge(v, w), None)

    # Query for a non existent edge with both vertices present
    g.clear()
    g.add_vertex(v)
    g.add_vertex(w)
    self.assertEqual(g.get_edge(v, w), None)

    # Query for an existent edge
    g.clear()
    g.add_edge(e1)
    g.add_edge(e2)
    self.assertEqual(g.get_edge(v,w), e1)

  def test_vertices(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')

    # Vertices when graph is empty
    self.verify_list_equal_unordered(g.vertices(), [])

    # Graph has one vertex
    g.add_vertex(v)
    self.verify_list_equal_unordered(g.vertices(), [v])

    # Graph has multiple vertex
    g.add_vertex(w)
    g.add_vertex(x)
    self.verify_list_equal_unordered(g.vertices(), [v, w, x])

  def test_edges(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e1 = Edge(v,w)
    e2 = Edge(w,x)
    e3 = Edge(v,x)

    # Edges when graph is empty
    self.verify_list_equal_unordered(g.edges(), [])

    # Edges when only vertices present
    g.add_vertex(v)
    g.add_vertex(w)
    self.verify_list_equal_unordered(g.edges(), [])

    # Edges when edges present
    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)
    self.verify_list_equal_unordered(g.edges(), [e1, e2, e3])

  def test_out_vertices(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e1 = Edge(v,w)
    e2 = Edge(w,x)
    e3 = Edge(v,x)

    # Test on a non existent vertex
    g.add_vertex(v)
    self.verify_list_equal_unordered(g.out_vertices(w), [])

    # Test on a edgeless graph
    g.add_vertex(w)
    g.add_vertex(x)
    self.verify_list_equal_unordered(g.out_vertices(v), [])

    # Test on a non-edgeless graph
    g.add_edge(e1)
    self.verify_list_equal_unordered(g.out_vertices(x), [])
    g.add_edge(e2)
    g.add_edge(e3)
    self.verify_list_equal_unordered(g.out_vertices(x), [v, w])

  def test_out_edges(self):
    g = Graph()
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e1 = Edge(v,w)
    e2 = Edge(w,x)
    e3 = Edge(v,x)

    # Test on a non existent vertex
    g.add_vertex(v)
    self.verify_list_equal_unordered(g.out_edges(w), [])

    # Test on a edgeless graph
    g.add_vertex(w)
    g.add_vertex(x)
    self.verify_list_equal_unordered(g.out_edges(v), [])

    # Test on a non-edgeless graph
    g.add_edge(e1)
    self.verify_list_equal_unordered(g.out_edges(x), [])
    g.add_edge(e2)
    g.add_edge(e3)
    self.verify_list_equal_unordered(g.out_edges(x), [e2, e3])








if __name__ == "__main__":
  unittest.main()

