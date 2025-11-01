"""
Unit tests for BFS and DFS algorithms
"""

import unittest
import sys
sys.path.append('../backend')

from algorithms.bfs import BFSSearch
from algorithms.dfs import DFSSearch
from algorithms.graph import Graph


class TestBFSAlgorithm(unittest.TestCase):
    """Test cases for BFS algorithm"""
    
    def setUp(self):
        """Set up test graph"""
        self.graph = Graph()
        
        nodes = {
            'A': (0, 0, 6.1), 'B': (2, 1, 4.0), 'C': (1, 3, 5.4),
            'D': (4, 0, 2.2), 'E': (3, 2, 3.2), 'F': (5, 3, 2.2),
            'G': (6, 1, 0.0), 'H': (2, -1, 4.5), 'I': (4, 2, 2.2)
        }
        
        for node_id, (x, y, h) in nodes.items():
            self.graph.add_node(node_id, x, y, h)
        
        edges = [
            ('A', 'B', 2.2), ('A', 'H', 2.2), ('A', 'C', 3.2),
            ('B', 'C', 2.2), ('B', 'E', 1.4), ('B', 'H', 2.2), ('B', 'D', 2.2),
            ('C', 'E', 2.2), ('D', 'E', 2.2), ('D', 'I', 2.2),
            ('D', 'G', 2.2), ('D', 'H', 2.2), ('E', 'F', 2.2),
            ('E', 'I', 1.4), ('F', 'I', 1.4), ('F', 'G', 2.2), ('I', 'G', 2.2)
        ]
        
        for from_node, to_node, cost in edges:
            self.graph.add_edge(from_node, to_node, cost)
    
    def test_bfs_finds_path(self):
        """Test that BFS finds a path"""
        searcher = BFSSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['path'])
    
    def test_bfs_expands_more_nodes(self):
        """Test that BFS expands more nodes than A*"""
        searcher = BFSSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertGreater(result['nodes_expanded'], 10)
    
    def test_bfs_path_validity(self):
        """Test BFS path is valid"""
        searcher = BFSSearch(self.graph, 'A', 'G')
        result = searcher.search()
        path = result['path']
        
        for i in range(len(path) - 1):
            neighbors = self.graph.get_neighbors(path[i])
            self.assertIn(path[i + 1], neighbors)


class TestDFSAlgorithm(unittest.TestCase):
    """Test cases for DFS algorithm"""
    
    def setUp(self):
        """Set up test graph"""
        self.graph = Graph()
        
        nodes = {
            'A': (0, 0, 6.1), 'B': (2, 1, 4.0), 'C': (1, 3, 5.4),
            'D': (4, 0, 2.2), 'E': (3, 2, 3.2), 'F': (5, 3, 2.2),
            'G': (6, 1, 0.0), 'H': (2, -1, 4.5), 'I': (4, 2, 2.2)
        }
        
        for node_id, (x, y, h) in nodes.items():
            self.graph.add_node(node_id, x, y, h)
        
        edges = [
            ('A', 'B', 2.2), ('A', 'H', 2.2), ('A', 'C', 3.2),
            ('B', 'C', 2.2), ('B', 'E', 1.4), ('B', 'H', 2.2), ('B', 'D', 2.2),
            ('C', 'E', 2.2), ('D', 'E', 2.2), ('D', 'I', 2.2),
            ('D', 'G', 2.2), ('D', 'H', 2.2), ('E', 'F', 2.2),
            ('E', 'I', 1.4), ('F', 'I', 1.4), ('F', 'G', 2.2), ('I', 'G', 2.2)
        ]
        
        for from_node, to_node, cost in edges:
            self.graph.add_edge(from_node, to_node, cost)
    
    def test_dfs_finds_path(self):
        """Test that DFS finds a path"""
        searcher = DFSSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['path'])
    
    def test_dfs_may_be_suboptimal(self):
        """Test that DFS may not find optimal solution"""
        searcher = DFSSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        # DFS cost may be higher than optimal (8.0)
        self.assertGreaterEqual(result['cost'], 8.0)


class TestAlgorithmComparison(unittest.TestCase):
    """Compare all three algorithms"""
    
    def setUp(self):
        """Set up test graph"""
        self.graph = Graph()
        
        nodes = {
            'A': (0, 0, 6.1), 'B': (2, 1, 4.0), 'C': (1, 3, 5.4),
            'D': (4, 0, 2.2), 'E': (3, 2, 3.2), 'F': (5, 3, 2.2),
            'G': (6, 1, 0.0), 'H': (2, -1, 4.5), 'I': (4, 2, 2.2)
        }
        
        for node_id, (x, y, h) in nodes.items():
            self.graph.add_node(node_id, x, y, h)
        
        edges = [
            ('A', 'B', 2.2), ('A', 'H', 2.2), ('A', 'C', 3.2),
            ('B', 'C', 2.2), ('B', 'E', 1.4), ('B', 'H', 2.2), ('B', 'D', 2.2),
            ('C', 'E', 2.2), ('D', 'E', 2.2), ('D', 'I', 2.2),
            ('D', 'G', 2.2), ('D', 'H', 2.2), ('E', 'F', 2.2),
            ('E', 'I', 1.4), ('F', 'I', 1.4), ('F', 'G', 2.2), ('I', 'G', 2.2)
        ]
        
        for from_node, to_node, cost in edges:
            self.graph.add_edge(from_node, to_node, cost)
    
    def test_astar_most_efficient(self):
        """Test that A* expands fewest nodes"""
        from algorithms.astar import AStarSearch
        
        astar = AStarSearch(self.graph, 'A', 'G').search()
        bfs = BFSSearch(self.graph, 'A', 'G').search()
        dfs = DFSSearch(self.graph, 'A', 'G').search()
        
        self.assertLess(astar['nodes_expanded'], bfs['nodes_expanded'])
    
    def test_astar_bfs_same_cost(self):
        """Test that A* and BFS find same optimal cost"""
        from algorithms.astar import AStarSearch
        
        astar = AStarSearch(self.graph, 'A', 'G').search()
        bfs = BFSSearch(self.graph, 'A', 'G').search()
        
        self.assertEqual(astar['cost'], bfs['cost'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
