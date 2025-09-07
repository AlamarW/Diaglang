#!/usr/bin/env python3
import sys
import argparse
from diaglang import DiagramRenderer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render diaglang files as ASCII art diagrams",
        prog="python main.py"
    )
    parser.add_argument("filename", help="Path to .diag file to render")
    parser.add_argument(
        "--default-shape", 
        choices=["rectangle", "square", "circle", "triangle", "diamond"],
        help="Default shape type for bare labels (enables simplified syntax)"
    )
    
    args = parser.parse_args()
    
    renderer = DiagramRenderer()
    result = renderer.render_ascii(args.filename, default_shape=args.default_shape)
    print(result)