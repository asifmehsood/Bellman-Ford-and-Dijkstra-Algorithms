"""
Dataset Generator for Shortest Path Algorithm Testing
CS412 - Algorithm Analysis & Design

Generates small, medium, and large weighted directed graphs for testing
"""

import random
import csv


def generate_graph_dataset(num_vertices, num_edges, min_weight=1, max_weight=50, filename="graph_dataset.csv"):
    """
    Generate a random weighted directed graph and save to CSV
    
    Args:
        num_vertices: Number of vertices in the graph
        num_edges: Number of edges to generate
        min_weight: Minimum edge weight
        max_weight: Maximum edge weight
        filename: Output CSV filename
    """
    edges = set()
    
    # Generate random edges
    while len(edges) < num_edges:
        source = random.randint(0, num_vertices - 1)
        target = random.randint(0, num_vertices - 1)
        
        # Avoid self-loops
        if source != target:
            edges.add((source, target))
    
    # Write to CSV file
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['source', 'target', 'weight'])
        
        for source, target in edges:
            weight = random.randint(min_weight, max_weight)
            writer.writerow([source, target, weight])
    
    print(f"Generated {filename}:")
    print(f"  - Vertices: {num_vertices}")
    print(f"  - Edges: {num_edges}")
    print(f"  - Weight range: [{min_weight}, {max_weight}]")
    print()


def generate_all_datasets():
    """
    Generate small, medium, and large datasets for comprehensive testing
    """
    print("=" * 60)
    print("DATASET GENERATOR")
    print("=" * 60)
    print()
    
    # Small dataset: ~50 vertices, ~200 edges
    print("Generating SMALL dataset...")
    generate_graph_dataset(
        num_vertices=50,
        num_edges=200,
        min_weight=1,
        max_weight=50,
        filename="dijkstra_bellman_small_dataset.csv"
    )
    
    # Medium dataset: ~500 vertices, ~2000 edges
    print("Generating MEDIUM dataset...")
    generate_graph_dataset(
        num_vertices=500,
        num_edges=2000,
        min_weight=1,
        max_weight=50,
        filename="dijkstra_bellman_medium_dataset.csv"
    )
    
    print("=" * 60)
    print("All datasets generated successfully!")
    print("=" * 60)
    print("\nDatasets created:")
    print("  1. dijkstra_bellman_small_dataset.csv   (50 vertices, 200 edges)")
    print("  2. dijkstra_bellman_medium_dataset.csv  (500 vertices, 2000 edges)")
    print("  3. dijkstra_bellman_large_dataset.csv   (3000 vertices, 8000 edges) - Already exists")


if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    
    # Generate all datasets
    generate_all_datasets()
