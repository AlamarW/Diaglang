from .shape_renderer import ShapeRenderer


class ConnectionSystem:
    def __init__(self):
        self.shape_renderer = ShapeRenderer()
    
    def parse_connection(self, connection_input):
        # Parse "Shape1(Label1) connects to[(label)] [horizontal] Shape2(Label2)" syntax
        if " connects to" not in connection_input:
            return None
        
        # Split on " connects to"
        parts = connection_input.split(" connects to", 1)
        if len(parts) != 2:
            return None
        
        from_part = parts[0].strip()
        to_part = parts[1].strip()
        
        # Check for connection label in parentheses
        connection_label = None
        arrow_type = None
        if to_part.startswith("(") and ")" in to_part:
            # Extract the content within parentheses
            end_paren = to_part.find(")")
            paren_content = to_part[1:end_paren]
            to_part = to_part[end_paren+1:].strip()
            
            # Check if content has comma (label, arrow_type format)
            if "," in paren_content:
                parts = paren_content.split(",", 1)
                connection_label = parts[0].strip()
                potential_arrow_type = parts[1].strip()
                if potential_arrow_type in ["point to", "point back", "double point"]:
                    arrow_type = potential_arrow_type
            else:
                # Single content - check if it's an arrow type or regular label
                if paren_content in ["point to", "point back", "double point"]:
                    arrow_type = paren_content
                else:
                    connection_label = paren_content
        
        # Check for required direction keyword
        horizontal = None
        if to_part.startswith("horizontal "):
            horizontal = True
            to_part = to_part[11:]  # Remove "horizontal " prefix
        elif to_part.startswith("vertical "):
            horizontal = False
            to_part = to_part[9:]  # Remove "vertical " prefix
        else:
            # No direction specified - return None to indicate invalid syntax
            return None
        
        return {
            "from": from_part,
            "to": to_part,
            "horizontal": horizontal,
            "label": connection_label,
            "arrow_type": arrow_type
        }
    
    def render_connection(self, from_shape, to_shape, horizontal=False, label=None, arrow_type=None):
        # Render the from shape
        from_rendered = self.shape_renderer.render_single_shape(from_shape)
        to_rendered = self.shape_renderer.render_single_shape(to_shape)
        
        if not from_rendered or not to_rendered:
            return ""
        
        from_lines = from_rendered.split('\n')
        to_lines = to_rendered.split('\n')
        
        if horizontal:
            return self.render_horizontal_connection(from_lines, to_lines, label, arrow_type)
        else:
            return self.render_vertical_connection(from_lines, to_lines, label, arrow_type)
    
    def render_vertical_connection(self, from_lines, to_lines, label=None, arrow_type=None):
        # Calculate center positions for both shapes
        from_center = self.shape_renderer.get_shape_center_position(from_lines)
        to_center = self.shape_renderer.get_shape_center_position(to_lines)
        
        # Use the maximum center position to ensure alignment
        connection_center = max(from_center, to_center)
        
        # Modify the from shape to have a connection point at the bottom middle
        modified_from = from_lines.copy()
        if len(modified_from) > 0:
            # Replace the bottom border with a connection point
            bottom_line = modified_from[-1]
            if '┘' in bottom_line:
                # Find the middle and replace with connection
                mid_pos = len(bottom_line) // 2
                modified_from[-1] = bottom_line[:mid_pos] + '┬' + bottom_line[mid_pos+1:]
        
        # Pad the from shape if needed to align with connection center
        if from_center < connection_center:
            padding = connection_center - from_center
            padded_from = []
            for line in modified_from:
                padded_from.append(' ' * padding + line)
            modified_from = padded_from
        
        # Create connecting lines with proper centering and arrow type
        connection_indent = ' ' * connection_center
        if arrow_type and label:
            # Handle both label and vertical arrow type
            label_padding = max(0, (connection_center * 2 + 1 - len(label)) // 2)
            label_line = ' ' * label_padding + label
            if arrow_type == "point to":
                connection_lines = [connection_indent + '|', label_line, connection_indent + 'v']
            elif arrow_type == "point back":
                connection_lines = [connection_indent + '^', label_line, connection_indent + '|']
            elif arrow_type == "double point":
                connection_lines = [connection_indent + '^', label_line, connection_indent + 'v']
            else:
                connection_lines = [connection_indent + '│', label_line, connection_indent + '│']  # fallback
        elif arrow_type:
            # Handle vertical arrow types only
            if arrow_type == "point to":
                connection_lines = [connection_indent + '|', connection_indent + '|', connection_indent + 'v']
            elif arrow_type == "point back":
                connection_lines = [connection_indent + '^', connection_indent + '|', connection_indent + '|']
            elif arrow_type == "double point":
                connection_lines = [connection_indent + '^', connection_indent + '|', connection_indent + 'v']
            else:
                connection_lines = [connection_indent + '│', connection_indent + '│']  # fallback
        elif label:
            # Center the label on the connection line
            label_padding = max(0, (connection_center * 2 + 1 - len(label)) // 2)
            label_line = ' ' * label_padding + label
            connection_lines = [connection_indent + '│', label_line, connection_indent + '│']
        else:
            connection_lines = [connection_indent + '│', connection_indent + '│']
        
        # Pad the to shape if needed to align with connection center
        modified_to = to_lines.copy()
        if to_center < connection_center:
            padding = connection_center - to_center
            padded_to = []
            for line in modified_to:
                padded_to.append(' ' * padding + line)
            modified_to = padded_to
        
        # Combine all parts
        result_lines = modified_from + connection_lines + modified_to
        return '\n'.join(result_lines)
    
    def render_horizontal_connection(self, from_lines, to_lines, label=None, arrow_type=None):
        # Place shapes side by side with horizontal connection
        from_height = len(from_lines)
        to_height = len(to_lines)
        max_height = max(from_height, to_height)
        
        # Find the middle line for connection
        from_middle = from_height // 2
        to_middle = to_height // 2
        
        # Get width of from shape
        from_width = max(len(line) for line in from_lines) if from_lines else 0
        
        # Create horizontal connection with optional label and arrow type
        if arrow_type and label:
            # Handle both label and arrow type: ───label───>
            dash_count = 3  # dashes on each side of label
            if arrow_type == "point to":
                connection_line = '─' * dash_count + label + '─' * dash_count + '>'
            elif arrow_type == "point back":
                connection_line = '<' + '─' * dash_count + label + '─' * dash_count
            elif arrow_type == "double point":
                connection_line = '<' + '─' * dash_count + label + '─' * dash_count + '>'
            else:
                connection_line = '─' * dash_count + label + '─' * dash_count  # fallback
            connection_length = len(connection_line)
        elif arrow_type:
            # Handle arrow types only
            if arrow_type == "point to":
                connection_line = "────────>"
            elif arrow_type == "point back":
                connection_line = "<────────"
            elif arrow_type == "double point":
                connection_line = "<──────>"
            else:
                connection_line = "─" * 9  # fallback
            connection_length = len(connection_line)
        elif label:
            # Include both dashes and label for horizontal connections
            dash_count = 3  # dashes on each side of label
            connection_line = '─' * dash_count + label + '─' * dash_count
            connection_length = len(connection_line)
        else:
            connection_length = 6  # Number of dashes for connection
            connection_line = '─' * connection_length
        
        result_lines = []
        
        for i in range(max_height):
            line = ""
            
            # Add from shape line (or padding)
            if i < from_height:
                from_line = from_lines[i]
                # If this is the middle line, modify it to have connection point
                if i == from_middle and '│' in from_line:
                    # Replace right border with regular border for clean connection
                    pass  # Keep the original line unchanged
                line += from_line
            else:
                line += ' ' * from_width
            
            # Add connection line (only on middle line)
            if i == from_middle:
                line += connection_line
            else:
                line += ' ' * connection_length
            
            # Add to shape line (or padding)  
            if i < to_height:
                line += to_lines[i]
            
            result_lines.append(line)
        
        return '\n'.join(result_lines)