from .shape_renderer import ShapeRenderer


class DivergentConnections:
    def __init__(self):
        self.shape_renderer = ShapeRenderer()

    def parse_divergent_connections(self, input_text):
        """Parse input for divergent connections where one source connects to multiple targets using 'and' keyword"""
        if " connects to" not in input_text or " and " not in input_text:
            return None
        
        # Pattern: Source connects to target1 and target2 and target3...
        # Split the input to extract the source and connection info from the first part
        connects_index = input_text.find(" connects to")
        if connects_index == -1:
            return None
        
        source_shape = input_text[:connects_index].strip()
        remainder = input_text[connects_index + len(" connects to"):].strip()
        
        # Parse the first connection to get the connection details (label, direction, etc.)
        first_connection_match = None
        connection_label = None
        arrow_type = None
        horizontal = None
        
        # Check for connection label/arrow in parentheses
        if remainder.startswith("(") and ")" in remainder:
            end_paren = remainder.find(")")
            paren_content = remainder[1:end_paren]
            remainder = remainder[end_paren+1:].strip()
            
            # Parse label and arrow type from parentheses
            if "," in paren_content:
                parts = paren_content.split(",", 1)
                connection_label = parts[0].strip()
                potential_arrow_type = parts[1].strip()
                if potential_arrow_type in ["point away", "point from", "double point"]:
                    arrow_type = potential_arrow_type
            else:
                if paren_content in ["point away", "point from", "double point"]:
                    arrow_type = paren_content
                else:
                    connection_label = paren_content
        
        # Check for direction keyword
        if remainder.startswith("horizontal "):
            horizontal = True
            remainder = remainder[11:].strip()
        elif remainder.startswith("vertical "):
            horizontal = False
            remainder = remainder[9:].strip()
        else:
            return None
        
        # Now split by " and " to get all targets
        if " and " not in remainder:
            return None
        
        targets = remainder.split(" and ")
        if len(targets) < 2:
            return None
        
        # Create connections from source to each target
        connections = []
        for target in targets:
            target = target.strip()
            if target:  # Make sure target is not empty
                connections.append({
                    "from": source_shape,
                    "to": target,
                    "horizontal": horizontal,
                    "label": connection_label,
                    "arrow_type": arrow_type
                })
        
        return connections if len(connections) >= 2 else None

    def render_divergent_connections(self, connections):
        """Render divergent connections where one source connects to multiple targets"""
        if not connections or len(connections) < 2:
            return ""
        
        # All connections share the same source
        source_shape = connections[0]["from"]
        source_rendered = self.shape_renderer.render_single_shape(source_shape)
        source_lines = source_rendered.split('\n')
        source_height = len(source_lines)
        source_width = max(len(line) for line in source_lines)
        source_center = source_height // 2
        
        # Render all target shapes
        target_renders = []
        for conn in connections:
            target_rendered = self.shape_renderer.render_single_shape(conn["to"])
            target_lines = target_rendered.split('\n')
            target_renders.append(target_lines)
        
        # Create connections with proper arrows and labels
        connection_lines = []
        for conn in connections:
            if conn.get("arrow_type") and conn.get("label"):
                # Handle both label and arrow type: ───label───>
                dash_count = 3
                if conn["arrow_type"] == "point away":
                    connection_line = '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                elif conn["arrow_type"] == "point from":
                    connection_line = '<' + '─' * dash_count + conn["label"] + '─' * dash_count
                elif conn["arrow_type"] == "double point":
                    connection_line = '<' + '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                else:
                    connection_line = '─' * dash_count + conn["label"] + '─' * dash_count
            elif conn.get("arrow_type"):
                if conn["arrow_type"] == "point away":
                    connection_line = "────────>"
                elif conn["arrow_type"] == "point from":
                    connection_line = "<────────"
                elif conn["arrow_type"] == "double point":
                    connection_line = "<──────>"
                else:
                    connection_line = "─" * 9
            elif conn.get("label"):
                connection_line = f"──{conn['label']}──"
            else:
                connection_line = "──────"
            connection_lines.append(connection_line)
        
        # Calculate layout: stack targets vertically, each with their own connection from source center
        result_lines = []
        
        # Calculate total height needed
        total_target_height = sum(len(target) for target in target_renders)
        spacing_between_targets = len(target_renders) - 1  # One space between each target
        total_height = total_target_height + spacing_between_targets
        
        # Position source vertically centered relative to all targets
        source_start_row = max(0, (total_height - source_height) // 2)
        
        # Add empty lines before source if needed
        for i in range(source_start_row):
            result_lines.append("")
        
        # Add source lines
        for line in source_lines:
            result_lines.append(line)
        
        # Add empty lines after source if needed
        while len(result_lines) < total_height:
            result_lines.append("")
        
        # Now add targets and connections
        target_row = 0
        connection_length = max(len(conn_line) for conn_line in connection_lines)
        
        for i, (target_lines, conn_line) in enumerate(zip(target_renders, connection_lines)):
            target_height = len(target_lines)
            target_center = target_row + target_height // 2
            
            # Add connection from source center to target center
            if target_center < len(result_lines):
                # Extend the line at target_center to include connection and target
                current_line = result_lines[target_center]
                # Pad to source width if needed
                if len(current_line) < source_width:
                    current_line += " " * (source_width - len(current_line))
                
                # Add connection
                current_line += conn_line
                
                # Add target center line
                if target_lines:
                    target_center_line = target_lines[target_height // 2]
                    current_line += target_center_line
                
                result_lines[target_center] = current_line
            
            # Add other target lines (non-center lines)
            for j, target_line in enumerate(target_lines):
                target_absolute_row = target_row + j
                if target_absolute_row < len(result_lines) and j != target_height // 2:  # Skip center line, already handled
                    current_line = result_lines[target_absolute_row]
                    # Pad to source width
                    if len(current_line) < source_width:
                        current_line += " " * (source_width - len(current_line))
                    # Pad to include connection space
                    current_line += " " * connection_length
                    # Add target line
                    current_line += target_line
                    result_lines[target_absolute_row] = current_line
            
            # Move to next target position
            target_row += target_height + 1  # +1 for spacing
        
        return '\n'.join(result_lines)