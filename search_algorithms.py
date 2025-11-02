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
    
