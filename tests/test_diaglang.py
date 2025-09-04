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
            expected = "  ____  \n /    \\ \n|      |\n \\____/ "
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
            expected = "   /\\   \n  /  \\  \n /    \\ \n/______\\"
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
            expected = "┌───────┐\n│ Node1 │\n└───────┘"
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
            expected = "  ______  \n /      \\ \n|   X    |\n \\______/ "
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
            expected = "  /\\\n /T \\\n/____\\"
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
            expected = "┌─────┐\n│ CLI │\n└─────┘"
            self.assertEqual(result.stdout.strip(), expected)
            self.assertEqual(result.returncode, 0)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_rectangle_handles_short_label(self):
        test_file = "test_short_rect.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───┐\n│ A │\n└───┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_rectangle_handles_long_label(self):
        test_file = "test_long_rect.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(VeryLongLabel)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───────────────┐\n│ VeryLongLabel │\n└───────────────┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_rectangle_handles_empty_label(self):
        test_file = "test_empty_rect.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle()")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌──┐\n│  │\n└──┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_circle_handles_short_label(self):
        test_file = "test_short_circle.diag"
        with open(test_file, "w") as f:
            f.write("Circle(A)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  ______  \n /      \\ \n|   A    |\n \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_circle_handles_long_label(self):
        test_file = "test_long_circle.diag"
        with open(test_file, "w") as f:
            f.write("Circle(VeryLongLabel)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  _______________  \n /               \\ \n|  VeryLongLabel  |\n \\_______________/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_circle_handles_empty_label(self):
        test_file = "test_empty_circle.diag"
        with open(test_file, "w") as f:
            f.write("Circle()")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  ______  \n /      \\ \n|        |\n \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_circle_handles_case_insensitive(self):
        test_file = "test_case_circle.diag"
        with open(test_file, "w") as f:
            f.write("CIRCLE(Test)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  ______  \n /      \\ \n|  Test  |\n \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


    def test_can_render_multiple_shapes(self):
        test_file = "test_multiple.diag"
        with open(test_file, "w") as f:
            f.write("Circle(Testing mctest)\nTriangle(Test)\nSquare(Test)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  ________________  \n /                \\ \n|  Testing mctest  |\n \\________________/ \n\n   /\\\n  /  \\\n /Test\\\n/______\\\n\n┌──────┐\n│ Test │\n└──────┘"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_connect_two_nodes(self):
        test_file = "test_connection.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(Node1) connects to Triangle(Node2)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───────┐\n│ Node1 │\n└───┬───┘\n    │\n    │\n   /\\\n  /  \\\n /Node2\\\n/_______\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_connect_two_nodes_horizontally(self):
        test_file = "test_horizontal_connection.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(Start) connects to horizontal Triangle(End)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───────┐        /\\\n│ Start │────── /End\\\n└───────┘      /_____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_triangle_handles_very_small_labels(self):
        test_file = "test_small_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle(a)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  /\\\n /a \\\n/____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_triangle_handles_two_char_labels(self):
        test_file = "test_two_char_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle(ab)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  /\\\n /ab\\\n/____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_triangle_handles_three_char_labels(self):
        test_file = "test_three_char_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle(abc)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  /\\\n /abc\\\n/_____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_connect_nodes_with_label(self):
        test_file = "test_labeled_connection.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(Start) connects to(uses) Triangle(End)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───────┐\n│ Start │\n└───┬───┘\n    │\nuses\n    │\n  /\\\n /End\\\n/_____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_connect_nodes_with_horizontal_label(self):
        test_file = "test_horizontal_labeled_connection.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(Start) connects to(uses) horizontal Triangle(End)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───────┐            /\\\n│ Start │───uses─── /End\\\n└───────┘          /_____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_circle_renders_as_oval_shape(self):
        test_file = "test_oval_circle.diag"
        with open(test_file, "w") as f:
            f.write("Circle(Test)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  ______  \n /      \\ \n|  Test  |\n \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_circle_empty_renders_as_oval_shape(self):
        test_file = "test_oval_empty.diag"
        with open(test_file, "w") as f:
            f.write("Circle()")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  ______  \n /      \\ \n|        |\n \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_triangle_handles_short_label(self):
        test_file = "test_short_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle(A)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "  /\\\n /A \\\n/____\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_triangle_handles_long_label(self):
        test_file = "test_long_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle(VeryLongLabel)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "       /\\\n      /  \\\n     /    \\\n    /      \\\n   /        \\\n  /          \\\n /VeryLongLabel\\\n/_______________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_triangle_handles_empty_label(self):
        test_file = "test_empty_triangle.diag"
        with open(test_file, "w") as f:
            f.write("Triangle()")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "   /\\   \n  /  \\  \n /    \\ \n/______\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


if __name__ == "__main__":
    unittest.main()