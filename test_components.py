"""
Simple test to check where the array comparison error occurs
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing imports...")
    from src.core.config import *
    print("✓ Config imported")
    
    from src.graphics.camera import Camera
    print("✓ Camera imported")
    
    from src.world.world import World
    print("✓ World imported")
    
    from src.player.player import Player
    print("✓ Player imported")
    
    from src.solo_leveling.hunter_system import HunterSystem
    print("✓ Hunter system imported")
    
    print("Testing object creation...")
    world = World()
    print("✓ World created")
    
    player = Player()
    print("✓ Player created")
    
    hunter_system = HunterSystem()
    print("✓ Hunter system created")
    
    print("All tests passed!")
    
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
