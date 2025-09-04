class DiagReader:
    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()
    
    def parse_shapes(self, filename):
        content = self.read_file(filename)
        return content.strip().split('\n') if content.strip() else []
    
    def render_ascii(self, filename):
        shapes = self.parse_shapes(filename)
        if shapes:
            shape_input = shapes[0]
            
            # Parse shape and label
            if '(' in shape_input and shape_input.endswith(')'):
                shape_type = shape_input.split('(')[0].lower()
                label = shape_input.split('(')[1][:-1]
            else:
                shape_type = shape_input.lower()
                label = None
            
            if shape_type == "square":
                if label:
                    return f"┌───┐\n│ {label} │\n└───┘"
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


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python diaglang.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    reader = DiagReader()
    result = reader.render_ascii(filename)
    print(result)