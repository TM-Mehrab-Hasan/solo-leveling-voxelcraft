"""
Player class for Solo Leveling Minecraft
"""

import numpy as np
import glfw
import math
from ..graphics.camera import Camera
from ..core.config import *

class Player:
    """Player character with Solo Leveling hunter abilities."""
    
    def __init__(self):
        """Initialize the player."""
        # Position and physics (start closer to terrain)
        self.position = np.array([8.0, 67.0, 8.0], dtype=np.float32)
        self.velocity = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.on_ground = False
        
        # Camera
        self.camera = Camera(self.position)
        
        # Player stats
        self.health = 100
        self.max_health = 100
        self.mana = 50
        self.max_mana = 50
        self.stamina = 100
        self.max_stamina = 100
        
        # Movement
        self.speed = PLAYER_SPEED
        self.jump_strength = PLAYER_JUMP_HEIGHT
        self.is_sprinting = False
        self.is_sneaking = False
        
        # Input state
        self.keys_pressed = set()
        
        # Block interaction
        self.reach_distance = 5.0
        self.selected_block_type = 1  # Grass by default
    
    def update(self, delta_time, window):
        """Update player state."""
        # Process movement
        self.process_movement(delta_time, window)
        
        # Apply physics
        self.apply_physics(delta_time)
        
        # Update camera position
        self.camera.position = self.position + np.array([0, PLAYER_HEIGHT * 0.8, 0])
    
    def process_movement(self, delta_time, window):
        """Process player movement input."""
        movement_vector = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # Get current speed
        current_speed = self.speed
        if self.is_sprinting:
            current_speed *= 1.5
        if self.is_sneaking:
            current_speed *= 0.3
        
        # Forward/backward movement
        if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
            movement_vector += self.camera.front
        if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
            movement_vector -= self.camera.front
        
        # Left/right movement
        if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
            movement_vector -= self.camera.right
        if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
            movement_vector += self.camera.right
        
        # Normalize movement vector (excluding Y component for flying)
        movement_length = np.linalg.norm([movement_vector[0], movement_vector[2]])
        if movement_length > 0:
            movement_vector = self.normalize_horizontal(movement_vector)
            self.velocity[0] = movement_vector[0] * current_speed
            self.velocity[2] = movement_vector[2] * current_speed
        else:
            # Apply friction
            self.velocity[0] *= 0.8
            self.velocity[2] *= 0.8
        
        # Jumping
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS and self.on_ground:
            self.velocity[1] = self.jump_strength
            self.on_ground = False
        
        # Sprinting
        self.is_sprinting = glfw.get_key(window, glfw.KEY_LEFT_SHIFT) == glfw.PRESS
        
        # Sneaking
        self.is_sneaking = glfw.get_key(window, glfw.KEY_LEFT_CONTROL) == glfw.PRESS
    
    def apply_physics(self, delta_time):
        """Apply physics to player movement."""
        # Apply gravity
        if not self.on_ground:
            self.velocity[1] += GRAVITY * delta_time
        
        # Update position
        self.position += self.velocity * delta_time
        
        # Simple ground collision (temporary)
        if self.position[1] < 65:  # Ground level
            self.position[1] = 65
            self.velocity[1] = 0
            self.on_ground = True
        else:
            self.on_ground = False
    
    def handle_key_input(self, key, action):
        """Handle key press events."""
        if action == glfw.PRESS:
            self.keys_pressed.add(key)
        elif action == glfw.RELEASE:
            self.keys_pressed.discard(key)
        
        # Number keys for block selection
        if action == glfw.PRESS:
            if key >= glfw.KEY_1 and key <= glfw.KEY_9:
                self.selected_block_type = key - glfw.KEY_1 + 1
    
    def handle_mouse_input(self, xoffset, yoffset):
        """Handle mouse movement for camera."""
        self.camera.process_mouse_movement(xoffset, yoffset)
    
    def break_block(self, world):
        """Break a block in the world."""
        target = self.get_target_block(world)
        if target:
            x, y, z = target
            world.set_block(x, y, z, 0)  # Set to air
            print(f"Broke block at {x}, {y}, {z}")
    
    def place_block(self, world):
        """Place a block in the world."""
        target = self.get_target_block_adjacent(world)
        if target:
            x, y, z = target
            world.set_block(x, y, z, self.selected_block_type)
            print(f"Placed block type {self.selected_block_type} at {x}, {y}, {z}")
    
    def get_target_block(self, world):
        """Get the block the player is looking at."""
        # Ray casting to find target block
        ray_start = self.camera.position
        ray_direction = self.camera.front
        
        # Step through ray
        step_size = 0.1
        for i in range(int(self.reach_distance / step_size)):
            point = ray_start + ray_direction * (i * step_size)
            block_x, block_y, block_z = int(point[0]), int(point[1]), int(point[2])
            
            if world.get_block(block_x, block_y, block_z) != 0:  # Not air
                return (block_x, block_y, block_z)
        
        return None
    
    def get_target_block_adjacent(self, world):
        """Get the position adjacent to the target block for placing."""
        target = self.get_target_block(world)
        if not target:
            return None
        
        # Find the face that was hit and place adjacent to it
        # For now, just place above the target block
        x, y, z = target
        return (x, y + 1, z)
    
    @staticmethod
    def normalize_horizontal(vector):
        """Normalize vector while keeping Y component."""
        horizontal = np.array([vector[0], 0, vector[2]])
        norm = np.linalg.norm(horizontal)
        if norm == 0:
            return vector
        normalized_horizontal = horizontal / norm
        return np.array([normalized_horizontal[0], vector[1], normalized_horizontal[2]])
