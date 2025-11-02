from collections import deque
import heapq
from search_node import SearchNode
from utils import euclidean_distance, get_closest_destination_heuristic


def _select_two_best(solutions: list):
    """
    Return (best_node_or_None, second_node_or_None) from list of SearchNode
    Sorted by cost, then hops, then path length for deterministic ordering.
    """
    if not solutions:
        return (None, None)
    sols = sorted(solutions, key=lambda n: (n.cost, n.hops, len(n.path)))
    best = sols[0]
    second = sols[1] if len(sols) > 1 else None
    return (best, second)


def _format_two_results(best, second, nodes_created):
    """
    Uniform return format for all search algorithms.
    Returns: (best_goal, nodes_created, best_path, second_goal, second_path)
    """
    best_goal = best.current_node if best else None
    best_path = best.path if best else []
    second_goal = second.current_node if second else None
    second_path = second.path if second else []
    return (best_goal, nodes_created, best_path, second_goal, second_path)



def search_dfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    Depth-First Search algorithm using GRAPH SEARCH.
    Returns best and second-best solutions found.
    
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
    """
    stack = []
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    stack.append(initial_node)
    nodes_created = 1
    visited = set()
    solutions = []

    while stack:
        current = stack.pop()

        if current.current_node in destinations:
            solutions.append(current)
            continue

        if current.current_node in visited:
            continue

        visited.add(current.current_node)
        
        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(reverse=True, key=lambda x: x[0])

        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )
            nodes_created += 1
            stack.append(new_node)

    best, second = _select_two_best(solutions)
    return _format_two_results(best, second, nodes_created)
    """
    Depth-First Search algorithm using GRAPH SEARCH.
    
    DFS uses a stack (LIFO - Last In First Out) to explore nodes. It expands
    the most recently added node first, diving deep into the graph before
    backtracking. This is memory-efficient but not guaranteed to find the
    shortest path.
    
    GRAPH SEARCH: Uses a visited set to avoid revisiting nodes, preventing
    infinite loops in graphs with cycles.
    
    Args:
        graph (dict): Adjacency list representation {node_id: [(neighbor_id, cost), ...]}
        node_coords (dict): Coordinates of each node {node_id: (x, y)}
        origin (int): Starting node ID
        destinations (list): List of goal node IDs
        
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
            Returns best and second-best solutions sorted by cost
            - goal_node: which destination was reached (None if no solution)
            - nodes_created: total number of SearchNode objects created
            - path: list of node IDs from origin to goal (empty list if no solution)
            
    Example:
        >>> graph = {1: [(2, 5)], 2: [(3, 3)], 3: []}
        >>> coords = {1: (0, 0), 2: (1, 1), 3: (2, 2)}
        >>> search_dfs(graph, coords, 1, [3])
        (3, 3, [1, 2, 3])
    """
    stack = []
    
    # Create the initial search node
    # Path starts with just the origin node
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    stack.append(initial_node)
    
    # Track number of nodes created - increment every time we create a SearchNode
    nodes_created = 1
    
    # Track visited nodes to avoid cycles (GRAPH SEARCH)
    # This prevents infinite loops in graphs with cycles
    visited = set()
    solutions = []  # Collect all solutions found
    
    # Continue until stack is empty (all reachable nodes explored)
    while stack:
        # Pop the most recently added node (LIFO - depth-first behavior)
        current = stack.pop()
        
        # Goal test: collect solutions instead of returning immediately
        if current.current_node in destinations:
            solutions.append(current)
            continue  # Keep exploring for more solutions
        
        # Skip if already visited (GRAPH SEARCH prevents revisiting)
        if current.current_node in visited:
            continue
        
        # Mark current node as visited
        visited.add(current.current_node)
        
        # Expand current node: get all neighbors from adjacency list
        neighbors = graph.get(current.current_node, [])
        
        # Sort neighbors by node_id in DESCENDING order for DFS
        # Why descending? Stack is LIFO, so we push highest IDs first.
        # When we pop, we get lowest IDs first, ensuring tie-breaking by ascending node_id.
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(reverse=True, key=lambda x: x[0])
        
        # Create child nodes for all unvisited neighbors
        for neighbor_id, edge_cost in neighbor_list:
            # Skip if already visited (optimization: don't create unnecessary nodes)
            if neighbor_id in visited:
                continue
            
            # Create new search node with updated path, cost, and hops
            new_path = current.path + [neighbor_id]  # Extend path
            new_cost = current.cost + edge_cost       # Accumulate cost
            new_hops = current.hops + 1               # Increment hop count
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=new_cost,
                hops=new_hops
            )
            
            # Push to stack (will be explored soon due to LIFO)
            stack.append(new_node)
            
            # Increment node counter (IMPORTANT: count ALL nodes created)
            nodes_created += 1
    
    # Select and return best two solutions found
    best, second = _select_two_best(solutions)
    return _format_two_results(best, second, nodes_created)


def search_bfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    Breadth-First Search algorithm using GRAPH SEARCH.
    Returns best and second-best solutions found.
    
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
    """
    queue = deque()
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    queue.append(initial_node)
    nodes_created = 1
    visited = set()
    solutions = []

    while queue:
        current = queue.popleft()

        if current.current_node in destinations:
            solutions.append(current)
            continue

        if current.current_node in visited:
            continue

        visited.add(current.current_node)

        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])

        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue

            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )
            nodes_created += 1
            queue.append(new_node)

    best, second = _select_two_best(solutions)
    return _format_two_results(best, second, nodes_created)
    """
    Breadth-First Search algorithm using GRAPH SEARCH.
    
    BFS uses a queue (FIFO) to explore nodes level by level. Guaranteed to find
    the shortest path in terms of number of edges (unweighted shortest path).
    
    Args:
        graph (dict): Adjacency list representation
        node_coords (dict): Coordinates of each node
        origin (int): Starting node ID
        destinations (list): List of goal node IDs
        
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
            Returns best and second-best solutions sorted by cost
    """
    # Initialize queue
    queue = deque()
    # Create initial SearchNode and enqueue
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    queue.append(initial_node)
    nodes_created = 1

    # Visited set for GRAPH SEARCH
    visited = set()
    solutions = []  # Collect all solutions found

    # Main loop
    while queue:
        current = queue.popleft()

        # Goal test
        if current.current_node in destinations:
            solutions.append(current)
            continue  # Keep exploring for more solutions

        # Skip if visited
        if current.current_node in visited:
            continue

        # Mark as visited
        visited.add(current.current_node)

        # Get neighbors and sort ascending by node_id for tie-breaking
        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])

        # Expand neighbors
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

    # No solution found
    return (None, nodes_created, [])

def search_ucs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    Uniform-Cost Search algorithm using GRAPH SEARCH.
    Returns best and second-best solutions found.
    
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
    """
    pq = []
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(pq, (initial_node.cost, initial_node))
    nodes_created = 1
    visited = set()
    solutions = []

    while pq:
        _, current = heapq.heappop(pq)

        if current.current_node in destinations:
            solutions.append(current)
            continue

        if current.current_node in visited:
            continue

        visited.add(current.current_node)

        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])

        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue

            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )
            nodes_created += 1
            heapq.heappush(pq, (new_node.cost, new_node))

    best, second = _select_two_best(solutions)
    return _format_two_results(best, second, nodes_created)
    """
    Uniform Cost Search algorithm using GRAPH SEARCH.
    
    UCS uses a priority queue ordered by path cost g(n). Always expands the
    node with the lowest total cost from the origin. Guaranteed to find the
    least-cost path.
    
    Args:
        graph (dict): Adjacency list representation
        node_coords (dict): Coordinates of each node
        origin (int): Starting node ID
        destinations (list): List of goal node IDs
        
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
            Returns best and second-best solutions sorted by cost. Due to UCS optimality,
            the first two solutions found will be the optimal and second-best paths.
    """
    # TODO: Elyn - IMPLEMENT UCS
    # Follow this pseudocode:
    
    # 1. Import and initialize priority queue
    #    import heapq
    #    priority_queue = []
    #    Use heapq.heappush(pq, (priority, node_id, search_node))
    #    Use heapq.heappop(pq) to get lowest priority
    
    # 2. Create initial SearchNode with origin
    #    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    #    Priority for UCS is the cost g(n)
    #    heapq.heappush(priority_queue, (0, origin, initial_node))
    #    nodes_created = 1
    
    # 3. Initialize visited set for GRAPH SEARCH
    #    visited = set()
    
    # 4. Main loop: while priority_queue is not empty
    #    priority, node_id, current = heapq.heappop(priority_queue)
    #    
    #    # Goal test
    #    if current.current_node in destinations:
    #        return (current.current_node, nodes_created, current.path)
    #    
    #    # Skip if visited
    #    if current.current_node in visited:
    #        continue
    #    
    #    # Mark as visited
    #    visited.add(current.current_node)
    #    
    #    # Get neighbors
    #    neighbors = graph.get(current.current_node, [])
    #    
    #    # Expand neighbors
    #    for neighbor_id, edge_cost in neighbors:
    #        if neighbor_id in visited:
    #            continue
    #        
    #        # Calculate new cost: g(n) = g(parent) + edge_cost
    #        new_cost = current.cost + edge_cost
    #        new_path = current.path + [neighbor_id]
    #        new_hops = current.hops + 1
    #        
    #        new_node = SearchNode(
    #            current_node=neighbor_id,
    #            path=new_path,
    #            cost=new_cost,
    #            hops=new_hops
    #        )
    #        
    #        # Push with cost as priority
    #        # Tuple format: (priority, node_id, search_node)
    #        # node_id is for tie-breaking when costs are equal
    #        heapq.heappush(priority_queue, (new_cost, neighbor_id, new_node))
    #        nodes_created += 1
    
    # 5. If loop ends without finding goal
    #    return (None, nodes_created, [])
    
    # Initialize priority queue (min-heap)
    priority_queue = []
    
    # Create initial node and push with priority = cost (g = 0)
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (0, origin, initial_node))
    nodes_created = 1
    
    # Visited set for GRAPH SEARCH
    visited = set()
    solutions = []  # Collect solutions found
    
    # Main loop
    while priority_queue:
        priority, node_id, current = heapq.heappop(priority_queue)
        
        # Goal test and solution collection
        if current.current_node in destinations:
            solutions.append(current)
            if len(solutions) >= 2:  # UCS: first two solutions will be optimal and second-best
                break
            continue
        
        # Skip if already visited
        if current.current_node in visited:
            continue
        
        # Mark visited
        visited.add(current.current_node)
        
        # Expand neighbors
        neighbors = graph.get(current.current_node, [])
        for neighbor_id, edge_cost in neighbors:
            if neighbor_id in visited:
                continue
            
            # Compute new path cost g(n)
            new_cost = current.cost + edge_cost
            new_path = current.path + [neighbor_id]
            new_hops = current.hops + 1
            
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=new_cost,
                hops=new_hops
            )
            
            # Push with (cost, node_id, node) so tie-breaks use node_id
            heapq.heappush(priority_queue, (new_cost, neighbor_id, new_node))
            nodes_created += 1
    
    # No solution found
    return (None, nodes_created, [])


def search_gbfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    Greedy Best-First Search algorithm using GRAPH SEARCH.
    
    GBFS uses a priority queue ordered by heuristic h(n) only. Always expands
    the node that appears closest to the goal (ignoring path cost). Fast but
    not guaranteed to find optimal path.
    
    Heuristic: Euclidean distance to the nearest destination.
    
    Args:
        graph (dict): Adjacency list representation
        node_coords (dict): Coordinates of each node
        origin (int): Starting node ID
        destinations (list): List of goal node IDs
        
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
            Returns best and second-best solutions sorted by actual path cost,
            not by heuristic values used during search.
    """

    #TODO: Elyn - IMPLEMENT GBFS

    # Initialize priority queue (min-heap)
    # Calculate initial heuristic for origin
    # Visited set for GRAPH SEARCH
    priority_queue = []
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heuristic = get_closest_destination_heuristic(node_coords, origin, destinations)
    heapq.heappush(priority_queue, (heuristic, initial_node))
    nodes_created = 1
    visited = set()
    solutions = []

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        # Goal test
        if current.current_node in destinations:
            solutions.append(current)
            continue  # Keep exploring for more solutions

        # Skip if already visited
        if current.current_node in visited:
            continue
        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])

        # Mark visited
        visited.add(current.current_node)

        # Expand neighbors
            # Heuristic only (greedy): Euclidean distance to closest destination
        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue

            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )

            # Priority is the heuristic; neighbor_id used to break ties deterministically
            nodes_created += 1
            h = get_closest_destination_heuristic(node_coords, neighbor_id, destinations)
            heapq.heappush(priority_queue, (h, new_node))

    # No solution found
    best, second = _select_two_best(solutions)
    return _format_two_results(best, second, nodes_created)


def search_astar(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    A* Search algorithm using GRAPH SEARCH.
    Returns best and second-best solutions found.
    
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
    """
    priority_queue = []
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heuristic = get_closest_destination_heuristic(node_coords, origin, destinations)
    heapq.heappush(priority_queue, (initial_node.cost + heuristic, initial_node))
    nodes_created = 1
    visited = set()
    solutions = []

    while priority_queue:
        _, current = heapq.heappop(priority_queue)

        if current.current_node in destinations:
            solutions.append(current)
            continue

        if current.current_node in visited:
            continue

        visited.add(current.current_node)

        neighbors = graph.get(current.current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])

        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id in visited:
                continue

            new_node = SearchNode(
                current_node=neighbor_id,
                path=current.path + [neighbor_id],
                cost=current.cost + edge_cost,
                hops=current.hops + 1
            )
            nodes_created += 1
            h = get_closest_destination_heuristic(node_coords, neighbor_id, destinations)
            heapq.heappush(priority_queue, (new_node.cost + h, new_node))

    best, second = _select_two_best(solutions)
    return _format_two_results(best, second, nodes_created)


def search_ida_star(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    Iterative Deepening A* Search algorithm using TREE SEARCH.
    Returns best and second-best solutions found.
    
    Returns:
        tuple: (best_goal, nodes_created, best_path, second_goal, second_path)
    """
    def ida_search(current_node, f_limit, current_path, current_cost, solutions, nodes_created):
        # Calculate f(n) = g(n) + h(n)
        h = get_closest_destination_heuristic(node_coords, current_node, destinations)
        f = current_cost + h
        
        # If f exceeds limit, return f as new minimum for next iteration
        if f > f_limit:
            return f, nodes_created
            
        # Goal test
        if current_node in destinations:
            # Create SearchNode for consistent solution handling
            solution_node = SearchNode(
                current_node=current_node,
                path=current_path,
                cost=current_cost,
                hops=len(current_path) - 1
            )
            solutions.append(solution_node)
            return float('inf'), nodes_created
            
        min_f = float('inf')
        neighbors = graph.get(current_node, [])
        neighbor_list = [(neighbor_id, cost) for neighbor_id, cost in neighbors]
        neighbor_list.sort(key=lambda x: x[0])  # Consistent ordering
        
        for neighbor_id, edge_cost in neighbor_list:
            if neighbor_id not in current_path:  # Tree search - only check path
                nodes_created[0] += 1
                # Recursively search with updated path and cost
                next_f, _ = ida_search(
                    neighbor_id,
                    f_limit,
                    current_path + [neighbor_id],
                    current_cost + edge_cost,
                    solutions,
                    nodes_created
                )
                min_f = min(min_f, next_f)
                
        return min_f, nodes_created

    nodes_created = [1]  # Using list to allow modification in nested function
    solutions = []
    initial_h = get_closest_destination_heuristic(node_coords, origin, destinations)
    f_limit = initial_h  # Initial f-limit is just the heuristic
    initial_path = [origin]
    
    while True:
        next_f, _ = ida_search(origin, f_limit, initial_path, 0, solutions, nodes_created)
        
        # No solution exists if we've exhausted all possibilities
        if not solutions and next_f == float('inf'):
            return None, nodes_created[0], [], None, []
            
        # If we have solutions, process them
        if solutions:
            best, second = _select_two_best(solutions)
            return _format_two_results(best, second, nodes_created[0])
            
        # No solutions found yet at this f-limit, increase bound and continue
        f_limit = next_f
    
