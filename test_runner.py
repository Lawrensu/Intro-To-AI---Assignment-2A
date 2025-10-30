"""
Automated test runner for all search algorithms
Runs all algorithms on all test cases and generates detailed report
"""

import subprocess
import time
import sys
from pathlib import Path

# Test case configurations
TEST_CASES = [
    ("test_cases/test_linear.txt", "Linear Path", "Simple baseline"),
    ("test_cases/test_diamond.txt", "Diamond Graph", "Multiple paths"),
    ("test_cases/test_wide.txt", "Wide Branching", "Branching factor test"),
    ("test_cases/test_depth.txt", "Deep vs Shallow", "DFS depth preference"),
    ("test_cases/test_misleading.txt", "Misleading Heuristic", "Heuristic quality"),
    ("test_cases/test_multi_destin.txt", "Multiple Destinations", "Multiple goals"),
    ("test_cases/test_sparse.txt", "Sparse Graph", "Long linear path"),
    ("test_cases/test_obstacle.txt", "Grid with Obstacles", "Grid pathfinding"),
    ("test_cases/test_no_solution.txt", "No Solution", "Unreachable goal"),
    ("test_cases/test_cycle.txt", "Cyclic Graph", "Cycle handling"),
    ("test_cases/test_exponential.txt", "Exponential Branching", "Memory stress"),
    ("test_cases/test_long_path.txt", "Long Path (50 nodes)", "Deep search stress"),
]

ALGORITHMS = ["DFS", "BFS", "UCS", "GBFS", "AS", "IDASTAR"]

ALGORITHM_NAMES = {
    "DFS": "DFS",
    "BFS": "BFS",
    "UCS": "UCS",
    "GBFS": "GBFS",
    "AS": "A*",
    "IDASTAR": "IDA*"
}

def calculate_path_cost(graph, path):
    """Calculate total cost of a path by summing edge costs."""
    if not path or len(path) < 2:
        return 0.0
    
    total_cost = 0.0
    for i in range(len(path) - 1):
        current = int(path[i])
        next_node = int(path[i + 1])
        
        if current in graph:
            for neighbor, cost in graph[current]:
                if neighbor == next_node:
                    total_cost += cost
                    break
    
    return total_cost

def parse_graph_from_file(filename):
    """Parse graph structure from input file to calculate path costs."""
    graph = {}
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        lines = [line.strip() for line in lines if line.strip()]
        current_section = None
        
        for line in lines:
            if line.startswith("Edges:"):
                current_section = "edges"
                continue
            elif line.startswith("Origin:") or line.startswith("Destinations:"):
                break
            
            if current_section == "edges":
                parts = line.split(':')
                if len(parts) != 2:
                    continue
                
                edge_str = parts[0].strip().strip('()')
                from_node, to_node = map(int, edge_str.split(','))
                cost = float(parts[1].strip())
                
                if from_node not in graph:
                    graph[from_node] = []
                graph[from_node].append((to_node, cost))
    
    except Exception as e:
        print(f"Warning: Could not parse graph from {filename}: {e}")
        return {}
    
    return graph

def run_search(filename, algorithm, timeout=30):
    """Run a single search and return results."""
    try:
        start = time.time()
        result = subprocess.run(
            ["python", "search.py", filename, algorithm, "--simple"],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        elapsed = (time.time() - start) * 1000
        
        if result.returncode != 0:
            return {
                'goal': 'ERROR', 'nodes': 0, 'path': [], 'path_str': '-',
                'path_cost': 0, 'time_ms': elapsed, 'success': False, 'error': result.stderr
            }
        
        lines = result.stdout.strip().split('\n')
        if len(lines) < 2:
            return {
                'goal': 'ERROR', 'nodes': 0, 'path': [], 'path_str': '-',
                'path_cost': 0, 'time_ms': elapsed, 'success': False, 'error': 'Invalid output format'
            }
        
        parts = lines[1].split()
        if parts[0] == "No":
            goal = "No solution"
            nodes = int(parts[2])
            path = []
            path_str = "No path"
            path_cost = 0
        else:
            goal = int(parts[0])
            nodes = int(parts[1])
            path = lines[2].split() if len(lines) > 2 else []
            path_str = " -> ".join(path) if path else "Empty"
            
            graph = parse_graph_from_file(filename)
            path_cost = calculate_path_cost(graph, path)
        
        return {
            'goal': goal, 'nodes': nodes, 'path': path, 'path_str': path_str,
            'path_cost': path_cost, 'time_ms': elapsed, 'success': True
        }
        
    except subprocess.TimeoutExpired:
        return {
            'goal': 'TIMEOUT', 'nodes': 0, 'path': [], 'path_str': '-',
            'path_cost': 0, 'time_ms': timeout * 1000, 'success': False,
            'error': f'Timeout after {timeout}s'
        }
    except Exception as e:
        return {
            'goal': 'ERROR', 'nodes': 0, 'path': [], 'path_str': '-',
            'path_cost': 0, 'time_ms': 0, 'success': False, 'error': str(e)
        }

def print_header():
    """Print the report header."""
    print("\n" + "=" * 120)
    print(f"{'SEARCH ALGORITHM TEST REPORT':^120}")
    print("=" * 120 + "\n")

def print_test_case_header(test_name, description):
    """Print test case header."""
    print(f"\n{'='*120}")
    print(f"Test: {test_name} - {description}")
    print(f"{'='*120}")
    print(f"{'Algo':<8} | {'Goal':<6} | {'Nodes':<6} | {'Cost':<7} | {'Time':<8} | {'Path':<55}")
    print("-" * 120)

def print_result_row(algo_name, result):
    """Print a single result row."""
    goal_str = str(result['goal']) if result['goal'] != 'No solution' else 'None'
    nodes_str = str(result['nodes'])
    cost_str = f"{result['path_cost']:.1f}" if result['path_cost'] > 0 else "-"
    time_str = f"{result['time_ms']:.1f}ms"
    
    path_str = result['path_str']
    if len(path_str) > 50:
        path_str = path_str[:47] + "..."
    
    status = "OK" if result['success'] else "FAIL"
    
    print(f"{algo_name:<8} | {goal_str:<6} | {nodes_str:<6} | {cost_str:<7} | {time_str:<8} | {path_str:<55} [{status}]")

def print_summary(all_results):
    """Print summary statistics."""
    print(f"\n{'='*120}")
    print(f"{'SUMMARY':^120}")
    print(f"{'='*120}\n")
    
    for test_file, test_name, description in TEST_CASES:
        print(f"\n[{test_name}]")
        
        test_results = {algo: all_results.get((test_file, algo)) for algo in ALGORITHMS}
        valid_results = {k: v for k, v in test_results.items() 
                        if v and v['success'] and v['goal'] != 'No solution'}
        
        if not valid_results:
            print("  No solution exists (as expected)")
            continue
        
        goals = {v['goal'] for v in valid_results.values()}
        if len(goals) != 1:
            print(f"  WARNING: Different goals reached: {goals}")
            continue
        
        print(f"  Goal: {list(goals)[0]}")
        
        # Cost analysis
        costs = {k: v['path_cost'] for k, v in valid_results.items()}
        min_cost = min(costs.values())
        max_cost = max(costs.values())
        
        optimal_algos = [k for k, cost in costs.items() if cost == min_cost]
        suboptimal_algos = [k for k, cost in costs.items() if cost > min_cost]
        
        print(f"  Optimal Cost: {min_cost:.1f}")
        print(f"    Found by: {', '.join(ALGORITHM_NAMES[a] for a in optimal_algos)}")
        
        if suboptimal_algos:
            print(f"  Suboptimal: {', '.join(ALGORITHM_NAMES[a] for a in suboptimal_algos)}")
            print(f"    Worst cost: {max_cost:.1f} ({max_cost/min_cost:.2f}x optimal)")
        
        # Memory efficiency
        min_nodes = min(v['nodes'] for v in valid_results.values())
        max_nodes = max(v['nodes'] for v in valid_results.values())
        
        most_efficient = [k for k, v in valid_results.items() if v['nodes'] == min_nodes]
        least_efficient = [k for k, v in valid_results.items() if v['nodes'] == max_nodes]
        
        print(f"  Memory: {min_nodes} - {max_nodes} nodes", end="")
        if min_nodes != max_nodes:
            print(f" ({max_nodes/min_nodes:.2f}x ratio)")
        else:
            print()
        print(f"    Most efficient: {', '.join(ALGORITHM_NAMES[a] for a in most_efficient)}")
        if min_nodes != max_nodes:
            print(f"    Least efficient: {', '.join(ALGORITHM_NAMES[a] for a in least_efficient)}")
        
        # Speed
        fastest_time = min(v['time_ms'] for v in valid_results.values())
        slowest_time = max(v['time_ms'] for v in valid_results.values())
        fastest = [k for k, v in valid_results.items() if v['time_ms'] == fastest_time]
        slowest = [k for k, v in valid_results.items() if v['time_ms'] == slowest_time]
        
        print(f"  Speed: {fastest_time:.1f}ms - {slowest_time:.1f}ms")
        print(f"    Fastest: {', '.join(ALGORITHM_NAMES[a] for a in fastest)}")
        if fastest_time != slowest_time:
            print(f"    Slowest: {', '.join(ALGORITHM_NAMES[a] for a in slowest)}")
        
        # Path differences
        paths = {ALGORITHM_NAMES[k]: (v['path_str'], v['path_cost']) for k, v in valid_results.items()}
        unique_paths = set((path, cost) for path, cost in paths.values())
        
        if len(unique_paths) > 1:
            print(f"  Different Paths:")
            for algo, (path, cost) in sorted(paths.items()):
                display_path = path if len(path) <= 45 else path[:42] + "..."
                cost_marker = "" if cost == min_cost else f" (suboptimal: {cost:.1f})"
                print(f"    {algo:6s}: {display_path}{cost_marker}")
    
    # Overall statistics
    print(f"\n{'='*120}")
    print(f"{'OVERALL STATISTICS':^120}")
    print(f"{'='*120}\n")
    
    total_tests = len(TEST_CASES) * len(ALGORITHMS)
    successful = sum(1 for r in all_results.values() if r and r['success'])
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful} ({successful/total_tests*100:.1f}%)\n")
    
    print(f"{'Algorithm':<10} | {'Avg Nodes':<10} | {'Avg Cost':<10} | {'Avg Time':<10} | {'Success':<8}")
    print("-" * 120)
    
    for algo in ALGORITHMS:
        algo_results = [r for r in all_results.values() 
                       if r and r.get('_algo') == algo and r['success']]
        
        if algo_results:
            avg_nodes = sum(r['nodes'] for r in algo_results) / len(algo_results)
            
            results_with_paths = [r for r in algo_results if r['path_cost'] > 0]
            avg_cost = sum(r['path_cost'] for r in results_with_paths) / len(results_with_paths) if results_with_paths else 0
            
            avg_time = sum(r['time_ms'] for r in algo_results) / len(algo_results)
            success_rate = len(algo_results) / len(TEST_CASES) * 100
            
            print(f"{ALGORITHM_NAMES[algo]:<10} | {avg_nodes:<10.1f} | {avg_cost:<10.1f} | {avg_time:<9.1f}ms | {success_rate:<7.1f}%")

def main():
    """Main test runner."""
    print_header()
    
    if not Path("search.py").exists():
        print("ERROR: search.py not found!")
        print("Make sure you're running this from the project root directory.")
        sys.exit(1)
    
    print(f"Running {len(TEST_CASES)} test cases with {len(ALGORITHMS)} algorithms")
    print(f"Total: {len(TEST_CASES) * len(ALGORITHMS)} tests\n")
    
    all_results = {}
    
    for test_file, test_name, description in TEST_CASES:
        print_test_case_header(test_name, description)
        
        for algo in ALGORITHMS:
            result = run_search(test_file, algo)
            result['_algo'] = algo
            all_results[(test_file, algo)] = result
            
            print_result_row(ALGORITHM_NAMES[algo], result)
    
    print_summary(all_results)
    
    print(f"\n{'='*120}")
    print(f"{'TEST COMPLETE':^120}")
    print(f"{'='*120}\n")

if __name__ == "__main__":
    main()