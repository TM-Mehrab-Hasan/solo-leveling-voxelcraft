"""
Test script to verify dependencies
"""

try:
    import pygame
    print("✓ Pygame imported successfully")
except ImportError as e:
    print(f"✗ Pygame import failed: {e}")

try:
    import numpy as np
    print("✓ NumPy imported successfully")
except ImportError as e:
    print(f"✗ NumPy import failed: {e}")

try:
    import OpenGL.GL as gl
    print("✓ PyOpenGL imported successfully")
except ImportError as e:
    print(f"✗ PyOpenGL import failed: {e}")

try:
    import moderngl
    print("✓ ModernGL imported successfully")
except ImportError as e:
    print(f"✗ ModernGL import failed: {e}")

try:
    import glfw
    print("✓ GLFW imported successfully")
except ImportError as e:
    print(f"✗ GLFW import failed: {e}")

try:
    import noise
    print("✓ Noise imported successfully")
except ImportError as e:
    print(f"✗ Noise import failed: {e}")

print("\nDependency check complete!")
