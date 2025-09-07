from .file_operations import FileOperations
from .shape_renderer import ShapeRenderer
from .connection_system import ConnectionSystem
from .chain_system import ChainSystem
from .divergent_connections import DivergentConnections
from .network_system import NetworkSystem


class DiagramRenderer:
    def __init__(self):
        self.file_operations = FileOperations()
        self.shape_renderer = ShapeRenderer()
        self.connection_system = ConnectionSystem()
        self.chain_system = ChainSystem()
        self.divergent_connections = DivergentConnections()
        self.network_system = NetworkSystem(self.shape_renderer, self.connection_system)
    
    # Expose file operations methods for backward compatibility with tests
    def read_file(self, filename):
        return self.file_operations.read_file(filename)
    
    def parse_shapes(self, filename):
        return self.file_operations.parse_shapes(filename)
    
    def _apply_default_shape(self, input_text, default_shape):
        """Convert bare labels to full shape syntax when default_shape is specified"""
        if not default_shape:
            return input_text
            
        import re
        
        # Pattern to find bare labels (words without parentheses that aren't already part of Shape(label) syntax)
        # This should match words that are:
        # 1. At the beginning of the string, or
        # 2. After "connects to" clauses, or  
        # 3. After "and" keywords
        # But NOT words that are already part of Shape(label) syntax
        
        # First, let's handle connections with bare labels
        # Pattern: "label connects to" where label is not Shape(label)
        # Updated to handle multi-word labels (words and spaces, but not other syntax elements)
        pattern_from = r'^([a-zA-Z_][a-zA-Z0-9_\s]*?)\s+connects\s+to'
        
        def replace_from_shape(match):
            label = match.group(1).strip()
            return f"{default_shape.capitalize()}({label}) connects to"
        
        result = re.sub(pattern_from, replace_from_shape, input_text)
        
        # Pattern: after direction keywords, find bare labels
        # Look for "horizontal label" or "vertical label" where label is not Shape(label)
        # Updated to handle multi-word labels at end of string
        pattern_to = r'\b(horizontal|vertical)\s+([a-zA-Z_][a-zA-Z0-9_\s]*?)$'
        
        def replace_to_shape(match):
            direction = match.group(1)
            label = match.group(2).strip()
            return f"{direction} {default_shape.capitalize()}({label})"
            
        result = re.sub(pattern_to, replace_to_shape, result)
        
        # Handle "and" cases: "and label"
        # Updated to handle multi-word labels at end of string or before other keywords
        pattern_and = r'\band\s+([a-zA-Z_][a-zA-Z0-9_\s]*?)(?=\s|$)'
        
        def replace_and_shape(match):
            label = match.group(1).strip()
            return f"and {default_shape.capitalize()}({label})"
            
        result = re.sub(pattern_and, replace_and_shape, result)
        
        # Handle standalone labels (entire string is just a label)
        # This should only match if the string doesn't contain "connects to" or other syntax
        if " connects to" not in result and not re.search(r'[(){}]', result):
            # It's likely a standalone label
            label = result.strip()
            if label and re.match(r'^[a-zA-Z_][a-zA-Z0-9_\s]*$', label):
                result = f"{default_shape.capitalize()}({label})"
        
        return result
    
    def _validate_syntax(self, shape_input):
        """Validate syntax and return error message if invalid, None if valid"""
        import re
        
        # Check for connection syntax without direction
        if " connects to" in shape_input:
            # Check if it has direction keywords
            if not re.search(r'\b(horizontal|vertical)\b', shape_input):
                return f"SYNTAX ERROR in '{shape_input}'\nMissing direction keyword. Use 'horizontal' or 'vertical'.\nExample: Rectangle(A) connects to horizontal Triangle(B)"
            
            # Check for invalid arrow types
            arrow_match = re.search(r'connects\s+to\(([^,)]+)(?:,\s*([^)]+))?\)', shape_input)
            if arrow_match:
                first_part = arrow_match.group(1).strip() if arrow_match.group(1) else ""
                second_part = arrow_match.group(2).strip() if arrow_match.group(2) else ""
                
                # If there's a comma, the second part should be the arrow type
                if second_part:
                    if second_part not in ["point to", "point back", "double point"]:
                        return f"SYNTAX ERROR in '{shape_input}'\nInvalid arrow type: '{second_part}'\nValid arrow types: 'point to', 'point back', 'double point'"
                # If no comma, check if the first part looks like it's trying to be an arrow type
                elif first_part and (" arrow" in first_part or "point" in first_part):
                    # This looks like it's trying to be an arrow type - validate it
                    if first_part not in ["point to", "point back", "double point"]:
                        return f"SYNTAX ERROR in '{shape_input}'\nInvalid arrow type: '{first_part}'\nValid arrow types: 'point to', 'point back', 'double point'"
        
        return None
    
    def render_ascii(self, filename, default_shape=None):
        shapes = self.file_operations.parse_shapes(filename)
        if not shapes:
            return ""
        
        # Check if first line is a title and extract it
        title = None
        diagram_shapes = shapes
        
        if shapes and shapes[0].strip().startswith('Title(') and shapes[0].strip().endswith(')'):
            title_line = shapes[0].strip()
            title = title_line[6:-1]  # Extract text between Title( and )
            diagram_shapes = shapes[1:]  # Rest of the shapes
        
        if not diagram_shapes:
            # Only title, no shapes
            return title if title else ""
        
        # Apply default shape transformation to all shapes first
        processed_shapes = []
        for shape_input in diagram_shapes:
            if default_shape:
                shape_input = self._apply_default_shape(shape_input, default_shape)
            processed_shapes.append(shape_input)
        
        # Check if this looks like a complex network (multiple connections with shared nodes that have both incoming and outgoing)
        connection_count = sum(1 for shape in processed_shapes if ' connects to ' in shape)
        if connection_count > 1:
            # Try to detect if there are nodes with both incoming and outgoing connections
            network = self.network_system.parse_network(processed_shapes)
            complex_nodes = [name for name, node in network['nodes'].items() 
                           if node['incoming'] and node['outgoing']]
            
            if complex_nodes:
                # This is a complex network, use network system
                diagram_content = self.network_system.render_network(network)
                if title:
                    return title + '\n\n' + diagram_content
                return diagram_content
        
        # Fall back to original per-shape rendering
        rendered_shapes = []
        for shape_input in processed_shapes:
            
            # Validate syntax first
            syntax_error = self._validate_syntax(shape_input)
            if syntax_error:
                rendered_shapes.append(syntax_error)
                continue
            
            # Check if this is convergent connections first
            convergent = self.divergent_connections.parse_convergent_connections(shape_input)
            if convergent:
                rendered_convergent = self.divergent_connections.render_convergent_connections(convergent)
                if rendered_convergent:
                    rendered_shapes.append(rendered_convergent)
            else:
                # Check if this is divergent connections  
                divergent = self.divergent_connections.parse_divergent_connections(shape_input)
                if divergent:
                    rendered_divergent = self.divergent_connections.render_divergent_connections(divergent)
                    if rendered_divergent:
                        rendered_shapes.append(rendered_divergent)
                else:
                    # Check if this is a chain
                    chain = self.chain_system.parse_chain(shape_input)
                    if chain:
                        rendered_chain = self.chain_system.render_chain(chain)
                        if rendered_chain:
                            rendered_shapes.append(rendered_chain)
                    else:
                        # Check if this is a single connection
                        connection = self.connection_system.parse_connection(shape_input)
                        if connection:
                            rendered_connection = self.connection_system.render_connection(
                                connection["from"], connection["to"], connection["horizontal"], 
                                connection["label"], connection.get("arrow_type")
                            )
                            if rendered_connection:
                                rendered_shapes.append(rendered_connection)
                        else:
                            rendered_shape = self.shape_renderer.render_single_shape(shape_input)
                            if rendered_shape:
                                rendered_shapes.append(rendered_shape)
        
        diagram_content = "\n\n".join(rendered_shapes)
        if title:
            return title + '\n\n' + diagram_content
        return diagram_content