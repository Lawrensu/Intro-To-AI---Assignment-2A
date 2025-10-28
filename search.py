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
from utils import format_output, format_output_simple


# Mapping of method names to search functions
METHOD_MAP = {
    'DFS': search_dfs,
    'BFS': search_bfs,
    'UCS': search_ucs,
    'CUS1': search_ucs,      # Alternative name for UCS
    'GBFS': search_gbfs,
    'AS': search_astar,
    'ASTAR': search_astar,   # Alternative name for A*
    'IDA': search_ida_star,
    'IDASTAR': search_ida_star  # Alternative name for IDA*
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
    print("  CUS2   - Best-First Search with Hop Count")
    print("\nOptions:")
    print("  --simple  Use simple output format (for assignment submission)")
    print("\nExamples:")
    print("  python search.py test_cases/test1.txt DFS")
    print("  python search.py test_cases/test1.txt BFS --simple")


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
        
        # Execute the search algorithm
        goal, nodes_created, path = search_function(graph, node_coords, origin, destinations)
        
        # Format and print the output (choose format based on flag)
        if use_simple_output:
            format_output_simple(filename, method, goal, nodes_created, path)
        else:
            format_output(filename, method, goal, nodes_created, path)
        
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