# Diaglang

Diaglang is a plain-language diagramming tool that generates ASCII art diagrams from simple text descriptions. It enables developers and technical writers to create visual flowcharts, process diagrams, and system architectures using intuitive syntax that reads like natural language.

## Purpose

Traditional diagramming tools require graphical interfaces and complex positioning. Diaglang eliminates this friction by allowing diagrams to be written as code, making them version-controllable, reviewable, and editable in any text editor.

## Core Features

- **Plain Language Syntax**: Write diagrams using natural language constructs
- **ASCII Art Output**: Generates clean, terminal-friendly visual diagrams
- **Multiple Shape Types**: Supports rectangles, circles, triangles, and squares
- **Flexible Connections**: Create horizontal, vertical, and mixed-direction chains
- **Labeled Elements**: Add descriptive labels to both shapes and connections
- **Command Line Interface**: Simple CLI for processing diagram files

## Basic Usage

### Primitive Shapes

Create individual shapes with labels:

```
Rectangle(Database)
Circle(User)
Triangle(Process)
Square(Cache)
```

### Connections

Connect shapes with explicit direction and optional labels:

```
Rectangle(Frontend) connects to(API calls) horizontal Circle(Backend)
Circle(Backend) connects to(queries) vertical Rectangle(Database)
```

### Chaining

Create complex flows with multiple connected elements:

```
Rectangle(User Input) connects to(validates) vertical Triangle(Validation) connects to(stores) vertical Circle(Database)
```

### Mixed Direction Chains

Combine horizontal and vertical connections in a single chain:

```
Rectangle(Start) connects to(process) horizontal Triangle(Logic) connects to(save) vertical Circle(Storage)
```

## Running Diaglang

Process a diagram file:

```bash
python3 src/diaglang.py example.diag
```

## Syntax Rules

1. **Shape Format**: `ShapeType(Label)` where ShapeType is Rectangle, Circle, Triangle, or Square
2. **Connection Format**: `connects to(optional_label) direction` where direction is either `horizontal` or `vertical`
3. **Direction Requirement**: All connections must explicitly specify horizontal or vertical direction
4. **Chaining**: Multiple connections can be chained together in a single statement

## Example Output

Input:
```
Rectangle(Web Server) connects to(HTTP) horizontal Circle(Load Balancer) connects to(distribute) vertical Triangle(App Instance)
```

Output:
```
┌────────────┐            _______________  
│ Web Server │───HTTP─── /               \ 
└────────────┘          |  Load Balancer  |
                         \_______________/ 
                     │
                distribute
                     │
                    /\
                   /  \
                  /    \
                 /      \
                /        \
               /          \
              /App Instance\
             /______________\
```

## File Extension

Diaglang files use the `.diag` extension for consistency and tooling integration.