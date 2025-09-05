# Main API exports for backward compatibility
from .diagram_renderer import DiagramRenderer
from .file_operations import FileOperations
from .shape_renderer import ShapeRenderer
from .connection_system import ConnectionSystem
from .chain_system import ChainSystem
from .divergent_connections import DivergentConnections

# For backward compatibility, maintain the original DiagReader interface
DiagReader = DiagramRenderer

__all__ = [
    'DiagramRenderer',
    'DiagReader',  # Backward compatibility alias
    'FileOperations',
    'ShapeRenderer', 
    'ConnectionSystem',
    'ChainSystem',
    'DivergentConnections'
]