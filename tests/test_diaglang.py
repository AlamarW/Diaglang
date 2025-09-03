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


if __name__ == "__main__":
    unittest.main()