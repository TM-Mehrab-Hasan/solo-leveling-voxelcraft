"""
Basic OpenGL renderer for the voxel world
"""

import moderngl
import numpy as np
from ..core.config import *

class Renderer:
    """OpenGL renderer for the game."""
    
    def __init__(self, ctx):
        """Initialize the renderer."""
        self.ctx = ctx
        
        # Create shaders
        self.create_shaders()
        
        # Block colors (simple colored cubes for now)
        self.block_colors = {
            0: (0, 0, 0, 0),        # Air (transparent)
            1: (0.2, 0.8, 0.2, 1),  # Grass (green)
            2: (0.5, 0.3, 0.1, 1),  # Dirt (brown)
            3: (0.5, 0.5, 0.5, 1),  # Stone (gray)
            4: (0.4, 0.2, 0.1, 1),  # Wood (brown)
            5: (0.1, 0.6, 0.1, 1),  # Leaves (dark green)
            6: (0.2, 0.4, 0.8, 0.7), # Water (blue, translucent)
            7: (0.9, 0.8, 0.6, 1),  # Sand (tan)
            8: (0.4, 0.4, 0.4, 1),  # Gravel (gray)
            9: (0.2, 0.2, 0.2, 1),  # Coal ore (dark)
            10: (0.7, 0.5, 0.3, 1), # Iron ore (rust)
            11: (0.8, 0.8, 0.2, 1), # Gold ore (yellow)
            12: (0.4, 0.8, 0.8, 1), # Diamond ore (cyan)
            13: (0.1, 0.0, 0.3, 1), # Shadow stone (dark purple)
            14: (0.3, 0.0, 0.6, 1), # Gate stone (purple)
            15: (0.8, 0.2, 0.8, 1)  # Mana crystal (magenta)
        }
        
        # Chunk meshes cache
        self.chunk_meshes = {}
    
    def create_shaders(self):
        """Create OpenGL shaders."""
        # Vertex shader
        vertex_shader = """
        #version 330 core
        
        layout (location = 0) in vec3 position;
        layout (location = 1) in vec4 color;
        layout (location = 2) in vec3 normal;
        
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        out vec4 vertexColor;
        out vec3 vertexNormal;
        out vec3 fragmentPos;
        
        void main() {
            gl_Position = projection * view * model * vec4(position, 1.0);
            vertexColor = color;
            vertexNormal = normal;
            fragmentPos = vec3(model * vec4(position, 1.0));
        }
        """
        
        # Fragment shader
        fragment_shader = """
        #version 330 core
        
        in vec4 vertexColor;
        in vec3 vertexNormal;
        in vec3 fragmentPos;
        
        out vec4 fragColor;
        
        uniform vec3 lightPos;
        uniform vec3 lightColor;
        uniform vec3 viewPos;
        
        void main() {
            // Ambient lighting
            float ambientStrength = 0.3;
            vec3 ambient = ambientStrength * lightColor;
            
            // Diffuse lighting
            vec3 norm = normalize(vertexNormal);
            vec3 lightDir = normalize(lightPos - fragmentPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * lightColor;
            
            vec3 result = (ambient + diffuse) * vertexColor.rgb;
            fragColor = vec4(result, vertexColor.a);
        }
        """
        
        # Create shader program
        self.shader_program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        
        # Set uniforms (with error checking)
        try:
            self.shader_program['lightPos'].value = (0, 100, 0)
            self.shader_program['lightColor'].value = (1.0, 1.0, 1.0)
        except KeyError as e:
            print(f"Warning: Shader uniform not found: {e}")
    
    def render_world(self, world, player):
        """Render the world."""
        try:
            # Update view and projection matrices (ModernGL programs are auto-bound)
            view_matrix = player.camera.get_view_matrix()
            projection_matrix = player.camera.projection_matrix
            
            # Debug: Print first matrix to verify they're valid
            if hasattr(self, '_debug_count'):
                self._debug_count += 1
            else:
                self._debug_count = 1
                print(f"View matrix shape: {view_matrix.shape}")
                print(f"Projection matrix shape: {projection_matrix.shape}")
                print(f"Camera position: {player.camera.position}")
                print(f"Camera front: {player.camera.front}")
            
            self.shader_program['view'].write(view_matrix.astype(np.float32).tobytes())
            self.shader_program['projection'].write(projection_matrix.astype(np.float32).tobytes())
            if 'viewPos' in self.shader_program:
                self.shader_program['viewPos'].value = tuple(player.camera.position)
        except KeyError as e:
            print(f"Warning: Shader uniform not found: {e}")
            return
        except Exception as e:
            print(f"Error setting shader uniforms: {e}")
            return
        
        # Render each loaded chunk with safety limits
        chunks_rendered = 0
        max_chunks_per_frame = 16  # Limit chunks per frame to prevent hanging
        
        for chunk in world.get_loaded_chunks():
            if chunks_rendered >= max_chunks_per_frame:
                break
                
            try:
                if chunk.dirty:
                    self.update_chunk_mesh(chunk)
                
                if (chunk.x, chunk.z) in self.chunk_meshes:
                    mesh = self.chunk_meshes[(chunk.x, chunk.z)]
                    if mesh:
                        # Set model matrix (identity for now)
                        model_matrix = np.eye(4, dtype=np.float32)
                        self.shader_program['model'].write(model_matrix.tobytes())
                        mesh.render()
                        chunks_rendered += 1
                        
                        # Debug: Log rendering info for first chunk only
                        if self._debug_count <= 1 and chunk.x == 0 and chunk.z == 0:
                            print(f"Rendered chunk ({chunk.x}, {chunk.z}) with {mesh.vertices} vertices")
                        
            except Exception as e:
                print(f"Error rendering chunk ({chunk.x}, {chunk.z}): {e}")
                continue
                
        if self._debug_count <= 1:
            print(f"Total chunks rendered this frame: {chunks_rendered}")
    
    def update_chunk_mesh(self, chunk):
        """Update mesh for a chunk."""
        vertices, indices = self.generate_chunk_mesh(chunk)
        
        if len(vertices) == 0:
            # No visible blocks in chunk
            self.chunk_meshes[(chunk.x, chunk.z)] = None
            chunk.dirty = False
            return
        
        # Create or update mesh using ModernGL efficiently
        vertices_data = np.array(vertices, dtype=np.float32)
        indices_data = np.array(indices, dtype=np.uint32)
        
        # Debug output for first chunk
        if not hasattr(self, '_mesh_debug_done'):
            self._mesh_debug_done = True
            print(f"First chunk mesh: {len(vertices)} vertices, {len(indices)} indices")
            print(f"Vertex data shape: {vertices_data.shape}")
            print(f"Index data shape: {indices_data.shape}")
            if len(vertices) > 0:
                print(f"First vertex: {vertices_data[0]}")
        
        vertex_buffer = self.ctx.buffer(vertices_data.tobytes())
        index_buffer = self.ctx.buffer(indices_data.tobytes())
        
        # Vertex array object with proper attribute layout
        vao = self.ctx.vertex_array(self.shader_program, [
            (vertex_buffer, '3f 4f 3f', 'position', 'color', 'normal')
        ], index_buffer)
        
        # Store vertex count for debugging
        vao.vertices = len(indices)
        
        # Clean up old mesh if it exists
        old_mesh = self.chunk_meshes.get((chunk.x, chunk.z))
        if old_mesh:
            old_mesh.release()
        
        self.chunk_meshes[(chunk.x, chunk.z)] = vao
        chunk.dirty = False
    
    def generate_chunk_mesh(self, chunk):
        """Generate mesh data for a chunk."""
        vertices = []
        indices = []
        index_offset = 0
        blocks_processed = 0
        visible_blocks = 0
        max_blocks_per_chunk = CHUNK_SIZE * WORLD_HEIGHT * CHUNK_SIZE
        
        # Debug: Check first few blocks
        debug_blocks = []
        
        for x in range(CHUNK_SIZE):
            for y in range(WORLD_HEIGHT):
                for z in range(CHUNK_SIZE):
                    blocks_processed += 1
                    if blocks_processed > max_blocks_per_chunk:
                        print(f"Warning: Chunk mesh generation exceeded maximum blocks")
                        break
                        
                    block_type = chunk.blocks[x, y, z]
                    
                    if block_type == 0:  # Air
                        continue
                    
                    visible_blocks += 1
                    world_x = chunk.x * CHUNK_SIZE + x
                    world_z = chunk.z * CHUNK_SIZE + z
                    
                    # Debug: Store first few blocks
                    if len(debug_blocks) < 3:
                        debug_blocks.append({
                            'local': (x, y, z),
                            'world': (world_x, y, world_z),
                            'type': block_type
                        })
                    
                    # Check each face for visibility
                    faces = self.get_visible_faces(chunk, x, y, z, world_x, world_z)
                    
                    if faces:
                        block_vertices, block_indices = self.create_block_mesh(
                            world_x, y, world_z, block_type, faces, index_offset
                        )
                        vertices.extend(block_vertices)
                        indices.extend(block_indices)
                        index_offset += len(block_vertices)
                
                if blocks_processed > max_blocks_per_chunk:
                    break
            if blocks_processed > max_blocks_per_chunk:
                break
        
        # Debug output - focus on chunk (0,0) where the player starts
        if visible_blocks > 0 and chunk.x == 0 and chunk.z == 0:
            print(f"PLAYER CHUNK (0,0): {visible_blocks} blocks, {len(vertices)} vertices")
            y_levels = set()
            for block in debug_blocks:
                y_levels.add(block['world'][1])
                print(f"  Block at {block['local']} -> {block['world']}, type {block['type']}")
            if len(debug_blocks) >= 3:
                print(f"  Terrain Y levels in this sample: {sorted(y_levels)}")
        
        return np.array(vertices), np.array(indices)
    
    def get_visible_faces(self, chunk, x, y, z, world_x, world_z):
        """Determine which faces of a block are visible."""
        faces = []
        
        # Check each direction
        directions = [
            (0, 1, 0),   # Top
            (0, -1, 0),  # Bottom
            (1, 0, 0),   # Right
            (-1, 0, 0),  # Left
            (0, 0, 1),   # Front
            (0, 0, -1)   # Back
        ]
        
        face_names = ['top', 'bottom', 'right', 'left', 'front', 'back']
        
        for i, (dx, dy, dz) in enumerate(directions):
            neighbor_x, neighbor_y, neighbor_z = x + dx, y + dy, z + dz
            
            # Check if neighbor is air or transparent
            if self.is_face_visible(chunk, neighbor_x, neighbor_y, neighbor_z, world_x + dx, world_z + dz):
                faces.append(face_names[i])
        
        return faces
    
    def is_face_visible(self, chunk, x, y, z, world_x, world_z):
        """Check if a face should be rendered."""
        if y < 0 or y >= WORLD_HEIGHT:
            return True  # Outside world bounds
        
        # Check within chunk first
        if 0 <= x < CHUNK_SIZE and 0 <= z < CHUNK_SIZE:
            neighbor_block = chunk.blocks[x, y, z]
        else:
            # Check adjacent chunk (simplified - assume air for now)
            neighbor_block = 0
        
        return neighbor_block == 0 or neighbor_block == 6  # Air or water
    
    def create_block_mesh(self, x, y, z, block_type, faces, index_offset):
        """Create mesh data for a single block."""
        vertices = []
        indices = []
        
        color = self.block_colors.get(block_type, (1, 1, 1, 1))
        
        # Face definitions
        face_data = {
            'top': {
                'vertices': [
                    [x, y+1, z], [x+1, y+1, z], [x+1, y+1, z+1], [x, y+1, z+1]
                ],
                'normal': [0, 1, 0],
                'indices': [0, 1, 2, 0, 2, 3]
            },
            'bottom': {
                'vertices': [
                    [x, y, z+1], [x+1, y, z+1], [x+1, y, z], [x, y, z]
                ],
                'normal': [0, -1, 0],
                'indices': [0, 1, 2, 0, 2, 3]
            },
            'right': {
                'vertices': [
                    [x+1, y, z], [x+1, y, z+1], [x+1, y+1, z+1], [x+1, y+1, z]
                ],
                'normal': [1, 0, 0],
                'indices': [0, 1, 2, 0, 2, 3]
            },
            'left': {
                'vertices': [
                    [x, y, z+1], [x, y, z], [x, y+1, z], [x, y+1, z+1]
                ],
                'normal': [-1, 0, 0],
                'indices': [0, 1, 2, 0, 2, 3]
            },
            'front': {
                'vertices': [
                    [x, y, z+1], [x+1, y, z+1], [x+1, y+1, z+1], [x, y+1, z+1]
                ],
                'normal': [0, 0, 1],
                'indices': [0, 1, 2, 0, 2, 3]
            },
            'back': {
                'vertices': [
                    [x+1, y, z], [x, y, z], [x, y+1, z], [x+1, y+1, z]
                ],
                'normal': [0, 0, -1],
                'indices': [0, 1, 2, 0, 2, 3]
            }
        }
        
        vertex_count = 0
        for face in faces:
            if face in face_data:
                face_info = face_data[face]
                
                # Add vertices
                for vertex in face_info['vertices']:
                    vertices.append([
                        vertex[0], vertex[1], vertex[2],  # Position
                        color[0], color[1], color[2], color[3],  # Color
                        face_info['normal'][0], face_info['normal'][1], face_info['normal'][2]  # Normal
                    ])
                
                # Add indices
                for idx in face_info['indices']:
                    indices.append(index_offset + vertex_count + idx)
                
                vertex_count += 4
        
        return vertices, indices
    
    def render_ui(self, player, hunter_system):
        """Render UI elements."""
        # Basic UI rendering would go here
        # For now, just print debug info occasionally
        pass
    
    def cleanup(self):
        """Clean up ModernGL resources."""
        for mesh in self.chunk_meshes.values():
            if mesh:
                mesh.release()
        self.chunk_meshes.clear()
        
        if hasattr(self, 'shader_program'):
            self.shader_program.release()
