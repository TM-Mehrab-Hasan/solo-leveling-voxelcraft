"""
3D Camera system for first-person view
"""

import numpy as np
import math
from ..core.config import *

class Camera:
    """First-person camera for 3D world navigation."""
    
    def __init__(self, position=None):
        """Initialize the camera."""
        if position is None:
            self.position = np.array([8.0, 67.0, 8.0], dtype=np.float32)
        else:
            self.position = position.copy() if isinstance(position, np.ndarray) else np.array(position, dtype=np.float32)
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self.right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self.world_up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Euler angles
        self.yaw = -90.0  # Looking towards negative Z
        self.pitch = 0.0  # Look straight ahead initially
        
        # Camera options
        self.movement_speed = PLAYER_SPEED
        self.mouse_sensitivity = 0.1
        self.zoom = 45.0
        
        # Projection matrix
        self.projection_matrix = self.get_projection_matrix(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        self.update_camera_vectors()
        print(f"Camera initialized at {self.position}, looking {self.front}")
    
    def get_view_matrix(self):
        """Get the view matrix for rendering."""
        return self.look_at(self.position, self.position + self.front, self.up)
    
    def get_projection_matrix(self, width, height):
        """Get the projection matrix."""
        aspect_ratio = width / height
        fov = math.radians(self.zoom)
        near = 0.1
        far = 1000.0
        
        # Create perspective projection matrix
        f = 1.0 / math.tan(fov / 2.0)
        projection = np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)
        
        return projection
    
    def update_projection(self, width, height):
        """Update projection matrix when window is resized."""
        self.projection_matrix = self.get_projection_matrix(width, height)
    
    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        """Process mouse movement for camera rotation."""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        
        self.yaw += xoffset
        self.pitch += yoffset
        
        # Constrain pitch to avoid screen flip
        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        
        self.update_camera_vectors()
    
    def update_camera_vectors(self):
        """Calculate front vector from euler angles."""
        front = np.array([
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        ], dtype=np.float32)
        
        self.front = self.normalize(front)
        self.right = self.normalize(np.cross(self.front, self.world_up))
        self.up = self.normalize(np.cross(self.right, self.front))
    
    @staticmethod
    def normalize(vector):
        """Normalize a vector."""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    @staticmethod
    def look_at(position, target, up):
        """Create a look-at matrix."""
        direction = Camera.normalize(position - target)
        right = Camera.normalize(np.cross(Camera.normalize(up), direction))
        up_vec = np.cross(direction, right)
        
        # Create look-at matrix
        look_at_matrix = np.array([
            [right[0], up_vec[0], direction[0], 0],
            [right[1], up_vec[1], direction[1], 0],
            [right[2], up_vec[2], direction[2], 0],
            [-np.dot(right, position), -np.dot(up_vec, position), -np.dot(direction, position), 1]
        ], dtype=np.float32)
        
        return look_at_matrix
