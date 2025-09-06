from .file_operations import FileOperations
from .shape_renderer import ShapeRenderer
from .connection_system import ConnectionSystem
from .chain_system import ChainSystem
from .divergent_connections import DivergentConnections


class DiagramRenderer:
    def __init__(self):
        self.file_operations = FileOperations()
        self.shape_renderer = ShapeRenderer()
        self.connection_system = ConnectionSystem()
        self.chain_system = ChainSystem()
        self.divergent_connections = DivergentConnections()
    
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
        pattern_from = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s+connects\s+to'
        
        def replace_from_shape(match):
            label = match.group(1)
            return f"{default_shape.capitalize()}({label}) connects to"
        
        result = re.sub(pattern_from, replace_from_shape, input_text)
        
        # Pattern: after direction keywords, find bare labels
        # Look for "horizontal label" or "vertical label" where label is not Shape(label)
        pattern_to = r'\b(horizontal|vertical)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_to_shape(match):
            direction = match.group(1)
            label = match.group(2)
            return f"{direction} {default_shape.capitalize()}({label})"
            
        result = re.sub(pattern_to, replace_to_shape, result)
        
        # Handle "and" cases: "and label"
        pattern_and = r'\band\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
        
        def replace_and_shape(match):
            label = match.group(1)
            return f"and {default_shape.capitalize()}({label})"
            
        result = re.sub(pattern_and, replace_and_shape, result)
        
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
                    if second_part not in ["point away", "point from", "double point"]:
                        return f"SYNTAX ERROR in '{shape_input}'\nInvalid arrow type: '{second_part}'\nValid arrow types: 'point away', 'point from', 'double point'"
                # If no comma, check if the first part looks like it's trying to be an arrow type
                elif first_part and (" arrow" in first_part or "point" in first_part):
                    # This looks like it's trying to be an arrow type - validate it
                    if first_part not in ["point away", "point from", "double point"]:
                        return f"SYNTAX ERROR in '{shape_input}'\nInvalid arrow type: '{first_part}'\nValid arrow types: 'point away', 'point from', 'double point'"
        
        return None
    
    def render_ascii(self, filename, default_shape=None):
        shapes = self.file_operations.parse_shapes(filename)
        if not shapes:
            return ""
        
        rendered_shapes = []
        for shape_input in shapes:
            # Apply default shape transformation if specified
            if default_shape:
                shape_input = self._apply_default_shape(shape_input, default_shape)
            
            # Validate syntax first
            syntax_error = self._validate_syntax(shape_input)
            if syntax_error:
                rendered_shapes.append(syntax_error)
                continue
            
            # Check if this is divergent connections first
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
        
        return "\n\n".join(rendered_shapes)