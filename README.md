# Route Finding Search Algorithms - Intro to AI Assignment 2

## 📋 Project Overview

This project implements 6 tree-based search algorithms for route finding in directed graphs:
- **DFS** (Depth-First Search)
- **BFS** (Breadth-First Search)
- **UCS** (Uniform Cost Search)
- **GBFS** (Greedy Best-First Search)
- **A*** (A-Star Search)
- **IDA*** (Iterative Deepening A*)

All algorithms use **GRAPH SEARCH** with a visited set to avoid revisiting nodes.

## 🗂️ Project Structure

```
project/
├── search.py              # Main entry point (✅ COMPLETE - DO NOT MODIFY)
├── search_node.py         # SearchNode class (✅ COMPLETE - DO NOT MODIFY)
├── graph_parser.py        # Input file parser (✅ COMPLETE - DO NOT MODIFY)
├── utils.py               # Helper functions (✅ COMPLETE - DO NOT MODIFY)
├── search_algorithms.py   # 🎯 IMPLEMENT YOUR ALGORITHMS HERE
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── test_cases/
    └── PathFinder-test.txt
```

## 🚀 How to Run

```bash
python search.py <filename> <method>
```

### Examples

```bash
python search.py PathFinder-test.txt DFS
python search.py PathFinder-test.txt BFS
python search.py PathFinder-test.txt UCS
python search.py PathFinder-test.txt GBFS
python search.py PathFinder-test.txt AS
python search.py PathFinder-test.txt CUS2
```

## 🔤 Algorithm Method Names

| Method Name | Algorithm | Alternative Name |
|-------------|-----------|------------------|
| `DFS` | Depth-First Search | - |
| `BFS` | Breadth-First Search | - |
| `UCS` | Uniform Cost Search | `CUS1` |
| `GBFS` | Greedy Best-First Search | - |
| `AS` | A* Search | `ASTAR` |
| `IDA*` | Interative Deepning A* Search | `CUS2` |

## 👥 Team Member Assignments

### ✅ Lawrence: DFS (COMPLETED)
- **File**: `search_algorithms.py`
- **Function**: `search_dfs()`
- **Status**: ✅ Fully implemented as reference example

### 🔨 Jason: BFS
- **File**: `search_algorithms.py`
- **Function**: `search_bfs()`
- **What to do**: Follow the detailed pseudocode in the function
- **Key points**: 
  - Use `collections.deque` (FIFO queue)
  - Sort neighbors ascending by node_id
  - Mark visited AFTER dequeuing

### 🔨 Elyn: UCS and GBFS
- **File**: `search_algorithms.py`
- **Functions**: `search_ucs()` and `search_gbfs()`
- **What to do**: Follow the detailed pseudocode in both functions
- **Key points**:
  - **UCS**: Priority = g(n) = total cost from origin
  - **GBFS**: Priority = h(n) = Euclidean distance to goal
  - Use `heapq` with format `(priority, node_id, search_node)`

### 🔨 Faisal: A* and IDA*
- **File**: `search_algorithms.py`
- **Functions**: `search_astar()` and `search_ida_star()`
- **What to do**: Follow the detailed pseudocode in both functions
- **Key points**:
  - **A***: Priority = f(n) = g(n) + h(n)
  - **IDA***: Uses recursive DFS with f-bound, memory efficient O(bd)

## 📚 Implementation Guide

### What's Already Done For You ✅

1. ✅ **File parsing** ([`graph_parser.py`](graph_parser.py))
   - Parses nodes, edges, origin, destinations
   - Returns graph as adjacency list

2. ✅ **SearchNode class** ([`search_node.py`](search_node.py))
   - Stores: current_node, path, cost, hops
   - Implements `__lt__` for priority queue tie-breaking

3. ✅ **Helper functions** ([`utils.py`](utils.py))
   - `euclidean_distance()` - calculates distance between points
   - `get_heuristic()` - calculates heuristic values
   - `get_closest_destination_heuristic()` - for multiple destinations
   - `format_output()` - prints results in required format

4. ✅ **Command-line interface** ([`search.py`](search.py))
   - Parses arguments
   - Calls appropriate search function
   - Handles errors

5. ✅ **DFS implementation** ([`search_algorithms.py`](search_algorithms.py))
   - Fully working example with detailed comments
   - Use as reference for your implementations

### What Each of You Need To Do 🎯

1. **Open** [`search_algorithms.py`](search_algorithms.py)
2. **Find** your assigned function (e.g., `search_bfs()`)
3. **Read** the detailed pseudocode in the comments
4. **Implement** the algorithm following the pseudocode
5. **Test** with: `python search.py PathFinder-test.txt <YOUR_METHOD>`

### Key Implementation Points

#### General Rules (ALL Algorithms)
- ✅ Use **GRAPH SEARCH** with `visited` set
- ✅ Count **ALL nodes created** (increment when creating `SearchNode`)
- ✅ Return format: `(goal_node, nodes_created, path)`
- ✅ If no solution: `(None, nodes_created, [])`
- ✅ Goal test AFTER popping from frontier (not when creating nodes)

#### Data Structures

**Stack (DFS)**
```python
stack = []
stack.append(node)  # Push
node = stack.pop()  # Pop (LIFO)
```

**Queue (BFS)**
```python
from collections import deque
queue = deque()
queue.append(node)      # Enqueue
node = queue.popleft()  # Dequeue (FIFO)
```

**Priority Queue (UCS, GBFS, A*)**
```python
import heapq
pq = []
heapq.heappush(pq, (priority, node_id, search_node))
priority, node_id, node = heapq.heappop(pq)
```

**Recursive DFS (IDA*):**

### SearchNode Creation
```python
def search_ida_star(...):
    bound = initial_heuristic
    
    # Recursive helper function
    def search(node, g, bound, visited):
        nonlocal nodes_created  # ← Important!
        
        f = g + h(node)
        
        # Base case 1: Exceeded bound
        if f > bound:
            return (None, f)
        
        # Base case 2: Found goal
        if is_goal(node):
            return (node, None)
        
        # Recursive case: Try all neighbors
        min_over = float('inf')
        for neighbor in neighbors:
            visited.add(neighbor)
            result, new_bound = search(neighbor, g + cost, bound, visited)
            visited.remove(neighbor)  # ← Backtrack!
            
            if result:
                return (result, None)
            
            if new_bound < min_over:
                min_over = new_bound
        
        return (None, min_over)
    
    # Iterative deepening loop
    while True:
        result, new_bound = search(initial, 0, bound, visited)
        if result:
            return result
        if new_bound == float('inf'):
            return None  # No solution
        bound = new_bound  # Increase bound
```

#### Tie-Breaking

When priorities are equal, expand nodes in **ascending order by node_id**.

**For DFS (stack)**: Sort neighbors **descending** before pushing
```python
neighbors.sort(reverse=True, key=lambda x: x[0])
```

**For BFS (queue)**: Sort neighbors **ascending** before appending
```python
neighbors.sort(key=lambda x: x[0])
```

**For priority queues**: Include `node_id` in tuple
```python
heapq.heappush(pq, (priority, node_id, search_node))
# heapq automatically uses node_id for tie-breaking
```

#### Creating Search Nodes

```python
new_node = SearchNode(
    current_node=neighbor_id,
    path=current.path + [neighbor_id],
    cost=current.cost + edge_cost,
    hops=current.hops + 1
)
nodes_created += 1  # Always increment!
```

#### Using Helper Functions

**Calculate heuristic to closest destination:**
```python
from utils import get_closest_destination_heuristic

h = get_closest_destination_heuristic(
    node_coords, 
    current_node, 
    destinations, 
    'euclidean'  # or 'hop_estimate'
)
```

### Algorithm-Specific Notes

#### BFS
- Use `deque` for O(1) append and popleft
- Guaranteed shortest path (in terms of edges)

#### UCS
- Priority = `g(n)` = total cost from origin
- Guaranteed optimal path (lowest cost)

#### GBFS
- Priority = `h(n)` = Euclidean distance to goal
- Fast but not optimal

#### A*
- Priority = `f(n) = g(n) + h(n)`
- Optimal with admissible heuristic
- Euclidean distance is admissible

#### IDA*
- Uses recursive DFS with f(n) = g(n) + h(n) bounds
- Memory efficient: O(bd) instead of A*'s O(b^d)
- Optimal with admissible heuristic
- **IMPORTANT**: No priority queue - uses recursion and backtracking
- May create more nodes than A* (revisits across iterations)
- Best for memory-constrained environments

## 🧪 Testing Your Algorithm

### Basic Test
```bash
python search.py PathFinder-test.txt BFS
```

### Expected Output Format
```
PathFinder-test.txt BFS
5 42
2 3 5
```

Where:
- Line 1: `<filename> <method>`
- Line 2: `<goal_node> <nodes_created>`
- Line 3: `<path as space-separated node IDs>`

### If No Solution Exists
```
PathFinder-test.txt BFS
No solution 15

```

### Debugging Tips

1. **Add print statements** to see what's happening:
```python
print(f"Expanding node: {current.current_node}")
print(f"Priority: {priority}, Path: {current.path}")
```

2. **Check your node count**:
```python
print(f"Nodes created so far: {nodes_created}")
```

3. **Verify visited set**:
```python
print(f"Visited: {visited}")
```

4. **Compare with DFS**:
   - Run DFS first to see expected behavior
   - Your algorithm should follow similar structure

## 🐛 Common Issues and Solutions

### Issue: Priority Queue Error
```
TypeError: '<' not supported between instances of 'SearchNode'
```
**Solution**: Make sure you're using the tuple format: `(priority, node_id, search_node)`

### Issue: Wrong Path
**Solution**: Check that you're building the path correctly:
```python
new_path = current.path + [neighbor_id]  # Extend the path
```

### Issue: Infinite Loop
**Solution**: Make sure you're using the visited set:
```python
if neighbor_id in visited:
    continue
```

### Issue: Wrong Node Count
**Solution**: Increment `nodes_created` EVERY time you create a SearchNode:
```python
new_node = SearchNode(...)
nodes_created += 1  # Don't forget this!
```

### Issue: No Solution Found (But Should Exist)
**Solution**: 
- Check goal test is AFTER popping, not when creating
- Make sure you're not skipping reachable nodes

## 📖 Input File Format

```
Nodes:
1: (4,1)
2: (2,2)
3: (5,3)

Edges:
(2,1): 4
(3,1): 5
(2,3): 2

Origin:
2

Destinations:
5; 4
```

- **Nodes**: `node_id: (x, y)` coordinates
- **Edges**: `(from, to): cost` (directed!)
- **Origin**: Starting node
- **Destinations**: Semicolon-separated list of goals

## 🔧 Git Workflow

### Getting Started
```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Get latest code
git pull origin main
```

### Working on Your Algorithm
```bash
# Create your feature branch
git checkout -b feature/your-algorithm

# Example:
git checkout -b feature/bfs
git checkout -b feature/ucs-gbfs
```

### Committing Your Work
```bash
# Check what files changed
git status

# Add your changes
git add search_algorithms.py

# Commit with descriptive message
git commit -m "Implement BFS algorithm"

# Push to your branch
git push origin feature/your-algorithm
```

### Creating Pull Request
1. Go to GitHub
2. Click "New Pull Request"
3. Select your branch
4. Add description of what you implemented
5. Request review from team leader

### Best Practices
- ✅ Commit often (after each working milestone)
- ✅ Write clear commit messages
- ✅ Test before pushing
- ✅ Don't modify files outside your responsibility
- ✅ Pull latest changes before starting work

## 📝 Code Style Guidelines

- Use **4 spaces** for indentation (not tabs)
- Keep lines under **100 characters** when possible
- Add **comments** to explain complex logic
- Use **meaningful variable names**
- Follow the **style of the DFS implementation**

## 🆘 Need Help?

1. **Check the DFS implementation** in [`search_algorithms.py`](search_algorithms.py) as reference
2. **Review pseudocode** in your assigned function
3. **Test with print statements** to debug
4. **Ask team leader** if stuck
5. **Discuss with teammates** - you're not alone!

## 📌 Quick Reference

### SearchNode Attributes
- `current_node` (int): Current graph node ID
- `path` (list): Full path from origin [origin, ..., current]
- `cost` (float): Total edge cost from origin
- `hops` (int): Number of edges from origin

### Return Format
```python
return (goal_node, nodes_created, path)
# or if no solution:
return (None, nodes_created, [])
```

### Priority Queue Format
```python
heapq.heappush(pq, (priority, node_id, search_node))
```

---

## 🎯 Success Checklist (TAKE NOTE)

Before submitting your pull request:

- [ ] Algorithm follows the pseudocode structure
- [ ] Uses GRAPH SEARCH with visited set
- [ ] Counts ALL nodes created
- [ ] Returns correct format: `(goal, nodes_created, path)`
- [ ] Handles "no solution" case
- [ ] Tie-breaking by node_id works correctly
- [ ] Tested with at least one input file
- [ ] Code has comments explaining key steps
- [ ] No modifications to other files
- [ ] Committed with clear message
- [ ] Pull request created

---

**God Bless Us! 🚀**

Remember: The foundation is complete. Each of you just need to implement the search logic following the detailed pseudocode. If you can implement one algorithm, you can implement them all - they essentially follow the same structure with different priority calculations.