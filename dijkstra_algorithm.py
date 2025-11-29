"""
Dijkstra's Algorithm Implementation (Greedy Approach)
CS412 - Algorithm Analysis & Design
Implemented from scratch without using any graph libraries
"""

import sys


class DijkstraAlgorithm:
    """
    Dijkstra's Algorithm for finding shortest paths from a source vertex
    to all other vertices in a weighted directed graph.
    
    Time Complexity: O((V + E) log V) with min-heap, O(V^2) with array
    Space Complexity: O(V)
    
    This implementation uses a simple array-based approach for clarity.
    """
    
    def __init__(self, graph, num_vertices):
        """
        Initialize Dijkstra's Algorithm
        
        Args:
            graph: Dictionary representing adjacency list {vertex: [(neighbor, weight), ...]}
            num_vertices: Total number of vertices in the graph
        """
        self.graph = graph
        self.num_vertices = num_vertices
    
    def find_min_distance_vertex(self, distances, visited):
        """
        Find the unvisited vertex with minimum distance
        
        Args:
            distances: Array of current shortest distances
            visited: Set of visited vertices
            
        Returns:
            Vertex with minimum distance that hasn't been visited
        """
        min_distance = sys.maxsize
        min_vertex = -1
        
        for vertex in range(self.num_vertices):
            if vertex not in visited and distances[vertex] < min_distance:
                min_distance = distances[vertex]
                min_vertex = vertex
        
        return min_vertex
    
    def shortest_path(self, source):
        """
        Calculate shortest paths from source to all other vertices
        
        Args:
            source: Starting vertex
            
        Returns:
            distances: Array of shortest distances from source to each vertex
            predecessors: Array to reconstruct shortest paths
        """
        # Initialize distances to infinity
        distances = [sys.maxsize] * self.num_vertices
        distances[source] = 0
        
        # Track visited vertices
        visited = set()
        
        # Store predecessors for path reconstruction
        predecessors = [-1] * self.num_vertices
        
        # Process all vertices
        for _ in range(self.num_vertices):
            # Find vertex with minimum distance among unvisited vertices
            current = self.find_min_distance_vertex(distances, visited)
            
            # If no reachable vertex found, break
            if current == -1:
                break
            
            # Mark current vertex as visited
            visited.add(current)
            
            # Update distances to neighbors
            if current in self.graph:
                for neighbor, weight in self.graph[current]:
                    # Relaxation step: check if path through current is shorter
                    if neighbor not in visited:
                        new_distance = distances[current] + weight
                        if new_distance < distances[neighbor]:
                            distances[neighbor] = new_distance
                            predecessors[neighbor] = current
        
        return distances, predecessors
    
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
        graph: Adjacency list representation
        num_vertices: Total number of unique vertices
    """
    graph = {}
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
                
                # Add edge to adjacency list
                if source not in graph:
                    graph[source] = []
                graph[source].append((target, weight))
    
    # Get maximum vertex number + 1 for array sizing
    num_vertices = max(vertices) + 1 if vertices else 0
    
    return graph, num_vertices


def run_dijkstra(filename, source_vertex=0):
    """
    Main function to run Dijkstra's algorithm on a graph from CSV
    
    Args:
        filename: Path to CSV file
        source_vertex: Starting vertex (default: 0)
        
    Returns:
        distances: Shortest distances from source
        predecessors: Predecessor array for path reconstruction
    """
    # Load graph
    graph, num_vertices = load_graph_from_csv(filename)
    
    # Create Dijkstra instance
    dijkstra = DijkstraAlgorithm(graph, num_vertices)
    
    # Find shortest paths
    distances, predecessors = dijkstra.shortest_path(source_vertex)
    
    return distances, predecessors


if __name__ == "__main__":
    # Example usage
    import time
    
    filename = "dijkstra_bellman_large_dataset.csv"
    source = 0
    
    print("=" * 60)
    print("DIJKSTRA'S ALGORITHM - Shortest Path Problem")
    print("=" * 60)
    print(f"\nDataset: {filename}")
    print(f"Source Vertex: {source}")
    
    # Time the algorithm
    start_time = time.time()
    distances, predecessors = run_dijkstra(filename, source)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
    
    print(f"\nExecution Time: {execution_time:.4f} ms")
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
