import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from diaglang import DiagReader


class TestDiagReader(unittest.TestCase):
    
    def test_can_read_blank_diag_file(self):
        # Create a blank .diag file
        test_file = "test.diag"
        with open(test_file, "w") as f:
            f.write("")
        
        try:
            reader = DiagReader()
            content = reader.read_file(test_file)
            self.assertEqual(content, "")
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_handle_primitive_shapes(self):
        test_file = "test_shapes.diag"
        with open(test_file, "w") as f:
            f.write("square\ncircle\ntriangle\nrectangle")
        
        try:
            reader = DiagReader()
            shapes = reader.parse_shapes(test_file)
            self.assertEqual(shapes, ["square", "circle", "triangle", "rectangle"])
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_square_as_ascii_art(self):
        test_file = "test_square.diag"
        with open(test_file, "w") as f:
            f.write("square")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───┐\n│   │\n└───┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_circle_as_ascii_art(self):
        test_file = "test_circle.diag"
        with open(test_file, "w") as f:
            f.write("circle")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = " ○ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_triangle_as_ascii_art(self):
        test_file = "test_triangle.diag"
        with open(test_file, "w") as f:
            f.write("triangle")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = " /\\ \n/__\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_rectangle_as_ascii_art(self):
        test_file = "test_rectangle.diag"
        with open(test_file, "w") as f:
            f.write("rectangle")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌─────┐\n│     │\n└─────┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_labeled_rectangle(self):
        test_file = "test_labeled_rect.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(Node1)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌─────┐\n│Node1│\n└─────┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_labeled_square(self):
        test_file = "test_labeled_square.diag"
        with open(test_file, "w") as f:
            f.write("Square(A)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───┐\n│ A │\n└───┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_labeled_circle(self):
        test_file = "test_labeled_circle.diag"
        with open(test_file, "w") as f:
            f.write("Circle(X)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "(X)"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_render_labeled_triangle(self):
        test_file = "test_labeled_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle(T)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = " /\\ \n/T \\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_cli_can_render_diag_file(self):
        import subprocess
        test_file = "test_cli.diag"
        with open(test_file, "w") as f:
            f.write("Square(CLI)")
        
        try:
            result = subprocess.run(["python3", "src/diaglang.py", test_file], 
                                  capture_output=True, text=True)
            expected = "┌───┐\n│ CLI │\n└───┘"
            self.assertEqual(result.stdout.strip(), expected)
            self.assertEqual(result.returncode, 0)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


if __name__ == "__main__":
    unittest.main()