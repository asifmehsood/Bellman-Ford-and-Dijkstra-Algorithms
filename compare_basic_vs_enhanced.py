"""
Comparison: Basic vs Enhanced Output
Shows the difference between output with and without metadata
"""

import sys
import csv
from collections import defaultdict


def load_dataset_basic(filename):
    """Load only basic graph data (source, target, weight)"""
    graph = defaultdict(list)
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
    
    return graph, len(vertices)


def load_dataset_enhanced(filename):
    """Load graph data WITH metadata"""
    graph = defaultdict(list)
    vertices = set()
    edge_metadata = {}
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            source = int(row['source'])
            target = int(row['target'])
            weight = int(row['weight'])
            
            graph[source].append((target, weight))
            vertices.add(source)
            vertices.add(target)
            
            edge_metadata[(source, target)] = {
                'street_name': row.get('street_name', 'Unknown'),
                'highway_type': row.get('highway_type', 'unknown'),
                'oneway': row.get('oneway', 'True'),
                'maxspeed': row.get('maxspeed', 'N/A'),
                'length_meters': row.get('length_meters', row['weight'])
            }
    
    return graph, len(vertices), edge_metadata


def basic_dijkstra(graph, num_vertices, source):
    """Basic Dijkstra without metadata"""
    distances = [sys.maxsize] * num_vertices
    distances[source] = 0
    predecessors = [-1] * num_vertices
    visited = set()
    
    for _ in range(num_vertices):
        current = -1
        min_dist = sys.maxsize
        
        for v in range(num_vertices):
            if v not in visited and distances[v] < min_dist:
                min_dist = distances[v]
                current = v
        
        if current == -1:
            break
        
        visited.add(current)
        
        if current in graph:
            for neighbor, weight in graph[current]:
                if neighbor not in visited:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = current
    
    return distances, predecessors


def get_path(predecessors, source, target):
    """Reconstruct path"""
    if predecessors[target] == -1 and target != source:
        return None
    
    path = []
    current = target
    while current != -1:
        path.append(current)
        current = predecessors[current]
    path.reverse()
    return path


def display_basic_output(path, distances, target):
    """BEFORE: Basic output without metadata"""
    print("\n" + "─" * 70)
    print(f"Path to Vertex {target}: Distance = {distances[target]} units")
    print("─" * 70)
    
    if path:
        path_str = " → ".join(map(str, path))
        print(f"Route: {path_str}")
        print(f"Steps: {len(path) - 1}")
    print()


def display_enhanced_output(path, distances, target, edge_metadata):
    """AFTER: Enhanced output WITH metadata"""
    print("\n" + "─" * 70)
    print(f"📍 PATH TO VERTEX {target}: Distance = {distances[target]} meters")
    print("─" * 70)
    
    if path and len(path) > 1:
        total_distance = 0
        total_time = 0
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            key = (u, v)
            
            if key in edge_metadata:
                meta = edge_metadata[key]
                print(f"\nStep {i+1}: Vertex {u} → {v}")
                print(f"  🛣️  {meta['street_name']} ({meta['highway_type']})")
                print(f"  📏 {meta['length_meters']} meters")
                print(f"  🚦 {meta['maxspeed']}", end="")
                
                # Calculate time if speed available
                if meta['maxspeed'] != 'N/A' and 'mph' in meta['maxspeed']:
                    try:
                        speed_mph = float(meta['maxspeed'].replace('mph', '').strip())
                        speed_mps = speed_mph * 0.44704
                        time_sec = float(meta['length_meters']) / speed_mps
                        print(f" → {time_sec:.0f}s")
                        total_time += time_sec
                    except:
                        print()
                else:
                    print()
                
                total_distance += float(meta['length_meters'])
        
        print(f"\n{'─'*70}")
        print(f"Total: {total_distance:.2f}m", end="")
        if total_time > 0:
            print(f" | Est. Time: {total_time/60:.1f} minutes")
        else:
            print()
    print()


def main():
    """
    Main comparison demonstration
    """
    filename = "dijkstra_bellman_medium_dataset.csv"
    source = 0
    
    print("=" * 80)
    print("COMPARISON: BASIC OUTPUT vs ENHANCED OUTPUT WITH METADATA")
    print("=" * 80)
    print(f"\nDataset: {filename}")
    print(f"Source Vertex: {source}")
    
    # Load data
    print("\nLoading data...")
    graph_basic, num_vertices_basic = load_dataset_basic(filename)
    graph_enhanced, num_vertices_enhanced, edge_metadata = load_dataset_enhanced(filename)
    
    # Run Dijkstra
    print("Running Dijkstra's algorithm...")
    distances, predecessors = basic_dijkstra(graph_basic, num_vertices_basic, source)
    
    # Find some sample paths
    reachable = [v for v in range(num_vertices_basic) if distances[v] != sys.maxsize and v != source]
    sample_targets = reachable[:3]  # First 3 reachable vertices
    
    # Display comparison
    for target in sample_targets:
        path = get_path(predecessors, source, target)
        
        print("\n" + "=" * 80)
        print(f"EXAMPLE: PATH TO VERTEX {target}")
        print("=" * 80)
        
        # BEFORE: Basic output
        print("\n🔴 BEFORE (Without Metadata):")
        print("─" * 80)
        display_basic_output(path, distances, target)
        
        # AFTER: Enhanced output
        print("\n🟢 AFTER (With Metadata):")
        print("─" * 80)
        display_enhanced_output(path, distances, target, edge_metadata)
    
    # Show use cases
    print("\n" + "=" * 80)
    print("💡 METADATA USE CASES")
    print("=" * 80)
    
    print("\n1️⃣  NAVIGATION SYSTEMS:")
    print("   Turn-by-turn directions with actual street names")
    print("   Example: 'Take Flatbush Avenue for 200m, then turn onto Bedford Ave'")
    
    print("\n2️⃣  ROUTE OPTIMIZATION:")
    print("   Filter routes by road type (highways only, avoid residential)")
    print("   Example: Find fastest route using major roads only")
    
    print("\n3️⃣  TRAVEL TIME ESTIMATION:")
    print("   Calculate realistic travel times using speed limits")
    print("   Example: 200m at 25mph = 18 seconds")
    
    print("\n4️⃣  TRAFFIC PLANNING:")
    print("   Analyze one-way vs two-way street patterns")
    print("   Example: Count one-way streets in shortest paths")
    
    print("\n5️⃣  ACADEMIC PRESENTATIONS:")
    print("   Show real-world examples with recognizable street names")
    print("   Example: 'Shortest path uses 3 residential streets and 1 highway'")
    
    print("\n6️⃣  ROUTE CONSTRAINTS:")
    print("   Apply rules like 'avoid highways' or 'prefer high-speed roads'")
    print("   Example: Find alternative route avoiding motorways")
    
    # Statistics
    print("\n" + "=" * 80)
    print("📊 DATASET STATISTICS")
    print("=" * 80)
    
    street_types = defaultdict(int)
    speeds = defaultdict(int)
    oneway_count = 0
    
    for (u, v), meta in edge_metadata.items():
        street_types[meta['highway_type']] += 1
        speeds[meta['maxspeed']] += 1
        if meta['oneway'] == 'True':
            oneway_count += 1
    
    print(f"\nTotal edges analyzed: {len(edge_metadata)}")
    print(f"Unique street names: {len(set(m['street_name'] for m in edge_metadata.values()))}")
    print(f"Road types: {len(street_types)}")
    print(f"One-way streets: {oneway_count} ({oneway_count/len(edge_metadata)*100:.1f}%)")
    
    print("\nTop 5 road types:")
    for i, (rtype, count) in enumerate(sorted(street_types.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        print(f"  {i}. {rtype}: {count} segments")
    
    print("\n" + "=" * 80)
    print("COMPARISON COMPLETE")
    print("=" * 80)
    
    print("\n✅ Key Takeaway:")
    print("   Metadata transforms abstract vertex numbers into meaningful,")
    print("   human-readable navigation instructions with real street names,")
    print("   road types, and travel time estimates!")


if __name__ == "__main__":
    main()
