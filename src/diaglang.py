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
    
    def parse_chain(self, chain_input):
        # Parse chain like "Rectangle(A) connects to(flows) Triangle(B) connects to(sends) Circle(C)"
        if " connects to" not in chain_input:
            return None
        
        # Count connections to see if this is a chain
        connects_count = chain_input.count(" connects to")
        if connects_count == 1:
            return None  # Single connection, not a chain
        
        # Use regex to find all shape definitions and connections
        import re
        
        # Pattern: ShapeType(Label) connects to(optional_label) [horizontal]
        pattern = r'(\w+\([^)]*\))\s+connects\s+to(\([^)]*\))?\s*(horizontal)?\s*'
        
        # Split the chain and parse each connection
        connections = []
        text = chain_input
        
        # Find all matches
        matches = list(re.finditer(pattern, text))
        
        if not matches:
            return None
            
        # Extract connections
        for i, match in enumerate(matches):
            from_shape = match.group(1)  # ShapeType(Label)
            label_group = match.group(2)  # (label) or None  
            horizontal = match.group(3) is not None  # horizontal keyword
            
            # Extract label
            connection_label = None
            if label_group:
                connection_label = label_group[1:-1]  # Remove parentheses
            
            # Find the target shape
            if i < len(matches) - 1:
                # Target is the from_shape of the next connection
                to_shape = matches[i + 1].group(1)
            else:
                # This is the last connection, find the final shape
                # Look after the current match
                remaining_text = text[match.end():].strip()
                # Extract the shape at the beginning of remaining text
                shape_match = re.match(r'(\w+\([^)]*\))', remaining_text)
                if shape_match:
                    to_shape = shape_match.group(1)
                else:
                    continue  # Skip if we can't find target shape
            
            connections.append({
                "from": from_shape,
                "to": to_shape,
                "horizontal": horizontal,
                "label": connection_label
            })
        
        return connections if connections else None

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
    
    def get_shape_center_position(self, shape_lines):
        """Calculate the horizontal center position of a shape"""
        if not shape_lines:
            return 0
        # Use the longest line to determine the shape's width
        max_width = max(len(line) for line in shape_lines)
        return max_width // 2
    
    def render_vertical_connection(self, from_lines, to_lines, label=None):
        # Calculate center positions for both shapes
        from_center = self.get_shape_center_position(from_lines)
        to_center = self.get_shape_center_position(to_lines)
        
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
        
        # Create connecting lines with proper centering
        connection_indent = ' ' * connection_center
        if label:
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
    
    def render_chain(self, connections):
        # Render a chain of connections as a single combined diagram
        if not connections:
            return ""
        
        # Check if all connections are horizontal
        all_horizontal = all(conn["horizontal"] for conn in connections)
        all_vertical = all(not conn["horizontal"] for conn in connections)
        
        if all_vertical:
            return self.render_vertical_chain(connections)
        elif all_horizontal:
            return self.render_horizontal_chain(connections)
        else:
            return self.render_mixed_chain(connections)
    
    def render_vertical_chain(self, connections):
        # Render a purely vertical chain
        if not connections:
            return ""
        
        # For chains, we need to maintain consistent alignment
        # First, render all shapes to determine the maximum center position
        all_shapes = [connections[0]["from"]]
        for conn in connections:
            all_shapes.append(conn["to"])
        
        rendered_shapes = []
        center_positions = []
        for shape in all_shapes:
            rendered = self.render_single_shape(shape)
            shape_lines = rendered.split('\n')
            rendered_shapes.append(shape_lines)
            center_positions.append(self.get_shape_center_position(shape_lines))
        
        # Use the maximum center position for all connections
        max_center = max(center_positions)
        connection_indent = ' ' * max_center
        
        # Build the chain
        result_parts = []
        
        for i, conn in enumerate(connections):
            if i == 0:
                # First shape with connection point
                from_shape = rendered_shapes[i]
                from_center = center_positions[i]
                
                # Pad first shape if needed
                if from_center < max_center:
                    padding = max_center - from_center
                    padded_shape = []
                    for line in from_shape:
                        padded_shape.append(' ' * padding + line)
                    from_shape = padded_shape
                
                # Add connection point to bottom line
                if from_shape:
                    bottom_line = from_shape[-1]
                    if '┘' in bottom_line:
                        mid_pos = len(bottom_line) // 2
                        from_shape[-1] = bottom_line[:mid_pos] + '┬' + bottom_line[mid_pos+1:]
                
                result_parts.extend(from_shape)
            
            # Add connection with label
            if conn["label"]:
                label_padding = max(0, (max_center * 2 + 1 - len(conn["label"])) // 2)
                label_line = ' ' * label_padding + conn["label"]
                connection_lines = [connection_indent + '│', label_line, connection_indent + '│']
            else:
                connection_lines = [connection_indent + '│', connection_indent + '│']
            
            result_parts.extend(connection_lines)
            
            # Add target shape
            to_shape = rendered_shapes[i + 1]
            to_center = center_positions[i + 1]
            
            # Pad target shape if needed
            if to_center < max_center:
                padding = max_center - to_center
                padded_shape = []
                for line in to_shape:
                    padded_shape.append(' ' * padding + line)
                to_shape = padded_shape
            
            result_parts.extend(to_shape)
        
        return '\n'.join(result_parts)
    
    def render_horizontal_chain(self, connections):
        # Render a purely horizontal chain
        if not connections:
            return ""
        
        # Get all unique shapes in the chain
        shapes = [connections[0]["from"]]
        for conn in connections:
            shapes.append(conn["to"])
        
        # Render each shape and calculate their widths
        rendered_shapes = []
        shape_widths = []
        for shape in shapes:
            shape_lines = self.render_single_shape(shape).split('\n')
            rendered_shapes.append(shape_lines)
            # Calculate the maximum width of this shape
            max_width = max(len(line) for line in shape_lines) if shape_lines else 0
            shape_widths.append(max_width)
        
        # Find max height and calculate optimal connection row
        max_height = max(len(shape_lines) for shape_lines in rendered_shapes)
        
        # Calculate the best connection row by finding where most shapes have their visual center
        shape_centers = []
        for shape_lines in rendered_shapes:
            shape_height = len(shape_lines)
            offset = (max_height - shape_height) // 2
            shape_center_in_layout = offset + (shape_height // 2)
            shape_centers.append(shape_center_in_layout)
        
        # Use the most common center position, or the median if they're all different
        from collections import Counter
        center_counts = Counter(shape_centers)
        if center_counts:
            # Use the most frequent center position
            global_middle_row = center_counts.most_common(1)[0][0]
        else:
            global_middle_row = max_height // 2
        
        # Calculate vertical offsets to center each shape
        shape_offsets = []
        for shape_lines in rendered_shapes:
            shape_height = len(shape_lines)
            offset = (max_height - shape_height) // 2
            shape_offsets.append(offset)
        
        # Build the horizontal layout
        result_lines = []
        
        for row in range(max_height):
            line = ""
            
            for i, shape_lines in enumerate(rendered_shapes):
                shape_offset = shape_offsets[i]
                
                # Check if this row contains part of this shape
                shape_row = row - shape_offset
                if 0 <= shape_row < len(shape_lines):
                    shape_line = shape_lines[shape_row]
                    line += shape_line
                    # Only pad if we're not the last shape and we need consistent alignment
                    # This preserves original spacing while ensuring circle alignment
                    if i < len(rendered_shapes) - 1:  # Not the last shape
                        padding_needed = shape_widths[i] - len(shape_line)
                        if padding_needed > 0:
                            line += ' ' * padding_needed
                else:
                    # Add padding to match the width of this shape's widest line
                    if shape_lines:
                        line += ' ' * shape_widths[i]
                
                # Add connection between shapes (except after last shape)
                if i < len(rendered_shapes) - 1:
                    conn = connections[i]
                    
                    if row == global_middle_row:
                        # Add labeled connection line
                        if conn["label"]:
                            connection = f"──{conn['label']}──"
                        else:
                            connection = "──────"
                        line += connection
                    else:
                        # Add spacing to match connection width
                        if conn["label"]:
                            line += ' ' * (len(conn["label"]) + 4)
                        else:
                            line += ' ' * 6
            
            result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def render_mixed_chain(self, connections):
        # Render a chain with mixed horizontal and vertical connections
        if not connections:
            return ""
        
        # Strategy: Build the chain step by step, combining shapes at connection points
        result_parts = []
        
        # Start with the first connection
        first_conn = connections[0]
        current_diagram = self.render_connection(
            first_conn["from"], first_conn["to"], 
            first_conn["horizontal"], first_conn["label"]
        )
        
        if len(connections) == 1:
            return current_diagram
        
        current_lines = current_diagram.split('\n')
        
        # Process remaining connections
        for i in range(1, len(connections)):
            conn = connections[i]
            
            # The "from" shape of this connection should already be the "to" shape of the previous
            # We need to append the new connection to the existing diagram
            
            if conn["horizontal"]:
                # Add horizontal connection to the right of current diagram
                current_lines = self.append_horizontal_connection(
                    current_lines, conn["to"], conn["label"]
                )
            else:
                # Add vertical connection below current diagram  
                current_lines = self.append_vertical_connection(
                    current_lines, conn["to"], conn["label"]
                )
        
        return '\n'.join(current_lines)
    
    def append_horizontal_connection(self, current_lines, to_shape, label):
        # Add a horizontal connection to the right of the current diagram
        to_rendered = self.render_single_shape(to_shape).split('\n')
        
        # Find the height and middle row
        current_height = len(current_lines)
        to_height = len(to_rendered)
        max_height = max(current_height, to_height)
        
        # Calculate middle row for connection
        middle_row = (max_height - 1) // 2
        
        # Build the combined layout
        result_lines = []
        for row in range(max_height):
            line = ""
            
            # Add current diagram content
            if row < current_height:
                line += current_lines[row]
            else:
                # Pad with spaces to match the width
                if current_lines:
                    line += ' ' * len(current_lines[0])
            
            # Add connection
            if row == middle_row:
                if label:
                    connection = f"──{label}──"
                else:
                    connection = "──────"
                line += connection
            else:
                # Add spacing
                if label:
                    line += ' ' * (len(label) + 4)
                else:
                    line += ' ' * 6
            
            # Add to shape
            if row < to_height:
                line += to_rendered[row]
            
            result_lines.append(line)
        
        return result_lines
    
    def append_vertical_connection(self, current_lines, to_shape, label):
        # Add a vertical connection below the current diagram
        to_rendered = self.render_single_shape(to_shape).split('\n')
        
        # Find the center of the current diagram to place the connection
        current_width = max(len(line) for line in current_lines) if current_lines else 0
        connection_center = current_width // 2
        
        # Modify the last line of current diagram to add connection point
        modified_current = current_lines.copy()
        if modified_current:
            last_line = modified_current[-1]
            # Look for shape borders that can have connection points added
            if '┘' in last_line or '└' in last_line:
                # Find a good position to add the connection point
                mid_pos = len(last_line.rstrip()) // 2
                if mid_pos < len(last_line) and last_line[mid_pos] in '─┘└':
                    # Replace with connection point
                    last_line = last_line[:mid_pos] + '┬' + last_line[mid_pos+1:]
                    modified_current[-1] = last_line
        
        # Create connection lines
        connection_indent = ' ' * connection_center
        if label:
            label_padding = max(0, (current_width - len(label)) // 2)
            label_line = ' ' * label_padding + label
            connection_lines = [connection_indent + '│', label_line, connection_indent + '│']
        else:
            connection_lines = [connection_indent + '│', connection_indent + '│']
        
        # Center the to_shape under the current diagram
        to_center = self.get_shape_center_position(to_rendered)
        to_padding = connection_center - to_center
        
        padded_to = []
        for line in to_rendered:
            if to_padding > 0:
                padded_to.append(' ' * to_padding + line)
            else:
                padded_to.append(line)
        
        # Combine all parts
        result_lines = modified_current + connection_lines + padded_to
        return result_lines
    
    def render_ascii(self, filename):
        shapes = self.parse_shapes(filename)
        if not shapes:
            return ""
        
        rendered_shapes = []
        for shape_input in shapes:
            # Check if this is a chain first
            chain = self.parse_chain(shape_input)
            if chain:
                rendered_chain = self.render_chain(chain)
                if rendered_chain:
                    rendered_shapes.append(rendered_chain)
            else:
                # Check if this is a single connection
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