"""
Game constants and configuration
"""

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Solo Leveling Minecraft"
FPS = 60

# World settings
CHUNK_SIZE = 16
WORLD_HEIGHT = 256
RENDER_DISTANCE = 8
SEA_LEVEL = 64

# Block types
BLOCK_TYPES = {
    0: "air",
    1: "grass",
    2: "dirt", 
    3: "stone",
    4: "wood",
    5: "leaves",
    6: "water",
    7: "sand",
    8: "gravel",
    9: "coal_ore",
    10: "iron_ore",
    11: "gold_ore",
    12: "diamond_ore",
    13: "shadow_stone",  # Solo Leveling special block
    14: "gate_stone",    # Portal blocks
    15: "mana_crystal"   # Magic blocks
}

# Player settings
PLAYER_SPEED = 5.0
PLAYER_JUMP_HEIGHT = 1.2
GRAVITY = -9.8
PLAYER_HEIGHT = 1.8
PLAYER_WIDTH = 0.6

# Solo Leveling settings
HUNTER_RANKS = ["E", "D", "C", "B", "A", "S"]
MAX_SHADOW_SOLDIERS = 100
GATE_SPAWN_CHANCE = 0.001

# Controls
CONTROLS = {
    "forward": "w",
    "backward": "s", 
    "left": "a",
    "right": "d",
    "jump": "space",
    "sneak": "shift",
    "inventory": "e",
    "menu": "escape",
    "break_block": "mouse_left",
    "place_block": "mouse_right"
}
