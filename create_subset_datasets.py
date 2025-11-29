"""
Create subset datasets of various sizes for performance testing
"""
import csv

def create_subset(source_file, output_file, max_edges):
    """
    Extract a subset of edges from the source dataset
    """
    edges = []
    
    # Read all edges from source file
    with open(source_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            edges.append(row)
            if len(edges) >= max_edges:
                break
    
    # Write subset to output file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if edges:
            fieldnames = edges[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(edges)
    
    # Count unique vertices
    vertices = set()
    for edge in edges:
        vertices.add(edge['source'])
        vertices.add(edge['target'])
    
    print(f"Created {output_file}: {len(edges)} edges, {len(vertices)} vertices")
    return len(edges), len(vertices)

def main():
    # Small Datasets - extract from small dataset
    print("Creating Small Datasets:")
    print("-" * 50)
    create_subset('dijkstra_bellman_small_dataset.csv', 
                  'dijkstra_bellman_250_dataset.csv', 250)
    create_subset('dijkstra_bellman_small_dataset.csv', 
                  'dijkstra_bellman_500_dataset.csv', 500)
    create_subset('dijkstra_bellman_small_dataset.csv', 
                  'dijkstra_bellman_750_dataset.csv', 750)
    create_subset('dijkstra_bellman_small_dataset.csv', 
                  'dijkstra_bellman_1000_dataset.csv', 1000)
    
    print("\nCreating Large Datasets:")
    print("-" * 50)
    # Large Datasets - extract from medium and large datasets
    create_subset('dijkstra_bellman_medium_dataset.csv', 
                  'dijkstra_bellman_5000_dataset.csv', 5000)
    create_subset('dijkstra_bellman_medium_dataset.csv', 
                  'dijkstra_bellman_10000_dataset.csv', 10000)
    create_subset('dijkstra_bellman_large_dataset.csv', 
                  'dijkstra_bellman_15000_dataset.csv', 15000)
    create_subset('dijkstra_bellman_large_dataset.csv', 
                  'dijkstra_bellman_20000_dataset.csv', 20000)
    
    print("\n✓ All subset datasets created successfully!")

if __name__ == "__main__":
    main()
