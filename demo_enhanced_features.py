"""
Enhanced Dataset Features Demonstration
Shows how to use the metadata columns for advanced analysis
"""

import csv
from collections import defaultdict


def load_enhanced_dataset(filename):
    """
    Load dataset with metadata
    
    Returns:
        edges: List of edge dictionaries with all metadata
        graph: Adjacency list for pathfinding
    """
    edges = []
    graph = defaultdict(list)
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edge = {
                'source': int(row['source']),
                'target': int(row['target']),
                'weight': int(row['weight']),
                'street_name': row['street_name'],
                'highway_type': row['highway_type'],
                'oneway': row['oneway'],
                'maxspeed': row['maxspeed'],
                'length_meters': float(row['length_meters'])
            }
            edges.append(edge)
            graph[edge['source']].append((edge['target'], edge['weight'], edge['street_name']))
    
    return edges, graph


def analyze_dataset_metadata(edges):
    """
    Analyze and display metadata statistics
    """
    street_names = set()
    highway_types = defaultdict(int)
    oneway_count = 0
    twoway_count = 0
    speed_limits = defaultdict(int)
    
    for edge in edges:
        street_names.add(edge['street_name'])
        highway_types[edge['highway_type']] += 1
        
        if edge['oneway'].lower() == 'true':
            oneway_count += 1
        else:
            twoway_count += 1
        
        speed_limits[edge['maxspeed']] += 1
    
    print("=" * 80)
    print("DATASET METADATA ANALYSIS")
    print("=" * 80)
    
    print(f"\n📊 Overall Statistics:")
    print(f"  Total Edges: {len(edges)}")
    print(f"  Unique Street Names: {len(street_names)}")
    print(f"  One-Way Streets: {oneway_count} ({oneway_count/len(edges)*100:.1f}%)")
    print(f"  Two-Way Streets: {twoway_count} ({twoway_count/len(edges)*100:.1f}%)")
    
    print(f"\n🛣️  Highway Type Distribution:")
    sorted_types = sorted(highway_types.items(), key=lambda x: x[1], reverse=True)
    for htype, count in sorted_types[:10]:
        print(f"  {htype:20s}: {count:5d} edges ({count/len(edges)*100:.1f}%)")
    
    print(f"\n🚦 Speed Limit Distribution:")
    sorted_speeds = sorted(speed_limits.items(), key=lambda x: x[1], reverse=True)
    for speed, count in sorted_speeds[:8]:
        print(f"  {speed:15s}: {count:5d} edges ({count/len(edges)*100:.1f}%)")
    
    print(f"\n🏙️  Sample Street Names (first 15 unique):")
    sample_streets = sorted(list(street_names))[:15]
    for i, street in enumerate(sample_streets, 1):
        print(f"  {i:2d}. {street}")


def find_path_with_names(graph, edges, source, target):
    """
    Find shortest path and display with street names
    """
    # Simple BFS to find a path (for demonstration)
    from collections import deque
    
    queue = deque([(source, [source])])
    visited = {source}
    
    while queue:
        node, path = queue.popleft()
        
        if node == target:
            # Found path, now get street names
            print(f"\n🗺️  Path from Vertex {source} to Vertex {target}:")
            print(f"{'='*60}")
            total_distance = 0
            
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                
                # Find edge details
                edge_info = None
                for edge in edges:
                    if edge['source'] == u and edge['target'] == v:
                        edge_info = edge
                        break
                
                if edge_info:
                    print(f"  Step {i+1}: Vertex {u} → Vertex {v}")
                    print(f"    📍 Street: {edge_info['street_name']}")
                    print(f"    🛣️  Type: {edge_info['highway_type']}")
                    print(f"    📏 Distance: {edge_info['length_meters']:.2f} meters")
                    print(f"    🚦 Speed: {edge_info['maxspeed']}")
                    print()
                    total_distance += edge_info['length_meters']
            
            print(f"{'='*60}")
            print(f"  Total Distance: {total_distance:.2f} meters")
            print(f"  Total Steps: {len(path) - 1}")
            return
        
        for neighbor, weight, street in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    print(f"❌ No path found from {source} to {target}")


def filter_by_highway_type(edges, highway_type):
    """
    Filter edges by highway type
    """
    filtered = [e for e in edges if e['highway_type'] == highway_type]
    return filtered


def calculate_travel_time(edges):
    """
    Calculate travel time based on speed limits
    """
    print("\n⏱️  Travel Time Analysis:")
    print("=" * 80)
    
    # Parse speed limits and calculate times
    for i, edge in enumerate(edges[:10]):
        speed_str = edge['maxspeed']
        distance = edge['length_meters']
        
        if speed_str != 'N/A' and 'mph' in speed_str:
            try:
                speed_mph = float(speed_str.replace('mph', '').strip())
                speed_mps = speed_mph * 0.44704  # mph to m/s
                time_seconds = distance / speed_mps
                
                print(f"Edge {i+1}: {edge['street_name']}")
                print(f"  Distance: {distance:.2f}m, Speed: {speed_mph} mph")
                print(f"  Estimated Time: {time_seconds:.2f} seconds ({time_seconds/60:.2f} minutes)")
                print()
            except:
                pass


def main():
    """
    Main demonstration function
    """
    print("\n" + "=" * 80)
    print("ENHANCED NYC STREET DATASET FEATURES DEMONSTRATION")
    print("=" * 80)
    
    # Use medium dataset for demonstration
    filename = "dijkstra_bellman_medium_dataset.csv"
    
    print(f"\nLoading dataset: {filename}...")
    edges, graph = load_enhanced_dataset(filename)
    print(f"✓ Loaded {len(edges)} edges")
    
    # Analyze metadata
    analyze_dataset_metadata(edges)
    
    # Show sample path with street names
    print("\n" + "=" * 80)
    print("SAMPLE PATH WITH STREET NAMES")
    print("=" * 80)
    find_path_with_names(graph, edges, 0, 5)
    
    # Filter by highway type
    print("\n" + "=" * 80)
    print("FILTERING BY HIGHWAY TYPE")
    print("=" * 80)
    motorways = filter_by_highway_type(edges, 'motorway')
    print(f"\nMotorways found: {len(motorways)}")
    print("\nSample motorway segments:")
    for i, edge in enumerate(motorways[:5], 1):
        print(f"  {i}. {edge['street_name']} - {edge['length_meters']:.2f}m @ {edge['maxspeed']}")
    
    # Calculate travel times
    calculate_travel_time(edges)
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nThese enhanced features can be used for:")
    print("  ✓ Human-readable path directions")
    print("  ✓ Filtering by road type (highways, residential, etc.)")
    print("  ✓ Travel time optimization (distance + speed)")
    print("  ✓ Academic visualizations with real street names")
    print("  ✓ Advanced routing constraints (avoid highways, etc.)")


if __name__ == "__main__":
    main()
