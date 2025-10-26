import math


def euclidean_distance(coord1: tuple, coord2: tuple) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Uses the formula: sqrt((x2-x1)^2 + (y2-y1)^2)
    
    Args:
        coord1 (tuple): (x, y) coordinates of first point
        coord2 (tuple): (x, y) coordinates of second point
        
    Returns:
        float: Euclidean distance between the two points
        
    Example:
        >>> euclidean_distance((0, 0), (3, 4))
        5.0
    """
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def format_output(filename: str, method: str, goal, nodes_created: int, path: list):
    """
    Print output in a more informative and readable format.
    
    Output format includes labels and separators to make it clear what each value represents.
    
    Args:
        filename (str): Name of the input file
        method (str): Search method used (e.g., "DFS", "BFS")
        goal (int): Goal node ID that was reached (None if no solution)
        nodes_created (int): Total number of SearchNode objects created
        path (list): List of node IDs from origin to goal
        
    Example:
        >>> format_output("test.txt", "DFS", 5, 42, [2, 3, 5])
        ==========================================
        File: test.txt
        Search Method: DFS
        ==========================================
        Goal Node: 5
        Nodes Created: 42
        Path: 2 -> 3 -> 5
        Path Length: 3 nodes
        ==========================================
    """
    # Print header with file and method information
    print("=" * 50)
    print(f"File: {filename}")
    print(f"Search Method: {method}")
    print("=" * 50)
    
    if goal is None:
        # If no solution found
        print("Result: NO SOLUTION FOUND")
        print(f"Nodes Created: {nodes_created}")
        print("Path: None")
    else:
        # Solution found
        print(f"Result: SOLUTION FOUND")
        print(f"Goal Node: {goal}")
        print(f"Nodes Created: {nodes_created}")
        
        # Format path with arrows for better visualization
        if path:
            path_str = ' -> '.join(map(str, path))
            print(f"Path: {path_str}")
            print(f"Path Length: {len(path)} nodes")
        else:
            print("Path: Empty")
    
    print("=" * 50)
    print()  

def format_output_simple(filename: str, method: str, goal, nodes_created: int, path: list):
    """
    Print output in the original simple format (for assignment submission).
    
    Use this if you need the exact format specified in the assignment requirements.
    
    Output format:
    Line 1: <filename> <method>
    Line 2: <goal_node> <nodes_created>
    Line 3: <path as space-separated node IDs>
    
    Args:
        filename (str): Name of the input file
        method (str): Search method used (e.g., "DFS", "BFS")
        goal (int): Goal node ID that was reached (None if no solution)
        nodes_created (int): Total number of SearchNode objects created
        path (list): List of node IDs from origin to goal
        
    Example:
        >>> format_output_simple("test.txt", "DFS", 5, 42, [2, 3, 5])
        test.txt DFS
        5 42
        2 3 5
    """
    print(f"{filename} {method}")
    
    if goal is None:
        # No solution found
        print(f"No solution {nodes_created}")
        print("")
    else:
        # Solution found
        print(f"{goal} {nodes_created}")
        # Convert path list to space-separated string
        path_str = ' '.join(map(str, path))
        print(path_str)


def get_heuristic(node_coords: dict, current_node: int, goal_node: int, 
                  heuristic_type: str = 'euclidean') -> float:
    """
    Calculate heuristic value based on the specified type.
    
    Args:
        node_coords (dict): Dictionary mapping node IDs to (x, y) coordinates
        current_node (int): Current node ID
        goal_node (int): Goal node ID
        heuristic_type (str): Type of heuristic to use:
            - 'euclidean': Straight-line distance (default)
            - 'hop_estimate': Estimated number of hops (distance / 5.0)
            
    Returns:
        float: Heuristic value
        
    Example:
        >>> node_coords = {1: (0, 0), 2: (3, 4)}
        >>> get_heuristic(node_coords, 1, 2, 'euclidean')
        5.0
        >>> get_heuristic(node_coords, 1, 2, 'hop_estimate')
        1.0
    """
    current_coord = node_coords[current_node]
    goal_coord = node_coords[goal_node]
    
    distance = euclidean_distance(current_coord, goal_coord)
    
    if heuristic_type == 'euclidean':
        return distance
    elif heuristic_type == 'hop_estimate':
        # Estimate number of hops by dividing distance by average edge length
        # Assuming average edge length is approximately 5 units
        return distance / 5.0
    else:
        raise ValueError(f"Unknown heuristic type: {heuristic_type}")


# Used by GBFS, A* and Hop Count
def get_closest_destination_heuristic(node_coords: dict, current_node: int, 
                                      destinations: list, heuristic_type: str = 'euclidean') -> float:
    """
    Calculate heuristic to the closest destination from multiple possible destinations.
    
    This is useful for problems with multiple goal nodes - we use the minimum
    distance to any destination as our heuristic.
    
    Args:
        node_coords (dict): Dictionary mapping node IDs to (x, y) coordinates
        current_node (int): Current node ID
        destinations (list): List of possible destination node IDs
        heuristic_type (str): Type of heuristic ('euclidean' or 'hop_estimate')
        
    Returns:
        float: Minimum heuristic value to any destination
        
    Example:
        >>> node_coords = {1: (0, 0), 2: (3, 4), 3: (6, 8)}
        >>> get_closest_destination_heuristic(node_coords, 1, [2, 3])
        5.0
    """
    min_heuristic = float('inf')
    
    for dest in destinations:
        h = get_heuristic(node_coords, current_node, dest, heuristic_type)
        if h < min_heuristic:
            min_heuristic = h
    
    return min_heuristic