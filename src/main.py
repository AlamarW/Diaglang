#!/usr/bin/env python3
import sys
from diaglang import DiagramRenderer


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    renderer = DiagramRenderer()
    result = renderer.render_ascii(filename)
    print(result)