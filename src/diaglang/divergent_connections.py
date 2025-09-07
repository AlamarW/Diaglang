from .shape_renderer import ShapeRenderer


class DivergentConnections:
    def __init__(self):
        self.shape_renderer = ShapeRenderer()

    def parse_convergent_connections(self, input_text):
        """Parse input for convergent connections where multiple sources connect to one target using 'and' keyword"""
        if " connects to" not in input_text or " and " not in input_text:
            return None
        
        # Pattern: Source1 and Source2 and Source3... connects to target
        # Split to find the "connects to" position
        connects_index = input_text.find(" connects to")
        if connects_index == -1:
            return None
        
        sources_part = input_text[:connects_index].strip()
        remainder = input_text[connects_index + len(" connects to"):].strip()
        
        # Check if sources_part contains "and" - indicating multiple sources
        if " and " not in sources_part:
            return None
        
        # Split sources by "and"
        source_shapes = [s.strip() for s in sources_part.split(" and ")]
        if len(source_shapes) < 2:
            return None
        
        # Parse the connection details from remainder (same as divergent)
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
                if potential_arrow_type in ["point to", "point back", "double point"]:
                    arrow_type = potential_arrow_type
            else:
                if paren_content in ["point to", "point back", "double point"]:
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
        
        # The remainder should be the target shape
        target_shape = remainder.strip()
        if not target_shape:
            return None
        
        # Create connections from each source to the target
        connections = []
        for source in source_shapes:
            if source:  # Make sure source is not empty
                connections.append({
                    "from": source,
                    "to": target_shape,
                    "horizontal": horizontal,
                    "label": connection_label,
                    "arrow_type": arrow_type
                })
        
        return connections if len(connections) >= 2 else None

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
                if potential_arrow_type in ["point to", "point back", "double point"]:
                    arrow_type = potential_arrow_type
            else:
                if paren_content in ["point to", "point back", "double point"]:
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
                if conn["arrow_type"] == "point to":
                    connection_line = '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                elif conn["arrow_type"] == "point back":
                    connection_line = '<' + '─' * dash_count + conn["label"] + '─' * dash_count
                elif conn["arrow_type"] == "double point":
                    connection_line = '<' + '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                else:
                    connection_line = '─' * dash_count + conn["label"] + '─' * dash_count
            elif conn.get("arrow_type"):
                if conn["arrow_type"] == "point to":
                    connection_line = "────────>"
                elif conn["arrow_type"] == "point back":
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

    def render_convergent_connections(self, connections):
        """Render convergent connections where multiple sources connect to one target"""
        if not connections or len(connections) < 2:
            return ""
        
        # All connections share the same target
        target_shape = connections[0]["to"]
        target_rendered = self.shape_renderer.render_single_shape(target_shape)
        target_lines = target_rendered.split('\n')
        target_height = len(target_lines)
        target_width = max(len(line) for line in target_lines)
        
        # Render all source shapes
        source_renders = []
        for conn in connections:
            source_rendered = self.shape_renderer.render_single_shape(conn["from"])
            source_lines = source_rendered.split('\n')
            source_renders.append(source_lines)
        
        # Create connections with proper arrows and labels
        connection_lines = []
        for conn in connections:
            if conn.get("arrow_type") and conn.get("label"):
                # Handle both label and arrow type: ───label───>
                dash_count = 3
                if conn["arrow_type"] == "point to":
                    connection_line = '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                elif conn["arrow_type"] == "point back":
                    connection_line = '<' + '─' * dash_count + conn["label"] + '─' * dash_count
                elif conn["arrow_type"] == "double point":
                    connection_line = '<' + '─' * dash_count + conn["label"] + '─' * dash_count + '>'
                else:
                    connection_line = '─' * dash_count + conn["label"] + '─' * dash_count
            elif conn.get("arrow_type"):
                if conn["arrow_type"] == "point to":
                    connection_line = "────────>"
                elif conn["arrow_type"] == "point back":
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
        
        # Layout: stack sources vertically on left, with target on right
        result_lines = []
        
        # Calculate total height needed for all sources
        total_source_height = sum(len(source) for source in source_renders)
        spacing_between_sources = len(source_renders) - 1  # One space between each source
        total_height = total_source_height + spacing_between_sources
        
        # Position target vertically centered relative to all sources
        target_start_row = max(0, (total_height - target_height) // 2)
        
        # Initialize result with empty lines
        for i in range(max(total_height, target_start_row + target_height)):
            result_lines.append("")
        
        # Add source lines and connections
        source_row = 0
        connection_length = max(len(conn_line) for conn_line in connection_lines)
        max_source_width = max(max(len(line) for line in source) if source else 0 for source in source_renders)
        
        for i, (source_lines, conn_line) in enumerate(zip(source_renders, connection_lines)):
            source_height = len(source_lines)
            source_center = source_row + source_height // 2
            
            # Add source lines
            for j, source_line in enumerate(source_lines):
                source_absolute_row = source_row + j
                if source_absolute_row < len(result_lines):
                    result_lines[source_absolute_row] = source_line
            
            # Add connection from source center to target
            if source_center < len(result_lines):
                current_line = result_lines[source_center]
                # Pad to max source width
                if len(current_line) < max_source_width:
                    current_line += " " * (max_source_width - len(current_line))
                
                # Add connection
                current_line += conn_line
                result_lines[source_center] = current_line
            
            # Move to next source position
            source_row += source_height + 1  # +1 for spacing
        
        # Add target lines
        for i, target_line in enumerate(target_lines):
            target_absolute_row = target_start_row + i
            if target_absolute_row < len(result_lines):
                current_line = result_lines[target_absolute_row]
                # Extend line to include target
                if len(current_line) < max_source_width + connection_length:
                    current_line += " " * (max_source_width + connection_length - len(current_line))
                current_line += target_line
                result_lines[target_absolute_row] = current_line
        
        return '\n'.join(result_lines)