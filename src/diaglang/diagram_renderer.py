from .file_operations import FileOperations
from .shape_renderer import ShapeRenderer
from .connection_system import ConnectionSystem
from .chain_system import ChainSystem
from .divergent_connections import DivergentConnections


class DiagramRenderer:
    def __init__(self):
        self.file_operations = FileOperations()
        self.shape_renderer = ShapeRenderer()
        self.connection_system = ConnectionSystem()
        self.chain_system = ChainSystem()
        self.divergent_connections = DivergentConnections()
    
    # Expose file operations methods for backward compatibility with tests
    def read_file(self, filename):
        return self.file_operations.read_file(filename)
    
    def parse_shapes(self, filename):
        return self.file_operations.parse_shapes(filename)
    
    def render_ascii(self, filename):
        shapes = self.file_operations.parse_shapes(filename)
        if not shapes:
            return ""
        
        rendered_shapes = []
        for shape_input in shapes:
            # Check if this is divergent connections first
            divergent = self.divergent_connections.parse_divergent_connections(shape_input)
            if divergent:
                rendered_divergent = self.divergent_connections.render_divergent_connections(divergent)
                if rendered_divergent:
                    rendered_shapes.append(rendered_divergent)
            else:
                # Check if this is a chain
                chain = self.chain_system.parse_chain(shape_input)
                if chain:
                    rendered_chain = self.chain_system.render_chain(chain)
                    if rendered_chain:
                        rendered_shapes.append(rendered_chain)
                else:
                    # Check if this is a single connection
                    connection = self.connection_system.parse_connection(shape_input)
                    if connection:
                        rendered_connection = self.connection_system.render_connection(
                            connection["from"], connection["to"], connection["horizontal"], 
                            connection["label"], connection.get("arrow_type")
                        )
                        if rendered_connection:
                            rendered_shapes.append(rendered_connection)
                    else:
                        rendered_shape = self.shape_renderer.render_single_shape(shape_input)
                        if rendered_shape:
                            rendered_shapes.append(rendered_shape)
        
        return "\n\n".join(rendered_shapes)