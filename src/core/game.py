"""
Main game class that manages the game loop and all systems
"""

import pygame
import moderngl
import glfw
import numpy as np
import sys

from .config import *
from ..graphics.renderer import Renderer
from ..world.world import World
from ..player.player import Player
from ..solo_leveling.hunter_system import HunterSystem

class Game:
    """Main game class that handles the game loop."""
    
    def __init__(self):
        """Initialize the game."""
        self.running = True
        self.clock = pygame.time.Clock()
        self.delta_time = 0.0
        
        # Initialize GLFW
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")
        
        # Create window
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        
        self.window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        
        # Set callbacks
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)
        
        # Initialize OpenGL context
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.enable(moderngl.CULL_FACE)
        
        # Debug: Print OpenGL info
        print(f"OpenGL Version: {self.ctx.version_code}")
        print(f"OpenGL Vendor: {self.ctx.info.get('GL_VENDOR', 'Unknown')}")
        
        # Set depth function
        self.ctx.depth_func = '<'
        
        # Initialize game systems
        self.renderer = Renderer(self.ctx)
        self.world = World()
        self.player = Player()
        self.hunter_system = HunterSystem()
        
        # Mouse state
        self.first_mouse = True
        self.last_x = WINDOW_WIDTH / 2
        self.last_y = WINDOW_HEIGHT / 2
        
        print("Solo Leveling Minecraft initialized successfully!")
    
    def run(self):
        """Main game loop."""
        last_time = glfw.get_time()
        frame_count = 0
        
        print("Starting game loop...")
        
        while not glfw.window_should_close(self.window) and self.running:
            try:
                # Calculate delta time
                current_time = glfw.get_time()
                self.delta_time = current_time - last_time
                last_time = current_time
                
                # Process events
                glfw.poll_events()
                
                # Update game
                self.update()
                
                # Render game
                self.render()
                
                # Swap buffers
                glfw.swap_buffers(self.window)
                
                # Frame rate debugging
                frame_count += 1
                if frame_count % 60 == 0:  # Print FPS every 60 frames
                    fps = 60 / (current_time - (last_time - self.delta_time * 60))
                    print(f"FPS: {fps:.1f}, Player pos: {self.player.position}")
                
                # Maintain FPS with a small sleep to prevent CPU spinning
                self.clock.tick(FPS)
                
            except Exception as e:
                print(f"Error in game loop: {e}")
                self.running = False
                break
        
        print("Exiting game loop...")
        self.cleanup()
    
    def update(self):
        """Update all game systems."""
        # Update player
        self.player.update(self.delta_time, self.window)
        
        # Update world around player
        self.world.update(self.player.position)
        
        # Update hunter system
        self.hunter_system.update(self.delta_time, self.player)
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.ctx.clear(0.4, 0.6, 1.0)  # Sky blue background
        
        # Render world
        self.renderer.render_world(self.world, self.player)
        
        # Render UI
        self.renderer.render_ui(self.player, self.hunter_system)
    
    def key_callback(self, window, key, scancode, action, mods):
        """Handle key input."""
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        
        # Pass to player for movement
        self.player.handle_key_input(key, action)
    
    def mouse_callback(self, window, xpos, ypos):
        """Handle mouse movement."""
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
        
        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos  # Reversed since y-coordinates go from bottom to top
        
        self.last_x = xpos
        self.last_y = ypos
        
        self.player.handle_mouse_input(xoffset, yoffset)
    
    def mouse_button_callback(self, window, button, action, mods):
        """Handle mouse button input."""
        if action == glfw.PRESS:
            if button == glfw.MOUSE_BUTTON_LEFT:
                # Break block
                self.player.break_block(self.world)
            elif button == glfw.MOUSE_BUTTON_RIGHT:
                # Place block
                self.player.place_block(self.world)
    
    def framebuffer_size_callback(self, window, width, height):
        """Handle window resize."""
        self.ctx.viewport = (0, 0, width, height)
        self.player.camera.update_projection(width, height)
    
    def cleanup(self):
        """Clean up resources."""
        self.renderer.cleanup()
        glfw.terminate()
        print("Game cleanup completed.")
