"""
Entity system for mobs and creatures
"""

import numpy as np
from ..core.config import *

class Entity:
    """Base entity class."""
    
    def __init__(self, x, y, z, entity_type="unknown"):
        """Initialize entity."""
        self.position = np.array([x, y, z], dtype=np.float32)
        self.velocity = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.entity_type = entity_type
        self.health = 100
        self.max_health = 100
        self.is_alive = True
        self.level = 1
    
    def update(self, delta_time):
        """Update entity."""
        if not self.is_alive:
            return
        
        # Apply gravity
        self.velocity[1] += GRAVITY * delta_time
        
        # Update position
        self.position += self.velocity * delta_time
        
        # Simple ground collision
        if self.position[1] < 65:  # Ground level
            self.position[1] = 65
            self.velocity[1] = 0
    
    def take_damage(self, damage):
        """Take damage."""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.entity_type} defeated!")
    
    def heal(self, amount):
        """Heal entity."""
        self.health = min(self.max_health, self.health + amount)


class Monster(Entity):
    """Monster entity for Solo Leveling dungeons."""
    
    def __init__(self, x, y, z, monster_type, level=1):
        """Initialize monster."""
        super().__init__(x, y, z, monster_type)
        self.level = level
        self.attack_power = 20 * level
        self.experience_reward = 50 * level
        self.can_be_extracted = True  # Can become shadow soldier
        
        # Monster-specific stats
        monster_stats = {
            "ant": {"health": 80, "attack": 15, "speed": 1.5},
            "wolf": {"health": 120, "attack": 25, "speed": 2.0},
            "orc": {"health": 200, "attack": 35, "speed": 1.2},
            "knight": {"health": 300, "attack": 50, "speed": 1.0},
            "dragon": {"health": 1000, "attack": 100, "speed": 0.8}
        }
        
        if monster_type in monster_stats:
            stats = monster_stats[monster_type]
            self.max_health = stats["health"] * level
            self.health = self.max_health
            self.attack_power = stats["attack"] * level
            self.move_speed = stats["speed"]
        
        # AI state
        self.target = None
        self.attack_cooldown = 0
        self.detection_range = 10.0
    
    def update(self, delta_time, player, world):
        """Update monster AI."""
        super().update(delta_time)
        
        if not self.is_alive:
            return
        
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= delta_time
        
        # Simple AI: chase player if in range
        distance_to_player = np.linalg.norm(self.position - player.position)
        
        if distance_to_player <= self.detection_range:
            self.target = player
            
            # Move towards player
            if distance_to_player > 2.0:  # Don't get too close
                direction = player.position - self.position
                direction[1] = 0  # Don't move vertically
                if np.linalg.norm(direction) > 0:
                    direction = direction / np.linalg.norm(direction)
                    self.velocity[0] = direction[0] * self.move_speed
                    self.velocity[2] = direction[2] * self.move_speed
            else:
                # Close enough to attack
                self.velocity[0] = 0
                self.velocity[2] = 0
                
                if self.attack_cooldown <= 0:
                    self.attack_player(player)
        else:
            # No target, stop moving
            self.velocity[0] = 0
            self.velocity[2] = 0
            self.target = None
    
    def attack_player(self, player):
        """Attack the player."""
        if self.attack_cooldown <= 0:
            damage = np.random.randint(self.attack_power // 2, self.attack_power + 1)
            print(f"{self.entity_type} attacks for {damage} damage!")
            # player.take_damage(damage)  # Implement player damage system
            self.attack_cooldown = 2.0  # 2 second cooldown


class DungeonBoss(Monster):
    """Boss monster for dungeon gates."""
    
    def __init__(self, x, y, z, boss_type, level=1):
        """Initialize boss."""
        super().__init__(x, y, z, boss_type, level)
        
        # Bosses are much stronger
        self.max_health *= 5
        self.health = self.max_health
        self.attack_power *= 3
        self.experience_reward *= 10
        self.detection_range = 20.0
        
        # Special abilities
        self.special_abilities = []
        self.ability_cooldown = 0
        
        if boss_type == "shadow_monarch":
            self.special_abilities = ["shadow_army", "darkness_aura"]
        elif boss_type == "ice_queen":
            self.special_abilities = ["ice_spikes", "freeze"]
        elif boss_type == "flame_lord":
            self.special_abilities = ["fire_breath", "meteor"]
    
    def update(self, delta_time, player, world):
        """Update boss AI with special abilities."""
        super().update(delta_time, player, world)
        
        # Update ability cooldown
        if self.ability_cooldown > 0:
            self.ability_cooldown -= delta_time
        
        # Use special abilities
        if self.target and self.ability_cooldown <= 0:
            self.use_special_ability()
    
    def use_special_ability(self):
        """Use a random special ability."""
        if self.special_abilities:
            ability = np.random.choice(self.special_abilities)
            print(f"{self.entity_type} uses {ability}!")
            
            # Implement ability effects here
            if ability == "shadow_army":
                # Spawn shadow minions
                pass
            elif ability == "ice_spikes":
                # Create ice projectiles
                pass
            elif ability == "fire_breath":
                # Area damage
                pass
            
            self.ability_cooldown = 10.0  # 10 second cooldown
