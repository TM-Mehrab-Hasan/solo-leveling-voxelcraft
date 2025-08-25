"""
Simplified Solo Leveling Minecraft Clone using Pygame
2.5D Isometric view initially, can be upgraded to 3D later
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.core.simple_game import SimpleGame
    print("Starting Solo Leveling Minecraft (2.5D Version)...")
    game = SimpleGame()
    game.run()
except ImportError as e:
    print(f"Import error: {e}")
    print("Falling back to basic implementation...")
    
    # Basic fallback
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Solo Leveling Minecraft - Basic Version")
    clock = pygame.time.Clock()
    
    print("Solo Leveling Minecraft - Basic Mode")
    print("This is a placeholder. Full 3D version requires additional dependencies.")
    print("Press ESC to quit.")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        screen.fill((135, 206, 250))  # Sky blue
        
        # Draw simple text
        font = pygame.font.Font(None, 36)
        text = font.render("Solo Leveling Minecraft", True, (255, 255, 255))
        screen.blit(text, (screen.get_width()//2 - text.get_width()//2, 100))
        
        info_text = font.render("Full 3D version requires OpenGL dependencies", True, (255, 255, 255))
        screen.blit(info_text, (screen.get_width()//2 - info_text.get_width()//2, 200))
        
        controls = font.render("Press ESC to quit", True, (255, 255, 255))
        screen.blit(controls, (screen.get_width()//2 - controls.get_width()//2, 300))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    pass
