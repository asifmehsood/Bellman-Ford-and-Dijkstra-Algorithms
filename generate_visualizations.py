"""
Visualization Generator for Algorithm Performance Results
CS412 - Algorithm Analysis & Design

Creates charts and graphs comparing Dijkstra's and Bellman-Ford algorithms
"""

import csv
import matplotlib.pyplot as plt
import numpy as np
import os


def load_results_from_csv(filename="performance_results.csv"):
    """
    Load performance results from CSV file
    
    Args:
        filename: CSV file with results
        
    Returns:
        List of result dictionaries
    """
    results = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append({
                'algorithm': row['Algorithm'],
                'dataset': row['Dataset'],
                'best_time': float(row['Best Time (ms)']),
                'average_time': float(row['Average Time (ms)']),
                'worst_time': float(row['Worst Time (ms)']),
                'num_runs': int(row['Num Runs'])
            })
    
    return results


def create_comparison_charts(results):
    """
    Create comprehensive comparison charts
    
    Args:
        results: List of performance results
    """
    # Organize data
    datasets = ['SMALL', 'MEDIUM', 'LARGE']
    dijkstra_best = []
    dijkstra_avg = []
    dijkstra_worst = []
    bellman_best = []
    bellman_avg = []
    bellman_worst = []
    
    for dataset in datasets:
        for result in results:
            if dataset.lower() in result['dataset'].lower():
                if result['algorithm'] == 'Dijkstra':
                    dijkstra_best.append(result['best_time'])
                    dijkstra_avg.append(result['average_time'])
                    dijkstra_worst.append(result['worst_time'])
                elif result['algorithm'] == 'Bellman-Ford':
                    bellman_best.append(result['best_time'])
                    bellman_avg.append(result['average_time'])
                    bellman_worst.append(result['worst_time'])
    
    # Create figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Shortest Path Algorithms Performance Comparison\nDijkstra (Greedy) vs Bellman-Ford (Dynamic Programming)', 
                 fontsize=16, fontweight='bold')
    
    # Chart 1: Average Time Comparison (Bar Chart)
    ax1 = axes[0, 0]
    x = np.arange(len(datasets))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, dijkstra_avg, width, label='Dijkstra', color='#3498db', alpha=0.8)
    bars2 = ax1.bar(x + width/2, bellman_avg, width, label='Bellman-Ford', color='#e74c3c', alpha=0.8)
    
    ax1.set_xlabel('Dataset Size', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Average Time (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('Average Execution Time Comparison', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(datasets)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=9)
    
    # Chart 2: Best/Average/Worst Times for Dijkstra
    ax2 = axes[0, 1]
    x = np.arange(len(datasets))
    width = 0.25
    
    ax2.bar(x - width, dijkstra_best, width, label='Best', color='#2ecc71', alpha=0.8)
    ax2.bar(x, dijkstra_avg, width, label='Average', color='#3498db', alpha=0.8)
    ax2.bar(x + width, dijkstra_worst, width, label='Worst', color='#e67e22', alpha=0.8)
    
    ax2.set_xlabel('Dataset Size', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Time (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('Dijkstra Algorithm - Best/Avg/Worst Times', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(datasets)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    # Chart 3: Best/Average/Worst Times for Bellman-Ford
    ax3 = axes[1, 0]
    
    ax3.bar(x - width, bellman_best, width, label='Best', color='#2ecc71', alpha=0.8)
    ax3.bar(x, bellman_avg, width, label='Average', color='#e74c3c', alpha=0.8)
    ax3.bar(x + width, bellman_worst, width, label='Worst', color='#e67e22', alpha=0.8)
    
    ax3.set_xlabel('Dataset Size', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Time (ms)', fontsize=12, fontweight='bold')
    ax3.set_title('Bellman-Ford Algorithm - Best/Avg/Worst Times', fontsize=13, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(datasets)
    ax3.legend()
    ax3.grid(axis='y', alpha=0.3)
    
    # Chart 4: Speedup Factor (Dijkstra time / Bellman-Ford time)
    ax4 = axes[1, 1]
    speedup = [d/b for d, b in zip(dijkstra_avg, bellman_avg)]
    
    bars = ax4.bar(datasets, speedup, color='#9b59b6', alpha=0.8)
    ax4.axhline(y=1, color='red', linestyle='--', linewidth=2, label='Equal Performance')
    
    ax4.set_xlabel('Dataset Size', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Speedup Factor', fontsize=12, fontweight='bold')
    ax4.set_title('Bellman-Ford Speedup over Dijkstra\n(Values > 1 mean Bellman-Ford is faster)', 
                  fontsize=13, fontweight='bold')
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, value in zip(bars, speedup):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{value:.2f}x',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('algorithm_comparison_charts.png', dpi=300, bbox_inches='tight')
    print("\n✓ Saved: algorithm_comparison_charts.png")
    plt.close()
    
    # Create separate line chart for trends
    create_trend_chart(datasets, dijkstra_avg, bellman_avg)


def create_trend_chart(datasets, dijkstra_times, bellman_times):
    """
    Create a line chart showing performance trends
    """
    plt.figure(figsize=(10, 6))
    
    x = range(len(datasets))
    
    plt.plot(x, dijkstra_times, marker='o', linewidth=2, markersize=10, 
             label='Dijkstra', color='#3498db')
    plt.plot(x, bellman_times, marker='s', linewidth=2, markersize=10,
             label='Bellman-Ford', color='#e74c3c')
    
    plt.xlabel('Dataset Size', fontsize=12, fontweight='bold')
    plt.ylabel('Average Execution Time (ms)', fontsize=12, fontweight='bold')
    plt.title('Performance Trend: Execution Time vs Dataset Size', fontsize=14, fontweight='bold')
    plt.xticks(x, datasets)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Add value annotations
    for i, (d_time, b_time) in enumerate(zip(dijkstra_times, bellman_times)):
        plt.annotate(f'{d_time:.2f}', (i, d_time), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
        plt.annotate(f'{b_time:.2f}', (i, b_time), textcoords="offset points",
                    xytext=(0,-15), ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('performance_trend_chart.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: performance_trend_chart.png")
    plt.close()


def create_results_table_image(results):
    """
    Create a visual table of results
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = [['Algorithm', 'Dataset', 'Best (ms)', 'Average (ms)', 'Worst (ms)']]
    
    for result in results:
        dataset_name = result['dataset'].replace('dijkstra_bellman_', '').replace('_dataset.csv', '').upper()
        table_data.append([
            result['algorithm'],
            dataset_name,
            f"{result['best_time']:.4f}",
            f"{result['average_time']:.4f}",
            f"{result['worst_time']:.4f}"
        ])
    
    # Create table
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.15, 0.15, 0.15, 0.15, 0.15])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(5):
        cell = table[(0, i)]
        cell.set_facecolor('#34495e')
        cell.set_text_props(weight='bold', color='white')
    
    # Alternate row colors
    for i in range(1, len(table_data)):
        for j in range(5):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ecf0f1')
            else:
                cell.set_facecolor('#ffffff')
    
    plt.title('Performance Results Summary', fontsize=16, fontweight='bold', pad=20)
    plt.savefig('results_table.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: results_table.png")
    plt.close()


def main():
    """
    Main function to generate all visualizations
    """
    print("=" * 70)
    print("VISUALIZATION GENERATOR")
    print("=" * 70)
    print("\nGenerating performance comparison charts...")
    
    # Load results
    results = load_results_from_csv("performance_results.csv")
    
    # Create charts
    create_comparison_charts(results)
    create_results_table_image(results)

    # Additional: Experimental vs Theoretical comparison charts
    print("\nGenerating Experimental vs Theoretical comparison charts...")

    def _plot_experimental_vs_theoretical(title, input_sizes, experimental, theoretical, ratios, outfile):
        plt.figure(figsize=(8, 5))
        plt.plot(input_sizes, experimental, marker='o', label='Experimental Average (ms)')
        plt.plot(input_sizes, theoretical, marker='s', label='Theoretical Estimate (ms)')
        for x, y, r in zip(input_sizes, experimental, ratios):
            plt.annotate(f"×{r:.3f}", (x, y), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=8)
        plt.title(title)
        plt.xlabel('Input size (edges)')
        plt.ylabel('Time (ms)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        plt.savefig(outfile, dpi=300)
        plt.close()

    # Table 4: Dijkstra small
    _plot_experimental_vs_theoretical(
        title="Table 4: Dijkstra (Small) Experimental vs Theoretical",
        input_sizes=[250, 500, 750, 1000],
        experimental=[0.4007, 0.7595, 1.1474, 1.4088],
        theoretical=[0.4176, 0.7586, 1.0996, 1.4406],
        ratios=[0.9595, 1.0012, 1.0435, 0.9779],
        outfile=os.path.join('.', 'table4_dijkstra_small.png')
    )

    # Table 6: Dijkstra large
    _plot_experimental_vs_theoretical(
        title="Table 6: Dijkstra (Large) Experimental vs Theoretical",
        input_sizes=[5000, 10000, 15000, 20000],
        experimental=[6.7311, 15.1701, 37.8444, 181.3139],
        theoretical=[6.8970, 13.7175, 20.5380, 27.3585],
        ratios=[0.9760, 1.1059, 1.8436, 6.6274],
        outfile=os.path.join('.', 'table6_dijkstra_large.png')
    )

    # Table 8: Bellman-Ford small
    _plot_experimental_vs_theoretical(
        title="Table 8: Bellman-Ford (Small) Experimental vs Theoretical",
        input_sizes=[250, 500, 750, 1000],
        experimental=[0.6052, 0.6521, 0.9871, 1.2778],
        theoretical=[0.4176, 0.7586, 1.0996, 1.4406],
        ratios=[1.4500, 0.8594, 0.8980, 0.8870],
        outfile=os.path.join('.', 'table8_bf_small.png')
    )

    # Table 10: Bellman-Ford large
    _plot_experimental_vs_theoretical(
        title="Table 10: Bellman-Ford (Large) Experimental vs Theoretical",
        input_sizes=[5000, 10000, 15000, 20000],
        experimental=[6.1730, 12.8179, 26.2307, 44.2544],
        theoretical=[6.8970, 13.7175, 20.5125, 27.3585],
        ratios=[0.8959, 0.4500, 0.3011, 0.2256],
        outfile=os.path.join('.', 'table10_bf_large.png')
    )
    
    print("\n" + "=" * 70)
    print("All visualizations generated successfully!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  1. algorithm_comparison_charts.png - Comprehensive comparison charts")
    print("  2. performance_trend_chart.png     - Performance trend line chart")
    print("  3. results_table.png               - Results summary table")
    print("  4. table4_dijkstra_small.png       - Dijkstra small: Experimental vs Theoretical")
    print("  5. table6_dijkstra_large.png       - Dijkstra large: Experimental vs Theoretical")
    print("  6. table8_bf_small.png             - Bellman-Ford small: Experimental vs Theoretical")
    print("  7. table10_bf_large.png            - Bellman-Ford large: Experimental vs Theoretical")
    print("=" * 70)


if __name__ == "__main__":
    main()
