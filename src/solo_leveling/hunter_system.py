"""
Solo Leveling Hunter System
Implements the hunter ranking, shadow soldiers, and abilities
"""

import numpy as np
from ..core.config import *

class HunterRank:
    """Hunter rank system from Solo Leveling."""
    
    def __init__(self, rank="E"):
        """Initialize hunter rank."""
        self.rank = rank
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Rank multipliers
        self.rank_multipliers = {
            "E": 1.0,
            "D": 1.5,
            "C": 2.0,
            "B": 3.0,
            "A": 5.0,
            "S": 10.0
        }
    
    def get_multiplier(self):
        """Get the current rank multiplier."""
        return self.rank_multipliers.get(self.rank, 1.0)
    
    def add_experience(self, amount):
        """Add experience points."""
        self.experience += amount
        
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the hunter."""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        
        # Check for rank up
        if self.can_rank_up():
            self.rank_up()
        
        print(f"Level up! Now level {self.level}")
    
    def can_rank_up(self):
        """Check if hunter can rank up."""
        rank_thresholds = {
            "E": 10,
            "D": 25,
            "C": 50,
            "B": 100,
            "A": 200
        }
        
        threshold = rank_thresholds.get(self.rank, float('inf'))
        return self.level >= threshold and self.rank != "S"
    
    def rank_up(self):
        """Rank up the hunter."""
        current_index = HUNTER_RANKS.index(self.rank)
        if current_index < len(HUNTER_RANKS) - 1:
            self.rank = HUNTER_RANKS[current_index + 1]
            print(f"Rank up! Now {self.rank}-rank hunter!")


class ShadowSoldier:
    """Shadow soldier from Solo Leveling."""
    
    def __init__(self, name, soldier_type, level=1):
        """Initialize a shadow soldier."""
        self.name = name
        self.type = soldier_type  # "ant", "wolf", "knight", etc.
        self.level = level
        self.health = 100 * level
        self.max_health = self.health
        self.attack_power = 20 * level
        self.position = np.array([0.0, 0.0, 0.0])
        self.is_active = False
        self.experience = 0
    
    def level_up(self):
        """Level up the shadow soldier."""
        self.level += 1
        old_max_health = self.max_health
        self.max_health = 100 * self.level
        self.health += (self.max_health - old_max_health)  # Heal on level up
        self.attack_power = 20 * self.level
        print(f"{self.name} leveled up to {self.level}!")
    
    def add_experience(self, amount):
        """Add experience to shadow soldier."""
        self.experience += amount
        exp_needed = self.level * 50
        
        if self.experience >= exp_needed:
            self.experience -= exp_needed
            self.level_up()


class Ability:
    """Hunter ability system."""
    
    def __init__(self, name, mana_cost, cooldown, description):
        """Initialize an ability."""
        self.name = name
        self.mana_cost = mana_cost
        self.cooldown = cooldown
        self.description = description
        self.current_cooldown = 0
        self.level = 1
    
    def can_use(self, player_mana):
        """Check if ability can be used."""
        return self.current_cooldown <= 0 and player_mana >= self.mana_cost
    
    def use(self):
        """Use the ability."""
        if self.current_cooldown <= 0:
            self.current_cooldown = self.cooldown
            return True
        return False
    
    def update(self, delta_time):
        """Update ability cooldown."""
        if self.current_cooldown > 0:
            self.current_cooldown -= delta_time


class HunterSystem:
    """Main hunter system managing all Solo Leveling features."""
    
    def __init__(self):
        """Initialize the hunter system."""
        self.rank = HunterRank("E")
        self.shadow_soldiers = []
        self.max_shadow_soldiers = 5  # Starts low, increases with rank
        
        # Abilities
        self.abilities = {
            "shadow_extraction": Ability("Shadow Extraction", 30, 10.0, 
                                       "Extract shadows from defeated enemies"),
            "shadow_exchange": Ability("Shadow Exchange", 20, 5.0,
                                     "Teleport through shadows"),
            "shadow_army": Ability("Shadow Army", 50, 30.0,
                                 "Summon all shadow soldiers"),
            "stealth": Ability("Stealth", 25, 15.0,
                             "Become invisible for a short time")
        }
        
        # Stats
        self.stats = {
            "strength": 10,
            "agility": 10,
            "intelligence": 10,
            "vitality": 10,
            "sense": 10
        }
        
        # Available stat points
        self.stat_points = 0
    
    def update(self, delta_time, player):
        """Update hunter system."""
        # Update ability cooldowns
        for ability in self.abilities.values():
            ability.update(delta_time)
        
        # Update shadow soldiers
        for soldier in self.shadow_soldiers:
            if soldier.is_active:
                # Simple AI: follow player
                direction = player.position - soldier.position
                if np.linalg.norm(direction) > 3.0:  # Too far, teleport closer
                    soldier.position = player.position + np.random.uniform(-2, 2, 3)
                    soldier.position[1] = player.position[1]  # Same height
    
    def extract_shadow(self, enemy_type, enemy_level):
        """Extract a shadow from a defeated enemy."""
        if len(self.shadow_soldiers) >= self.max_shadow_soldiers:
            print("Shadow army is full! Dismiss a soldier first.")
            return False
        
        if not self.abilities["shadow_extraction"].can_use(50):  # Assume player has 50+ mana
            print("Not enough mana or ability on cooldown!")
            return False
        
        # Create shadow soldier
        soldier_name = f"Shadow {enemy_type.title()} #{len(self.shadow_soldiers) + 1}"
        shadow = ShadowSoldier(soldier_name, enemy_type, enemy_level)
        self.shadow_soldiers.append(shadow)
        
        self.abilities["shadow_extraction"].use()
        print(f"Successfully extracted {soldier_name}!")
        return True
    
    def summon_shadow(self, index):
        """Summon a specific shadow soldier."""
        if 0 <= index < len(self.shadow_soldiers):
            self.shadow_soldiers[index].is_active = True
            print(f"Summoned {self.shadow_soldiers[index].name}!")
    
    def dismiss_shadow(self, index):
        """Dismiss a shadow soldier."""
        if 0 <= index < len(self.shadow_soldiers):
            self.shadow_soldiers[index].is_active = False
            print(f"Dismissed {self.shadow_soldiers[index].name}!")
    
    def summon_army(self):
        """Summon all shadow soldiers."""
        if not self.abilities["shadow_army"].can_use(100):  # High mana cost
            print("Not enough mana for Shadow Army!")
            return False
        
        for soldier in self.shadow_soldiers:
            soldier.is_active = True
        
        self.abilities["shadow_army"].use()
        print("Shadow Army summoned!")
        return True
    
    def gain_experience(self, amount):
        """Gain experience from actions."""
        self.rank.add_experience(amount)
        
        # Also give experience to active shadow soldiers
        active_soldiers = [s for s in self.shadow_soldiers if s.is_active]
        if active_soldiers:
            soldier_exp = amount // len(active_soldiers)
            for soldier in active_soldiers:
                soldier.add_experience(soldier_exp)
    
    def allocate_stat_point(self, stat_name):
        """Allocate a stat point."""
        if self.stat_points > 0 and stat_name in self.stats:
            self.stats[stat_name] += 1
            self.stat_points -= 1
            print(f"Increased {stat_name} to {self.stats[stat_name]}")
            return True
        return False
    
    def on_level_up(self):
        """Called when hunter levels up."""
        # Gain stat points
        self.stat_points += 3
        
        # Increase max shadow soldiers based on rank
        rank_multiplier = self.rank.get_multiplier()
        self.max_shadow_soldiers = min(MAX_SHADOW_SOLDIERS, int(5 * rank_multiplier))
    
    def get_total_attack_power(self):
        """Get total attack power including stats and rank."""
        base_attack = 10
        strength_bonus = self.stats["strength"] * 2
        rank_multiplier = self.rank.get_multiplier()
        return int((base_attack + strength_bonus) * rank_multiplier)
    
    def get_active_shadows_count(self):
        """Get number of active shadow soldiers."""
        return sum(1 for soldier in self.shadow_soldiers if soldier.is_active)
