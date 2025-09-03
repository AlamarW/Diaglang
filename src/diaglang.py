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
            elif shape_type == "circle" or shape_type == "cirle":
                if label is not None:
                    if label == "":
                        return "  ____  \n /    \\ \n|      |\n \\____/ "
                    # Create proper oval shape  
                    label_len = len(label)
                    width = max(6, label_len + 2)
                    padding_total = width - label_len
                    pad_left = " " * (padding_total // 2)
                    pad_right = " " * (padding_total // 2)
                    # If odd padding, add extra space to right
                    if padding_total % 2 == 1:
                        pad_right += " "
                    underline = "_" * width
                    spaces = " " * width
                    
                    return f"  {underline}  \n /{spaces}\\ \n|{pad_left}{label}{pad_right}|\n \\{underline}/ "
                return "  ____  \n /    \\ \n|      |\n \\____/ "
            elif shape_type == "triangle":
                if label:
                    return f" /\\ \n/{label} \\"
                return " /\\ \n/__\\"
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