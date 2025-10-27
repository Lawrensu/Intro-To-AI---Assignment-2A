from collections import deque
import heapq
from search_node import SearchNode
from utils import euclidean_distance, get_closest_destination_heuristic


def search_dfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
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
        tuple: (goal_node, nodes_created, path)
            - goal_node: which destination was reached (None if no solution)
            - nodes_created: total number of SearchNode objects created
            - path: list of node IDs from origin to goal (empty list if no solution)
            
    Example:
        >>> graph = {1: [(2, 5)], 2: [(3, 3)], 3: []}
        >>> coords = {1: (0, 0), 2: (1, 1), 3: (2, 2)}
        >>> search_dfs(graph, coords, 1, [3])
        (3, 3, [1, 2, 3])
    """
    # Initialize the stack with the origin node
    # Stack is a Python list - use append() to push, pop() to pop (LIFO)
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
    
    # Continue until stack is empty (all reachable nodes explored)
    while stack:
        # Pop the most recently added node (LIFO - depth-first behavior)
        current = stack.pop()
        
        # Goal test: check if we've reached any destination
        if current.current_node in destinations:
            # Success! Return the goal node, total nodes created, and the path
            return (current.current_node, nodes_created, current.path)
        
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
    
    # No solution found - explored all reachable nodes without finding destination
    return (None, nodes_created, [])


def search_bfs(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
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
        tuple: (goal_node, nodes_created, path)
    """
    # Initialize queue
    queue = deque()
    # Create initial SearchNode and enqueue
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    queue.append(initial_node)
    nodes_created = 1

    # Visited set for GRAPH SEARCH
    visited = set()

    # Main loop
    while queue:
        current = queue.popleft()

        # Goal test
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)

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
        tuple: (goal_node, nodes_created, path)
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
    
    # Main loop
    while priority_queue:
        priority, node_id, current = heapq.heappop(priority_queue)
        
        # Goal test
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        
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
        tuple: (goal_node, nodes_created, path)
    """
    # TODO: Elyn - IMPLEMENT GBFS
    # Follow this pseudocode:
    
    # 1. Import heapq and initialize priority queue
    #    import heapq
    #    priority_queue = []
    
    # 2. Calculate initial heuristic
    #    h_value = get_closest_destination_heuristic(node_coords, origin, destinations, 'euclidean')
    #    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    #    heapq.heappush(priority_queue, (h_value, origin, initial_node))
    #    nodes_created = 1
    
    # 3. Initialize visited set
    #    visited = set()
    
    # 4. Main loop: while priority_queue is not empty
    #    h_priority, node_id, current = heapq.heappop(priority_queue)
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
    #        # Calculate heuristic h(n) = Euclidean distance to closest destination
    #        h_value = get_closest_destination_heuristic(
    #            node_coords, neighbor_id, destinations, 'euclidean'
    #        )
    #        
    #        new_path = current.path + [neighbor_id]
    #        new_cost = current.cost + edge_cost  # Track cost for completeness
    #        new_hops = current.hops + 1
    #        
    #        new_node = SearchNode(
    #            current_node=neighbor_id,
    #            path=new_path,
    #            cost=new_cost,
    #            hops=new_hops
    #        )
    #        
    #        # Priority is ONLY the heuristic h(n)
    #        heapq.heappush(priority_queue, (h_value, neighbor_id, new_node))
    #        nodes_created += 1
    
    # 5. If loop ends without finding goal
    #    return (None, nodes_created, [])
    
    nodes_created = 0
    return (None, nodes_created, [])


def search_astar(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    A* Search algorithm using GRAPH SEARCH.
    
    A* uses a priority queue ordered by f(n) = g(n) + h(n).
    - g(n) = actual cost from origin to current node
    - h(n) = estimated cost from current node to goal (Euclidean distance)
    
    Balances path cost and estimated distance to goal. With admissible heuristic,
    guaranteed to find optimal path.
    
    Args:
        graph (dict): Adjacency list representation
        node_coords (dict): Coordinates of each node
        origin (int): Starting node ID
        destinations (list): List of goal node IDs
        
    Returns:
        tuple: (goal_node, nodes_created, path)
    """
    # TODO: Faisal - IMPLEMENT A*
    # Follow this pseudocode:
    
    # 1. Import heapq and initialize priority queue
    #    import heapq
    #    priority_queue = []
    priority_queue = []
    
    # 2. Calculate initial f(n) = g(n) + h(n)
    #    g_value = 0  # Cost from origin
    #    h_value = get_closest_destination_heuristic(node_coords, origin, destinations, 'euclidean')
    #    f_value = g_value + h_value
    #    
    #    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    #    heapq.heappush(priority_queue, (f_value, origin, initial_node))
    #    nodes_created = 1
    g_value = 0
    h_value = get_closest_destination_heuristic(node_coords, origin, destinations, 'euclidean')
    f_value = g_value + h_value
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (f_value, origin, initial_node))
    nodes_created = 1
    
    # 3. Initialize visited set
    #    visited = set()
    visited = set()
    
    # 4. Main loop: while priority_queue is not empty
    #    f_priority, node_id, current = heapq.heappop(priority_queue)
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
    #        # Calculate g(n) = cost from origin to neighbor
    #        g_value = current.cost + edge_cost
    #        
    #        # Calculate h(n) = heuristic from neighbor to closest goal
    #        h_value = get_closest_destination_heuristic(
    #            node_coords, neighbor_id, destinations, 'euclidean'
    #        )
    #        
    #        # Calculate f(n) = g(n) + h(n)
    #        f_value = g_value + h_value
    #        
    #        new_path = current.path + [neighbor_id]
    #        new_hops = current.hops + 1
    #        
    #        new_node = SearchNode(
    #            current_node=neighbor_id,
    #            path=new_path,
    #            cost=g_value,  # Store g(n) in cost attribute
    #            hops=new_hops
    #        )
    #        
    #        # Priority is f(n) = g(n) + h(n)
    #        heapq.heappush(priority_queue, (f_value, neighbor_id, new_node))
    #        nodes_created += 1
    while priority_queue:
        f_value, node_id, current = heapq.heappop(priority_queue)
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
    
    # 5. If loop ends without finding goal
    #    return (None, nodes_created, [])
    return (None, nodes_created, [])
    
    nodes_created = 0
    return (None, nodes_created, [])


def search_hop_count(graph: dict, node_coords: dict, origin: int, destinations: list) -> tuple:
    """
    Best-First Search with Hop Count heuristic using GRAPH SEARCH.
    
    This algorithm uses f(n) = hops + h_hops(n) where:
    - hops = number of edges traversed (NOT cost, just count)
    - h_hops(n) = estimated hops to goal (Euclidean distance / 5.0)
    
    IMPORTANT: This algorithm minimizes NUMBER OF MOVES, completely ignoring
    edge costs. It's useful when you want the fewest steps, regardless of cost.
    
    Args:
        graph (dict): Adjacency list representation
        node_coords (dict): Coordinates of each node
        origin (int): Starting node ID
        destinations (list): List of goal node IDs
        
    Returns:
        tuple: (goal_node, nodes_created, path)
    """
    # TODO: Faisal - IMPLEMENT HOP COUNT BEST-FIRST SEARCH
    # Follow this pseudocode:
    
    # 1. Define constant for hop estimation
    #    AVERAGE_EDGE_LENGTH = 5.0  # Assume average edge is 5 units
    #    This converts Euclidean distance to estimated number of hops
    AVERAGE_EDGE_LENGTH = 5.0
    
    
    # 2. Import heapq and initialize priority queue
    #    import heapq
    #    priority_queue = []
    priority_queue = []
    
    # 3. Calculate initial f(n) = hops + h_hops(n)
    #    hops = 0  # No edges traversed yet
    #    h_hops = get_closest_destination_heuristic(
    #        node_coords, origin, destinations, 'hop_estimate'
    #    )
    #    # Note: 'hop_estimate' type divides Euclidean distance by 5.0
    #    
    #    f_value = hops + h_hops
    #    
    #    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    #    heapq.heappush(priority_queue, (f_value, origin, initial_node))
    #    nodes_created = 1
    hops = 0
    h_hops = get_closest_destination_heuristic(node_coords, origin, destinations, 'hop_estimate')
    f_value = hops + h_hops
    initial_node = SearchNode(current_node=origin, path=[origin], cost=0, hops=0)
    heapq.heappush(priority_queue, (f_value, origin, initial_node))
    nodes_created = 1
    
    # 4. Initialize visited set
    #    visited = set()
    visited = set()
    
    # 5. Main loop: while priority_queue is not empty
    #    f_priority, node_id, current = heapq.heappop(priority_queue)
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
    #        # IMPORTANT: Increment hops by 1 (just count edges, ignore cost!)
    #        new_hops = current.hops + 1
    #        
    #        # Calculate hop heuristic
    #        h_hops = get_closest_destination_heuristic(
    #            node_coords, neighbor_id, destinations, 'hop_estimate'
    #        )
    #        
    #        # Calculate f(n) = hops + h_hops
    #        f_value = new_hops + h_hops
    #        
    #        new_path = current.path + [neighbor_id]
    #        new_cost = current.cost + edge_cost  # Track for completeness
    #        
    #        new_node = SearchNode(
    #            current_node=neighbor_id,
    #            path=new_path,
    #            cost=new_cost,
    #            hops=new_hops  # Store hop count
    #        )
    #        
    #        # Priority is f(n) = hops + h_hops
    #        heapq.heappush(priority_queue, (f_value, neighbor_id, new_node))
    #        nodes_created += 1
    while priority_queue:
        f_value, node_id, current = heapq.heappop(priority_queue)
        if current.current_node in destinations:
            return (current.current_node, nodes_created, current.path)
        if current.current_node in visited:
            continue
        visited.add(current.current_node)
        neighbors = graph.get(current.current_node, [])
        for neighbor_id, edge_cost in neighbors:
            if neighbor_id in visited:
                continue
            new_hops = current.hops + 1
            h_hops = get_closest_destination_heuristic(
                node_coords, neighbor_id, destinations, 'hop_estimate'
            )
            f_value = new_hops + h_hops
            new_path = current.path + [neighbor_id]
            new_cost = current.cost + edge_cost
            new_node = SearchNode(
                current_node=neighbor_id,
                path=new_path,
                cost=new_cost,
                hops=new_hops
            )
            heapq.heappush(priority_queue, (f_value, neighbor_id, new_node))
            nodes_created += 1
    # 6. If loop ends without finding goal
    #    return (None, nodes_created, [])
    return (None, nodes_created, [])
    
    nodes_created = 0
    return (None, nodes_created, [])
