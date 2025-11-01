# 🚀 Team Implementation Guide - Route Finding Algorithms

**Last Updated:** November 2025
**Team Leader:** Lawrence Lian Anak Matius Ding
**Project:** AI Search Algorithms Assignment

---

## 📊 Quick Status Overview

| Team Member | Algorithm(s) | Status | File Location |
|-------------|-------------|--------|---------------|
| **Me (Team Leader)** | DFS | ✅ COMPLETE (Reference) | [`search_algorithms.py`](search_algorithms.py) line 7 |
| **Jason** | BFS | ✅ COMPLETE | [`search_algorithms.py`](search_algorithms.py) line 113 |
| **Elyn** | UCS + GBFS | ✅ COMPLETE | [`search_algorithms.py`](search_algorithms.py) lines 170, 227 |
| **Faisal** | A* + IDA* | ✅ COMPLETE | [`search_algorithms.py`](search_algorithms.py) lines 290, 420 |

**Project Status:** **ALL ALGORITHMS COMPLETE**  
**Test Suite:** **72/72 Tests Passing**  
**Documentation:** **Complete**

---

## 🎯 Algorithm Summary

### Uninformed Search (No Heuristic)
1. **DFS** - Stack, goes deep first, memory-efficient
2. **BFS** - Queue, explores level by level, shortest hop count
3. **UCS** - Priority queue by cost, finds cheapest path

### Informed Search (Uses Heuristic)
4. **GBFS** - Priority queue by h(n), greedy toward goal, fast but not optimal
5. **A*** - Priority queue by f(n)=g(n)+h(n), optimal and efficient
6. **IDA*** - Iterative deepening with f-limit, optimal with minimal memory

---

## 🆕 What's New

### Latest Updates
- ✅ **All 6 algorithms implemented and tested**
- ✅ **Automated test suite ([`test_runner.py`](test_runner.py))** - Run all 72 tests automatically
- ✅ **12 comprehensive test cases** covering all edge cases
- ✅ **Updated README** with test results and performance analysis
- ✅ **Path cost calculation** in test runner output
- ✅ **Detailed performance comparison** across all algorithms

### New Features
1. **Automated Testing:** Run `python test_runner.py` to test all algorithms on all cases
2. **Path Cost Display:** See actual path costs in test results
3. **Performance Metrics:** Average nodes, costs, and execution times
4. **Optimality Analysis:** Identifies which algorithms found optimal paths

---

## 🎯 Quick Start (For New Team Members)

### If You're Just Starting

1. **Read the README first:** [`README.md`](README.md) has the big picture
2. **Test the complete DFS implementation:**
   ```bash
   python search.py test_cases/test_linear.txt DFS
   ```
3. **Run the test suite to see what "done" looks like:**
   ```bash
   python test_runner.py
   ```
4. **Follow the implementation guide below** for your assigned algorithm

### What You Need to Do

**90% of the work is already done!** You just need to:
1. Open [`search_algorithms.py`](search_algorithms.py)
2. Find your function (search for your name in comments)
3. Translate the detailed pseudocode to Python
4. Test with provided test cases

### The Files You DON'T Touch
❌ **DO NOT MODIFY THESE FILES:**
- [`search.py`](search.py) - Main program (complete)
- [`graph_parser.py`](graph_parser.py) - File parser (complete)
- [`search_node.py`](search_node.py) - SearchNode class (complete)
- [`utils.py`](utils.py) - Helper functions (complete)
- [`test_runner.py`](test_runner.py) - Test suite (complete)

### The ONE File You Edit
✅ **ONLY EDIT THIS FILE:**
- [`search_algorithms.py`](search_algorithms.py) - Your algorithm implementations

---

## 📖 Understanding the Project Structure

### Complete File Overview

```
project/
├── search.py              # Main entry point - handles CLI
├── search_node.py         # SearchNode class definition
├── graph_parser.py        # Parses input files
├── utils.py               # Helper functions (heuristics, formatting)
├── search_algorithms.py   # ✅ YOUR WORKSPACE - All 6 algorithms
├── test_runner.py         # Automated test suite (NEW!)
├── Guide.md               # This file - implementation guide
├── README.md              # User documentation
├── .gitignore            # Git ignore rules
└── test_cases/
    ├── test_linear.txt        # Simple baseline (5 nodes)
    ├── test_diamond.txt       # Multiple paths (4 nodes)
    ├── test_wide.txt          # Branching factor test (8 nodes)
    ├── test_depth.txt         # DFS depth preference (6 nodes)
    ├── test_misleading.txt    # Heuristic quality test (5 nodes)
    ├── test_multi_destin.txt  # Multiple goals (6 nodes)
    ├── test_sparse.txt        # Long linear path (10 nodes)
    ├── test_obstacle.txt      # Grid pathfinding (8 nodes)
    ├── test_no_solution.txt   # Unreachable goal (no solution)
    ├── test_cycle.txt         # Cycle handling (4 nodes)
    ├── test_exponential.txt   # Memory stress test (16 nodes)
    └── test_long_path.txt     # Deep search (50 nodes)
```

### How Everything Connects

```
User runs: python search.py test_cases/test_linear.txt BFS
                    ↓
            search.py (main entry point)
                    ↓
            Parses: filename="test_cases/test_linear.txt", method="BFS"
                    ↓
            graph_parser.py reads file
                    ↓
            Returns: graph, node_coords, origin, destinations
                    ↓
            search.py calls: search_bfs(graph, node_coords, origin, destinations)
                    ↓
            Your BFS algorithm runs in search_algorithms.py
                    ↓
            Returns: (goal_node, nodes_created, path)
                    ↓
            utils.py formats and prints results
```

---

## 🎓 Step-by-Step Implementation Guide

### STEP 1: Understand SearchNode Class

**Every algorithm uses SearchNode** - it's already implemented in [`search_node.py`](search_node.py):

```python
class SearchNode:
    current_node: int    # Current graph node ID
    path: list          # Full path from origin [origin, ..., current]
    cost: float         # Total edge cost from origin (g(n))
    hops: int          # Number of edges from origin
```

**Creating a SearchNode:**
```python
node = SearchNode(
    current_node=5,           # Which node we're at
    path=[1, 3, 5],          # How we got here
    cost=10.5,               # Total cost so far
    hops=2                   # Number of edges traversed
)
```

### STEP 2: Read the Complete DFS Implementation

**Location:** [`search_algorithms.py`](search_algorithms.py) lines 7-110

This is your **reference implementation** - study it carefully!

**Key patterns to notice:**
```python
# 1. Initialize data structure
stack = []

# 2. Create initial node
initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
stack.append(initial_node)
nodes_created = 1  # Count every SearchNode you create!

# 3. Initialize visited set (GRAPH SEARCH)
visited = set()

# 4. Main loop
while stack:
    current = stack.pop()
    
    # 5. Goal test (check AFTER popping)
    if current.current_node in destinations:
        return (current.current_node, nodes_created, current.path)
    
    # 6. Skip if visited (prevents cycles)
    if current.current_node in visited:
        continue
    
    # 7. Mark as visited
    visited.add(current.current_node)
    
    # 8. Expand neighbors
    neighbors = graph.get(current.current_node, [])
    
    for neighbor_id, edge_cost in neighbors:
        if neighbor_id in visited:
            continue  # Skip visited neighbors
        
        # 9. Create child node
        new_node = SearchNode(
            current_node=neighbor_id,
            path=current.path + [neighbor_id],  # Extend path
            cost=current.cost + edge_cost,      # Accumulate cost
            hops=current.hops + 1               # Increment hops
        )
        
        stack.append(new_node)
        nodes_created += 1  # Count it!

# 10. No solution found
return (None, nodes_created, [])
```

### STEP 3: Understand Your Algorithm's Differences

All algorithms follow the **same structure** but differ in:

1. **Data structure used** (stack vs queue vs priority queue)
2. **Order of expansion** (LIFO vs FIFO vs priority-based)
3. **Priority calculation** (none vs cost vs heuristic vs f-value)

| Algorithm | Data Structure | Priority | Expansion Order |
|-----------|---------------|----------|-----------------|
| DFS | Stack (list) | None | LIFO - last added first |
| BFS | Queue (deque) | None | FIFO - first added first |
| UCS | Priority Queue (heapq) | g(n) | Lowest cost first |
| GBFS | Priority Queue (heapq) | h(n) | Closest to goal first |
| A* | Priority Queue (heapq) | f(n)=g(n)+h(n) | Lowest f-value first |
| IDA* | Recursive DFS | f(n) bound | DFS within bound |

---

## 👤 Detailed Algorithm Implementation Guides

### 🔵 BFS (Breadth-First Search)

**Implementer:** Jason  
**Status:** ✅ COMPLETE  
**Location:** [`search_algorithms.py`](search_algorithms.py) line 113

**Key Differences from DFS:**
- Uses **queue (deque)** instead of stack
- `queue.append()` to add (same as stack)
- `queue.popleft()` to remove (FIFO instead of LIFO)
- Sort neighbors **ascending** (not descending like DFS)

**Complete Implementation:**
```python
def search_bfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    # Initialize queue (FIFO)
    queue = deque()
    
    # Create and enqueue initial node
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    queue.append(initial_node)
    nodes_created = 1
    
    # Visited set for GRAPH SEARCH
    visited = set()
    
    # Main loop
    while queue:
        # Dequeue oldest node (FIFO)
        current = queue.popleft()
        
        # Goal test
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
        # Skip if visited
        if current.current_node in visited:
            continue
        
        # Mark as visited
        visited.add(current.current_node)
        
        # Get and sort neighbors (ascending for BFS)
        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(nid, cost) for nid, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])  # Ascending
        
        # Expand neighbors
        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )
            
            queue.append(new_node)
            nodes_created += 1
    
    # No solution
    return (None, nodes_created, [])
```

**Test:**
```bash
python search.py test_cases/test_linear.txt BFS
python search.py test_cases/test_diamond.txt BFS --simple
```

---

### 🟢 UCS (Uniform Cost Search)

**Implementer:** Elyn  
**Status:** ✅ COMPLETE  
**Location:** [`search_algorithms.py`](search_algorithms.py) line 170

**Key Differences from BFS:**
- Uses **priority queue (heapq)** instead of queue
- Priority = **g(n)** (total cost from origin)
- Always expands **lowest-cost** node first
- Tuple format: `(priority, node_id, search_node)`

**Complete Implementation:**
```python
def search_ucs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    # Initialize priority queue
    priority_queue = []
    
    # Create initial node and push with priority=0
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (0, origin, initial_node))
    nodes_created = 1
    
    # Visited set
    visited = set()
    
    # Main loop
    while priority_queue:
        # Pop node with lowest cost
        priority, node_id, current = heapq.heappop(priority_queue)
        
        # Goal test
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
        # Skip if visited
        if current.current_node in visited:
            continue
        
        # Mark visited
        visited.add(current.current_node)
        
        # Expand neighbors
        neighbors = graph.get(current.current_node, [])
        for neighbor_id, edge_cost in neighbors:
            if neighbor_id in visited:
                continue
            
            # Calculate g(n) = cost so far
            new_cost = current.cost + edge_cost
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=new_cost,
                hops=current.hops + 1
            )
            
            # Push with cost as priority
            heapq.heappush(priority_queue, (new_cost, neighbor_id, new_node))
            nodes_created += 1
    
    return (None, nodes_created, [])
```

**Test:**
```bash
python search.py test_cases/test_diamond.txt UCS
python search.py test_cases/test_depth.txt UCS
```

---

### 🟢 GBFS (Greedy Best-First Search)

**Implementer:** Elyn  
**Status:** ✅ COMPLETE  
**Location:** [`search_algorithms.py`](search_algorithms.py) line 227

**Key Differences from UCS:**
- Priority = **h(n)** (heuristic only, not cost!)
- Uses `get_closest_destination_heuristic()` helper
- Greedy - goes straight toward goal
- Not optimal - can be misled by bad heuristics

**Complete Implementation:**
```python
def search_gbfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    # Initialize priority queue
    priority_queue = []
    
    # Calculate initial heuristic
    h_value = get_closest_destination_heuristic(
        node_coords, origin, destinations, 'euclidean'
    )
    
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (h_value, origin, initial_node))
    nodes_created = 1
    
    visited = set()
    
    while priority_queue:
        h_priority, node_id, current = heapq.heappop(priority_queue)
        
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
        if current.current_node in visited:
            continue
        
        visited.add(current.current_node)
        
        neighbors = graph.get(current.current_node, [])
        for neighbor_id, edge_cost in neighbors:
            if neighbor_id in visited:
                continue
            
            # Calculate heuristic for neighbor
            h_neighbor = get_closest_destination_heuristic(
                node_coords, neighbor_id, destinations, 'euclidean'
            )
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )
            
            # Priority is heuristic only
            heapq.heappush(priority_queue, (h_neighbor, neighbor_id, new_node))
            nodes_created += 1
    
    return (None, nodes_created, [])
```

**Test:**
```bash
python search.py test_cases/test_misleading.txt GBFS  # Will find suboptimal path!
python search.py test_cases/test_wide.txt GBFS
```

---

### 🟣 A* (A-Star Search)

**Implementer:** Faisal  
**Status:** ✅ COMPLETE  
**Location:** [`search_algorithms.py`](search_algorithms.py) line 290

**Key Features:**
- Priority = **f(n) = g(n) + h(n)**
- g(n) = actual cost from origin (like UCS)
- h(n) = heuristic to goal (like GBFS)
- **Combines best of both** - optimal AND efficient!

**Complete Implementation:**
```python
def search_astar(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    priority_queue = []
    
    # Calculate initial f(n) = g(n) + h(n)
    g_value = 0
    h_value = get_closest_destination_heuristic(
        node_coords, origin, destinations, 'euclidean'
    )
    f_value = g_value + h_value
    
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (f_value, origin, initial_node))
    nodes_created = 1
    
    visited = set()
    
    while priority_queue:
        f_priority, node_id, current = heapq.heappop(priority_queue)
        
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
        if current.current_node in visited:
            continue
        
        visited.add(current.current_node)
        
        neighbors = graph.get(current.current_node, [])
        for neighbor_id, edge_cost in neighbors:
            if neighbor_id in visited:
                continue
            
            # Calculate g(n) and h(n)
            g_value = current.cost + edge_cost
            h_value = get_closest_destination_heuristic(
                node_coords, neighbor_id, destinations, 'euclidean'
            )
            f_value = g_value + h_value  # f(n) = g(n) + h(n)
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=g_value,  # Store g(n)
                hops=current.hops + 1
            )
            
            heapq.heappush(priority_queue, (f_value, neighbor_id, new_node))
            nodes_created += 1
    
    return (None, nodes_created, [])
```

**Test:**
```bash
python search.py test_cases/test_misleading.txt AS  # Should find optimal path!
python search.py test_cases/test_exponential.txt AS
```

---

### 🟣 IDA* (Iterative Deepening A*)

**Implementer:** Faisal  
**Status:** ✅ COMPLETE  
**Location:** [`search_algorithms.py`](search_algorithms.py) line 420

**Key Features:**
- Uses **recursive DFS** (NOT priority queue!)
- f-value bound increases iteratively
- Memory: O(bd) instead of A*'s O(b^d)
- Still optimal with admissible heuristic
- May revisit nodes (trades time for space)

**Complete Implementation:**
```python
def search_ida_star(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    nodes_created = 1
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    
    # Initial bound = heuristic at start
    bound = get_closest_destination_heuristic(
        node_coords, origin, destinations, 'euclidean'
    )
    
    # Recursive DFS helper
    def search(node: SearchNode, g_value: float, bound: float, visited: set) -> tuple:
        nonlocal nodes_created  # Important for counting!
        
        # Calculate f(n) = g(n) + h(n)
        h_value = get_closest_destination_heuristic(
            node_coords, node.current_node, destinations, 'euclidean'
        )
        f_value = g_value + h_value
        
        # Exceeded bound - don't expand
        if f_value > bound:
            return (None, f_value)
        
        # Goal test
        if node.current_node in destinations:
            return (node, None)
        
        min_over = float('inf')
        
        # Get and sort neighbors
        neighbors = graph.get(node.current_node, [])
        neighbor_list = [(nid, cost) for nid, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])
        
        # Try each neighbor recursively
        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue
            
            # Create new node
            new_node = SearchNode(
                current_node=neighbor_id,
                path=node.path + [neighbor_id],
                cost=node.cost + edge_cost,
                hops=node.hops + 1
            )
            nodes_created += 1
            
            # Recursive call
            visited.add(neighbor_id)
            result, new_bound = search(new_node, g_value + edge_cost, bound, visited)
            visited.remove(neighbor_id)  # Backtrack!
            
            if result is not None:
                return (result, None)
            
            if new_bound < min_over:
                min_over = new_bound
        
        return (None, min_over)
    
    # Iterative deepening loop
    while True:
        visited = {origin}
        result, new_bound = search(initial_node, 0, bound, visited)
        
        if result is not None:
            return (result.current_node, nodes_created, result.path)
        
        if new_bound == float('inf'):
            return (None, nodes_created, [])
        
        bound = new_bound  # Increase bound
```

**Test:**
```bash
python search.py test_cases/test_linear.txt IDASTAR
python search.py test_cases/test_wide.txt IDASTAR  # Creates more nodes than A*
```

---

## 🧪 Complete Testing Guide

### Level 1: Individual Algorithm Testing

**Test each algorithm on simple cases first:**

```bash
# Test DFS (reference)
python search.py test_cases/test_linear.txt DFS

# Test your algorithm
python search.py test_cases/test_linear.txt BFS
python search.py test_cases/test_linear.txt UCS
python search.py test_cases/test_linear.txt GBFS
python search.py test_cases/test_linear.txt AS
python search.py test_cases/test_linear.txt IDASTAR
```

### Level 2: Test All Cases

**Test on all 12 test cases manually:**

```bash
# Loop through all test cases
for test in test_cases/*.txt; do
    echo "Testing $test with BFS..."
    python search.py "$test" BFS
done
```

### Level 3: Automated Test Suite

**Run the comprehensive test suite:**

```bash
python test_runner.py
```

**This will:**
- Run all 6 algorithms on all 12 test cases (72 tests)
- Show results in organized tables
- Display path costs and nodes created
- Compare performance metrics
- Generate summary statistics

**Expected output:**
```
============================================================================================================================
                                            SEARCH ALGORITHM TEST REPORT
============================================================================================================================

Running 12 test cases with 6 algorithms
Total: 72 tests

============================================================================================================================
Test: Linear Path - Simple baseline
============================================================================================================================
Algo     | Goal   | Nodes  | Cost    | Time     | Path
------------------------------------------------------------------------------------------------------------------------
DFS      | 5      | 5      | 4.0     | 83.7ms   | 1 -> 2 -> 3 -> 4 -> 5                    [OK]
BFS      | 5      | 5      | 4.0     | 80.1ms   | 1 -> 2 -> 3 -> 4 -> 5                    [OK]
UCS      | 5      | 5      | 4.0     | 79.2ms   | 1 -> 2 -> 3 -> 4 -> 5                    [OK]
...

[Summary Statistics showing performance comparison]
```

### Level 4: Specific Edge Case Testing

**Test critical cases:**

```bash
# Test with no solution
python search.py test_cases/test_no_solution.txt BFS

# Test with cycles
python search.py test_cases/test_cycle.txt DFS

# Test misleading heuristic (GBFS should fail)
python search.py test_cases/test_misleading.txt GBFS  # Suboptimal
python search.py test_cases/test_misleading.txt AS    # Optimal

# Test deep search
python search.py test_cases/test_long_path.txt IDASTAR
```

### Level 5: Output Format Testing

**Test simple output format (for submission):**

```bash
python search.py test_cases/test_linear.txt BFS --simple
```

**Expected:**
```
test_cases/test_linear.txt BFS
5 5
1 2 3 4 5
```

---

## 🐛 Common Issues and Solutions

### Issue 1: Wrong Node Count

**Problem:** `nodes_created` doesn't match expected value

**Solution:**
```python
# ❌ Wrong - only counting when adding to data structure
if neighbor_id not in visited:
    new_node = SearchNode(...)
    nodes_created += 1  # Only counts non-visited

# ✅ Correct - count EVERY SearchNode created
new_node = SearchNode(...)
nodes_created += 1  # Always increment
if neighbor_id not in visited:
    queue.append(new_node)
```

### Issue 2: Infinite Loop

**Problem:** Algorithm never terminates

**Checklist:**
```python
# ✅ Check 1: Are you using visited set?
visited = set()

# ✅ Check 2: Are you checking before expanding?
if current.current_node in visited:
    continue

# ✅ Check 3: Are you marking as visited?
visited.add(current.current_node)

# ✅ Check 4: Are you checking neighbors?
for neighbor_id, edge_cost in neighbors:
    if neighbor_id in visited:
        continue  # Skip visited neighbors
```

### Issue 3: Priority Queue Errors

**Problem:** `TypeError: '<' not supported between instances of 'SearchNode'`

**Solution:**
```python
# ❌ Wrong - missing node_id for tie-breaking
heapq.heappush(pq, (priority, search_node))

# ✅ Correct - include node_id
heapq.heappush(pq, (priority, node_id, search_node))
```

### Issue 4: Path Not Building Correctly

**Problem:** All nodes have same path or path gets modified

**Solution:**
```python
# ❌ Wrong - modifies original path
new_path = current.path
new_path.append(neighbor_id)  # Modifies current.path!

# ✅ Correct - creates new list
new_path = current.path + [neighbor_id]
```

### Issue 5: Goal Test in Wrong Place

**Problem:** Solution not found even though it exists

**Solution:**
```python
# ❌ Wrong - testing before adding to data structure
for neighbor in neighbors:
    if neighbor in destinations:  # Too early!
        return ...

# ✅ Correct - test after popping from data structure
while queue:
    current = queue.popleft()
    if current.current_node in destinations:  # Right place!
        return ...
```

### Issue 6: IDA* Specific - `nodes_created` Not Updating

**Problem:** Node count stuck at initial value

**Solution:**
```python
# ❌ Wrong - forgot nonlocal
def search(node, g, bound, visited):
    nodes_created += 1  # Error! Can't modify outer variable

# ✅ Correct - use nonlocal
def search(node, g, bound, visited):
    nonlocal nodes_created  # Important!
    nodes_created += 1
```

### Issue 7: Heuristic Not Working

**Problem:** A*/GBFS/IDA* behaving like uninformed search

**Solution:**
```python
# ❌ Wrong - not using helper function
h_value = 0  # No heuristic!

# ✅ Correct - use provided helper
h_value = get_closest_destination_heuristic(
    node_coords, 
    neighbor_id, 
    destinations, 
    'euclidean'
)
```

---

## 📊 Performance Expectations (result may slightly differ but should be around)

### Expected Results by Test Case

Based on test suite results:

**test_linear.txt (Simple Path)**
- All algorithms: 5 nodes, cost 4.0
- Reason: Only one path exists

**test_misleading.txt (Critical Test!)**
- Optimal (UCS, A*, IDA*): cost 3.0, path `1->2->3->5`
- Suboptimal (BFS, GBFS): cost 101.0, path `1->4->5`
- DFS: Depends on expansion order
- **This shows heuristic can mislead!**

**test_wide.txt (Branching)**
- DFS/GBFS: ~6 nodes (memory efficient)
- BFS/UCS/A*: ~10 nodes
- IDA*: ~33 nodes (revisits due to iterative deepening)

**test_exponential.txt (Memory Stress)**
- DFS/GBFS: ~8 nodes (most efficient)
- A*: ~10 nodes
- BFS/UCS: ~23 nodes (least efficient)

### Memory Efficiency Ranking

1. **GBFS**: 9.1 nodes avg ⭐
2. **DFS**: 9.2 nodes avg
3. **A***: 9.8 nodes avg
4. **BFS/UCS**: 11.3 nodes avg
5. **IDA***: 13.2 nodes avg (creates more due to revisits, but uses less memory at once!)

### Optimality Ranking

1. **UCS/A*/IDA***: 100% optimal ⭐⭐⭐
2. **DFS**: ~60% optimal
3. **BFS**: ~50% optimal (optimizes hops, not cost)
4. **GBFS**: ~40% optimal (can be misled)

### Speed Ranking (Average)

1. **UCS**: 80.2ms ⭐
2. **GBFS**: 81.6ms
3. **IDA***: 81.6ms
4. **A***: 81.9ms
5. **BFS**: 83.9ms
6. **DFS**: 88.1ms

---

## ✅ Pre-Submission Checklist

Before submitting, verify ALL of these:

### Code Quality
- [ ] No syntax errors
- [ ] No runtime errors
- [ ] No infinite loops
- [ ] No hardcoded test values
- [ ] No debug print statements left in code
- [ ] Proper indentation and formatting
- [ ] Comments explain key logic

### Algorithm Correctness
- [ ] Uses correct data structure (stack/queue/pq/recursive)
- [ ] Increments `nodes_created` for EVERY SearchNode
- [ ] Uses visited set correctly (check, skip, add)
- [ ] Builds paths correctly (creates new list, doesn't modify)
- [ ] Returns correct format: `(goal, nodes_created, path)`
- [ ] Handles "no solution" case: `(None, nodes_created, [])`
- [ ] Goal test in correct location (after popping)
- [ ] Tie-breaking works (ascending node_id)

### Testing
- [ ] Tested with `test_linear.txt` ✅
- [ ] Tested with `test_diamond.txt` ✅
- [ ] Tested with `test_misleading.txt` ✅
- [ ] Tested with `test_no_solution.txt` ✅
- [ ] Tested with `test_cycle.txt` ✅
- [ ] Tested with `test_long_path.txt` ✅
- [ ] Tested with `--simple` flag ✅
- [ ] Ran full test suite (`python test_runner.py`) ✅
- [ ] All 72 tests pass ✅

### Documentation
- [ ] Function docstring complete
- [ ] Key variables explained
- [ ] Algorithm strategy clear
- [ ] No misleading comments

### File Management
- [ ] Only modified [`search_algorithms.py`](search_algorithms.py)
- [ ] Did NOT modify other files
- [ ] No extra files added
- [ ] `.gitignore` prevents `__pycache__/` commits

---

## Getting Help

### Debugging Strategy (In Order)

1. **Read the error message carefully**
   - Python errors usually tell you exactly what's wrong
   - Line numbers point to the problem

2. **Add print statements**
   ```python
   print(f"DEBUG: current node = {current.current_node}")
   print(f"DEBUG: path so far = {current.path}")
   print(f"DEBUG: nodes created = {nodes_created}")
   ```

3. **Test with simplest case first**
   ```bash
   python search.py test_cases/test_linear.txt YOUR_ALGO
   ```

4. **Compare with DFS implementation**
   - Your algorithm should follow same structure
   - Only data structure and priority differ

5. **Run test suite to see patterns**
   ```bash
   python test_runner.py
   ```

6. **Check this guide's "Common Issues" section**

7. **Ask team leader or teammates**

### Questions to Ask Yourself (ples do)

Before asking for help, check:
- [ ] Did I follow the pseudocode exactly?
- [ ] Did I test with DFS first to verify setup works?
- [ ] Did I increment `nodes_created` every time?
- [ ] Did I use the visited set correctly?
- [ ] Did I check the priority queue tuple format?
- [ ] Did I compare my output with expected output?
- [ ] Did I read the error message?

**Before asking for help:**
1. Try debugging steps above
2. Note what you've tried
3. Have error message ready
4. Know which test case fails

---

## 🎯 Quick Reference Card

### Data Structures

```python
# Stack (DFS)
stack = []
stack.append(item)  # Push
item = stack.pop()  # Pop (LIFO)

# Queue (BFS)
from collections import deque
queue = deque()
queue.append(item)      # Enqueue
item = queue.popleft()  # Dequeue (FIFO)

# Priority Queue (UCS, GBFS, A*)
import heapq
pq = []
heapq.heappush(pq, (priority, node_id, item))
priority, node_id, item = heapq.heappop(pq)
```

### SearchNode Usage

```python
# Create node
node = SearchNode(
    current_node=5,
    path=[1, 3, 5],
    cost=10.5,
    hops=2
)

# Extend path (creates NEW list)
new_path = node.path + [next_node]

# Update cost
new_cost = node.cost + edge_cost

# Increment hops
new_hops = node.hops + 1
```

### Heuristic Functions

```python
# For single destination
h = euclidean_distance(node_coords[current], node_coords[goal])

# For multiple destinations
h = get_closest_destination_heuristic(
    node_coords,
    current_node,
    destinations,
    'euclidean'
)
```

### Return Format

```python
# Solution found
return (goal_node, nodes_created, path)

# No solution
return (None, nodes_created, [])
```

---

## Final Tips for Success (maybe)

### Do's 

1. **Follow the structure** - All algorithms are similar
2. **Test frequently** - After each major section
3. **Use helper functions** - They're there for a reason
4. **Read error messages** - They usually tell you what's wrong
5. **Start simple** - Test with `test_linear.txt` first
6. **Compare with DFS** - Use it as your reference
7. **Run test suite** - See what "done" looks like
8. **Ask for help** - If stuck for more than 30 minutes

### Don'ts 

1. **Don't rewrite from scratch** - Follow the pseudocode
2. **Don't skip testing** - Test as you go
3. **Don't modify other files** - Only [`search_algorithms.py`](search_algorithms.py)
4. **Don't forget `nodes_created`** - Increment every time
5. **Don't skip visited set** - You'll get infinite loops
6. **Don't be creative** - Just follow the pattern
7. **Don't assume it works** - Always test
8. **Don't leave debug prints** - Remove before submission

### Remember

> "The code is simple. The structure is already there. Just translate the pseudocode line by line, test frequently, and you'll be done in no time" - Lawrence 2025

---

**Project Status:** ✅ COMPLETE  

Good luck! 🚀