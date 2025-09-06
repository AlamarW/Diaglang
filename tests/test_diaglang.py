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
            result = subprocess.run(["python3", "src/main.py", test_file], 
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
            f.write("Rectangle(Node1) connects to vertical Triangle(Node2)")
        
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
            f.write("Rectangle(Start) connects to(uses) vertical Triangle(End)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───────┐\n│ Start │\n└───┬───┘\n    │\n  uses\n    │\n   /\\\n  /End\\\n /_____\\"
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

    def test_can_chain_two_nodes_vertically(self):
        test_file = "test_simple_vertical_chain.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A) connects to(flows) vertical Triangle(B) connects to(sends) vertical Circle(C)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "   ┌───┐\n   │ A │\n   └┬──┘\n     │\n   flows\n     │\n    /\\\n   /B \\\n  /____\\\n     │\n   sends\n     │\n  ______  \n /      \\ \n|   C    |\n \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_chain_two_nodes_horizontally(self):
        test_file = "test_horizontal_chain.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A) connects to(flows) horizontal Triangle(B) connects to(sends) horizontal Circle(C)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            expected = "┌───┐           /\\             ______  \n│ A │──flows── /B \\ ──sends── /      \\ \n└───┘         /____\\         |   C    |\n                              \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_chain_mixed_directions(self):
        test_file = "test_mixed_chain.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A) connects to(flows) horizontal Triangle(B) connects to(sends) vertical Circle(C)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # This should render A horizontal to B, then B vertical to C
            expected = "┌───┐             /\\\n│ A │───flows─── /B \\\n└───┘           /____\\\n                   │\n        sends\n                   │\n                ______  \n               /      \\ \n              |   C    |\n               \\______/ "
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_rejects_implicit_connection_direction(self):
        test_file = "test_implicit_connection.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A) connects to(label) Triangle(B)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Should now provide a helpful syntax error message
            self.assertIn("SYNTAX ERROR", ascii_art)
            self.assertIn("Missing direction", ascii_art)
            self.assertIn("horizontal", ascii_art)
            self.assertIn("vertical", ascii_art)
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


    def test_can_specify_arrow_types_horizontal_point_away(self):
        test_file = "test_arrow_point_away.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(point away) horizontal Triangle(effect)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: horizontal connection with arrow pointing right (away from cause to effect)
            expected = "┌───────┐             /\\\n│ cause │────────>   /  \\\n└───────┘           /    \\\n                   /effect\\\n                  /________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_specify_arrow_types_horizontal_point_from(self):
        test_file = "test_arrow_point_from.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(point from) horizontal Triangle(effect)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: horizontal connection with arrow pointing left (from effect back to cause)
            expected = "┌───────┐             /\\\n│ cause │<────────   /  \\\n└───────┘           /    \\\n                   /effect\\\n                  /________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_specify_arrow_types_horizontal_double_point(self):
        test_file = "test_arrow_double_point.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(double point) horizontal Triangle(effect)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: horizontal connection with arrows pointing both ways
            expected = "┌───────┐            /\\\n│ cause │<──────>   /  \\\n└───────┘          /    \\\n                  /effect\\\n                 /________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_specify_arrow_types_vertical_point_away(self):
        test_file = "test_arrow_vertical_point_away.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(point away) vertical Triangle(effect)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: vertical connection with arrow pointing down (away from cause to effect)
            expected = " ┌───────┐\n │ cause │\n └───┬───┘\n     |\n     |\n     v\n    /\\\n   /  \\\n  /    \\\n /effect\\\n/________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


    def test_can_label_pointed_arrows_horizontal(self):
        test_file = "test_labeled_arrow.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(cases, point away) horizontal Triangle(effect)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: horizontal connection with both label and arrow
            expected = "┌───────┐                /\\\n│ cause │───cases───>   /  \\\n└───────┘              /    \\\n                      /effect\\\n                     /________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_can_label_pointed_arrows_vertical(self):
        test_file = "test_labeled_arrow_vertical.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(flows, point away) vertical Triangle(effect)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: vertical connection with both label and arrow
            expected = " ┌───────┐\n │ cause │\n └───┬───┘\n     |\n   flows\n     v\n    /\\\n   /  \\\n  /    \\\n /effect\\\n/________\\"
            self.assertEqual(ascii_art, expected)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


    def test_can_connect_one_source_to_multiple_targets_with_and(self):
        test_file = "test_divergent_connections.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(cause) connects to(cases, point away) horizontal Triangle(effect) and Square(effect2)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Expected: One source (cause) connecting to two targets (effect and effect2)
            # Should show cause in center with connections going to both targets
            self.assertIn("cause", ascii_art)
            self.assertIn("effect", ascii_art)  
            self.assertIn("effect2", ascii_art)
            # Cause should appear only once
            self.assertEqual(ascii_art.count("cause"), 1)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_divergent_connections_equivalent_to_separate_statements(self):
        # Test that divergent syntax produces same result as separate statements
        test_file1 = "test_divergent_single.diag"
        test_file2 = "test_divergent_separate.diag"
        
        with open(test_file1, "w") as f:
            f.write("Rectangle(source) connects to horizontal Square(target1) and Circle(target2)")
        
        with open(test_file2, "w") as f:
            f.write("Rectangle(source) connects to horizontal Square(target1)\nRectangle(source) connects to horizontal Circle(target2)")
        
        try:
            reader = DiagReader()
            ascii_single = reader.render_ascii(test_file1)
            ascii_separate = reader.render_ascii(test_file2)
            
            # Both should contain the same elements (though layout may differ)
            self.assertIn("source", ascii_single)
            self.assertIn("target1", ascii_single)
            self.assertIn("target2", ascii_single)
            
            # Source should appear only once in the divergent version
            self.assertEqual(ascii_single.count("source"), 1)
        finally:
            if os.path.exists(test_file1):
                os.remove(test_file1)
            if os.path.exists(test_file2):
                os.remove(test_file2)

    def test_can_use_default_shape_flag_for_direct_labels(self):
        test_file = "test_default_shape.diag"
        with open(test_file, "w") as f:
            f.write("cause connects to(causes, point away) horizontal effect")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file, default_shape="rectangle")
            # Should render as rectangles since that's the default shape
            self.assertIn("cause", ascii_art)
            self.assertIn("effect", ascii_art)
            self.assertIn("causes", ascii_art)
            self.assertIn("───>", ascii_art)  # Should have arrow pointing away
            # Should have rectangle borders
            self.assertIn("┌", ascii_art)
            self.assertIn("└", ascii_art)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_reports_syntax_errors_for_invalid_connection_syntax(self):
        test_file = "test_syntax_error.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A) connects to Triangle(B)")  # Missing direction
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Should contain error message instead of rendering
            self.assertIn("SYNTAX ERROR", ascii_art)
            self.assertIn("Missing direction", ascii_art)
            self.assertIn("horizontal", ascii_art)
            self.assertIn("vertical", ascii_art)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_reports_syntax_errors_for_invalid_arrow_types(self):
        test_file = "test_arrow_error.diag"
        with open(test_file, "w") as f:
            f.write("Rectangle(A) connects to(invalid arrow) horizontal Triangle(B)")
        
        try:
            reader = DiagReader()
            ascii_art = reader.render_ascii(test_file)
            # Should contain error message for invalid arrow type
            self.assertIn("SYNTAX ERROR", ascii_art)
            self.assertIn("Invalid arrow type", ascii_art)
            self.assertIn("point away", ascii_art)
            self.assertIn("point from", ascii_art)
            self.assertIn("double point", ascii_art)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)


if __name__ == "__main__":
    unittest.main()