class SearchNode:
    """
    Represents a node in the search tree.
    
    Each SearchNode tracks the current position in the graph, the path taken
    to reach it, the total cost, and the number of hops (edges traversed).
    
    Attributes:
        current_node (int): The graph node ID we're currently at
        path (list): List of node IDs representing the full path from origin
        cost (float): Total edge cost from origin to current node
        hops (int): Number of edges traversed from origin
    """
    
    def __init__(self, current_node: int, path: list, cost: float = 0, hops: int = 0):
        """
        Initialize a search node.
        
        Args:
            current_node (int): The graph node ID we're currently at
            path (list): List of node IDs representing the full path from origin
            cost (float): Total edge cost from origin to current node (default: 0)
            hops (int): Number of edges traversed from origin (default: 0)
        """
        self.current_node = current_node
        self.path = path.copy()  # Create a copy to avoid reference issues
        self.cost = cost
        self.hops = hops
    
    def __lt__(self, other):
        """
        Less-than comparison for priority queue tie-breaking.
        
        When priorities are equal in heapq, this method is used to break ties.
        We compare by current_node to ensure consistent, deterministic ordering.
        
        Args:
            other (SearchNode): Another SearchNode to compare with
            
        Returns:
            bool: True if this node's ID is less than the other's
        """
        return self.current_node < other.current_node
    
    def __repr__(self):
        """
        String representation for debugging.
        
        Returns:
            str: Human-readable representation of the SearchNode
        """
        return (f"SearchNode(node={self.current_node}, path={self.path}, "
                f"cost={self.cost:.2f}, hops={self.hops})")