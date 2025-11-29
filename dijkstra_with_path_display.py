"""
Enhanced Dijkstra's Algorithm with Human-Readable Path Display
Shows actual street names and metadata in the output
"""

import sys
import csv
import time
import os
from collections import defaultdict


class EnhancedDijkstra:
    """
    Dijkstra's Algorithm with metadata support for displaying street names
    """
    
    def __init__(self, graph, num_vertices, edge_metadata):
        """
        Initialize Enhanced Dijkstra's Algorithm
        
        Args:
            graph: Dictionary representing adjacency list
            num_vertices: Total number of vertices
            edge_metadata: Dictionary mapping (source, target) to metadata
        """
        self.graph = graph
        self.num_vertices = num_vertices
        self.edge_metadata = edge_metadata
    
    def find_min_distance_vertex(self, distances, visited):
        """Find the unvisited vertex with minimum distance"""
        min_distance = sys.maxsize
        min_vertex = -1
        
        for vertex in range(self.num_vertices):
            if vertex not in visited and distances[vertex] < min_distance:
                min_distance = distances[vertex]
                min_vertex = vertex
        
        return min_vertex
    
    def shortest_path(self, source):
        """
        Calculate shortest paths from source to all vertices
        
        Returns:
            distances: Array of shortest distances
            predecessors: Array to reconstruct paths
        """
        distances = [sys.maxsize] * self.num_vertices
        distances[source] = 0
        
        predecessors = [-1] * self.num_vertices
        visited = set()
        
        for _ in range(self.num_vertices):
            current = self.find_min_distance_vertex(distances, visited)
            
            if current == -1:
                break
            
            visited.add(current)
            
            if current in self.graph:
                for neighbor, weight in self.graph[current]:
                    if neighbor not in visited:
                        new_distance = distances[current] + weight
                        
                        if new_distance < distances[neighbor]:
                            distances[neighbor] = new_distance
                            predecessors[neighbor] = current
        
        return distances, predecessors
    
    def get_path(self, predecessors, source, target):
        """
        Reconstruct path from source to target
        
        Returns:
            List of vertices in the path
        """
        if predecessors[target] == -1 and target != source:
            return None
        
        path = []
        current = target
        
        while current != -1:
            path.append(current)
            current = predecessors[current]
        
        path.reverse()
        return path
    
    def display_path_with_streets(self, path):
        """
        Display path with actual street names and metadata
        """
        if not path or len(path) < 2:
            print("  No valid path to display")
            return
        
        print(f"\n{'='*80}")
        print(f"🗺️  ROUTE DETAILS: {len(path)} vertices, {len(path)-1} segments")
        print(f"{'='*80}\n")
        
        total_distance = 0
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            key = (u, v)
            
            if key in self.edge_metadata:
                meta = self.edge_metadata[key]
                segment_num = i + 1
                
                print(f"Step {segment_num}: Vertex {u} → Vertex {v}")
                print(f"  📍 Street: {meta['street_name']}")
                print(f"  🛣️  Type: {meta['highway_type']}")
                print(f"  📏 Distance: {meta['length_meters']} meters")
                print(f"  ↔️  Direction: {'One-way' if meta['oneway'] == 'True' else 'Two-way'}")
                print(f"  🚦 Speed Limit: {meta['maxspeed']}")
                
                # Calculate estimated time if speed available
                if meta['maxspeed'] != 'N/A' and 'mph' in meta['maxspeed']:
                    try:
                        speed_mph = float(meta['maxspeed'].replace('mph', '').strip())
                        speed_mps = speed_mph * 0.44704  # Convert mph to m/s
                        time_seconds = float(meta['length_meters']) / speed_mps
                        print(f"  ⏱️  Est. Time: {time_seconds:.1f} seconds ({time_seconds/60:.2f} min)")
                    except:
                        pass
                
                print()
                total_distance += float(meta['length_meters'])
            else:
                print(f"Step {i+1}: Vertex {u} → Vertex {v} (metadata not available)")
                print()
        
        print(f"{'='*80}")
        print(f"📊 TOTAL DISTANCE: {total_distance:.2f} meters ({total_distance/1000:.2f} km)")
        print(f"{'='*80}\n")


def load_enhanced_dataset(filename):
    """
    Load dataset with metadata
    
    Returns:
        graph: Adjacency list
        num_vertices: Total vertices
        edge_metadata: Metadata dictionary
    """
    graph = defaultdict(list)
    edge_metadata = {}
    vertices = set()
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            source = int(row['source'])
            target = int(row['target'])
            weight = int(row['weight'])
            
            graph[source].append((target, weight))
            vertices.add(source)
            vertices.add(target)
            
            # Store metadata
            edge_metadata[(source, target)] = {
                'street_name': row.get('street_name', 'Unknown'),
                'highway_type': row.get('highway_type', 'unknown'),
                'oneway': row.get('oneway', 'True'),
                'maxspeed': row.get('maxspeed', 'N/A'),
                'length_meters': row.get('length_meters', row['weight'])
            }
    
    num_vertices = len(vertices)
    return graph, num_vertices, edge_metadata


def main():
    """
    Main demonstration with enhanced path display
    """
    print("=" * 80)
    print("ENHANCED DIJKSTRA'S ALGORITHM - WITH STREET NAME DISPLAY")
    print("=" * 80)
    
    # Load dataset with fallbacks to available subset files
    candidates = [
        "dijkstra_bellman_small_dataset.csv",
        "dijkstra_bellman_1000_dataset.csv",
        "dijkstra_bellman_750_dataset.csv",
        "dijkstra_bellman_500_dataset.csv",
        "dijkstra_bellman_250_dataset.csv",
    ]
    filename = None
    for f in candidates:
        if os.path.exists(f):
            filename = f
            break
    if filename is None:
        print("ERROR: No suitable dataset found. Please create datasets via 'create_nyc_datasets.py' or 'create_subset_datasets.py'.")
        return 1
    print(f"\nLoading dataset: {filename}...")
    
    try:
        graph, num_vertices, edge_metadata = load_enhanced_dataset(filename)
    except FileNotFoundError:
        print(f"ERROR: Dataset file '{filename}' not found.")
        return 1
    
    print(f"✓ Loaded {len(edge_metadata)} edges")
    print(f"✓ Total vertices: {num_vertices}")
    
    # Run Dijkstra
    source = 0
    print(f"\n{'='*80}")
    print(f"Running Dijkstra's Algorithm from source vertex {source}...")
    print(f"{'='*80}\n")
    
    dijkstra = EnhancedDijkstra(graph, num_vertices, edge_metadata)
    
    start_time = time.time()
    distances, predecessors = dijkstra.shortest_path(source)
    end_time = time.time()
    
    execution_time = (end_time - start_time) * 1000
    
    print(f"✓ Execution completed in {execution_time:.4f} ms\n")
    
    # Find reachable vertices
    reachable = [v for v in range(num_vertices) if distances[v] != sys.maxsize]
    print(f"✓ Found paths to {len(reachable)} vertices\n")
    
    # Display sample shortest paths with street names
    print("=" * 80)
    print("SAMPLE SHORTEST PATHS WITH STREET NAMES")
    print("=" * 80)
    
    # Show paths to first few reachable vertices
    sample_targets = [v for v in reachable if v != source][:5]
    
    for target in sample_targets:
        print(f"\n{'─'*80}")
        print(f"📍 PATH FROM VERTEX {source} TO VERTEX {target}")
        print(f"   Shortest Distance: {distances[target]} meters")
        print(f"{'─'*80}")
        
        path = dijkstra.get_path(predecessors, source, target)
        
        if path:
            dijkstra.display_path_with_streets(path)
    
    # Display street type statistics
    print("\n" + "=" * 80)
    print("📊 STREET TYPE ANALYSIS IN SHORTEST PATHS")
    print("=" * 80)
    
    street_types = defaultdict(int)
    for (u, v), meta in edge_metadata.items():
        street_types[meta['highway_type']] += 1
    
    print("\nRoad type distribution in dataset:")
    for road_type, count in sorted(street_types.items(), key=lambda x: x[1], reverse=True):
        print(f"  {road_type:20s}: {count:4d} segments")
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\n💡 The metadata enhances the output by showing:")
    print("  ✓ Real street names instead of just vertex numbers")
    print("  ✓ Road types (motorway, residential, etc.)")
    print("  ✓ Direction constraints (one-way vs two-way)")
    print("  ✓ Speed limits for travel time estimates")
    print("  ✓ Precise distances in meters")


if __name__ == "__main__":
    code = main()
    if isinstance(code, int):
        sys.exit(code)
