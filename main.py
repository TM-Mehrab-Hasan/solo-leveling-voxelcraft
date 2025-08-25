"""
Solo Leveling Minecraft Clone
A 3D voxel-based game with Solo Leveling themes
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.game import Game

def main():
    """Main entry point for the game."""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error starting game: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
