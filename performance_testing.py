"""
Performance Testing Framework for Dijkstra's and Bellman-Ford Algorithms
CS412 - Algorithm Analysis & Design

Runs both algorithms 20 times on each dataset and collects performance metrics
"""

import time
import csv
import sys
from dijkstra_algorithm import run_dijkstra
from bellman_ford_algorithm import run_bellman_ford


class PerformanceTester:
    """
    Performance testing framework for comparing shortest path algorithms
    """
    
    def __init__(self):
        self.results = []
    
    def run_single_test(self, algorithm_func, filename, source=0):
        """
        Run a single test of an algorithm and measure execution time
        
        Args:
            algorithm_func: Function to test (run_dijkstra or run_bellman_ford)
            filename: Dataset filename
            source: Source vertex
            
        Returns:
            Execution time in milliseconds
        """
        start_time = time.time()
        algorithm_func(filename, source)
        end_time = time.time()
        
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
        return execution_time
    
    def run_multiple_tests(self, algorithm_name, algorithm_func, filename, num_runs=20):
        """
        Run algorithm multiple times and collect statistics
        
        Args:
            algorithm_name: Name of the algorithm (for display)
            algorithm_func: Function to test
            filename: Dataset filename
            num_runs: Number of times to run the algorithm
            
        Returns:
            Dictionary with best, average, and worst times
        """
        print(f"\nTesting {algorithm_name} on {filename}...")
        print(f"Running {num_runs} iterations...")
        
        times = []
        
        for i in range(num_runs):
            exec_time = self.run_single_test(algorithm_func, filename)
            times.append(exec_time)
            
            # Show progress
            if (i + 1) % 5 == 0:
                print(f"  Completed {i + 1}/{num_runs} runs")
        
        # Calculate statistics
        best_time = min(times)
        worst_time = max(times)
        avg_time = sum(times) / len(times)
        
        result = {
            'algorithm': algorithm_name,
            'dataset': filename,
            'best_time': best_time,
            'average_time': avg_time,
            'worst_time': worst_time,
            'num_runs': num_runs,
            'all_times': times
        }
        
        self.results.append(result)
        
        print(f"  Best Time:    {best_time:.4f} ms")
        print(f"  Average Time: {avg_time:.4f} ms")
        print(f"  Worst Time:   {worst_time:.4f} ms")
        
        return result
    
    def test_all_datasets(self):
        """
        Test both algorithms on all datasets (small, medium, large)
        """
        datasets = [
            "dijkstra_bellman_small_dataset.csv",
            "dijkstra_bellman_medium_dataset.csv",
            "dijkstra_bellman_large_dataset.csv"
        ]
        
        dataset_sizes = ["SMALL", "MEDIUM", "LARGE"]
        
        print("=" * 70)
        print("PERFORMANCE TESTING - SHORTEST PATH ALGORITHMS")
        print("=" * 70)
        print("\nTesting Parameters:")
        print("  - Number of runs per test: 20")
        print("  - Source vertex: 0")
        print("  - Algorithms: Dijkstra (Greedy), Bellman-Ford (Dynamic Programming)")
        print("=" * 70)
        
        for dataset, size in zip(datasets, dataset_sizes):
            print(f"\n{'=' * 70}")
            print(f"TESTING ON {size} DATASET: {dataset}")
            print("=" * 70)
            
            # Test Dijkstra's Algorithm
            self.run_multiple_tests(
                algorithm_name="Dijkstra",
                algorithm_func=run_dijkstra,
                filename=dataset,
                num_runs=20
            )
            
            # Test Bellman-Ford Algorithm
            self.run_multiple_tests(
                algorithm_name="Bellman-Ford",
                algorithm_func=run_bellman_ford,
                filename=dataset,
                num_runs=20
            )
        
        print("\n" + "=" * 70)
        print("ALL TESTS COMPLETED!")
        print("=" * 70)
    
    def save_results_to_csv(self, filename="performance_results.csv"):
        """
        Save all results to a CSV file
        
        Args:
            filename: Output CSV filename
        """
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Algorithm', 'Dataset', 'Best Time (ms)', 
                'Average Time (ms)', 'Worst Time (ms)', 'Num Runs'
            ])
            
            for result in self.results:
                writer.writerow([
                    result['algorithm'],
                    result['dataset'],
                    f"{result['best_time']:.4f}",
                    f"{result['average_time']:.4f}",
                    f"{result['worst_time']:.4f}",
                    result['num_runs']
                ])
        
        print(f"\nResults saved to {filename}")
    
    def print_comparison_table(self):
        """
        Print a formatted comparison table of all results
        """
        print("\n" + "=" * 90)
        print("PERFORMANCE COMPARISON TABLE")
        print("=" * 90)
        print(f"{'Algorithm':<15} {'Dataset':<35} {'Best (ms)':<12} {'Avg (ms)':<12} {'Worst (ms)':<12}")
        print("-" * 90)
        
        for result in self.results:
            dataset_name = result['dataset'].replace('dijkstra_bellman_', '').replace('_dataset.csv', '').upper()
            print(f"{result['algorithm']:<15} {dataset_name:<35} "
                  f"{result['best_time']:<12.4f} {result['average_time']:<12.4f} "
                  f"{result['worst_time']:<12.4f}")
        
        print("=" * 90)
    
    def print_summary(self):
        """
        Print summary analysis comparing both algorithms
        """
        print("\n" + "=" * 70)
        print("PERFORMANCE ANALYSIS SUMMARY")
        print("=" * 70)
        
        # Group results by dataset
        datasets = {}
        for result in self.results:
            dataset = result['dataset']
            if dataset not in datasets:
                datasets[dataset] = {}
            datasets[dataset][result['algorithm']] = result
        
        for dataset, algos in datasets.items():
            dataset_name = dataset.replace('dijkstra_bellman_', '').replace('_dataset.csv', '').upper()
            print(f"\n{dataset_name} Dataset:")
            print("-" * 70)
            
            if 'Dijkstra' in algos and 'Bellman-Ford' in algos:
                dijk = algos['Dijkstra']
                bell = algos['Bellman-Ford']
                
                # Compare average times
                speedup = bell['average_time'] / dijk['average_time']
                
                print(f"  Dijkstra Average:     {dijk['average_time']:.4f} ms")
                print(f"  Bellman-Ford Average: {bell['average_time']:.4f} ms")
                
                if speedup > 1:
                    print(f"  → Dijkstra is {speedup:.2f}x FASTER than Bellman-Ford")
                else:
                    print(f"  → Bellman-Ford is {1/speedup:.2f}x FASTER than Dijkstra")
        
        print("\n" + "=" * 70)


def main():
    """
    Main function to run all performance tests
    """
    # Create tester instance
    tester = PerformanceTester()
    
    # Run all tests
    tester.test_all_datasets()
    
    # Display results
    tester.print_comparison_table()
    tester.print_summary()
    
    # Save results to CSV
    tester.save_results_to_csv("performance_results.csv")
    
    print("\n" + "=" * 70)
    print("Testing complete! Check 'performance_results.csv' for detailed results.")
    print("=" * 70)


if __name__ == "__main__":
    main()
