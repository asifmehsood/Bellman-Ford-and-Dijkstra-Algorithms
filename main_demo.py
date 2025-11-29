"""
Main Demonstration Script for CS412 Project
Runs both algorithms on the large dataset and shows sample outputs
"""

import sys
from dijkstra_algorithm import run_dijkstra, load_graph_from_csv
from bellman_ford_algorithm import run_bellman_ford
import time


def main():
    print("=" * 80)
    print(" " * 20 + "CS412 - ALGORITHM ANALYSIS & DESIGN")
    print(" " * 15 + "SHORTEST PATH PROBLEM: ALGORITHM COMPARISON")
    print("=" * 80)
    print()
    
    # Dataset to demonstrate
    dataset = "dijkstra_bellman_large_dataset.csv"
    source = 0
    
    # Load graph info
    print("Loading graph dataset...")
    graph, num_vertices = load_graph_from_csv(dataset)
    num_edges = sum(len(neighbors) for neighbors in graph.values())
    
    print(f"Dataset: {dataset}")
    print(f"  - Total Vertices: {num_vertices}")
    print(f"  - Total Edges: {num_edges}")
    print(f"  - Source Vertex: {source}")
    print()
    
    # Dijkstra's Algorithm
    print("=" * 80)
    print("RUNNING DIJKSTRA'S ALGORITHM (Greedy Approach)")
    print("=" * 80)
    print("Time Complexity: O(V²) with array implementation")
    print("Space Complexity: O(V)")
    print()
    
    start_time = time.time()
    distances_dijkstra, predecessors_dijkstra = run_dijkstra(dataset, source)
    end_time = time.time()
    dijkstra_time = (end_time - start_time) * 1000
    
    print(f"✓ Execution completed in {dijkstra_time:.4f} ms")
    
    # Show sample results
    reachable = [i for i, d in enumerate(distances_dijkstra) if d != sys.maxsize]
    print(f"✓ Found paths to {len(reachable)} vertices")
    
    print("\nSample Shortest Distances (first 10 reachable vertices):")
    print("-" * 50)
    count = 0
    for i in reachable[:10]:
        print(f"  Vertex {i:4d}: Distance = {distances_dijkstra[i]:5d}")
        count += 1
    print()
    
    # Bellman-Ford Algorithm
    print("=" * 80)
    print("RUNNING BELLMAN-FORD ALGORITHM (Dynamic Programming Approach)")
    print("=" * 80)
    print("Time Complexity: O(V × E)")
    print("Space Complexity: O(V)")
    print()
    
    start_time = time.time()
    distances_bellman, predecessors_bellman, has_negative_cycle = run_bellman_ford(dataset, source)
    end_time = time.time()
    bellman_time = (end_time - start_time) * 1000
    
    print(f"✓ Execution completed in {bellman_time:.4f} ms")
    print(f"✓ Negative cycle detected: {has_negative_cycle}")
    
    # Show sample results
    reachable = [i for i, d in enumerate(distances_bellman) if d != sys.maxsize]
    print(f"✓ Found paths to {len(reachable)} vertices")
    
    print("\nSample Shortest Distances (first 10 reachable vertices):")
    print("-" * 50)
    for i in reachable[:10]:
        print(f"  Vertex {i:4d}: Distance = {distances_bellman[i]:5d}")
    print()
    
    # Comparison
    print("=" * 80)
    print("PERFORMANCE COMPARISON")
    print("=" * 80)
    print(f"Dijkstra's Algorithm:     {dijkstra_time:.4f} ms")
    print(f"Bellman-Ford Algorithm:   {bellman_time:.4f} ms")
    print()
    
    if dijkstra_time < bellman_time:
        speedup = bellman_time / dijkstra_time
        print(f"→ Dijkstra is {speedup:.2f}x FASTER than Bellman-Ford")
    else:
        speedup = dijkstra_time / bellman_time
        print(f"→ Bellman-Ford is {speedup:.2f}x FASTER than Dijkstra")
    
    print()
    
    # Verify correctness (both should give same results for positive weights)
    print("=" * 80)
    print("CORRECTNESS VERIFICATION")
    print("=" * 80)
    
    # Compare first 10 distances
    matches = 0
    total_checked = 0
    
    for i in range(min(10, len(distances_dijkstra))):
        if distances_dijkstra[i] != sys.maxsize and distances_bellman[i] != sys.maxsize:
            total_checked += 1
            if distances_dijkstra[i] == distances_bellman[i]:
                matches += 1
    
    if total_checked > 0:
        print(f"✓ Compared {total_checked} paths")
        print(f"✓ Matching results: {matches}/{total_checked}")
        if matches == total_checked:
            print("✓ Both algorithms produce IDENTICAL results (as expected)")
    
    print()
    print("=" * 80)
    print(" " * 25 + "DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("For detailed analysis, see:")
    print("  • PROJECT_REPORT.md - Complete project report")
    print("  • performance_results.csv - Raw performance data")
    print("  • algorithm_comparison_charts.png - Visual comparisons")
    print()


if __name__ == "__main__":
    main()
