import csv
import time
import os
from dijkstra_algorithm import run_dijkstra

def run_detailed_test(filename, dataset_name, num_runs=20):
    """Run tests and record all 20 times individually"""
    
    print(f"\n{'='*70}")
    print(f"Testing Dijkstra on {dataset_name}")
    print(f"{'='*70}\n")
    
    times = []
    
    for i in range(1, num_runs + 1):
        start_time = time.time()
        run_dijkstra(filename, source_vertex=0)
        end_time = time.time()
        
        exec_time_ms = (end_time - start_time) * 1000
        times.append(exec_time_ms)
        
        print(f"Time {i:2d}: {exec_time_ms:10.4f} ms")
    
    avg_time = sum(times) / len(times)
    best_time = min(times)
    worst_time = max(times)
    
    print(f"\n{'─'*70}")
    print(f"Experimental Average: {avg_time:.4f} ms")
    print(f"Best Time: {best_time:.4f} ms")
    print(f"Worst Time: {worst_time:.4f} ms")
    print(f"{'='*70}\n")
    
    return times, avg_time

# Run for all datasets
# Prefer base datasets; fall back to available subset files
candidate_datasets = [
    ("dijkstra_bellman_small_dataset.csv", "SMALL (1,000 edges)"),
    ("dijkstra_bellman_medium_dataset.csv", "MEDIUM (10,000 edges)"),
    ("dijkstra_bellman_large_dataset.csv", "LARGE (50,000 edges)"),
    ("dijkstra_bellman_250_dataset.csv", "SMALL SUBSET (250 edges)"),
    ("dijkstra_bellman_500_dataset.csv", "SMALL SUBSET (500 edges)"),
    ("dijkstra_bellman_750_dataset.csv", "SMALL SUBSET (750 edges)"),
    ("dijkstra_bellman_1000_dataset.csv", "SMALL SUBSET (1000 edges)"),
    ("dijkstra_bellman_5000_dataset.csv", "LARGE SUBSET (5000 edges)"),
    ("dijkstra_bellman_10000_dataset.csv", "LARGE SUBSET (10000 edges)"),
    ("dijkstra_bellman_15000_dataset.csv", "LARGE SUBSET (15000 edges)"),
    ("dijkstra_bellman_20000_dataset.csv", "LARGE SUBSET (20000 edges)")
]

datasets = [(f, label) for f, label in candidate_datasets if os.path.exists(f)]

if not datasets:
    print("ERROR: No dataset CSV files found. Create them via 'create_nyc_datasets.py' or 'create_subset_datasets.py'.")
    raise SystemExit(1)

all_results = {}

for filename, name in datasets:
    try:
        times, avg = run_detailed_test(filename, name)
        all_results[name] = {'times': times, 'average': avg}
    except Exception as e:
        print(f"[ERROR] Failed on {name} ({filename}): {e}")

print("\n" + "="*70)
print("SUMMARY - ALL DATASETS")
print("="*70)

for name, data in all_results.items():
    print(f"\n{name}:")
    print(f"  Average: {data['average']:.4f} ms")