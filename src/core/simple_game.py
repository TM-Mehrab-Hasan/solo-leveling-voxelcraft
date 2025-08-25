"""
Simplified 2.5D version of Solo Leveling Minecraft using only Pygame
"""

import pygame
import numpy as np
import math
import random
from opensimplex import OpenSimplex
from ..core.config import *

class SimpleGame:
    """Simplified game class using Pygame for 2.5D isometric rendering."""
    
    def __init__(self):
        """Initialize the simple game."""
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE + " - 2.5D Version")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Simple world
        self.world_size = 100
        self.world = np.zeros((self.world_size, 32, self.world_size), dtype=np.uint8)
        self.generate_simple_world()
        
        # Player
        self.player_x = self.world_size // 2
        self.player_y = 20
        self.player_z = self.world_size // 2
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        self.zoom = 1.0
        
        # Hunter system
        self.hunter_level = 1
        self.hunter_rank = "E"
        self.experience = 0
        self.shadow_soldiers = []
        
        print("Solo Leveling Minecraft 2.5D initialized!")
    
    def generate_simple_world(self):
        """Generate a simple world with basic terrain."""
        noise = OpenSimplex(seed=12345)
        
        for x in range(self.world_size):
            for z in range(self.world_size):
                # Generate height using noise
                height = int(noise.noise2(x * 0.1, z * 0.1) * 10 + 16)
                height = max(1, min(30, height))
                
                for y in range(height):
                    if y < height - 3:
                        self.world[x, y, z] = 3  # Stone
                    elif y < height - 1:
                        self.world[x, y, z] = 2  # Dirt
                    else:
                        self.world[x, y, z] = 1  # Grass
        
        # Add some special Solo Leveling blocks
        for _ in range(20):
            x, z = random.randint(5, self.world_size-5), random.randint(5, self.world_size-5)
            y = random.randint(5, 15)
            self.world[x, y, z] = 13  # Shadow stone
        
        print("Simple world generated!")
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
        
        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_z = max(0, self.player_z - 1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_z = min(self.world_size - 1, self.player_z + 1)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_x = max(0, self.player_x - 1)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_x = min(self.world_size - 1, self.player_x + 1)
        
        # Camera movement
        if keys[pygame.K_i]:
            self.camera_y -= 5
        if keys[pygame.K_k]:
            self.camera_y += 5
        if keys[pygame.K_j]:
            self.camera_x -= 5
        if keys[pygame.K_l]:
            self.camera_x += 5
    
    def update(self):
        """Update game state."""
        # Update camera to follow player
        target_camera_x = -self.player_x * 20 + WINDOW_WIDTH // 2
        target_camera_y = -self.player_z * 20 + WINDOW_HEIGHT // 2
        
        self.camera_x += (target_camera_x - self.camera_x) * 0.1
        self.camera_y += (target_camera_y - self.camera_y) * 0.1
    
    def render(self):
        """Render the game."""
        self.screen.fill((135, 206, 250))  # Sky blue background
        
        # Render world (simple top-down for now)
        for x in range(max(0, self.player_x - 20), min(self.world_size, self.player_x + 20)):
            for z in range(max(0, self.player_z - 20), min(self.world_size, self.player_z + 20)):
                # Find surface block
                surface_y = 0
                for y in range(31, -1, -1):
                    if self.world[x, y, z] != 0:
                        surface_y = y
                        break
                
                block_type = self.world[x, surface_y, z]
                color = self.get_block_color(block_type)
                
                # Calculate screen position
                screen_x = int(self.camera_x + x * 20)
                screen_y = int(self.camera_y + z * 20 - surface_y * 2)
                
                if 0 <= screen_x < WINDOW_WIDTH and 0 <= screen_y < WINDOW_HEIGHT:
                    pygame.draw.rect(self.screen, color, (screen_x, screen_y, 18, 18))
        
        # Render player
        player_screen_x = int(self.camera_x + self.player_x * 20)
        player_screen_y = int(self.camera_y + self.player_z * 20)
        pygame.draw.circle(self.screen, (255, 255, 0), (player_screen_x + 9, player_screen_y + 9), 8)
        
        # Render UI
        self.render_ui()
        
        pygame.display.flip()
    
    def get_block_color(self, block_type):
        """Get color for block type."""
        colors = {
            0: (0, 0, 0),           # Air
            1: (50, 200, 50),       # Grass
            2: (139, 69, 19),       # Dirt
            3: (128, 128, 128),     # Stone
            4: (101, 67, 33),       # Wood
            5: (34, 139, 34),       # Leaves
            6: (65, 105, 225),      # Water
            7: (238, 203, 173),     # Sand
            8: (105, 105, 105),     # Gravel
            9: (64, 64, 64),        # Coal ore
            10: (184, 134, 11),     # Iron ore
            11: (255, 215, 0),      # Gold ore
            12: (185, 242, 255),    # Diamond ore
            13: (75, 0, 130),       # Shadow stone
            14: (138, 43, 226),     # Gate stone
            15: (255, 20, 147)      # Mana crystal
        }
        return colors.get(block_type, (255, 255, 255))
    
    def render_ui(self):
        """Render UI elements."""
        font = pygame.font.Font(None, 36)
        
        # Hunter info
        hunter_text = font.render(f"Hunter Rank: {self.hunter_rank} | Level: {self.hunter_level}", True, (255, 255, 255))
        self.screen.blit(hunter_text, (10, 10))
        
        exp_text = font.render(f"EXP: {self.experience}", True, (255, 255, 255))
        self.screen.blit(exp_text, (10, 50))
        
        # Position
        pos_text = font.render(f"Position: ({self.player_x}, {self.player_y}, {self.player_z})", True, (255, 255, 255))
        self.screen.blit(pos_text, (10, 90))
        
        # Controls
        controls = [
            "WASD/Arrows: Move",
            "IJKL: Move Camera", 
            "ESC: Quit"
        ]
        
        small_font = pygame.font.Font(None, 24)
        for i, control in enumerate(controls):
            text = small_font.render(control, True, (255, 255, 255))
            self.screen.blit(text, (10, WINDOW_HEIGHT - 80 + i * 25))
        
        # Solo Leveling features
        shadow_text = small_font.render(f"Shadow Soldiers: {len(self.shadow_soldiers)}", True, (255, 255, 255))
        self.screen.blit(shadow_text, (WINDOW_WIDTH - 200, 10))
