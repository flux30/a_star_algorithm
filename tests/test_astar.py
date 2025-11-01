"""
Unit tests for A* Search Algorithm
"""

import unittest
import sys
sys.path.append('../backend')

from algorithms.astar import AStarSearch
from algorithms.graph import Graph


class TestAStarAlgorithm(unittest.TestCase):
    """Test cases for A* algorithm"""
    
    def setUp(self):
        """Set up test graph"""
        self.graph = Graph()
        
        # Add nodes
        nodes = {
            'A': (0, 0, 6.1), 'B': (2, 1, 4.0), 'C': (1, 3, 5.4),
            'D': (4, 0, 2.2), 'E': (3, 2, 3.2), 'F': (5, 3, 2.2),
            'G': (6, 1, 0.0), 'H': (2, -1, 4.5), 'I': (4, 2, 2.2)
        }
        
        for node_id, (x, y, h) in nodes.items():
            self.graph.add_node(node_id, x, y, h)
        
        # Add edges
        edges = [
            ('A', 'B', 2.2), ('A', 'H', 2.2), ('A', 'C', 3.2),
            ('B', 'C', 2.2), ('B', 'E', 1.4), ('B', 'H', 2.2), ('B', 'D', 2.2),
            ('C', 'E', 2.2), ('D', 'E', 2.2), ('D', 'I', 2.2),
            ('D', 'G', 2.2), ('D', 'H', 2.2), ('E', 'F', 2.2),
            ('E', 'I', 1.4), ('F', 'I', 1.4), ('F', 'G', 2.2), ('I', 'G', 2.2)
        ]
        
        for from_node, to_node, cost in edges:
            self.graph.add_edge(from_node, to_node, cost)
    
    def test_astar_finds_path(self):
        """Test that A* finds a path from A to G"""
        searcher = AStarSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['path'])
        self.assertEqual(result['path'][0], 'A')
        self.assertEqual(result['path'][-1], 'G')
    
    def test_astar_optimal_cost(self):
        """Test that A* finds optimal cost"""
        searcher = AStarSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertEqual(result['cost'], 8.0)
    
    def test_astar_nodes_expanded(self):
        """Test node expansion count"""
        searcher = AStarSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertLessEqual(result['nodes_expanded'], 10)
    
    def test_astar_path_validity(self):
        """Test that returned path is valid"""
        searcher = AStarSearch(self.graph, 'A', 'G')
        result = searcher.search()
        path = result['path']
        
        # Check all nodes in path are connected
        for i in range(len(path) - 1):
            neighbors = self.graph.get_neighbors(path[i])
            self.assertIn(path[i + 1], neighbors)
    
    def test_astar_trace_recorded(self):
        """Test that execution trace is recorded"""
        searcher = AStarSearch(self.graph, 'A', 'G')
        result = searcher.search()
        
        self.assertGreater(len(result['trace']), 0)
        self.assertIn('step', result['trace'][0])
        self.assertIn('node', result['trace'][0])
        self.assertIn('g', result['trace'][0])
        self.assertIn('h', result['trace'][0])
        self.assertIn('f', result['trace'][0])
    
    def test_astar_start_equals_goal(self):
        """Test when start and goal are the same"""
        searcher = AStarSearch(self.graph, 'A', 'A')
        result = searcher.search()
        
        self.assertTrue(result['success'])
        self.assertEqual(result['path'], ['A'])
        self.assertEqual(result['cost'], 0)
    
    def test_astar_different_start_goal(self):
        """Test A* with different start-goal pairs"""
        test_cases = [
            ('B', 'G', 7.8),
            ('C', 'G', 9.2),
            ('H', 'G', 6.6)
        ]
        
        for start, goal, expected_max_cost in test_cases:
            with self.subTest(start=start, goal=goal):
                searcher = AStarSearch(self.graph, start, goal)
                result = searcher.search()
                
                self.assertTrue(result['success'])
                self.assertLessEqual(result['cost'], expected_max_cost)


class TestAStarHeuristic(unittest.TestCase):
    """Test heuristic function properties"""
    
    def setUp(self):
        """Set up test graph"""
        self.graph = Graph()
        self.graph.add_node('A', 0, 0, 6.1)
        self.graph.add_node('G', 6, 1, 0.0)
    
    def test_heuristic_admissible(self):
        """Test that heuristic never overestimates"""
        import math
        
        h_value = self.graph.get_heuristic('A')
        coord_a = self.graph.get_coordinate('A')
        coord_g = self.graph.get_coordinate('G')
        
        straight_line = math.sqrt((coord_g[0] - coord_a[0])**2 + 
                                  (coord_g[1] - coord_a[1])**2)
        
        self.assertAlmostEqual(h_value, straight_line, places=1)
    
    def test_goal_heuristic_zero(self):
        """Test that heuristic at goal is zero"""
        h_goal = self.graph.get_heuristic('G')
        self.assertEqual(h_goal, 0.0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
