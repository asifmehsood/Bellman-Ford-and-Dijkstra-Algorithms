"""
Bellman-Ford Algorithm Implementation (Dynamic Programming Approach)
CS412 - Algorithm Analysis & Design
Implemented from scratch without using any graph libraries
"""

import sys


class BellmanFordAlgorithm:
    """
    Bellman-Ford Algorithm for finding shortest paths from a source vertex
    to all other vertices in a weighted directed graph.
    
    Can handle negative edge weights and detect negative cycles.
    
    Time Complexity: O(V * E)
    Space Complexity: O(V)
    
    Dynamic Programming approach: relaxes all edges V-1 times
    """
    
    def __init__(self, edges, num_vertices):
        """
        Initialize Bellman-Ford Algorithm
        
        Args:
            edges: List of tuples (source, target, weight)
            num_vertices: Total number of vertices in the graph
        """
        self.edges = edges
        self.num_vertices = num_vertices
    
    def shortest_path(self, source):
        """
        Calculate shortest paths from source to all other vertices using DP
        
        Args:
            source: Starting vertex
            
        Returns:
            distances: Array of shortest distances from source to each vertex
            predecessors: Array to reconstruct shortest paths
            has_negative_cycle: Boolean indicating if negative cycle exists
        """
        # Initialize distances to infinity
        distances = [sys.maxsize] * self.num_vertices
        distances[source] = 0
        
        # Store predecessors for path reconstruction
        predecessors = [-1] * self.num_vertices
        
        # Relax all edges V-1 times (Dynamic Programming iterations)
        # After i iterations, we have shortest paths with at most i edges
        for iteration in range(self.num_vertices - 1):
            updated = False
            
            # Try to relax each edge
            for src, dest, weight in self.edges:
                # Only update if source is reachable
                if distances[src] != sys.maxsize:
                    new_distance = distances[src] + weight
                    
                    # If we found a shorter path, update it
                    if new_distance < distances[dest]:
                        distances[dest] = new_distance
                        predecessors[dest] = src
                        updated = True
            
            # If no update in this iteration, we can break early
            if not updated:
                break
        
        # Check for negative weight cycles
        # If we can still relax edges, there's a negative cycle
        has_negative_cycle = False
        for src, dest, weight in self.edges:
            if distances[src] != sys.maxsize:
                if distances[src] + weight < distances[dest]:
                    has_negative_cycle = True
                    break
        
        return distances, predecessors, has_negative_cycle
    
    def get_path(self, predecessors, source, destination):
        """
        Reconstruct the shortest path from source to destination
        
        Args:
            predecessors: Array of predecessor vertices
            source: Starting vertex
            destination: Target vertex
            
        Returns:
            List representing the path from source to destination
        """
        if predecessors[destination] == -1 and destination != source:
            return []  # No path exists
        
        path = []
        current = destination
        
        # Build path backwards from destination to source
        while current != -1:
            path.append(current)
            current = predecessors[current]
        
        path.reverse()
        return path


def load_graph_from_csv(filename):
    """
    Load graph from CSV file
    
    Args:
        filename: Path to CSV file with columns: source, target, weight
        
    Returns:
        edges: List of tuples (source, target, weight)
        num_vertices: Total number of unique vertices
    """
    edges = []
    vertices = set()
    
    with open(filename, 'r') as file:
        # Skip header
        next(file)
        
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(',')
                source = int(parts[0])
                target = int(parts[1])
                weight = int(parts[2])
                
                # Add vertices to set
                vertices.add(source)
                vertices.add(target)
                
                # Add edge to list
                edges.append((source, target, weight))
    
    # Get maximum vertex number + 1 for array sizing
    num_vertices = max(vertices) + 1 if vertices else 0
    
    return edges, num_vertices


def run_bellman_ford(filename, source_vertex=0):
    """
    Main function to run Bellman-Ford algorithm on a graph from CSV
    
    Args:
        filename: Path to CSV file
        source_vertex: Starting vertex (default: 0)
        
    Returns:
        distances: Shortest distances from source
        predecessors: Predecessor array for path reconstruction
        has_negative_cycle: Boolean indicating negative cycle presence
    """
    # Load graph
    edges, num_vertices = load_graph_from_csv(filename)
    
    # Create Bellman-Ford instance
    bellman_ford = BellmanFordAlgorithm(edges, num_vertices)
    
    # Find shortest paths
    distances, predecessors, has_negative_cycle = bellman_ford.shortest_path(source_vertex)
    
    return distances, predecessors, has_negative_cycle


if __name__ == "__main__":
    # Example usage
    import time
    
    filename = "dijkstra_bellman_large_dataset.csv"
    source = 0
    
    print("=" * 60)
    print("BELLMAN-FORD ALGORITHM - Shortest Path Problem")
    print("=" * 60)
    print(f"\nDataset: {filename}")
    print(f"Source Vertex: {source}")
    
    # Time the algorithm
    start_time = time.time()
    distances, predecessors, has_negative_cycle = run_bellman_ford(filename, source)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    print(f"\nExecution Time: {execution_time:.4f} ms")
    print(f"Negative Cycle Detected: {has_negative_cycle}")
    print(f"Total vertices processed: {len([d for d in distances if d != sys.maxsize])}")
    
    # Show sample results (first 10 reachable vertices)
    print("\nSample Shortest Distances:")
    print("-" * 40)
    count = 0
    for i, dist in enumerate(distances):
        if dist != sys.maxsize and count < 10:
            print(f"Vertex {i}: Distance = {dist}")
            count += 1
    
    print("\n" + "=" * 60)
