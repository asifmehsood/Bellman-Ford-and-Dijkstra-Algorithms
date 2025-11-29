"""
Extract detailed results (20 individual runs) for all 8 dataset sizes
"""
import time
from dijkstra_algorithm import run_dijkstra
from bellman_ford_algorithm import run_bellman_ford

def run_detailed_test(filename, algorithm_name, algorithm_func, num_runs=20):
    """
    Run algorithm multiple times and record each individual time
    """
    times = []
    
    for i in range(num_runs):
        start_time = time.perf_counter()
        algorithm_func(filename, source_vertex=0)
        end_time = time.perf_counter()
        
        elapsed_ms = (end_time - start_time) * 1000
        times.append(elapsed_ms)
    
    return times

def main():
    # Define all dataset files
    datasets = [
        # Small datasets
        ('dijkstra_bellman_250_dataset.csv', '250 edges', 193),
        ('dijkstra_bellman_500_dataset.csv', '500 edges', 418),
        ('dijkstra_bellman_750_dataset.csv', '750 edges', 581),
        ('dijkstra_bellman_1000_dataset.csv', '1000 edges', 695),
        # Large datasets
        ('dijkstra_bellman_5000_dataset.csv', '5000 edges', 3162),
        ('dijkstra_bellman_10000_dataset.csv', '10000 edges', 5588),
        ('dijkstra_bellman_15000_dataset.csv', '15000 edges', 6965),
        ('dijkstra_bellman_20000_dataset.csv', '20000 edges', 8180),
    ]
    
    print("=" * 80)
    print("DETAILED PERFORMANCE RESULTS - 20 INDIVIDUAL RUNS")
    print("=" * 80)
    
    for filename, label, vertices in datasets:
        print(f"\n{'='*80}")
        print(f"Dataset: {label} ({vertices} vertices)")
        print(f"File: {filename}")
        print(f"{'='*80}")
        
        # Run Dijkstra
        print(f"\nDijkstra's Algorithm (20 runs):")
        print("-" * 80)
        dijkstra_times = run_detailed_test(filename, "Dijkstra", run_dijkstra)
        for i, t in enumerate(dijkstra_times, 1):
            print(f"Run {i:2d}: {t:8.4f} ms")
        
        dijkstra_avg = sum(dijkstra_times) / len(dijkstra_times)
        dijkstra_min = min(dijkstra_times)
        dijkstra_max = max(dijkstra_times)
        
        print(f"\nStatistics:")
        print(f"  Average: {dijkstra_avg:8.4f} ms")
        print(f"  Best:    {dijkstra_min:8.4f} ms")
        print(f"  Worst:   {dijkstra_max:8.4f} ms")
        
        # Run Bellman-Ford
        print(f"\nBellman-Ford Algorithm (20 runs):")
        print("-" * 80)
        bellman_times = run_detailed_test(filename, "Bellman-Ford", run_bellman_ford)
        for i, t in enumerate(bellman_times, 1):
            print(f"Run {i:2d}: {t:8.4f} ms")
        
        bellman_avg = sum(bellman_times) / len(bellman_times)
        bellman_min = min(bellman_times)
        bellman_max = max(bellman_times)
        
        print(f"\nStatistics:")
        print(f"  Average: {bellman_avg:8.4f} ms")
        print(f"  Best:    {bellman_min:8.4f} ms")
        print(f"  Worst:   {bellman_max:8.4f} ms")
        
        # Comparison
        print(f"\nComparison:")
        print(f"  Dijkstra Average:     {dijkstra_avg:8.4f} ms")
        print(f"  Bellman-Ford Average: {bellman_avg:8.4f} ms")
        if dijkstra_avg > bellman_avg:
            ratio = dijkstra_avg / bellman_avg
            print(f"  Bellman-Ford is {ratio:.2f}x faster")
        else:
            ratio = bellman_avg / dijkstra_avg
            print(f"  Dijkstra is {ratio:.2f}x faster")
    
    print(f"\n{'='*80}")
    print("TESTING COMPLETED")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
