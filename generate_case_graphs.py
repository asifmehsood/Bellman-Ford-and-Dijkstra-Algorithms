"""
Generate case-specific performance graphs (Best/Average/Worst for Small/Large inputs)
showing running times and order of growth for Dijkstra and Bellman-Ford algorithms.
"""

import matplotlib.pyplot as plt
import time
from dijkstra_algorithm import run_dijkstra
from bellman_ford_algorithm import run_bellman_ford

def run_performance_test(filename, num_runs=20):
    """
    Run both algorithms multiple times and collect statistics.
    
    Returns:
        Dictionary with best, average, and worst times for both algorithms
    """
    dijkstra_times = []
    bellman_times = []
    
    print(f"  Testing {filename}...")
    
    for i in range(num_runs):
        # Test Dijkstra
        start = time.perf_counter()
        run_dijkstra(filename, source_vertex=0)
        end = time.perf_counter()
        dijkstra_times.append((end - start) * 1000)
        
        # Test Bellman-Ford
        start = time.perf_counter()
        run_bellman_ford(filename, source_vertex=0)
        end = time.perf_counter()
        bellman_times.append((end - start) * 1000)
    
    return {
        'dijkstra': {
            'best': min(dijkstra_times),
            'average': sum(dijkstra_times) / len(dijkstra_times),
            'worst': max(dijkstra_times)
        },
        'bellman': {
            'best': min(bellman_times),
            'average': sum(bellman_times) / len(bellman_times),
            'worst': max(bellman_times)
        }
    }

def plot_case_graph(sizes, dijkstra_times, bellman_times, case_type, size_category, output_filename):
    """
    Create a single case-specific graph.
    
    Args:
        sizes: List of edge sizes
        dijkstra_times: List of Dijkstra times
        bellman_times: List of Bellman-Ford times
        case_type: 'Best', 'Average', or 'Worst'
        size_category: 'Small' or 'Large'
        output_filename: Name for the output file
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    x_pos = list(range(len(sizes)))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar([x - width/2 for x in x_pos], dijkstra_times, width, 
                   label="Dijkstra's Algorithm", color='#3498db', alpha=0.8)
    bars2 = ax.bar([x + width/2 for x in x_pos], bellman_times, width,
                   label="Bellman-Ford Algorithm", color='#e74c3c', alpha=0.8)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.4f}',
                   ha='center', va='bottom', fontsize=9)
    
    # Customize the plot
    ax.set_xlabel('Input Size (Edges)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Running Time (ms)', fontsize=12, fontweight='bold')
    ax.set_title(f'{case_type} Case Running Time - {size_category} Input\nOrder of Growth Comparison',
                fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([f'{s}' for s in sizes])
    ax.legend(loc='upper left', fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add order of growth annotations
    if size_category == 'Small':
        growth_text = "Dijkstra: O(V²)\nBellman-Ford: O(V×E)"
    else:
        growth_text = "Dijkstra: O(V²)\nBellman-Ford: O(V×E) with early stopping"
    
    ax.text(0.98, 0.97, growth_text,
           transform=ax.transAxes,
           fontsize=10,
           verticalalignment='top',
           horizontalalignment='right',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"✓ Generated: {output_filename}")
    plt.close()

def main():
    """Generate all 6 case-specific graphs."""
    print("Collecting performance data...")
    print("This will run 20 tests per dataset per algorithm (320 total tests)")
    print("Please wait...\n")
    
    # Define small and large input sizes
    small_datasets = [
        (250, 'dijkstra_bellman_250_dataset.csv'),
        (500, 'dijkstra_bellman_500_dataset.csv'),
        (750, 'dijkstra_bellman_750_dataset.csv'),
        (1000, 'dijkstra_bellman_1000_dataset.csv')
    ]
    
    large_datasets = [
        (5000, 'dijkstra_bellman_5000_dataset.csv'),
        (10000, 'dijkstra_bellman_10000_dataset.csv'),
        (15000, 'dijkstra_bellman_15000_dataset.csv'),
        (20000, 'dijkstra_bellman_20000_dataset.csv')
    ]
    
    # Collect results for small inputs
    print("Testing small datasets...")
    small_results = []
    for size, filename in small_datasets:
        results = run_performance_test(filename)
        small_results.append(results)
    
    # Collect results for large inputs
    print("\nTesting large datasets...")
    large_results = []
    for size, filename in large_datasets:
        results = run_performance_test(filename)
        large_results.append(results)
    
    print("\nGenerating case-specific graphs...\n")
    
    # Extract data for each case type
    small_sizes = [size for size, _ in small_datasets]
    large_sizes = [size for size, _ in large_datasets]
    
    case_types = ['best', 'average', 'worst']
    case_labels = ['Best', 'Average', 'Worst']
    
    for case_type, case_label in zip(case_types, case_labels):
        # Small input - extract times for this case
        small_dijkstra = [r['dijkstra'][case_type] for r in small_results]
        small_bellman = [r['bellman'][case_type] for r in small_results]
        
        plot_case_graph(
            small_sizes,
            small_dijkstra,
            small_bellman,
            case_label,
            'Small',
            f'{case_type.lower()}_case_small_input.png'
        )
        
        # Large input - extract times for this case
        large_dijkstra = [r['dijkstra'][case_type] for r in large_results]
        large_bellman = [r['bellman'][case_type] for r in large_results]
        
        plot_case_graph(
            large_sizes,
            large_dijkstra,
            large_bellman,
            case_label,
            'Large',
            f'{case_type.lower()}_case_large_input.png'
        )
    
    print("\n" + "="*60)
    print("All 6 case-specific graphs generated successfully!")
    print("="*60)
    print("\nGenerated files:")
    print("  1. best_case_small_input.png")
    print("  2. best_case_large_input.png")
    print("  3. average_case_small_input.png")
    print("  4. average_case_large_input.png")
    print("  5. worst_case_small_input.png")
    print("  6. worst_case_large_input.png")

if __name__ == "__main__":
    main()
