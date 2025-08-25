"""
World generation and management system
"""

import numpy as np
from opensimplex import OpenSimplex
from ..core.config import *

class Chunk:
    """A chunk of the world containing blocks."""
    
    def __init__(self, x, z):
        """Initialize a chunk at given coordinates."""
        self.x = x
        self.z = z
        self.blocks = np.zeros((CHUNK_SIZE, WORLD_HEIGHT, CHUNK_SIZE), dtype=np.uint8)
        self.generated = False
        self.dirty = True  # Needs mesh update
    
    def generate_terrain(self, world_seed=0):
        """Generate terrain for this chunk."""
        if self.generated:
            return
        
        # Initialize noise generator
        noise_gen = OpenSimplex(seed=world_seed)
        
        # Generate height map using OpenSimplex noise
        for local_x in range(CHUNK_SIZE):
            for local_z in range(CHUNK_SIZE):
                world_x = self.x * CHUNK_SIZE + local_x
                world_z = self.z * CHUNK_SIZE + local_z
                
                # Generate height using multiple octaves of noise
                height = self.get_height(world_x, world_z, noise_gen)
                
                # Fill blocks based on height
                for y in range(int(height)):
                    if y < SEA_LEVEL - 50:
                        # Deep underground - stone
                        self.blocks[local_x, y, local_z] = 3  # Stone
                    elif y < height - 3:
                        # Underground - dirt
                        self.blocks[local_x, y, local_z] = 2  # Dirt
                    elif y < height:
                        if height > SEA_LEVEL:
                            # Surface - grass
                            self.blocks[local_x, y, local_z] = 1  # Grass
                        else:
                            # Below sea level - sand
                            self.blocks[local_x, y, local_z] = 7  # Sand
                
                # Add water at sea level
                if height < SEA_LEVEL:
                    for y in range(int(height), SEA_LEVEL):
                        if self.blocks[local_x, y, local_z] == 0:
                            self.blocks[local_x, y, local_z] = 6  # Water
        
        # Add ores
        self.generate_ores(world_seed)
        
        # Add Solo Leveling features
        self.generate_solo_leveling_features(world_seed)
        
        self.generated = True
        self.dirty = True
    
    def get_height(self, x, z, noise_gen):
        """Get terrain height at world coordinates."""
        # Base terrain
        height = noise_gen.noise2(x * 0.01, z * 0.01) * 50 + SEA_LEVEL
        
        # Add hills with different frequency
        hills = noise_gen.noise2(x * 0.005, z * 0.005) * 30
        
        return max(1, height + hills)
    
    def generate_ores(self, seed):
        """Generate ore deposits in the chunk."""
        np.random.seed(seed + self.x * 1000 + self.z)
        
        # Coal ore
        for _ in range(np.random.randint(5, 15)):
            x, y, z = (np.random.randint(0, CHUNK_SIZE),
                      np.random.randint(5, 60),
                      np.random.randint(0, CHUNK_SIZE))
            if self.blocks[x, y, z] == 3:  # Stone
                self.generate_ore_vein(x, y, z, 9, 3)  # Coal ore
        
        # Iron ore
        for _ in range(np.random.randint(3, 8)):
            x, y, z = (np.random.randint(0, CHUNK_SIZE),
                      np.random.randint(5, 40),
                      np.random.randint(0, CHUNK_SIZE))
            if self.blocks[x, y, z] == 3:  # Stone
                self.generate_ore_vein(x, y, z, 10, 2)  # Iron ore
        
        # Diamond ore
        for _ in range(np.random.randint(1, 3)):
            x, y, z = (np.random.randint(0, CHUNK_SIZE),
                      np.random.randint(5, 20),
                      np.random.randint(0, CHUNK_SIZE))
            if self.blocks[x, y, z] == 3:  # Stone
                self.generate_ore_vein(x, y, z, 12, 1)  # Diamond ore
    
    def generate_ore_vein(self, start_x, start_y, start_z, ore_type, size):
        """Generate a vein of ore around a starting position."""
        for _ in range(size):
            x = start_x + np.random.randint(-2, 3)
            y = start_y + np.random.randint(-1, 2)
            z = start_z + np.random.randint(-2, 3)
            
            if (0 <= x < CHUNK_SIZE and 0 <= y < WORLD_HEIGHT and 
                0 <= z < CHUNK_SIZE and self.blocks[x, y, z] == 3):
                self.blocks[x, y, z] = ore_type
    
    def generate_solo_leveling_features(self, seed):
        """Generate Solo Leveling specific features."""
        np.random.seed(seed + self.x * 2000 + self.z * 3000)
        
        # Shadow stones (rare)
        for _ in range(np.random.randint(0, 2)):
            x, y, z = (np.random.randint(0, CHUNK_SIZE),
                      np.random.randint(5, 30),
                      np.random.randint(0, CHUNK_SIZE))
            if self.blocks[x, y, z] == 3:  # Stone
                self.blocks[x, y, z] = 13  # Shadow stone
        
        # Mana crystals (magical ore)
        for _ in range(np.random.randint(1, 4)):
            x, y, z = (np.random.randint(0, CHUNK_SIZE),
                      np.random.randint(10, 50),
                      np.random.randint(0, CHUNK_SIZE))
            if self.blocks[x, y, z] == 3:  # Stone
                self.blocks[x, y, z] = 15  # Mana crystal
        
        # Gate spawn chance (very rare)
        if np.random.random() < GATE_SPAWN_CHANCE:
            self.spawn_gate()
    
    def spawn_gate(self):
        """Spawn a dungeon gate in this chunk."""
        # Find a suitable surface location
        for attempt in range(10):
            x, z = np.random.randint(2, CHUNK_SIZE-2), np.random.randint(2, CHUNK_SIZE-2)
            
            # Find surface height
            for y in range(WORLD_HEIGHT-1, 0, -1):
                if self.blocks[x, y, z] != 0:  # Not air
                    # Create gate structure
                    gate_height = 5
                    gate_width = 3
                    
                    # Clear area and build gate
                    for gx in range(gate_width):
                        for gy in range(gate_height):
                            gate_x = x - 1 + gx
                            gate_y = y + 1 + gy
                            
                            if (0 <= gate_x < CHUNK_SIZE and 
                                0 <= gate_y < WORLD_HEIGHT):
                                if gx == 0 or gx == gate_width-1 or gy == gate_height-1:
                                    self.blocks[gate_x, gate_y, z] = 14  # Gate stone
                                else:
                                    self.blocks[gate_x, gate_y, z] = 0  # Air (portal)
                    
                    print(f"Gate spawned in chunk ({self.x}, {self.z}) at ({x}, {y+1}, {z})")
                    return


class World:
    """World management system."""
    
    def __init__(self, seed=None):
        """Initialize the world."""
        self.seed = seed or np.random.randint(0, 1000000)
        self.chunks = {}
        self.loaded_chunks = set()
        
        print(f"World initialized with seed: {self.seed}")
    
    def get_chunk_coords(self, x, z):
        """Get chunk coordinates from world coordinates."""
        return int(x // CHUNK_SIZE), int(z // CHUNK_SIZE)
    
    def get_chunk(self, chunk_x, chunk_z):
        """Get or create a chunk."""
        coords = (chunk_x, chunk_z)
        
        if coords not in self.chunks:
            chunk = Chunk(chunk_x, chunk_z)
            chunk.generate_terrain(self.seed)
            self.chunks[coords] = chunk
        
        return self.chunks[coords]
    
    def get_block(self, x, y, z):
        """Get block type at world coordinates."""
        if y < 0 or y >= WORLD_HEIGHT:
            return 0  # Air
        
        chunk_x, chunk_z = self.get_chunk_coords(x, z)
        chunk = self.get_chunk(chunk_x, chunk_z)
        
        local_x = x - chunk_x * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE
        
        if 0 <= local_x < CHUNK_SIZE and 0 <= local_z < CHUNK_SIZE:
            return chunk.blocks[local_x, y, local_z]
        
        return 0  # Air
    
    def set_block(self, x, y, z, block_type):
        """Set block type at world coordinates."""
        if y < 0 or y >= WORLD_HEIGHT:
            return False
        
        chunk_x, chunk_z = self.get_chunk_coords(x, z)
        chunk = self.get_chunk(chunk_x, chunk_z)
        
        local_x = x - chunk_x * CHUNK_SIZE
        local_z = z - chunk_z * CHUNK_SIZE
        
        if 0 <= local_x < CHUNK_SIZE and 0 <= local_z < CHUNK_SIZE:
            chunk.blocks[local_x, y, local_z] = block_type
            chunk.dirty = True
            return True
        
        return False
    
    def update(self, player_position):
        """Update world around player position."""
        player_chunk_x, player_chunk_z = self.get_chunk_coords(
            player_position[0], player_position[2]
        )
        
        # Debug output
        if not hasattr(self, '_debug_player_chunk'):
            self._debug_player_chunk = True
            print(f"Player at {player_position[0]:.1f}, {player_position[2]:.1f} -> chunk ({player_chunk_x}, {player_chunk_z})")
        
        # Load chunks around player (limit per frame to prevent hanging)
        chunks_loaded_this_frame = 0
        max_chunks_per_frame = 2  # Limit chunk generation per frame
        
        for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
                if chunks_loaded_this_frame >= max_chunks_per_frame:
                    break
                    
                chunk_x = player_chunk_x + dx
                chunk_z = player_chunk_z + dz
                
                coords = (chunk_x, chunk_z)
                if coords not in self.loaded_chunks:
                    self.get_chunk(chunk_x, chunk_z)
                    self.loaded_chunks.add(coords)
                    chunks_loaded_this_frame += 1
            
            if chunks_loaded_this_frame >= max_chunks_per_frame:
                break
        
        # Unload distant chunks
        chunks_to_unload = []
        for coords in self.loaded_chunks:
            chunk_x, chunk_z = coords
            distance = max(abs(chunk_x - player_chunk_x), abs(chunk_z - player_chunk_z))
            if distance > RENDER_DISTANCE + 2:
                chunks_to_unload.append(coords)
        
        for coords in chunks_to_unload:
            self.loaded_chunks.discard(coords)
            if coords in self.chunks:
                del self.chunks[coords]
    
    def get_loaded_chunks(self):
        """Get all loaded chunks."""
        return [self.chunks[coords] for coords in self.loaded_chunks if coords in self.chunks]
