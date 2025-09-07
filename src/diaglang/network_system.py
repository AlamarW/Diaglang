class NetworkSystem:
    def __init__(self, shape_renderer, connection_system):
        self.shape_renderer = shape_renderer
        self.connection_system = connection_system
    
    def parse_network(self, lines):
        """Parse all connection lines and build a network graph"""
        network = {
            'nodes': {},  # node_name -> node_info
            'connections': []  # list of connection info
        }
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if this is a connection line
            if ' connects to ' in line:
                connection_info = self._parse_connection_line(line)
                if connection_info:
                    # Add nodes to network
                    source = connection_info['source']
                    target = connection_info['target']
                    
                    if source['name'] not in network['nodes']:
                        network['nodes'][source['name']] = {
                            'shape': source['shape'],
                            'label': source['label'],
                            'incoming': [],
                            'outgoing': []
                        }
                    
                    if target['name'] not in network['nodes']:
                        network['nodes'][target['name']] = {
                            'shape': target['shape'], 
                            'label': target['label'],
                            'incoming': [],
                            'outgoing': []
                        }
                    
                    # Add connection
                    network['connections'].append(connection_info)
                    network['nodes'][source['name']]['outgoing'].append(connection_info)
                    network['nodes'][target['name']]['incoming'].append(connection_info)
            else:
                # Single shape
                shape_info = self._parse_single_shape(line)
                if shape_info and shape_info['name'] not in network['nodes']:
                    network['nodes'][shape_info['name']] = {
                        'shape': shape_info['shape'],
                        'label': shape_info['label'],
                        'incoming': [],
                        'outgoing': []
                    }
        
        return network
    
    def _parse_connection_line(self, line):
        """Parse a single connection line"""
        import re
        
        # Basic pattern: Source connects to [label] direction Target
        pattern = r'(\w+(?:\([^)]*\))?)\s+connects\s+to(?:\(([^)]*)\))?\s+(horizontal|vertical)\s+(\w+(?:\([^)]*\))?)'
        match = re.match(pattern, line)
        
        if not match:
            return None
            
        source_str, label, direction, target_str = match.groups()
        
        return {
            'source': self._parse_shape_ref(source_str),
            'target': self._parse_shape_ref(target_str),
            'label': label,
            'direction': direction
        }
    
    def _parse_shape_ref(self, shape_str):
        """Parse a shape reference like Rectangle(label) or just label"""
        if '(' in shape_str and shape_str.endswith(')'):
            shape_type = shape_str.split('(')[0].lower()
            label = shape_str.split('(')[1][:-1]
            name = label if label else shape_type
        else:
            shape_type = 'rectangle'  # default
            label = shape_str
            name = shape_str
            
        return {
            'shape': shape_type,
            'label': label,
            'name': name
        }
    
    def _parse_single_shape(self, line):
        """Parse a single shape line"""
        return self._parse_shape_ref(line)
    
    def render_network(self, network):
        """Render a complete network with proper layout"""
        if not network['nodes']:
            return ""
            
        # For now, implement a simple layout strategy
        # TODO: Implement more sophisticated layout algorithms
        
        # If there are no connections, render individual shapes
        if not network['connections']:
            results = []
            for node_name, node_info in network['nodes'].items():
                shape_input = f"{node_info['shape'].capitalize()}({node_info['label']})"
                rendered = self.shape_renderer.render_single_shape(shape_input)
                results.append(rendered)
            return "\n\n".join(results)
        
        # For complex networks, use a grid-based layout approach
        return self._render_complex_network(network)
    
    def _render_complex_network(self, network):
        """Render complex network with multiple connections"""
        # Identify node types
        central_nodes = []
        input_nodes = []
        output_nodes = []
        
        for name, node in network['nodes'].items():
            if node['incoming'] and node['outgoing']:
                central_nodes.append(name)
            elif not node['incoming'] and node['outgoing']:
                input_nodes.append(name)
            elif node['incoming'] and not node['outgoing']:
                output_nodes.append(name)
        
        if not central_nodes:
            # No central nodes, fall back to individual connections
            return self._render_separate_connections(network)
        
        # Take the first central node as the main hub
        central_node = central_nodes[0]
        central_info = network['nodes'][central_node]
        central_shape = f"{central_info['shape'].capitalize()}({central_info['label']})"
        central_rendered = self.shape_renderer.render_single_shape(central_shape)
        central_lines = central_rendered.split('\n')
        
        # Create a grid layout
        result_sections = []
        
        # Render input connections (multiple inputs connecting to central)
        if input_nodes:
            for input_node in input_nodes:
                input_info = network['nodes'][input_node]
                input_shape = f"{input_info['shape'].capitalize()}({input_info['label']})"
                
                # Use the connection system to render this pair
                connection_line = f"{input_shape} connects to horizontal {central_shape}"
                parsed_connection = self.connection_system.parse_connection(connection_line)
                if parsed_connection:
                    rendered_connection = self.connection_system.render_connection(
                        parsed_connection["from"], parsed_connection["to"], parsed_connection["horizontal"], 
                        parsed_connection["label"], parsed_connection.get("arrow_type")
                    )
                    if rendered_connection:
                        result_sections.append(rendered_connection)
        
        # Render output connections (central connecting to multiple outputs)
        if output_nodes:
            for output_node in output_nodes:
                output_info = network['nodes'][output_node]
                output_shape = f"{output_info['shape'].capitalize()}({output_info['label']})"
                
                # Use the connection system to render this pair
                connection_line = f"{central_shape} connects to horizontal {output_shape}"
                parsed_connection = self.connection_system.parse_connection(connection_line)
                if parsed_connection:
                    rendered_connection = self.connection_system.render_connection(
                        parsed_connection["from"], parsed_connection["to"], parsed_connection["horizontal"], 
                        parsed_connection["label"], parsed_connection.get("arrow_type")
                    )
                    if rendered_connection:
                        result_sections.append(rendered_connection)
        
        # If we have both inputs and outputs, we need a different approach
        if input_nodes and output_nodes:
            # Create a comprehensive layout showing the central node only once
            # This is complex - for now, show input->central and central->output separately
            # but ensure central appears only once by using the first input->central connection
            # and replacing subsequent central nodes with spacing
            
            if result_sections:
                first_section = result_sections[0]  # This contains central node
                remaining_sections = []
                
                for section in result_sections[1:]:
                    # Replace central node appearances with equivalent spacing
                    section_lines = section.split('\n')
                    cleaned_lines = []
                    for line in section_lines:
                        if central_info['label'] in line:
                            # Replace the central node with spaces to maintain layout
                            cleaned_line = line.replace(central_info['label'], ' ' * len(central_info['label']))
                            # Also clean up the box characters
                            for char in ['┌', '┐', '└', '┘', '│', '─']:
                                cleaned_line = cleaned_line.replace(char, ' ')
                            cleaned_lines.append(cleaned_line)
                        else:
                            cleaned_lines.append(line)
                    remaining_sections.append('\n'.join(cleaned_lines))
                
                return first_section + '\n\n' + '\n\n'.join(remaining_sections)
        
        return '\n\n'.join(result_sections) if result_sections else central_rendered
    
    def _render_separate_connections(self, network):
        """Render connections separately (fallback method)"""
        results = []
        for connection in network['connections']:
            source = connection['source']
            target = connection['target']
            
            source_shape = f"{source['shape'].capitalize()}({source['label']})"
            target_shape = f"{target['shape'].capitalize()}({target['label']})"
            
            connection_line = f"{source_shape} connects to {connection['direction']} {target_shape}"
            if connection['label']:
                connection_line = f"{source_shape} connects to({connection['label']}) {connection['direction']} {target_shape}"
            
            parsed = self.connection_system.parse_connection(connection_line)
            if parsed:
                rendered = self.connection_system.render_connection(
                    parsed["from"], parsed["to"], parsed["horizontal"], 
                    parsed["label"], parsed.get("arrow_type")
                )
                results.append(rendered)
        
        return '\n\n'.join(results)