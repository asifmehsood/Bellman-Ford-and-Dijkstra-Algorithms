"""
Generate space complexity comparison charts for Small and Large inputs
matching the requested style. Uses vertex counts from the dataset parameters
already documented in the report.
"""

import matplotlib.pyplot as plt

# Vertex counts from report's Dataset Parameters
SMALL_INPUTS = [
    (250, 193),
    (500, 357),
    (750, 521),
    (1000, 693),
]

LARGE_INPUTS = [
    (5000, 2708),
    (10000, 4743),
    (15000, 6530),
    (20000, 8180),
]

ALGOS = ["Dijkstra's Algorithm", "Bellman-Ford Algorithm"]
COLORS = ['#f1c40f', '#e74c3c']


def plot_space_chart(inputs, title, filename):
    edges = [e for e, _ in inputs]
    vertices = [v for _, v in inputs]

    plt.figure(figsize=(10, 6))

    # Each algorithm has O(V) space; we plot identical lines to reflect same order of growth
    for algo, color in zip(ALGOS, COLORS):
        plt.plot(edges, vertices, marker='o', color=color, linewidth=2, label=algo)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Input Size (Edges)', fontsize=12, fontweight='bold')
    plt.ylabel('Space Usage (proportional to Vertices V)', fontsize=12, fontweight='bold')
    plt.grid(alpha=0.3, linestyle='--')
    plt.legend(loc='lower right')

    # Annotation noting O(V)
    plt.text(0.98, 0.04, 'Space Complexity: O(V) for both',
             transform=plt.gca().transAxes,
             ha='right', va='bottom', fontsize=10,
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.6))

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"✓ Saved {filename}")
    plt.close()


def main():
    plot_space_chart(SMALL_INPUTS,
                     'Space Complexity Comparison with Small Inputs',
                     'space_complexity_small.png')

    plot_space_chart(LARGE_INPUTS,
                     'Space Complexity Comparison with Large Inputs',
                     'space_complexity_large.png')

    print("All space complexity charts generated.")


if __name__ == '__main__':
    main()
