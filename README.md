# Graph-Based-Logistics-Optimizer-Python-Network-Analysis-
This project uses Dijkstra's algorithm optimized with a min-heap priority queue to solve a time-dependent, multi-stop routing problem.
import heapq
from typing import Dict, List, Tuple, Optional

class LogisticsGraph:
    """Represents a sparse directed graph using an adjacency list."""
    def __init__(self):
        # Format: { node: [(neighbor, base_weight, traffic_factor)] }
        self.adj_list: Dict[str, List[Tuple[str, float, float]]] = {}

    def add_node(self, node: str) -> None:
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, u: str, v: str, weight: float, traffic_factor: float = 1.0) -> None:
        self.add_node(u)
        self.add_node(v)
        self.adj_list[u].append((v, weight, traffic_factor))

    def compute_shortest_path(self, start: str, target: str, time_of_day: float) -> Tuple[Optional[List[str]], float]:
        """
        Implements an optimized Dijkstra's algorithm with dynamic time-dependent weights.
        Time Complexity: O((V + E) log V) using a binary heap.
        """
        # Priority Queue storage: (cumulative_cost, current_node, path_history)
        pq: List[Tuple[float, str, List[str]]] = [(0.0, start, [start])]
        visited: Dict[str, float] = {}

        while pq:
            current_cost, current_node, path = heapq.heappop(pq)

            if current_node == target:
                return path, current_cost

            if current_node in visited and visited[current_node] <= current_cost:
                continue
            visited[current_node] = current_cost

            for neighbor, base_weight, traffic in self.adj_list.get(current_node, []):
                # Simulate dynamic peak hours (e.g., higher traffic between 08:00-10:00 and 16:00-18:00)
                is_peak = (8.0 <= time_of_day <= 10.0) or (16.0 <= time_of_day <= 18.0)
                dynamic_weight = base_weight * (traffic if is_peak else 1.0)
                total_cost = current_cost + dynamic_weight

                if neighbor not in visited or total_cost < visited.get(neighbor, float('inf')):
                    heapq.heappush(pq, (total_cost, neighbor, path + [neighbor]))

        return None, float('inf')

if __name__ == "__main__":
    # Mock data setup showcasing scalable object architecture
    optimizer = LogisticsGraph()
    optimizer.add_edge("Berlin_Hub", "Hannover_Node", 280.0, 1.4)
    optimizer.add_edge("Hannover_Node", "Frankfurt_Hub", 350.0, 1.1)
    optimizer.add_edge("Berlin_Hub", "Leipzig_Node", 190.0, 1.2)
    optimizer.add_edge("Leipzig_Node", "Frankfurt_Hub", 380.0, 1.5)

    print("🤖 Executing Time-Dependent Network Optimization...")
    # Execute routing at 09:00 AM (Peak traffic simulation)
    route, cost = optimizer.compute_shortest_path("Berlin_Hub", "Frankfurt_Hub", time_of_day=9.0)
    print(f"Optimal Path (Peak): {route} | Calculated Cost Indicator: {cost:.2f}")
