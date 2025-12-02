# Step 1: Basic Board Setup

## What You'll Learn
- How to represent a chess board in Python
- Display the board with proper chess coordinates
- Understand the piece representation system

## Key Concepts

### Board Representation
We use a 2D list (list of lists) to represent the 8x8 chess board:
```python
board = [
    ["r","n","b","q","k","b","n","r"],  # Row 0 = Rank 8
    ["p","p","p","p","p","p","p","p"],  # Row 1 = Rank 7
    # ... empty squares ...
    ["P","P","P","P","P","P","P","P"],  # Row 6 = Rank 2
    ["R","N","B","Q","K","B","N","R"]   # Row 7 = Rank 1
]
```

### Piece Encoding
- **Uppercase letters** = White pieces (P, R, N, B, Q, K)
- **Lowercase letters** = Black pieces (p, r, n, b, q, k)
- **Period (.)** = Empty square

### Chess Notation Mapping
- **Files (columns)**: a-h → Array indices 0-7
- **Ranks (rows)**: 1-8 → Array indices 7-0 (reversed!)

### Why Array Indices Are Reversed
In chess notation, rank 1 is at the bottom (where white pieces start), but in programming, index 0 is typically the "first" or "top" element. So we map:
- Chess rank 8 → Array row 0
- Chess rank 1 → Array row 7

## Running This Step
```bash
python chess_step_1.py
```

You'll see the chess board displayed with coordinates. Notice how the pieces are arranged in their starting positions.

## Next Step
Step 2 will teach you how to convert between chess notation (like "e4") and array coordinates.