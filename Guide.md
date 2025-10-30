# 🚀 Team Implementation Guide - Route Finding Algorithms

**Last Updated:** 26/10/25
**Team Leader:** Lawrence Lian Anak Matius Ding
**Project:** AI Search Algorithms Assignment

---

## 📊 Quick Status Overview

| Team Member | Algorithm(s) | Status | File Location |
|-------------|-------------|--------|---------------|
| **Me (Team Leader)** | DFS | ✅ COMPLETE (Reference) | [`search_algorithms.py`](search_algorithms.py) |
| **Jason** | BFS | ✅ COMPLETE | [`search_algorithms.py`](search_algorithms.py) |
| **Elyn** | UCS + GBFS | ✅ COMPLETE | [`search_algorithms.py`](search_algorithms.py) |
| **Faisal** | A* + IDA* | ✅ COMPLETE | [`search_algorithms.py`](search_algorithms.py)  |

---

## 🎯 Algorithm Summary

### Uninformed Search (No Heuristic)
1. **DFS** - Stack, goes deep first
2. **BFS** - Queue, explores level by level
3. **UCS** - Priority queue by cost, finds cheapest path

### Informed Search (Uses Heuristic)
4. **GBFS** - Priority queue by h(n), greedy toward goal
5. **A*** - Priority queue by f(n)=g(n)+h(n), optimal and efficient
6. **IDA*** - Iterative deepening with f-limit, optimal with minimal memory

---

## 🎯 What You Need to Do

### The Good News
**90% of the work is already done!** You just need to:
1. Open [`search_algorithms.py`](search_algorithms.py)
2. Find your function
3. Translate the pseudocode (hardwork ahh) to actual Python code
4. Test it

### The Files You DON'T Touch
❌ **DO NOT MODIFY THESE FILES:**
- [`search.py`](search.py) - Main program (complete)
- [`graph_parser.py`](graph_parser.py) - File parser (complete)
- [`search_node.py`](search_node.py) - SearchNode class (complete)
- [`utils.py`](utils.py) - Helper functions (complete)

### The ONE File You Edit
✅ **ONLY EDIT THIS FILE:**
- [`search_algorithms.py`](search_algorithms.py) - Your algorithm implementations

---

## 📖 Understanding the Project Structure

### How Everything Fits Together

```
User runs: python search.py test_cases/test1.txt BFS
                    ↓
            search.py (main entry)
                    ↓
            Parses command-line args
                    ↓
            graph_parser.py reads the file
                    ↓
            Calls search_bfs() from search_algorithms.py
                    ↓
            Your algorithm runs!
                    ↓
            utils.py formats and prints results
```

### What Each File Does

**[`search.py`](search.py)** - The Boss
- Takes command-line arguments
- Calls the right search function
- Handles errors
- You don't touch this!

**[`graph_parser.py`](graph_parser.py)** - The Reader
- Reads input files
- Extracts nodes, edges, origin, destinations
- Returns everything in nice dictionaries
- You don't touch this!

**[`search_node.py`](search_node.py)** - The Data Container
- Stores: current_node, path, cost, hops
- Used by ALL algorithms
- You don't touch this!

**[`utils.py`](utils.py)** - The Helper
- Calculates Euclidean distance
- Formats output
- Provides heuristic functions
- You don't touch this!

**[`search_algorithms.py`](search_algorithms.py)** - YOUR WORKSPACE
- Contains all 6 search algorithms
- DFS is complete (your example)
- You implement the other 5
- **This is where you work!**

---

## 🎓 Step-by-Step Implementation Guide

### STEP 1: Read the DFS Implementation First

Before you start, **read the complete DFS code** in [`search_algorithms.py`](search_algorithms.py) (lines 7-110).

**Pay special attention to:**
```python
# How nodes_created is incremented
nodes_created = 1  # Start with origin
# ...
new_node = SearchNode(...)
nodes_created += 1  # Increment for EVERY node created

# How visited set works
visited = set()
if current.current_node in visited:
    continue  # Skip if already visited
visited.add(current.current_node)  # Mark as visited

# How paths are built
new_path = current.path + [neighbor_id]  # Extend path

# How to return results
return (goal_node, nodes_created, path)  # Success
return (None, nodes_created, [])  # Failure
```

### STEP 2: Understand Your Algorithm's Structure

All algorithms follow this pattern:

```python
def search_algorithm(graph, node_coords, origin, destinations):
    # 1. Initialize data structure (stack/queue/priority queue)
    # 2. Create initial SearchNode with origin
    # 3. Initialize visited set
    # 4. Main loop: while data structure not empty
    #    a. Get next node
    #    b. Check if goal → return success
    #    c. Skip if visited
    #    d. Mark as visited
    #    e. Expand neighbors
    # 5. Return failure if loop ends
```

### STEP 3: Follow the Pseudocode Line-by-Line

Your function already has **extremely detailed pseudocode**. Use brain and translate it.

**Example: Converting Pseudocode to Code**

❌ **Don't skip the pseudocode!**
❌ **Don't try to be clever!**
❌ **Don't rewrite from scratch!**

✅ **Do follow it line by line!**

**Pseudocode says:**
```python
# 1. Import and initialize queue
#    from collections import deque
#    queue = deque()
```

**You write:**
```python
queue = deque()
```
*(Note: `from collections import deque` is already at the top of the file)*

**Pseudocode says:**
```python
# 2. Create initial SearchNode with origin
#    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
#    queue.append(initial_node)
#    nodes_created = 1
```

**You write:**
```python
initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
queue.append(initial_node)
nodes_created = 1
```

**That's it!** Continue until the pseudocode ends.

---

## 👤 Individual Team Member Instructions

### 🔵 Jason: Implement BFS

**Location:** [`search_algorithms.py`](search_algorithms.py) line 113  
**Function:** `search_bfs()`

**What makes BFS different:**
- Uses a **queue** (FIFO - First In First Out)
- `deque.append()` to add
- `deque.popleft()` to remove
- Sort neighbors **ascending**: `neighbor_list.sort(key=lambda x: x[0])`

**Quick Start Template:**
```python
def search_bfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    queue = deque()
    
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    queue.append(initial_node)
    nodes_created = 1
    
    visited = set()
    
    while queue:
        current = queue.popleft()  # FIFO - oldest first
        
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
        if current.current_node in visited:
            continue
        
        visited.add(current.current_node)
        
        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])  # Ascending
        
        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue
            
            new_path = current.path + [neighbor_id]
            new_cost = current.cost + edge_cost
            new_hops = current.hops + 1
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=new_cost,
                hops=new_hops
            )
            
            queue.append(new_node)
            nodes_created += 1
    
    return (None, nodes_created, [])
```

**Test your implementation:**
```bash
python search.py test_cases/test1.txt BFS
python search.py test_cases/test2.txt BFS
```

---

### 🟢 Elyn: Implement UCS and GBFS

#### Part 1: UCS (Uniform Cost Search)

**Location:** [`search_algorithms.py`](search_algorithms.py) line 170  
**Function:** `search_ucs()`

**What makes UCS different:**
- Uses **priority queue** with `heapq`
- Priority = **g(n)** = total cost from origin
- Format: `heapq.heappush(pq, (cost, node_id, search_node))`
- Expands lowest-cost node first

**Quick Start Template:**
```python
def search_ucs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    priority_queue = []
    
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (0, origin, initial_node))  # priority = cost
    nodes_created = 1
    
    visited = set()
    
    while priority_queue:
        priority, node_id, current = heapq.heappop(priority_queue)
        
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
        if current.current_node in visited:
            continue
        
        visited.add(current.current_node)
        
        neighbors = graph.get(current.current_node, [])
        
        for neighbor_id, edge_cost in neighbors:
            if neighbor_id in visited:
                continue
            
            new_cost = current.cost + edge_cost  # g(n)
            new_path = current.path + [neighbor_id]
            new_hops = current.hops + 1
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=new_cost,
                hops=new_hops
            )
            
            heapq.heappush(priority_queue, (new_cost, neighbor_id, new_node))
            nodes_created += 1
    
    return (None, nodes_created, [])
```

#### Part 2: GBFS (Greedy Best-First Search)

**Location:** [`search_algorithms.py`](search_algorithms.py) line 227  
**Function:** `search_gbfs()`

**What makes GBFS different:**
- Uses **priority queue** with `heapq`
- Priority = **h(n)** = heuristic only (Euclidean distance)
- Use helper: `get_closest_destination_heuristic(node_coords, node_id, destinations, 'euclidean')`
- Expands node closest to goal first

**Quick Start Template:**
```python
def search_gbfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    priority_queue = []
    
    h_value = get_closest_destination_heuristic(node_coords, origin, destinations, 'euclidean')
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
            
            h_value = get_closest_destination_heuristic(
                node_coords, neighbor_id, destinations, 'euclidean'
            )
            
            new_path = current.path + [neighbor_id]
            new_cost = current.cost + edge_cost
            new_hops = current.hops + 1
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=new_cost,
                hops=new_hops
            )
            
            heapq.heappush(priority_queue, (h_value, neighbor_id, new_node))
            nodes_created += 1
    
    return (None, nodes_created, [])
```

**Test your implementations:**
```bash
python search.py test_cases/test1.txt UCS
python search.py test_cases/test1.txt GBFS
python search.py test_cases/test2.txt UCS
python search.py test_cases/test2.txt GBFS
```

---

### 🟣 Faisal: Implement A* and Iterative Deepening A*

#### Part 1: A* Search

**Location:** [`search_algorithms.py`](search_algorithms.py) line 290  
**Function:** `search_astar()`

**What makes A* different:**
- Uses **priority queue** with `heapq`
- Priority = **f(n) = g(n) + h(n)**
- g(n) = actual cost from origin
- h(n) = Euclidean distance to goal
- Combines UCS and GBFS!

**Quick Start Template:**
```python
def search_astar(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    priority_queue = []
    
    g_value = 0
    h_value = get_closest_destination_heuristic(node_coords, origin, destinations, 'euclidean')
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
            
            g_value = current.cost + edge_cost
            h_value = get_closest_destination_heuristic(
                node_coords, neighbor_id, destinations, 'euclidean'
            )
            f_value = g_value + h_value
            
            new_path = current.path + [neighbor_id]
            new_hops = current.hops + 1
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=g_value,
                hops=new_hops
            )
            
            heapq.heappush(priority_queue, (f_value, neighbor_id, new_node))
            nodes_created += 1
    
    return (None, nodes_created, [])
```


#### Part 2: IDA* (Iterative Deepening A*)

**Location:** [`search_algorithms.py`](search_algorithms.py) line 420  
**Function:** `search_ida_star()`
**Data Structure:** ❌ **NOT Priority Queue!** ✅ **Recursive DFS**

**What makes IDA* different:**
- Uses **recursive DFS** with increasing f-value bounds
- **NO priority queue** - just recursive function calls
- Memory efficient: **O(bd)** instead of A*'s **O(b^d)**
- Still **optimal** with admissible heuristic
- Trades time for space (may revisit nodes)

**How IDA* works:**
1. Start with bound = h(origin) (initial heuristic estimate)
2. Perform **recursive DFS**, but only expand nodes where f(n) ≤ bound
3. If no solution found, set bound = minimum f-value that exceeded current bound
4. Repeat until solution found or bound = ∞

**Key Structure:**
```python
def search_ida_star(...):
    bound = h(origin)
        
    # Recursive DFS helper function
    def search(node, g_value, bound, visited):
        f = g_value + h(node)
            
        if f > bound:
            return (None, f)  # Don't expand, return f
            
        if is_goal(node):
            return (node, None)  # Found!
            
        # Recursive DFS (NOT priority queue!)
        for neighbor in neighbors:
            result, new_f = search(neighbor, g + cost, bound, visited)
            if result:
                return (result, None)
            
        return (None, min_f_that_exceeded_bound)
        
    # Iterative deepening loop
    while True:
        result, new_bound = search(initial, 0, bound, visited)
        if result:
            return result
        bound = new_bound
```

---


**Test your implementations:**
```bash
python search.py test_cases/test1.txt AS
python search.py test_cases/test1.txt CUS2
python search.py test_cases/test2.txt AS
python search.py test_cases/test2.txt CUS2
```

---

## 🧪 Testing Guide

### Step 1: Test DFS First (Verify Everything Works)
```bash
python search.py test_cases/test1.txt DFS
```

**Expected output:**
```
==================================================
File: test_cases/test1.txt
Search Method: DFS
==================================================
Result: SOLUTION FOUND
Goal Node: 5
Nodes Created: 7
Path: 1 -> 3 -> 4 -> 5
Path Length: 4 nodes
==================================================
```

### Step 2: Test Your Algorithm
```bash
# Jason
python search.py test_cases/test1.txt BFS

# Elyn
python search.py test_cases/test1.txt UCS
python search.py test_cases/test1.txt GBFS

# Faisal
python search.py test_cases/test1.txt AS
python search.py test_cases/test1.txt CUS2
```

### Step 3: Test with All Test Files
```bash
python search.py test_cases/test1.txt BFS
python search.py test_cases/test2.txt BFS
python search.py test_cases/testDebugging.txt BFS
python search.py test_cases/testNoSolution.txt BFS
```

### Step 4: Test with Simple Output (For Submission)
```bash
python search.py test_cases/test1.txt BFS --simple
```

**Expected format:**
```
test_cases/test1.txt BFS
5 12
1 2 4 5
```

---

## 🐛 Common Errors and Solutions

### Error 1: NameError: name 'deque' is not defined
**Solution:** The import is already at the top of [`search_algorithms.py`](search_algorithms.py):
```python
from collections import deque
```
Just use `deque()` directly.

### Error 2: NameError: name 'heapq' is not defined
**Solution:** The import is already at the top of [`search_algorithms.py`](search_algorithms.py):
```python
import heapq
```
Just use `heapq.heappush()` and `heapq.heappop()` directly.

### Error 3: TypeError: '<' not supported between instances of 'SearchNode'
**Problem:** You forgot to include `node_id` in the tuple.

**Wrong:**
```python
heapq.heappush(pq, (priority, search_node))  # ❌ Missing node_id
```

**Correct:**
```python
heapq.heappush(pq, (priority, node_id, search_node))  # ✅
```

### Error 4: Wrong Node Count
**Problem:** Not incrementing `nodes_created` every time.

**Make sure:**
```python
new_node = SearchNode(...)
nodes_created += 1  # ✅ Always increment here!
```

### Error 5: Infinite Loop
**Problem:** Not checking visited set properly.

**Make sure:**
```python
if neighbor_id in visited:
    continue  # ✅ Skip visited nodes
```

### Error 6: No Solution Found (But One Exists)
**Problem:** Goal test in wrong place.

**Correct location:**
```python
while queue:
    current = queue.popleft()
    
    # ✅ Goal test AFTER popping
    if current.current_node in destinations:
        return (current.current_node, nodes_created, current.path)
```

### Error 7: Path Not Building Correctly
**Problem:** Modifying original path instead of creating new one.

**Wrong:**
```python
new_path = current.path
new_path.append(neighbor_id)  # ❌ Modifies original!
```

**Correct:**
```python
new_path = current.path + [neighbor_id]  # ✅ Creates new list
```

---

## 🔍 Debugging Tips

### Add Print Statements
```python
while queue:
    current = queue.popleft()
    print(f"DEBUG: Exploring node {current.current_node}")
    print(f"DEBUG: Current path: {current.path}")
    print(f"DEBUG: Nodes created so far: {nodes_created}")
```

### Verify Your Data Structures
```python
print(f"DEBUG: Queue size: {len(queue)}")
print(f"DEBUG: Visited nodes: {visited}")
print(f"DEBUG: Priority queue: {priority_queue[:3]}")  # First 3 items
```

### Check Neighbors
```python
neighbors = graph.get(current.current_node, [])
print(f"DEBUG: Node {current.current_node} has neighbors: {neighbors}")
```

### Test with Simple Input
Create a tiny test file with just 3-4 nodes to trace execution manually.

---

## ✅ Pre-Submission Checklist

Before you say "I'm done", check ALL of these:

- [ ] My algorithm follows the pseudocode structure
- [ ] I use the correct data structure (stack/queue/priority queue)
- [ ] I increment `nodes_created` for EVERY SearchNode I create
- [ ] I use the `visited` set correctly (check before expanding, add after popping)
- [ ] I return the correct format: `(goal_node, nodes_created, path)`
- [ ] I handle "no solution" case: `(None, nodes_created, [])`
- [ ] I build paths correctly: `current.path + [neighbor_id]`
- [ ] I tested with test1.txt successfully
- [ ] I tested with test2.txt successfully
- [ ] I tested with testDebugging.txt successfully
- [ ] I tested with testNoSolution.txt successfully
- [ ] My output format matches DFS output format
- [ ] I tested with `--simple` flag
- [ ] I didn't modify any other files
- [ ] My code has no syntax errors
- [ ] My code has no runtime errors

---

## 📞 Getting Help

### Priority Order:
1. **First:** Re-read the DFS implementation in [`search_algorithms.py`](search_algorithms.py) (lines 7-110)
2. **Second:** Check your pseudocode comments in your function
3. **Third:** Add print statements to see what's happening
4. **Fourth:** Test with simpler test files
5. **Fifth:** Compare your code with the quick start templates above
6. **Sixth:** Ask team leader (me) in our chat
7. **Finally:** Ask teammates who finished their algorithms

### Questions to Ask Yourself:
- Did I follow the pseudocode exactly?
- Did I test with DFS first to make sure everything works?
- Did I increment nodes_created every time?
- Did I use the visited set correctly?
- Did I check my priority queue tuple format?

---

## 🎯 Quick Reference

### Data Structures

**Stack (DFS):**
```python
stack = []
stack.append(item)  # Push
item = stack.pop()  # Pop (LIFO)
```

**Queue (BFS):**
```python
from collections import deque
queue = deque()
queue.append(item)      # Enqueue
item = queue.popleft()  # Dequeue (FIFO)
```

**Priority Queue (UCS, GBFS, A*):**
```python
import heapq
pq = []
heapq.heappush(pq, (priority, node_id, item))
priority, node_id, item = heapq.heappop(pq)
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

### Helper Functions
```python
# Get heuristic to closest destination
h = get_closest_destination_heuristic(
    node_coords, 
    current_node, 
    destinations, 
    'euclidean'  # or 'hop_estimate'
)
```

### Return Format
```python
# Success
return (goal_node, nodes_created, path)

# Failure
return (None, nodes_created, [])
```

---

## 💡 Final Tips

### Success Strategy
1. ✅ Start with the quick start template
2. ✅ Don't overthink it - just translate pseudocode
3. ✅ Test after writing each major section
4. ✅ Compare your output with DFS output
5. ✅ Use print statements liberally while debugging
6. ✅ Remove print statements when done

### Common Misconceptions
❌ "I need to be creative" - NO! Just follow the pseudocode!
❌ "I should optimize this" - NO! Make it work first!
❌ "I'll test after finishing" - NO! Test as you go!
❌ "I'll skip the visited set" - NO! You'll get infinite loops!

✅ Follow the pseudocode exactly
✅ Test frequently
✅ Use the helper functions provided
✅ Ask for help if stuck for more than 30 minutes

---