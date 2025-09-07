import re
from collections import Counter
from .connection_system import ConnectionSystem
from .shape_renderer import ShapeRenderer


class ChainSystem:
    def __init__(self):
        self.connection_system = ConnectionSystem()
        self.shape_renderer = ShapeRenderer()
    
    def parse_chain(self, chain_input):
        # Parse chain like "Rectangle(A) connects to(flows) Triangle(B) connects to(sends) Circle(C)"
        if " connects to" not in chain_input:
            return None
        
        # Count connections to see if this is a chain
        connects_count = chain_input.count(" connects to")
        if connects_count == 1:
            return None  # Single connection, not a chain
        
        # Use regex to find all shape definitions and connections
        # Pattern: ShapeType(Label) connects to(optional_label) (horizontal|vertical)
        pattern = r'(\w+\([^)]*\))\s+connects\s+to(\([^)]*\))?\s+(horizontal|vertical)\s*'
        
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
            direction = match.group(3)  # horizontal or vertical
            horizontal = (direction == "horizontal")
            
            # Extract label and arrow type
            connection_label = None
            arrow_type = None
            if label_group:
                paren_content = label_group[1:-1]  # Remove parentheses
                
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
                "label": connection_label,
                "arrow_type": arrow_type
            })
        
        return connections if connections else None

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
            rendered = self.shape_renderer.render_single_shape(shape)
            shape_lines = rendered.split('\n')
            rendered_shapes.append(shape_lines)
            center_positions.append(self.shape_renderer.get_shape_center_position(shape_lines))
        
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
            shape_lines = self.shape_renderer.render_single_shape(shape).split('\n')
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
                        # Add connection line with arrow type and label support
                        if conn.get("arrow_type") and conn.get("label"):
                            # Handle both label and arrow type: ───label───>
                            dash_count = 3
                            if conn["arrow_type"] == "point to":
                                connection = '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                            elif conn["arrow_type"] == "point back":
                                connection = '<' + '─' * dash_count + conn["label"] + '─' * dash_count
                            elif conn["arrow_type"] == "double point":
                                connection = '<' + '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                            else:
                                connection = '─' * dash_count + conn["label"] + '─' * dash_count  # fallback
                        elif conn.get("arrow_type"):
                            # Handle arrow types only
                            if conn["arrow_type"] == "point to":
                                connection = "────────>"
                            elif conn["arrow_type"] == "point back":
                                connection = "<────────"
                            elif conn["arrow_type"] == "double point":
                                connection = "<──────>"
                            else:
                                connection = "─" * 9  # fallback
                        elif conn["label"]:
                            connection = f"──{conn['label']}──"
                        else:
                            connection = "──────"
                        line += connection
                    else:
                        # Add spacing to match connection width
                        if conn.get("arrow_type") and conn.get("label"):
                            # Labeled arrow connections: length = 3 + label_length + 3 + 1
                            line += ' ' * (len(conn["label"]) + 7)
                        elif conn.get("arrow_type"):
                            line += ' ' * 9  # Arrow connections are 9 characters
                        elif conn["label"]:
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
        current_diagram = self.connection_system.render_connection(
            first_conn["from"], first_conn["to"], 
            first_conn["horizontal"], first_conn["label"], first_conn.get("arrow_type")
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
        to_rendered = self.shape_renderer.render_single_shape(to_shape).split('\n')
        
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
        to_rendered = self.shape_renderer.render_single_shape(to_shape).split('\n')
        
        # Find the center of the last shape in the current diagram to place the connection
        # For mixed chains, we need to connect to the rightmost shape, not the center of the whole diagram
        current_width = max(len(line) for line in current_lines) if current_lines else 0
        
        # Find the rightmost shape's center by looking at the bottom line of current diagram
        # The bottom line typically shows the shape boundaries most clearly
        if current_lines:
            bottom_line = current_lines[-1].rstrip()
            # Look for shape boundary characters from the right
            shape_end = len(bottom_line)
            shape_start = 0
            
            # Find the rightmost shape boundary by looking for shape characters
            # Work backwards from the end to find where the last shape starts
            for i in range(len(bottom_line) - 1, -1, -1):
                char = bottom_line[i]
                if char in '┘└/|\\':  # Shape boundary characters
                    shape_end = i + 1
                    break
            
            # Now find the start of this shape
            for i in range(shape_end - 1, -1, -1):
                char = bottom_line[i] 
                if char in ' ':  # Space indicates start of shape area
                    shape_start = i + 1
                    break
            
            # Center of the rightmost shape
            connection_center = (shape_start + shape_end) // 2
        else:
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
        to_center = self.shape_renderer.get_shape_center_position(to_rendered)
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