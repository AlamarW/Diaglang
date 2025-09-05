class ShapeRenderer:
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
    
    def get_shape_center_position(self, shape_lines):
        """Calculate the horizontal center position of a shape"""
        if not shape_lines:
            return 0
        # Use the longest line to determine the shape's width
        max_width = max(len(line) for line in shape_lines)
        return max_width // 2