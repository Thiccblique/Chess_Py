
# Simple Terminal Chess Game

A comprehensive educational chess game implementation designed for teaching programming concepts. This project demonstrates how to build a complete interactive application step by step.

## 🎯 Features

### Core Chess Gameplay
- ✅ Full piece movement rules (pawn, rook, knight, bishop, queen, king)
- ✅ Piece capture mechanics
- ✅ Turn-based gameplay
- ✅ Pawn promotion (automatic to Queen)
- ✅ Input validation and error handling

### Enhanced User Interface
- 🎮 **Piece Selection by Letter**: Type `p`, `r`, `n`, `b`, `q`, or `k` to see all pieces of that type
- 📋 **Interactive Move Selection**: Choose from numbered piece lists
- 🎯 **Move Preview**: See all legal moves for selected pieces
- 🔄 **Multiple Input Formats**: Support for `e2 e4`, `e2e4`, `e2-e4`

### Educational Features
- 📚 **Extensively Commented Code**: Every function and concept explained
- 🎓 **Step-by-Step Tutorial**: Learn by building the game progressively
- 🧩 **Modular Design**: Clean separation of concerns
- 📖 **Teaching-Friendly**: Perfect for classroom demonstrations

## 🚀 Quick Start

### Run the Complete Game
```bash
python main.py
```

### Try Different Input Methods
1. **Traditional notation**: `e2 e4`
2. **Piece selection**: Type `p` to see all pawns, then select by number
3. **Concatenated**: `e2e4`

## 📚 Tutorial Structure

Perfect for teaching programming step-by-step! Each tutorial step builds on the previous:

```
tutorial/
├── step_1_board_setup/         # Learn board representation
├── step_2_coordinates/         # Chess notation ↔ array indices
├── step_3_basic_movement/      # Simple pawn movement
├── step_4_all_pieces/          # Complete piece rules
├── step_5_captures_and_turns/  # Game mechanics
├── step_6_advanced_features/   # Pawn promotion, etc.
└── step_7_enhanced_interface/  # Final polished version
```

Each step includes:
- 🎯 **Runnable code** demonstrating concepts
- 📖 **Detailed README** explaining new features  
- 💪 **Practice exercises** to reinforce learning
- 🔧 **Teaching notes** for instructors

## 🎓 Educational Value

### Programming Concepts Demonstrated
- **Data Structures**: 2D arrays, lists, coordinate systems
- **Functions**: Modular design, parameter passing, return values
- **Control Flow**: Loops, conditionals, input validation
- **String Processing**: Parsing, format conversion
- **Error Handling**: Try/catch, user feedback
- **User Interface**: Interactive console applications

### Game Development Concepts
- **Game State Management**: Board representation, turn tracking
- **Rule Implementation**: Movement validation, game logic
- **Input Systems**: Multiple input formats, user experience
- **Code Organization**: Clean architecture, documentation

## 🎮 How to Play

### Basic Commands
- **Make a move**: `e2 e4` (from square to square)
- **Select piece type**: `p` (shows all pawns), `n` (knights), etc.
- **Quit game**: `quit`, `exit`, or `q`

### Example Gameplay
```
    a b c d e f g h
  +----------------+
8 | r n b q k b n r |
7 | p p p p p p p p |
6 | . . . . . . . . |
5 | . . . . . . . . |
4 | . . . . . . . . |
3 | . . . . . . . . |
2 | P P P P P P P P |
1 | R N B Q K B N R |
  +----------------+

White move (piece letter like 'p', e2 e4, or 'quit'): p

Available pieces and their moves:
1. P at a2: a3, a4
2. P at b2: b3, b4
3. P at c2: c3, c4
...

Select piece number (1-8) or enter move: 5
Selected P at e2
Legal moves: e3, e4
Enter destination square: e4
```

## 🔧 Code Structure

### Main Components
- **Board Representation**: 2D list with piece encoding
- **Coordinate System**: Chess notation ↔ array indices  
- **Move Generation**: Legal move calculation for each piece type
- **Input Processing**: Parse and validate user commands
- **Game Loop**: Turn management and user interaction

### Key Functions
- `print_board()`: Display the current game state
- `legal_moves_from(r,c)`: Calculate valid moves for any piece
- `find_pieces_by_type()`: Locate pieces for interactive selection
- `coord_to_index()`: Convert chess notation to array coordinates
- `main()`: Handle the game loop and user input

## 🚫 Current Limitations (By Design)

These limitations keep the code simple for educational purposes:
- No castling
- No en passant
- No check/checkmate detection  
- Automatic pawn promotion to Queen only
- No AI opponent

## 👨‍🎓 For Instructors

### Teaching Progression
1. **Start Simple**: Begin with Step 1 (board display)
2. **Build Incrementally**: Add one concept per lesson
3. **Hands-On Practice**: Students modify and extend each step
4. **Real Application**: End with a fully functional game

### Classroom Activities
- **Code Reading**: Analyze different sections together
- **Debugging**: Introduce intentional bugs to fix
- **Extensions**: Add features like move history, timers
- **Variations**: Create different board games using same concepts

### Assessment Ideas
- Implement missing piece movements
- Add new features (undo, save/load)
- Optimize performance
- Create graphical interface

## 📄 License

This project is designed for educational use. Feel free to use, modify, and distribute for learning purposes.

## 🤝 Contributing

Found a bug or have an educational improvement? Contributions are welcome! This project prioritizes code clarity and educational value over performance.

---

**Perfect for**: Computer Science courses, coding bootcamps, self-learners, and anyone wanting to understand how complex programs are built step by step.
