"""
NYC Street Dataset Converter
Creates small, medium, and large graph datasets from new_york_streets.csv
Converts street network data into graph format suitable for Dijkstra and Bellman-Ford algorithms
"""

import csv
import random


def parse_linestring(geometry):
    """
    Extract start and end coordinates from LINESTRING geometry
    
    Args:
        geometry: LINESTRING string format
        
    Returns:
        tuple: (start_point, end_point) as coordinate strings
    """
    if not geometry or geometry == '':
        return None, None
    
    try:
        # Remove "LINESTRING (" and ")"
        coords_str = geometry.replace('LINESTRING (', '').replace(')', '')
        
        # Split by comma to get individual coordinate pairs
        coord_pairs = coords_str.split(', ')
        
        if len(coord_pairs) < 2:
            return None, None
        
        # Get first and last coordinate pairs
        start = coord_pairs[0].strip()
        end = coord_pairs[-1].strip()
        
        return start, end
    except:
        return None, None


def create_graph_dataset_from_nyc(input_file, output_file, num_rows, start_row=1):
    """
    Create a graph dataset from NYC streets data with enhanced metadata
    
    Args:
        input_file: Source NYC streets CSV file
        output_file: Output graph CSV file
        num_rows: Number of rows to extract
        start_row: Starting row (to get different sections)
    """
    edges_created = 0
    node_mapping = {}  # Map coordinate strings to integer node IDs
    next_node_id = 0
    edges = []
    
    print(f"\nProcessing {output_file}...")
    print(f"Target: {num_rows} edges")
    
    # Read NYC streets data
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        
        # Select rows (skip header is already done by DictReader)
        # Use a range to get consecutive street segments for connectivity
        selected_rows = rows[start_row:start_row + num_rows + 5000]  # Extra buffer for filtering
        
        for row in selected_rows:
            if edges_created >= num_rows:
                break
            
            # Get geometry and length
            geometry = row.get('geometry', '')
            length_str = row.get('length', '')
            
            if not geometry or not length_str:
                continue
            
            try:
                length = float(length_str)
                if length <= 0:
                    continue
            except:
                continue
            
            # Parse start and end points
            start_coord, end_coord = parse_linestring(geometry)
            
            if not start_coord or not end_coord:
                continue
            
            # Map coordinates to node IDs
            if start_coord not in node_mapping:
                node_mapping[start_coord] = next_node_id
                next_node_id += 1
            
            if end_coord not in node_mapping:
                node_mapping[end_coord] = next_node_id
                next_node_id += 1
            
            source = node_mapping[start_coord]
            target = node_mapping[end_coord]
            
            # Round weight to integer for simplicity
            weight = int(round(length))
            if weight < 1:
                weight = 1
            
            # Extract metadata
            street_name = row.get('name', 'Unnamed Street').strip()
            if not street_name or street_name == '':
                street_name = 'Unnamed Street'
            
            highway_type = row.get('highway', 'unclassified').strip()
            if not highway_type or highway_type == '':
                highway_type = 'unclassified'
            
            oneway = row.get('oneway', 'True').strip()
            
            maxspeed = row.get('maxspeed', 'N/A').strip()
            if not maxspeed or maxspeed == '':
                maxspeed = 'N/A'
            
            length_meters = f"{length:.2f}"
            
            edges.append((source, target, weight, street_name, highway_type, oneway, maxspeed, length_meters))
            edges_created += 1
            
            # Check if it's a two-way street (oneway = False)
            if oneway.lower() == 'false':
                # Add reverse edge for two-way streets
                if edges_created < num_rows:
                    edges.append((target, source, weight, street_name, highway_type, oneway, maxspeed, length_meters))
                    edges_created += 1
    
    # Write to output file
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['source', 'target', 'weight', 'street_name', 'highway_type', 'oneway', 'maxspeed', 'length_meters'])
        
        for edge in edges:
            writer.writerow(edge)
    
    print(f"✓ Created: {output_file}")
    print(f"  - Edges: {len(edges)}")
    print(f"  - Unique Nodes: {len(node_mapping)}")
    print(f"  - Weight Range: [{min(e[2] for e in edges)}, {max(e[2] for e in edges)}]")


def verify_dataset(filename):
    """
    Verify the created dataset
    
    Args:
        filename: CSV file to verify
    """
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
        if len(rows) > 0:
            # Get unique nodes
            nodes = set()
            weights = []
            street_names = set()
            highway_types = set()
            
            for row in rows:
                nodes.add(int(row['source']))
                nodes.add(int(row['target']))
                weights.append(int(row['weight']))
                street_names.add(row.get('street_name', 'N/A'))
                highway_types.add(row.get('highway_type', 'N/A'))
            
            print(f"\n✓ Verification: {filename}")
            print(f"  - Total Edges: {len(rows)}")
            print(f"  - Unique Vertices: {len(nodes)}")
            print(f"  - Min Node ID: {min(nodes)}")
            print(f"  - Max Node ID: {max(nodes)}")
            print(f"  - Avg Weight: {sum(weights) / len(weights):.2f} meters")
            print(f"  - Unique Streets: {len(street_names)}")
            print(f"  - Highway Types: {len(highway_types)}")


def main():
    """
    Main function to create all three datasets
    """
    print("=" * 70)
    print("NYC STREET NETWORK DATASET CREATOR")
    print("=" * 70)
    print("\nConverting new_york_streets.csv to graph format...")
    print("Creating three dataset sizes: Small, Medium, Large")
    
    input_file = "new_york_streets.csv"
    
    # Create small dataset (1000 edges)
    create_graph_dataset_from_nyc(
        input_file=input_file,
        output_file="dijkstra_bellman_small_dataset.csv",
        num_rows=1000,
        start_row=0
    )
    
    # Create medium dataset (10,000 edges)
    create_graph_dataset_from_nyc(
        input_file=input_file,
        output_file="dijkstra_bellman_medium_dataset.csv",
        num_rows=10000,
        start_row=5000
    )
    
    # Create large dataset (50,000 edges)
    create_graph_dataset_from_nyc(
        input_file=input_file,
        output_file="dijkstra_bellman_large_dataset.csv",
        num_rows=50000,
        start_row=20000
    )
    
    print("\n" + "=" * 70)
    print("DATASET VERIFICATION")
    print("=" * 70)
    
    # Verify all datasets
    verify_dataset("dijkstra_bellman_small_dataset.csv")
    verify_dataset("dijkstra_bellman_medium_dataset.csv")
    verify_dataset("dijkstra_bellman_large_dataset.csv")
    
    print("\n" + "=" * 70)
    print("ALL DATASETS CREATED SUCCESSFULLY!")
    print("=" * 70)
    print("\nDatasets ready for testing:")
    print("  1. dijkstra_bellman_small_dataset.csv   (~1,000 edges)")
    print("  2. dijkstra_bellman_medium_dataset.csv  (~10,000 edges)")
    print("  3. dijkstra_bellman_large_dataset.csv   (~50,000 edges)")
    print("\nThese datasets are extracted from real NYC street network data.")
    print("Edge weights represent actual street lengths in meters (rounded to integers).")
    print("\nEnhanced with metadata columns:")
    print("  - street_name: Human-readable street names")
    print("  - highway_type: Road classification (motorway, residential, etc.)")
    print("  - oneway: Direction information (True/False)")
    print("  - maxspeed: Speed limits")
    print("  - length_meters: Precise length in meters")
    print("\nYou can now run:")
    print("  python performance_testing.py")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Create all datasets
    main()
