import unittest
from routing_optimizer import LogisticsGraph

class TestLogisticsGraph(unittest.TestCase):
    def setUp(self):
        """Initializes a standardized test graph network structure."""
        self.graph = LogisticsGraph()
        self.graph.add_edge("A", "B", 10.0, 2.0) # Edge with a peak traffic factor of 2.0
        self.graph.add_edge("B", "C", 15.0, 1.0)
        self.graph.add_edge("A", "C", 40.0, 1.0)

    def test_standard_non_peak_routing(self):
        """Verifies correct shortest path calculations during non-peak operational hours."""
        # Expected optimal path: A -> B -> C (Cost: 10 + 15 = 25)
        path, cost = self.graph.compute_shortest_path("A", "C", time_of_day=12.0)
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 25.0)

    def test_peak_traffic_rerouting(self):
        """Verifies that the algorithm correctly routes around peak congestion bottlenecks."""
        # During peak hours (09:00), edge A->B cost scales to 10 * 2.0 = 20. Total path cost = 35.
        # Direct route A -> C stays at 40.0. The algorithm should still pick A -> B -> C.
        path, cost = self.graph.compute_shortest_path("A", "C", time_of_day=9.0)
        self.assertEqual(path, ["A", "B", "C"])
        self.assertEqual(cost, 35.0)

    def test_unreachable_node_boundary(self):
        """Verifies graceful handling and infinity tracking for completely disconnected components."""
        self.graph.add_node("Isolated_Node")
        path, cost = self.graph.compute_shortest_path("A", "Isolated_Node", time_of_day=12.0)
        self.assertIsNone(path)
        self.assertEqual(cost, float('inf'))

if __name__ == "__main__":
    unittest.main()
  
