class DiagReader:
    def read_file(self, filename):
        with open(filename, 'r') as f:
            return f.read()
    
    def parse_shapes(self, filename):
        content = self.read_file(filename)
        return content.strip().split('\n') if content.strip() else []
    
    def render_ascii(self, filename):
        shapes = self.parse_shapes(filename)
        if shapes and shapes[0] == "square":
            return "┌───┐\n│   │\n└───┘"
        return ""