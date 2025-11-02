"""
Main entry point for the route finding search algorithms.

Usage:
    python search.py <filename> <method> [--simple]

Example:
    python search.py test_cases/test1.txt DFS
    python search.py test_cases/test1.txt BFS --simple
"""

# The flow:
# 1. User runs: python search.py test_cases/test1.txt BFS
# 2. search.py parses command-line arguments
# 3. Calls graph_parser to read the file
# 4. Calls search_bfs() from search_algorithms.py
# 5. Gets results back
# 6. Calls format_output() to print results

import sys
from graph_parser import parse_input
from search_algorithms import (
    search_dfs,
    search_bfs,
    search_ucs,
    search_gbfs,
    search_astar,
    search_ida_star
)
from utils_2 import format_output, format_output_simple


# ==============================================================================
# NEW HELPER FUNCTION
# Add this function to calculate the cost of a found path.
# ==============================================================================
def calculate_path_cost(graph, path):
    """Calculate total cost of a path by summing edge costs."""
    if not path or len(path) < 2:
        return 0.0
    
    total_cost = 0.0
    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]
        
        if current in graph:
            for neighbor, cost in graph[current]:
                if neighbor == next_node:
                    total_cost += cost
                    break
    
    return total_cost


# Mapping of method names to search functions
METHOD_MAP = {
    'DFS': search_dfs,
    'BFS': search_bfs,
    'UCS': search_ucs,
    'CUS1': search_ucs,      # Alternative name for UCS (uninformed)
    'GBFS': search_gbfs,
    'AS': search_astar,
    'ASTAR': search_astar,   # Alternative name for A* 
    'IDASTAR': search_ida_star,
    'CUS2': search_ida_star  # Alternative name for IDA* based on the assignment (informed)
}


def print_usage():
    """Print usage information."""
    print("Usage: python search.py <filename> <method> [--simple]")
    print("\nAvailable methods:")
    print("  DFS    - Depth-First Search")
    print("  BFS    - Breadth-First Search")
    print("  UCS    - Uniform Cost Search (also: CUS1)")
    print("  GBFS   - Greedy Best-First Search")
    print("  AS     - A* Search (also: ASTAR)")
    print("  IDASTAR    - IDA* Search (also: IDASTAR, CUS2)")
    print("\nOptions:")
    print("  --simple  Use simple output format (for assignment submission)")
    print("\nExamples:")
    print("  python search.py test_cases/test1.txt DFS")
    print("  python search.py test_cases/test1.txt BFS --simple")
    print("  python search.py test_cases/test1.txt IDA")


def main():
    """
    Main entry point for the search program.
    
    Parses command-line arguments, loads the graph from file,
    executes the requested search algorithm, and prints results.
    """
    # Check command-line arguments (minimum 2, maximum 3)
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Error: Incorrect number of arguments\n")
        print_usage()
        sys.exit(1)
    
    filename = sys.argv[1]
    method = sys.argv[2].upper()  # Convert to uppercase for case-insensitive matching
    
    # Check for --simple flag
    use_simple_output = False
    if len(sys.argv) == 4:
        if sys.argv[3] == "--simple":
            use_simple_output = True
        else:
            print(f"Error: Unknown option '{sys.argv[3]}'\n")
            print_usage()
            sys.exit(1)
    
    # Validate method name
    if method not in METHOD_MAP:
        print(f"Error: Invalid method '{sys.argv[2]}'\n")
        print_usage()
        sys.exit(1)
    
    try:
        # Parse the input file to extract graph structure
        graph, node_coords, origin, destinations = parse_input(filename)
        
        # Get the appropriate search function
        search_function = METHOD_MAP[method]
        
        # Execute the search algorithm and get both paths
        # NOTE: Your search algorithms must be modified to return a second_path
        goal, nodes_created, path, second_goal, second_path = search_function(graph, node_coords, origin, destinations)
        
        # ========================================================================
        # MODIFIED SECTION
        # Calculate costs and update the call to the simple formatter
        # ========================================================================
        if use_simple_output:
            if goal is not None:
                # Calculate costs for the paths
                best_cost = calculate_path_cost(graph, path)
                second_cost = calculate_path_cost(graph, second_path) if second_path else None
                
                # Call the updated simple formatter with the new cost information
                format_output_simple(filename, method, goal, nodes_created, path, second_path, best_cost, second_cost)
            else:
                # Handle the "No solution" case for the simple output
                format_output_simple(filename, method, None, 0, [], [], 0.0, None)
        else:
            # The detailed output format is unchanged for now
            format_output(filename, method, goal, nodes_created, path, second_goal, second_path)
        
    except FileNotFoundError as e:
        print("=" * 50)
        print(f"ERROR: {e}")
        print("=" * 50)
        sys.exit(1)
    except ValueError as e:
        print("=" * 50)
        print(f"ERROR: {e}")
        print("=" * 50)
        sys.exit(1)
    except Exception as e:
        print("=" * 50)
        print(f"UNEXPECTED ERROR: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()