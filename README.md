# Solo Leveling VoxelCraft

> A 3D voxel-based Minecraft-style game featuring Solo Leveling characters, abilities, and world elements. Experience the power of the Shadow Monarch in a fully interactive block world!

## 🎮 Repository Name: `solo-leveling-voxelcraft`

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenGL](https://img.shields.io/badge/OpenGL-3.3+-green.svg)](https://www.opengl.org/)
[![Solo Leveling](https://img.shields.io/badge/Theme-Solo%20Leveling-purple.svg)](https://en.wikipedia.org/wiki/Solo_Leveling)
[![Status](https://img.shields.io/badge/Status-Beta-orange.svg)](https://github.com/user/solo-leveling-voxelcraft)

## 🌟 Features

### 🎯 Core Gameplay
- **🧊 3D Voxel World**: Infinite procedurally generated terrain using OpenSimplex noise
- **⛏️ Block Mining & Building**: Minecraft-style block interaction system
- **🎮 First-Person View**: Smooth 3D camera with mouse look and WASD movement
- **🔄 Chunk Loading**: Optimized world streaming around player position
- **💨 Physics**: Gravity, jumping, and collision detection

### 🗡️ Solo Leveling Elements
- **👤 Hunter System**: Character progression from E-Rank to S-Rank
- **👥 Shadow Soldiers**: Extract and command shadow minions (planned)
- **🚪 Gate Dungeons**: Randomly spawning dungeon portals in the world
- **💎 Special Blocks**:
  - **Shadow Stone** (Dark Purple) - Rare magical ore with shadow essence
  - **Gate Stone** (Purple) - Portal construction material
  - **Mana Crystal** (Magenta) - Energy source for abilities
- **⚔️ Abilities**: Special hunter powers and shadow manipulation (planned)

### 🎨 3D Graphics Engine
- **🔧 Modern OpenGL**: Shader-based rendering pipeline using ModernGL
- **💡 Dynamic Lighting**: Ambient and diffuse lighting with normal mapping
- **🎪 Face Culling**: Optimized rendering with backface culling
- **� Multi-Platform**: Cross-platform support via GLFW
- **⚡ Performance**: 60+ FPS with chunk-based optimization

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (3.13+ recommended)
- **Virtual Environment** (recommended)
- **Modern GPU** with OpenGL 3.3+ support

### 📦 Installation

1. **Clone the Repository**
```bash
git clone https://github.com/username/solo-leveling-voxelcraft.git
cd solo-leveling-voxelcraft
```

2. **Create Virtual Environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install pygame==2.6.1 PyOpenGL==3.1.7 PyOpenGL-accelerate==3.1.10 numpy==2.3.2 opensimplex moderngl==5.12.0 glfw==2.6.2 Pillow==11.3.0
```

### 🎮 Running the Game

**3D Version (Main Game):**
```bash
python main.py
```

**2.5D Fallback Version:**
```bash
python main_simple.py
```

## 🎯 Controls

### 🖱️ 3D Mode Controls
| Input | Action |
|-------|--------|
| **WASD** | Move (Forward/Left/Backward/Right) |
| **Mouse** | Look around (First-person camera) |
| **Space** | Jump |
| **Shift** | Sprint/Run faster |
| **Ctrl** | Sneak/Crouch |
| **Left Click** | Break/Mine blocks |
| **Right Click** | Place blocks |
| **1-9** | Select block type |
| **E** | Open inventory (planned) |
| **ESC** | Pause/Exit game |

### 🎮 2.5D Mode Controls  
| Input | Action |
|-------|--------|
| **WASD/Arrows** | Move player |
| **IJKL** | Move camera |
| **ESC** | Exit game |

## 🏗️ Project Structure

```
solo-leveling-voxelcraft/
├── 📁 src/
│   ├── 📁 core/           # Game engine core
│   │   ├── game.py        # Main game loop & OpenGL context
│   │   └── config.py      # Game configuration & constants
│   ├── 📁 graphics/       # 3D rendering system
│   │   ├── renderer.py    # OpenGL renderer & shaders
│   │   └── camera.py      # First-person 3D camera
│   ├── 📁 world/          # Voxel world generation
│   │   └── world.py       # Terrain generation & chunk loading
│   ├── 📁 player/         # Player character system
│   │   └── player.py      # Player movement & interaction
│   └── 📁 solo_leveling/  # Solo Leveling game mechanics
│       └── hunter_system.py # Hunter ranks, abilities, shadows
├── 📄 main.py             # 3D game launcher
├── 📄 main_simple.py      # 2.5D fallback launcher
├── 📄 requirements.txt    # Python dependencies
└── 📄 README.md          # This file
```

## 🔧 Technical Details

### 🎨 3D Graphics Pipeline
- **Rendering Engine**: ModernGL (Modern OpenGL wrapper)
- **Shaders**: GLSL vertex/fragment shaders for lighting
- **Vertex Format**: Position (3f) + Color (4f) + Normal (3f)
- **Culling**: Backface culling for performance
- **Depth Testing**: Z-buffer for proper depth sorting

### 🌍 World Generation
- **Algorithm**: OpenSimplex noise for natural terrain
- **Chunk Size**: 16x16x256 blocks per chunk
- **Loading**: Dynamic chunk loading/unloading around player
- **Render Distance**: 8 chunks (128 blocks) in each direction

### ⚡ Performance Optimization
- **Frame Rate**: Target 60 FPS with VSync
- **Chunk Limits**: Max 16 chunks rendered per frame
- **Memory Management**: Automatic cleanup of distant chunks
- **Vertex Buffers**: Efficient OpenGL buffer management

## 🗺️ Solo Leveling World Elements

### 💎 Special Block Types
| Block | Rarity | Description | Use |
|-------|--------|-------------|-----|
| **Shadow Stone** | Very Rare | Dark purple ore with shadow essence | Shadow soldier extraction |
| **Gate Stone** | Rare | Purple portal material | Dungeon gate construction |
| **Mana Crystal** | Uncommon | Magenta energy source | Ability charging |
| **Normal Ores** | Common | Coal, Iron, Gold, Diamond | Traditional crafting |

### 🚪 Gate Dungeons
- **Spawn Rate**: 0.1% chance per chunk
- **Structure**: 3x3 gate frame with portal
- **Difficulty**: Scales with player level
- **Rewards**: Shadow extraction opportunities

### 👤 Hunter Progression
```
E-Rank → D-Rank → C-Rank → B-Rank → A-Rank → S-Rank
```
- **Experience**: Gained through dungeon clearing
- **Abilities**: Unlock new shadow powers per rank
- **Stats**: Strength, Agility, Intelligence scaling

## 🐛 Troubleshooting

### Common Issues

**Game shows blue screen:**
- Check OpenGL support: Minimum OpenGL 3.3 required
- Update graphics drivers
- Try 2.5D fallback: `python main_simple.py`

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: Requires 3.8+

**Performance issues:**
- Reduce render distance in `config.py`
- Close other applications
- Check GPU usage in task manager

## 🛣️ Development Roadmap

### Phase 1: Core Systems ✅
- [x] 3D world generation
- [x] Player movement and camera
- [x] Block rendering with OpenGL
- [x] Chunk loading system

### Phase 2: Gameplay 🔄
- [ ] Block breaking and placing
- [ ] Inventory system
- [ ] Crafting mechanics
- [ ] Save/Load world data

### Phase 3: Solo Leveling Features 🔄
- [ ] Shadow soldier extraction
- [ ] Hunter ability system
- [ ] Gate dungeon instances
- [ ] Monster spawning and AI

### Phase 4: Polish 📋
- [ ] Texture system
- [ ] Audio and sound effects
- [ ] UI/HUD improvements
- [ ] Multiplayer foundation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Solo Leveling**: Original manhwa by Chugong
- **Minecraft**: Inspiration for voxel world mechanics
- **ModernGL**: Excellent Python OpenGL wrapper
- **OpenSimplex**: Noise generation library

---

**🎮 Ready to become the Shadow Monarch? Start your hunter journey today!**
