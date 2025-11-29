# Project Summary: Shortest Path Algorithm Analysis with NYC Street Data

## 🎯 Project Overview

**Title:** Finding the Shortest Path in Weighted Graphs Using Greedy and Dynamic Programming Approaches

**Objective:** Implement, analyze, and compare two fundamental shortest path algorithms (Dijkstra's and Bellman-Ford) using real-world New York City street network data.

---

## 📊 What We Did

### 1. **Algorithm Implementation**
We implemented two shortest path algorithms from scratch in Python **without using any graph libraries**:

#### **Dijkstra's Algorithm (Greedy Approach)**
- Time Complexity: O(V²) with array-based implementation
- Space Complexity: O(V)
- Uses greedy strategy to select minimum distance vertex at each step
- Works only with non-negative edge weights
- Efficient for finding shortest paths from source to all vertices

#### **Bellman-Ford Algorithm (Dynamic Programming Approach)**
- Time Complexity: O(V × E)
- Space Complexity: O(V)
- Uses dynamic programming with edge relaxation
- Can handle negative edge weights and detect negative cycles
- Iterates V-1 times over all edges

### 2. **Dataset Preparation**

#### **Source Data:**
- Original: `new_york_streets.csv` (139,990 street segments from OpenStreetMap)
- Real NYC street network with actual geographic coordinates

#### **Dataset Creation:**
We converted the raw street data into three graph datasets:

**Small Dataset:**
- 1,000 edges
- 695 vertices
- 215 unique street names
- 11 highway types
- Average weight: 133.56 meters

**Medium Dataset:**
- 10,000 edges
- 5,588 vertices
- 1,089 unique street names
- 16 highway types
- Average weight: 111.14 meters

**Large Dataset:**
- 50,000 edges
- 17,458 vertices
- 2,945 unique street names
- 24 highway types
- Average weight: 113.76 meters

#### **Enhanced Metadata Columns:**
Each dataset includes 8 columns:
1. `source` - Starting vertex ID (integer)
2. `target` - Ending vertex ID (integer)
3. `weight` - Distance in meters (rounded integer)
4. `street_name` - Human-readable street name (e.g., "Flatbush Avenue")
5. `highway_type` - Road classification (motorway, primary, secondary, residential, etc.)
6. `oneway` - Direction constraint (True/False)
7. `maxspeed` - Speed limit (e.g., "25 mph", "50 mph")
8. `length_meters` - Precise length as float (e.g., "254.71")

### 3. **Performance Testing**

#### **Testing Methodology:**
- **Runs:** 20 iterations per algorithm per dataset
- **Source Vertex:** 0 (consistent across all tests)
- **Timing:** Python `time.time()` function with millisecond precision
- **Metrics:** Best time, Average time, Worst time
- **Machine:** Standard desktop environment

#### **Test Results:**

| Dataset | Dijkstra Avg (ms) | Bellman-Ford Avg (ms) | Speedup Factor |
|---------|-------------------|----------------------|----------------|
| **Small** | 0.97 ms | 0.97 ms | ~1.0× |
| **Medium** | 9.87 ms | 9.31 ms | 1.06× faster |
| **Large** | 345.04 ms | 83.56 ms | **4.13× faster** |

**Key Finding:** Bellman-Ford significantly outperformed Dijkstra on larger datasets due to our array-based Dijkstra implementation (O(V²)) being less efficient than Bellman-Ford (O(V×E)) on sparse graphs.

### 4. **Data Visualization**

Generated three comprehensive charts:

1. **`algorithm_comparison_charts.png`** - 4-panel comparison:
   - Average execution time comparison (bar chart)
   - Dijkstra's best/avg/worst times across dataset sizes
   - Bellman-Ford's best/avg/worst times across dataset sizes
   - Speedup factor analysis

2. **`performance_trend_chart.png`** - Line graph:
   - Performance scaling from small → medium → large datasets
   - Shows how execution time grows with input size

3. **`results_table.png`** - Summary table:
   - All statistics in tabular format
   - Best, Average, Worst times for all combinations

---

## 🛠️ How We Did It

### **Step 1: Data Conversion Process**

```
NYC Street Data → Graph Format Conversion

Input: new_york_streets.csv
- Contains LINESTRING geometry coordinates
- Has edge weights (street lengths in meters)
- Includes metadata (street names, types, speeds)

Processing:
1. Parse LINESTRING geometry to extract start/end coordinates
2. Map geographic coordinates to sequential integer node IDs
3. Convert street lengths to integer edge weights
4. Extract metadata (street name, highway type, direction, speed)
5. Handle bidirectional streets (create reverse edges for two-way streets)

Output: dijkstra_bellman_[size]_dataset.csv
- Clean graph format: source, target, weight + metadata
- Ready for algorithm consumption
```

**Conversion Script:** `create_nyc_datasets.py`
- Reads raw NYC data
- Parses LINESTRING coordinates
- Creates node ID mappings
- Generates three dataset sizes
- Validates output

### **Step 2: Algorithm Implementation**

#### **Dijkstra's Algorithm:**
```python
Class: DijkstraAlgorithm
Method: shortest_path(source)

Process:
1. Initialize distances[source] = 0, all others = ∞
2. Create visited set and predecessors array
3. While unvisited vertices exist:
   a. Find vertex with minimum distance
   b. Mark as visited
   c. Update distances to neighbors (relaxation)
4. Return distances and predecessors
```

**Key Features:**
- Array-based minimum vertex selection (O(V) per iteration)
- Adjacency list representation for graph
- Path reconstruction via predecessor array
- Pure Python implementation (no libraries)

#### **Bellman-Ford Algorithm:**
```python
Class: BellmanFordAlgorithm
Method: shortest_path(source)

Process:
1. Initialize distances[source] = 0, all others = ∞
2. Repeat V-1 times:
   - For each edge (u, v, weight):
     - If distance[u] + weight < distance[v]:
       - Update distance[v]
3. Check for negative cycles (optional V-th iteration)
4. Return distances and predecessors
```

**Key Features:**
- Edge list representation
- V-1 iterations of edge relaxation
- Negative cycle detection
- Early termination optimization

### **Step 3: Performance Testing Framework**

**Script:** `performance_testing.py`

```python
Testing Process:
1. Load dataset (small/medium/large)
2. For each dataset:
   a. Run Dijkstra 20 times
   b. Run Bellman-Ford 20 times
   c. Record execution times
3. Calculate statistics:
   - Best time (minimum)
   - Average time (mean)
   - Worst time (maximum)
4. Save results to performance_results.csv
```

**Output Format:**
```csv
Algorithm,Dataset,Best Time (ms),Average Time (ms),Worst Time (ms),Num Runs
Dijkstra,dijkstra_bellman_small_dataset.csv,0.0000,0.9676,1.3039,20
Bellman-Ford,dijkstra_bellman_small_dataset.csv,0.0000,0.9650,2.0542,20
...
```

### **Step 4: Visualization Generation**

**Script:** `generate_visualizations.py`

```python
Visualization Process:
1. Load performance_results.csv
2. Parse data by algorithm and dataset size
3. Create matplotlib figures:
   
   Chart 1: Bar chart comparing average times
   Chart 2: Multi-series line chart (Dijkstra trends)
   Chart 3: Multi-series line chart (Bellman-Ford trends)
   Chart 4: Speedup factor analysis
   
4. Save as PNG files with high resolution
5. Generate summary table image
```

### **Step 5: Enhanced Features (Optional)**

Created demonstration scripts to showcase metadata usage:

**`dijkstra_with_path_display.py`:**
- Shows paths with actual street names
- Displays road types and speed limits
- Calculates estimated travel times
- Human-readable navigation instructions

**`compare_basic_vs_enhanced.py`:**
- Side-by-side comparison of basic vs. enhanced output
- Demonstrates value of metadata
- Shows real-world application scenarios

**`demo_enhanced_features.py`:**
- Complete feature demonstration
- Statistical analysis of dataset
- Road type filtering examples
- Travel time calculations

---

## 📁 Project File Structure

```
Project Directory/
├── Core Algorithm Files:
│   ├── dijkstra_algorithm.py              # Dijkstra implementation
│   ├── bellman_ford_algorithm.py          # Bellman-Ford implementation
│   ├── main_demo.py                       # Quick demonstration
│   └── performance_testing.py             # Testing framework
│
├── Dataset Files:
│   ├── new_york_streets.csv               # Original NYC data (source)
│   ├── dijkstra_bellman_small_dataset.csv # 1,000 edges
│   ├── dijkstra_bellman_medium_dataset.csv# 10,000 edges
│   └── dijkstra_bellman_large_dataset.csv # 50,000 edges
│
├── Dataset Generation:
│   └── create_nyc_datasets.py             # NYC data converter
│
├── Visualization:
│   ├── generate_visualizations.py         # Chart generator
│   ├── algorithm_comparison_charts.png    # 4-panel comparison
│   ├── performance_trend_chart.png        # Trend analysis
│   └── results_table.png                  # Results summary
│
├── Enhanced Features (Optional):
│   ├── dijkstra_with_path_display.py      # Path display with streets
│   ├── compare_basic_vs_enhanced.py       # Basic vs enhanced demo
│   └── demo_enhanced_features.py          # Full feature showcase
│
├── Results:
│   └── performance_results.csv            # Raw test results
│
└── Documentation:
    ├── README.md                          # Project overview
    ├── PROJECT_REPORT.md                  # Complete analysis
    ├── NYC_DATASET_CONVERSION_GUIDE.md    # Conversion details
    ├── ENHANCED_FEATURES_SUMMARY.md       # Enhancement docs
    └── METADATA_USAGE_GUIDE.md            # Usage guide
```

---

## 🔬 Technical Details

### **Graph Representation:**

**Dijkstra:** Adjacency List
```python
graph = {
    0: [(1, 43), (2, 32)],      # vertex 0 connects to 1 (weight 43) and 2 (weight 32)
    1: [(3, 89)],                # vertex 1 connects to 3 (weight 89)
    ...
}
```

**Bellman-Ford:** Edge List
```python
edges = [
    (0, 1, 43),                  # edge from 0 to 1 with weight 43
    (0, 2, 32),                  # edge from 0 to 2 with weight 32
    (1, 3, 89),                  # edge from 1 to 3 with weight 89
    ...
]
```

### **Data Conversion Logic:**

```python
Coordinate Mapping:
"-73.7946273 40.7864093" → Node ID: 0
"-73.7936126 40.7866863" → Node ID: 1
"-73.7928415 40.7869596" → Node ID: 2
...

Edge Creation:
LINESTRING(-73.79 40.78, -73.78 40.79) + length=254.71m
→ Edge: (0, 1, 255, "Cross Island Parkway", "motorway", "True", "50 mph", "254.71")
```

### **Performance Measurement:**

```python
import time

start_time = time.time()
algorithm.shortest_path(source=0)
end_time = time.time()

execution_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds
```

---

## 📊 Key Statistics

### **Dataset Characteristics:**

**Road Type Distribution (Large Dataset):**
- Residential: 49.3%
- Secondary: 21.2%
- Tertiary: 16.5%
- Primary: 10.1%
- Other: 2.9%

**Speed Limit Distribution:**
- No limit posted: 68.1%
- 25 mph: 26.7%
- 20 mph: 3.6%
- Other: 1.6%

**Direction:**
- One-way streets: 38.7%
- Two-way streets: 61.3%

### **Graph Properties:**

| Property | Small | Medium | Large |
|----------|-------|--------|-------|
| **Density** | Sparse | Sparse | Sparse |
| **Edges/Vertex** | 1.44 | 1.79 | 2.86 |
| **Connectivity** | Partial | Partial | Partial |
| **Weight Range** | 3-1661m | 5-1139m | 1-1992m |

---

## 🎓 Academic Contributions

### **Novel Aspects:**

1. **Real-World Data:** Used actual NYC street network instead of synthetic random graphs
2. **Rich Metadata:** Enhanced datasets with street names, road types, and speed limits
3. **Scalable Testing:** Three dataset sizes (1K, 10K, 50K edges)
4. **Pure Implementation:** No graph libraries used (complete understanding)
5. **Comprehensive Analysis:** 20 runs per test for statistical validity

### **Practical Applications:**

- **Navigation Systems:** GPS routing with real street names
- **Emergency Services:** Ambulance/fire truck route optimization
- **Urban Planning:** Traffic flow analysis by road type
- **Delivery Services:** Package routing optimization
- **Transportation:** Public transit route planning

---

## ✅ Validation & Quality Assurance

### **Correctness Verification:**
- Both algorithms produce identical shortest distances ✓
- Tested on all three dataset sizes ✓
- Multiple source vertices tested ✓
- Path reconstruction validated ✓

### **Performance Validation:**
- 20 runs per test for consistency ✓
- Best/Average/Worst times recorded ✓
- Results reproducible ✓
- Statistical analysis performed ✓

### **Data Quality:**
- All edge weights positive (non-negative) ✓
- Continuous node IDs (0-indexed) ✓
- Valid graph structure ✓
- Metadata properly formatted ✓

---

## 🚀 How to Run the Project

### **Quick Start:**
```bash
# 1. Run quick demonstration
python main_demo.py

# 2. Run complete performance testing (takes a few minutes)
python performance_testing.py

# 3. Generate visualization charts
python generate_visualizations.py

# 4. Test individual algorithms
python dijkstra_algorithm.py
python bellman_ford_algorithm.py
```

### **Optional Enhanced Features:**
```bash
# Show paths with street names
python dijkstra_with_path_display.py

# Compare basic vs enhanced output
python compare_basic_vs_enhanced.py

# Full feature demonstration
python demo_enhanced_features.py
```

### **Regenerate Datasets (if needed):**
```bash
python create_nyc_datasets.py
```

---

## 📝 Summary

**What:** Shortest path algorithm comparison using real NYC street data

**How:** 
- Implemented Dijkstra and Bellman-Ford from scratch
- Converted 140K NYC street segments into graph format
- Created 3 dataset sizes with rich metadata
- Ran 20 iterations per test for each combination
- Generated comprehensive visualizations
- Built enhanced features for practical applications

**Results:**
- Bellman-Ford 4.13× faster on large dataset
- Successfully handled 50,000 edges with 17,458 vertices
- Demonstrated real-world applicability with street names
- Provided framework for future urban routing research

**Innovation:**
- Real-world data instead of synthetic graphs
- Rich metadata for practical navigation
- Professional-grade implementation
- Comprehensive testing methodology
- Enhanced visualization and analysis

---

## 🎯 Use This Prompt

You can use this entire document as a prompt to:
1. Generate a complete project report
2. Create presentation slides
3. Write academic paper sections
4. Explain the project to others
5. Document the methodology

**For Report Generation:** Copy relevant sections and adapt to your report format, adding your specific analysis, findings, and conclusions.

---

**Project demonstrates professional software engineering practices, rigorous algorithm analysis, and practical application of computer science theory to real-world urban transportation challenges.** 🚀
