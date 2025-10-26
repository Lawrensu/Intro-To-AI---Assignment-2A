def parse_input(filename):
    """
    Parse input file and extract graph information.
    
    The input file format has four sections:
    - Nodes: node_id: (x, y)
    - Edges: (from, to): cost
    - Origin: starting_node_id
    - Destinations: goal1; goal2; ...
    
    Args:
        filename (str): Path to input text file
        
    Returns:
        tuple: (graph, node_coords, origin, destinations)
            - graph: dict mapping node_id to list of (neighbor_id, cost) tuples
            - node_coords: dict mapping node_id to (x, y) coordinate tuple
            - origin: integer node ID of starting node
            - destinations: list of integer node IDs that are valid goals
            
    Raises:
        FileNotFoundError: If the input file doesn't exist
        ValueError: If the file format is invalid
    """
    graph = {}
    node_coords = {}
    origin = None
    destinations = []
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Remove empty lines and strip whitespace
        lines = [line.strip() for line in lines if line.strip()]
        
        current_section = None
        
        for line in lines:
            # Identify section headers
            if line.startswith("Nodes:"):
                current_section = "nodes"
                continue
            elif line.startswith("Edges:"):
                current_section = "edges"
                continue
            elif line.startswith("Origin:"):
                current_section = "origin"
                continue
            elif line.startswith("Destinations:"):
                current_section = "destinations"
                continue
            
            # Parse each section
            if current_section == "nodes":
                # Format: "1: (4,1)"
                parts = line.split(':')
                if len(parts) != 2:
                    continue
                    
                node_id = int(parts[0].strip())
                # Extract coordinates from "(x,y)" format
                coords_str = parts[1].strip().strip('()')
                x, y = map(int, coords_str.split(','))
                node_coords[node_id] = (x, y)
                
                # Initialize empty adjacency list for this node
                if node_id not in graph:
                    graph[node_id] = []
                    
            elif current_section == "edges":
                # Format: "(2,1): 4" means edge from node 2 to node 1 with cost 4
                parts = line.split(':')
                if len(parts) != 2:
                    continue
                    
                # Extract from and to nodes
                edge_str = parts[0].strip().strip('()')
                from_node, to_node = map(int, edge_str.split(','))
                
                # Extract cost
                cost = float(parts[1].strip())
                
                # Add edge to adjacency list (directed graph)
                if from_node not in graph:
                    graph[from_node] = []
                graph[from_node].append((to_node, cost))
                
                # Ensure to_node exists in graph even if it has no outgoing edges
                if to_node not in graph:
                    graph[to_node] = []
                    
            elif current_section == "origin":
                origin = int(line.strip())
                
            elif current_section == "destinations":
                # Format: "5; 4" or "5;4" - semicolon-separated list
                dest_parts = line.split(';')
                destinations = [int(d.strip()) for d in dest_parts]
        
        # Validate that we got all required information
        if origin is None:
            raise ValueError("No origin node specified in input file")
        if not destinations:
            raise ValueError("No destination nodes specified in input file")
        if not graph:
            raise ValueError("No graph edges found in input file")
            
        return graph, node_coords, origin, destinations
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{filename}' not found")
    except Exception as e:
        raise ValueError(f"Error parsing input file: {str(e)}")