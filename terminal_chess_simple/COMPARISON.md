# Chess Game Comparison: Terminal vs Pygame

This project includes **both** terminal and graphical versions of the same chess game, perfect for comparing different user interface approaches!

## 🎮 Quick Start

### Option 1: Use the Launcher
```bash
python launcher.py
```
Choose between terminal or pygame version from the menu.

### Option 2: Run Directly
```bash
# Terminal version
python main.py

# Pygame version  
python chess_pygame.py
```

## 📊 Version Comparison

| Feature | Terminal Version | Pygame Version |
|---------|------------------|----------------|
| **Interface** | Text-based, terminal | Graphical window |
| **Piece Selection** | Type letter (p, n, r...) | Click on piece |
| **Move Input** | Type coordinates (e2 e4) | Click destination |
| **Visual Feedback** | Colored text + green highlights | Yellow selection + green highlights |
| **Portability** | Works anywhere Python runs | Requires pygame library |
| **Performance** | Instant | Smooth 60fps |
| **Learning Value** | Shows text UI concepts | Shows game development concepts |

## 🖥️ Terminal Version Features

### What Makes It Special:
- **🎨 Color Coding**: Red pieces = White, Blue pieces = Black
- **💚 Move Highlighting**: Green dots show available moves
- **📝 Smart Input**: Multiple input formats supported
- **🔤 Piece Selection**: Type `p` to see all pawns, `n` for knights, etc.
- **📚 Educational**: Extensively commented for learning

### Usage Examples:
```
White move: p                    # Show all pawns
Select piece number (1-8): 5     # Pick pawn #5
Enter destination square: e4     # Move to e4

# OR traditional notation:
White move: e2 e4               # Direct move notation
```

## 🎮 Pygame Version Features

### What Makes It Special:
- **🖼️ Visual Board**: Beautiful graphical chess board
- **🖱️ Mouse Control**: Click to select and move pieces
- **✨ Smooth Highlighting**: Visual feedback for selections and moves
- **📏 Coordinate Labels**: Files (a-h) and ranks (1-8) displayed
- **⌨️ Keyboard Support**: ESC to quit

### How to Play:
1. **Click** a piece to select it (yellow highlight)
2. **See** available moves highlighted in green  
3. **Click** a green square to move there
4. **ESC** to quit the game

## 🔧 Technical Details

### Shared Game Logic
Both versions use **identical** chess logic:
- Same `board` representation (2D array)
- Same `legal_moves_from()` function
- Same piece movement rules
- Same validation system

### Different Interface Layers
- **Terminal**: Text-based I/O with colored output
- **Pygame**: Event-driven GUI with graphics

### Code Organization
```
terminal_chess_simple/
├── main.py              # Terminal version
├── chess_pygame.py      # Pygame version  
├── launcher.py          # Choose version menu
├── README.md           # Main documentation
├── COMPARISON.md       # This comparison (you are here)
└── tutorial/           # Step-by-step learning
```

## 🎓 Educational Value

### For Learning Programming:
- **Terminal Version**: Text processing, input parsing, console output
- **Pygame Version**: Game loops, event handling, graphics rendering
- **Both**: Object-oriented design, game logic, state management

### For Teaching Chess:
- **Visual Learning**: See moves highlighted before making them
- **Interactive**: Immediate feedback on piece selection
- **Experimental**: Easy to try different moves and see results

## 🔄 Converting Between Versions

### What Transfers Directly:
- All chess movement logic
- Board representation
- Piece validation
- Game state management

### What Changes:
- **Input Method**: Text → Mouse clicks
- **Display Method**: Terminal colors → Graphics
- **Game Loop**: Input prompts → Event handling

## 🚀 Next Steps

### Possible Enhancements:
1. **Sound Effects**: Add move/capture sounds to Pygame version
2. **Animations**: Smooth piece movement animations
3. **AI Opponent**: Add computer player to both versions
4. **Network Play**: Multiplayer over internet
5. **Move History**: Track and display game notation
6. **Save/Load**: Persist games to disk

### Learning Projects:
1. **Add Features**: Implement castling, en passant
2. **Different Graphics**: Try different piece designs
3. **Mobile Version**: Adapt for touch interfaces
4. **3D Version**: Create 3D chess board
5. **Analysis Mode**: Add move suggestion features

---

**Perfect for**: Students learning programming, chess enthusiasts, developers interested in game development, anyone wanting to understand UI design differences!