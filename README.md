# Route Finding Search Algorithms - Intro to AI Assignment 2

## 📋 Project Overview

This project implements 6 tree-based search algorithms for route finding in directed graphs:
- **DFS** (Depth-First Search) - Stack-based, goes deep first
- **BFS** (Breadth-First Search) - Queue-based, explores level by level
- **UCS** (Uniform Cost Search) - Priority queue by cost, finds cheapest path
- **GBFS** (Greedy Best-First Search) - Priority queue by heuristic, fast but not optimal
- **A*** (A-Star Search) - Priority queue by f(n)=g(n)+h(n), optimal and efficient
- **IDA*** (Iterative Deepening A*) - Recursive DFS with f-limit, optimal with minimal memory

All algorithms use **GRAPH SEARCH** with a visited set to avoid revisiting nodes.

## 🗂️ Project Structure

```
project/
├── search.py              # Main entry point 
├── search_node.py         # SearchNode class 
├── graph_parser.py        # Input file parser 
├── utils.py               # Helper functions 
├── search_algorithms.py   # All 6 algorithms 
├── test_runner.py         # Automated test suite 
├── Guide.md               # Detailed implementation guide
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── test_cases/
    ├── test_linear.txt        # Simple baseline
    ├── test_diamond.txt       # Multiple paths
    ├── test_wide.txt          # Branching factor test
    ├── test_depth.txt         # DFS depth preference
    ├── test_misleading.txt    # Heuristic quality test
    ├── test_multi_destin.txt  # Multiple goals
    ├── test_sparse.txt        # Long linear path
    ├── test_obstacle.txt      # Grid pathfinding
    ├── test_no_solution.txt   # Unreachable goal
    ├── test_cycle.txt         # Cycle handling
    ├── test_exponential.txt   # Memory stress test
    └── test_long_path.txt     # Deep search (50 nodes)
```

## 🚀 How to Run

### Run Single Algorithm

```bash
python search.py <filename> <method> [--simple]
```

#### Examples

```bash
# Detailed output
python search.py test_cases/test_linear.txt DFS
python search.py test_cases/test_diamond.txt BFS
python search.py test_cases/test_misleading.txt AS

# Simple output (for submission)
python search.py test_cases/test_linear.txt DFS --simple
```

### Run All Tests (Automated Test Suite)

```bash
python test_runner.py
```

This will:
- ✅ Run all 6 algorithms on all 12 test cases (72 tests total)
- ✅ Display results in organized tables
- ✅ Show path costs, nodes created, and execution time
- ✅ Compare algorithm performance
- ✅ Identify optimal vs suboptimal solutions
- ✅ Generate comprehensive summary statistics

**Sample Test Runner Output:**
```
========================================================================================================================
                                            SEARCH ALGORITHM TEST REPORT
========================================================================================================================

Running 12 test cases with 6 algorithms
Total: 72 tests

========================================================================================================================
Test: Linear Path - Simple baseline
========================================================================================================================
Algo     | Goal   | Nodes  | Cost    | Time     | Path
------------------------------------------------------------------------------------------------------------------------
DFS      | 5      | 5      | 4.0     | 83.7ms   | 1 -> 2 -> 3 -> 4 -> 5                    [OK]
BFS      | 5      | 5      | 4.0     | 80.1ms   | 1 -> 2 -> 3 -> 4 -> 5                    [OK]
...

========================================================================================================================
                                                      SUMMARY
========================================================================================================================

[Linear Path]
  Goal: 5
  Optimal Cost: 4.0
    Found by: DFS, BFS, UCS, GBFS, A*, IDA*
  Memory: 5 - 5 nodes
    Most efficient: DFS, BFS, UCS, GBFS, A*, IDA*
  Speed: 78.0ms - 83.7ms
    Fastest: A*
    Slowest: DFS
...
```

## 🔤 Algorithm Method Names

| Method Name | Algorithm | Alternative Name |
|-------------|-----------|------------------|
| `DFS` | Depth-First Search | - |
| `BFS` | Breadth-First Search | - |
| `UCS` | Uniform Cost Search | `CUS1` |
| `GBFS` | Greedy Best-First Search | - |
| `AS` | A* Search | `ASTAR` |
| `IDASTAR` | Iterative Deepening A* | `CUS2` |

## 🎯 Algorithm Comparison

### Completeness & Optimality

| Algorithm | Complete? | Optimal? | Memory | Time Complexity |
|-----------|-----------|----------|--------|-----------------|
| **DFS** | ✅ Yes (graph search) | ❌ No | O(bd) | O(b^d) |
| **BFS** | ✅ Yes | ✅ Yes (unweighted) | O(b^d) | O(b^d) |
| **UCS** | ✅ Yes | ✅ Yes | O(b^d) | O(b^d) |
| **GBFS** | ✅ Yes | ❌ No | O(b^d) | O(b^d) |
| **A*** | ✅ Yes | ✅ Yes | O(b^d) | O(b^d) |
| **IDA*** | ✅ Yes | ✅ Yes | O(bd) | O(b^d) |

*Where b = branching factor, d = depth of solution*

### When to Use Each Algorithm

**DFS** - Memory-constrained environments, finding any solution quickly
- ✅ Very memory efficient
- ❌ Not optimal, may find long paths

**BFS** - Unweighted graphs, shortest hop count
- ✅ Finds shortest path (by edges)
- ❌ High memory usage

**UCS** - Weighted graphs, need optimal cost
- ✅ Guaranteed optimal cost
- ❌ Slower than A*, high memory

**GBFS** - Need fast solutions, optimality not critical
- ✅ Very fast (goes straight toward goal)
- ❌ Can be misled by bad heuristics

**A*** - Weighted graphs, need optimal + efficient
- ✅ Optimal AND efficient with good heuristic
- ❌ High memory usage

**IDA*** - Memory-constrained, need optimal solution
- ✅ Optimal with minimal memory (O(bd))
- ❌ May revisit nodes (slower than A*)

## 📊 Test Results Summary (results might slightly differ but should be near)

Based on automated test suite results across 12 test cases:

### Memory Efficiency (Avg Nodes Created)
1. **GBFS**: 9.1 nodes ⭐ (most efficient)
2. **DFS**: 9.2 nodes
3. **A***: 9.8 nodes
4. **BFS**: 11.3 nodes
5. **UCS**: 11.3 nodes
6. **IDA***: 13.2 nodes (least efficient - due to iterative deepening)

### Path Cost (Avg Cost)
1. **UCS**: 8.7 ⭐ (always optimal)
2. **A***: 8.7 ⭐ (always optimal)
3. **IDA***: 8.7 ⭐ (always optimal)
4. **DFS**: 8.7 (sometimes optimal by luck)
5. **GBFS**: 18.0 (often suboptimal)
6. **BFS**: 18.4 (optimizes hops, not cost)

### Execution Speed (Avg Time)
1. **UCS**: 80.2ms ⭐ (fastest)
2. **GBFS**: 81.6ms
3. **IDA***: 81.6ms
4. **A***: 81.9ms
5. **BFS**: 83.9ms
6. **DFS**: 88.1ms

### Key Insights

**Optimality Results:**
- ✅ **UCS, A*, IDA***: 100% optimal (found best cost in all cases)
- ⚠️ **DFS**: ~60% optimal (depends on graph structure)
- ❌ **GBFS**: ~40% optimal (misled by heuristic in 7/12 cases)
- ❌ **BFS**: ~50% optimal (optimizes hops, not cost)

**Most Dramatic Case - Misleading Heuristic:**
```
Optimal path (DFS, UCS, A*, IDA*): 1 -> 2 -> 3 -> 5 (cost: 3.0)
BFS/GBFS path (misled):             1 -> 4 -> 5     (cost: 101.0)
                                    33.67x worse! ❌
```

**Memory Stress Case - Exponential Branching:**
```
DFS/GBFS: 8 nodes ⭐
A*: 10 nodes
IDA*: 15 nodes (revisits due to iterative deepening)
BFS/UCS: 23 nodes
Ratio: 2.88x difference
```

## 📖 Input File Format

```
Nodes:
1: (0,0)
2: (1,0)
3: (2,0)

Edges:
(1,2): 1
(2,3): 1

Origin:
1

Destinations:
3
```

- **Nodes**: `node_id: (x, y)` coordinates
- **Edges**: `(from, to): cost` (directed graph)
- **Origin**: Starting node
- **Destinations**: Semicolon-separated list of goals (e.g., `3; 5; 7`)

## 🔍 Output Formats

### Detailed Output (Default)

```bash
python search.py test_cases/test_linear.txt DFS
```

Output:
```
==================================================
File: test_cases/test_linear.txt
Search Method: DFS
==================================================
Result: SOLUTION FOUND
Goal Node: 5
Nodes Created: 5
Path: 1 -> 2 -> 3 -> 4 -> 5
Path Length: 5 nodes
==================================================
```

### Simple Output (For Submission)

```bash
python search.py test_cases/test_linear.txt DFS --simple
```

Output:
```
test_cases/test_linear.txt DFS
5 5
1 2 3 4 5
```

Format:
- Line 1: `<filename> <method>`
- Line 2: `<goal_node> <nodes_created>`
- Line 3: `<path as space-separated node IDs>`

### No Solution Output

```
test_cases/test_no_solution.txt BFS
No solution 3

```

## 🧪 Testing Guide

### Quick Test Single Algorithm

```bash
# Test DFS
python search.py test_cases/test_linear.txt DFS

# Test BFS
python search.py test_cases/test_diamond.txt BFS

# Test with simple output
python search.py test_cases/test_linear.txt AS --simple
```

### Run Complete Test Suite

```bash
python test_runner.py
```

**What it tests:**
- ✅ All 6 algorithms × 12 test cases = 72 tests
- ✅ Path correctness (goal reached)
- ✅ Path optimality (cost comparison)
- ✅ Memory efficiency (nodes created)
- ✅ Execution speed (milliseconds)
- ✅ Edge cases (no solution, cycles, long paths)

### Expected Behaviors

**All Algorithms Should:**
- ✅ Find goal in test cases 1-11 (solution exists)
- ✅ Return "No solution" for test case 12
- ✅ Handle cycles without infinite loops (visited set)
- ✅ Complete within 30 seconds

**Optimal Algorithms (UCS, A*, IDA*) Should:**
- ✅ Always find the lowest-cost path
- ✅ All return same cost (may differ in path if ties exist)

**Non-Optimal Algorithms (DFS, BFS, GBFS) Should:**
- ⚠️ May find suboptimal paths
- ⚠️ Cost can be higher than optimal

## 🛠️ Implementation Details

### SearchNode Class

```python
class SearchNode:
    current_node: int    # Current graph node ID
    path: list          # Full path from origin [origin, ..., current]
    cost: float         # Total edge cost from origin (g(n))
    hops: int          # Number of edges from origin
```

### Data Structures Used

**DFS**: Stack (Python list)
```python
stack = []
stack.append(node)  # Push
node = stack.pop()  # Pop (LIFO)
```

**BFS**: Queue (deque)
```python
from collections import deque
queue = deque()
queue.append(node)      # Enqueue
node = queue.popleft()  # Dequeue (FIFO)
```

**UCS, GBFS, A***: Priority Queue (heapq)
```python
import heapq
pq = []
heapq.heappush(pq, (priority, node_id, search_node))
priority, node_id, node = heapq.heappop(pq)
```

**IDA***: Recursive DFS with f-bound
```python
def search(node, g, bound, visited):
    f = g + h(node)
    if f > bound:
        return (None, f)  # Exceeded bound
    # ... recursive expansion
```

### Heuristic Functions

**Euclidean Distance** (used by GBFS, A*, IDA*)
```python
h(n) = sqrt((x2-x1)^2 + (y2-y1)^2)
```

**Multiple Destinations**
```python
h(n) = min(distance_to_goal_1, distance_to_goal_2, ...)
```

### Tie-Breaking Rules

When priorities are equal, expand nodes in **ascending order by node_id**.

**DFS (stack)**: Sort neighbors **descending** before pushing
```python
neighbors.sort(reverse=True, key=lambda x: x[0])
```

**BFS (queue)**: Sort neighbors **ascending** before appending
```python
neighbors.sort(key=lambda x: x[0])
```

**Priority queues**: Include `node_id` in tuple for automatic tie-breaking
```python
heapq.heappush(pq, (priority, node_id, search_node))
```

## 📈 Performance Analysis

### Test Case Highlights

**1. Misleading Heuristic** - Tests heuristic quality
- Optimal: `1 -> 2 -> 3 -> 5` (cost 3)
- GBFS/BFS misled: `1 -> 4 -> 5` (cost 101)
- Shows: Greedy algorithms can fail badly with misleading heuristics

**2. Deep vs Shallow** - Tests depth preference
- BFS finds: `1 -> 3 -> 6` (2 hops, cost 11)
- Others find: `1 -> 2 -> 4 -> 5 -> 6` (5 hops, cost 4)
- Shows: BFS optimizes hops, not cost

**3. Wide Branching** - Tests memory efficiency
- DFS: 6 nodes
- A*: 10 nodes
- BFS/UCS: 10 nodes
- IDA*: 33 nodes (iterative deepening overhead)
- Shows: Different memory usage patterns

**4. Long Path (50 nodes)** - Tests scalability
- All algorithms: 50 nodes created
- Time range: 76-92ms
- Shows: All handle long paths efficiently

## 🐛 Troubleshooting

### Common Issues

**"No module named 'collections'"**
- Solution: Use Python 3.x (not Python 2.x)

**"File not found" error**
- Solution: Run from project root directory
- Check: `test_cases/` folder exists

**Wrong node count**
- Check: Increment `nodes_created` every time you create SearchNode
- Should count ALL nodes, not just unique nodes

**Infinite loop**
- Check: Using visited set correctly
- Should check `if node in visited: continue`

**Priority queue errors**
- Check: Tuple format is `(priority, node_id, search_node)`
- `node_id` is required for tie-breaking

### Debugging Tips

```python
# Add debug prints
print(f"Exploring: {current.current_node}")
print(f"Path so far: {current.path}")
print(f"Priority: {priority}, Cost: {current.cost}")
print(f"Visited: {visited}")
```

## 🔧 Git Workflow (For Team Development)

### Initial Setup
```bash
git clone <repository-url>
cd <project-directory>
git pull origin main
```

### Feature Branch Workflow
```bash
# Create branch
git checkout -b feature/your-feature

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Descriptive message"

# Push
git push origin feature/your-feature

# Create pull request on GitHub
```

### Best Practices
- ✅ Commit frequently
- ✅ Write clear commit messages
- ✅ Test before pushing
- ✅ Pull latest changes before starting work
- ✅ Review others' code

## 📚 Additional Resources

### File Links
- [`search.py`](search.py) - Main entry point
- [`search_algorithms.py`](search_algorithms.py) - All algorithm implementations
- [`test_runner.py`](test_runner.py) - Automated test suite
- [`Guide.md`](Guide.md) - Detailed implementation guide (for team development)
- [`search_node.py`](search_node.py) - SearchNode class
- [`graph_parser.py`](graph_parser.py) - Input file parser
- [`utils.py`](utils.py) - Helper functions

### Key Concepts
- **Graph Search**: Uses visited set to avoid revisiting nodes
- **Tree Search**: No visited set (can revisit nodes)
- **Admissible Heuristic**: Never overestimates (h(n) ≤ h*(n))
- **Consistent Heuristic**: h(n) ≤ c(n,n') + h(n') for all edges
- **f(n) = g(n) + h(n)**: Total estimated cost in A*/IDA*

## 📞 Support

### Self-Help Resources
1. Check this README
2. Read [`Guide.md`](Guide.md) for detailed explanations
3. Review algorithm implementations in [`search_algorithms.py`](search_algorithms.py)
4. Run test suite to identify issues
5. Add debug prints to trace execution

### Common Questions (just putting it here)

**Q: Why does IDA* create more nodes than A*?**
A: IDA* uses iterative deepening, revisiting nodes across iterations. This trades time for memory (O(bd) instead of O(b^d)).

**Q: Why does GBFS sometimes find suboptimal paths?**
A: GBFS is greedy - it only considers heuristic h(n), not actual cost g(n). Can be misled by heuristic.

**Q: Why does BFS find different path than UCS?**
A: BFS optimizes hop count (edges), UCS optimizes total cost. Different goals → different paths.

**Q: What's the difference between CUS1 and CUS2?**
A: Assignment naming convention. CUS1 = UCS (uninformed), CUS2 = IDA* (informed).

---

## 🎯 Quick Start Commands

```bash
# Run single test
python search.py test_cases/test_linear.txt DFS

# Run all tests
python test_runner.py

# Simple output format
python search.py test_cases/test_linear.txt BFS --simple
```

---

**Project Status**: ✅ Complete
**Last Updated**: 2024
**Python Version**: 3.x required

---

**Good luck with your assignment**

For detailed implementation guidance, see [`Guide.md`](Guide.md).