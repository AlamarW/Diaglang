class DiagReader:
    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()
    
    def parse_shapes(self, filename):
        content = self.read_file(filename)
        return content.strip().split('\n') if content.strip() else []
    
    def render_single_shape(self, shape_input):
        # Parse shape and label
        if '(' in shape_input and shape_input.endswith(')'):
            shape_type = shape_input.split('(')[0].lower()
            label = shape_input.split('(')[1][:-1]
        else:
            shape_type = shape_input.lower()
            label = None
        
        if shape_type == "square":
            if label:
                width = len(label) + 2  # padding on both sides
                border = "─" * width
                return f"┌{border}┐\n│ {label} │\n└{border}┘"
            return "┌───┐\n│   │\n└───┘"
        elif shape_type == "circle":
            if label is not None:
                # Create proper oval shape  
                label_len = len(label)
                width = max(6, label_len + 2)
                padding_total = width - label_len
                pad_left = " " * ((padding_total // 2)+1)
                pad_right = " " * ((padding_total // 2)+1)
                # If odd padding, add extra space to right
                if padding_total % 2 == 1:
                    pad_right += " "
                underline = "_" * width
                spaces = " " * width
                
                return f"  {underline}  \n /{spaces}\\ \n|{pad_left}{label}{pad_right}|\n \\{underline}/ "
            return "  ____  \n /    \\ \n|      |\n \\____/ "
        elif shape_type == "triangle":
            if label is not None:
                if label == "":
                    return "   /\\   \n  /  \\  \n /    \\ \n/______\\"
                # Create proper triangle shape that scales with label
                label_len = len(label)
                
                # For very small labels (1-3 chars), use minimal triangle
                if label_len <= 3:
                    if label_len == 1:
                        return f"  /\\\n /{label} \\\n/____\\"
                    elif label_len == 2:
                        return f"  /\\\n /{label}\\\n/____\\"
                    else:  # label_len == 3
                        return f"  /\\\n /{label}\\\n/_____\\"
                
                # For longer labels, use the scaling algorithm
                # Calculate how many rows we need based on label length
                min_rows = 4  # minimum: top, middle, label, base
                extra_rows = max(0, (label_len - 4) // 2)  # add rows for longer labels
                total_rows = min_rows + extra_rows
                
                lines = []
                
                # Build triangle from top down, each row indented one less than the previous
                for i in range(total_rows):
                    indent = " " * (total_rows - i - 1)
                    
                    if i == 0:
                        # Top point
                        lines.append(f"{indent}/\\")
                    elif i == total_rows - 2:
                        # Label row (second to last)
                        lines.append(f"{indent}/{label}\\")
                    elif i == total_rows - 1:
                        # Base row with underscores
                        base_width = label_len + 2
                        base = "_" * base_width
                        lines.append(f"{indent}/{base}\\")
                    else:
                        # Middle expanding rows
                        inner_spaces = " " * (2 * i)
                        lines.append(f"{indent}/{inner_spaces}\\")
                
                return "\n".join(lines)
            return "   /\\   \n  /  \\  \n /    \\ \n/______\\"
        elif shape_type == "rectangle":
            if label is not None:
                if label == "":
                    return "┌──┐\n│  │\n└──┘"
                width = len(label) + 2  # padding on both sides
                border = "─" * width
                return f"┌{border}┐\n│ {label} │\n└{border}┘"
            return "┌─────┐\n│     │\n└─────┘"
        return ""
    
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
        if to_part.startswith("(") and ")" in to_part:
            # Extract the connection label
            end_paren = to_part.find(")")
            connection_label = to_part[1:end_paren]
            to_part = to_part[end_paren+1:].strip()
        
        # Check if horizontal keyword is present
        horizontal = False
        if to_part.startswith("horizontal "):
            horizontal = True
            to_part = to_part[11:]  # Remove "horizontal " prefix
        
        return {
            "from": from_part,
            "to": to_part,
            "horizontal": horizontal,
            "label": connection_label
        }
    
    def render_connection(self, from_shape, to_shape, horizontal=False, label=None):
        # Render the from shape
        from_rendered = self.render_single_shape(from_shape)
        to_rendered = self.render_single_shape(to_shape)
        
        if not from_rendered or not to_rendered:
            return ""
        
        from_lines = from_rendered.split('\n')
        to_lines = to_rendered.split('\n')
        
        if horizontal:
            return self.render_horizontal_connection(from_lines, to_lines, label)
        else:
            return self.render_vertical_connection(from_lines, to_lines, label)
    
    def render_vertical_connection(self, from_lines, to_lines, label=None):
        # Find middle of each shape for connection
        from_middle_line = len(from_lines) // 2
        to_middle_line = len(to_lines) // 2
        
        # Get width of from shape to determine where to place connection
        from_width = len(from_lines[0]) if from_lines else 0
        from_center = from_width // 2
        
        # Modify the from shape to have a connection point at the bottom middle
        modified_from = from_lines.copy()
        if len(modified_from) > 0:
            # Replace the bottom border with a connection point
            bottom_line = modified_from[-1]
            if '┘' in bottom_line:
                # Find the middle and replace with connection
                mid_pos = len(bottom_line) // 2
                modified_from[-1] = bottom_line[:mid_pos] + '┬' + bottom_line[mid_pos+1:]
        
        # Create connecting lines with optional label
        if label:
            # Center the label properly on the connection line (4 spaces to align with │)
            label_padding = max(0, (4 - len(label)) // 2)
            label_line = ' ' * label_padding + label
            connection_lines = ['    │', label_line, '    │']
        else:
            connection_lines = ['    │', '    │']
        
        # Modify the to shape to have a connection point at the top edge
        modified_to = to_lines.copy()
        if len(modified_to) > 0 and modified_to[0].strip():
            # For triangle, the connection should terminate at the top point, not go through
            if '/' in modified_to[0] and '\\' in modified_to[0]:
                # The connection line should end right at the triangle's top point
                # Don't modify the triangle itself - it should remain intact
                pass
        
        # Combine all parts
        result_lines = modified_from + connection_lines + modified_to
        return '\n'.join(result_lines)
    
    def render_horizontal_connection(self, from_lines, to_lines, label=None):
        # Place shapes side by side with horizontal connection
        from_height = len(from_lines)
        to_height = len(to_lines)
        max_height = max(from_height, to_height)
        
        # Find the middle line for connection
        from_middle = from_height // 2
        to_middle = to_height // 2
        
        # Get width of from shape
        from_width = max(len(line) for line in from_lines) if from_lines else 0
        
        # Create horizontal connection with optional label
        if label:
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
    
    def render_ascii(self, filename):
        shapes = self.parse_shapes(filename)
        if not shapes:
            return ""
        
        rendered_shapes = []
        for shape_input in shapes:
            # Check if this is a connection
            connection = self.parse_connection(shape_input)
            if connection:
                rendered_connection = self.render_connection(connection["from"], connection["to"], connection["horizontal"], connection["label"])
                if rendered_connection:
                    rendered_shapes.append(rendered_connection)
            else:
                rendered_shape = self.render_single_shape(shape_input)
                if rendered_shape:
                    rendered_shapes.append(rendered_shape)
        
        return "\n\n".join(rendered_shapes)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python diaglang.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    reader = DiagReader()
    result = reader.render_ascii(filename)
    print(result)