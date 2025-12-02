# Step 2: Coordinate System

## What You'll Learn
- Convert between chess notation (like "e4") and array indices
- Handle user input for chess squares
- Understand the relationship between chess coordinates and programming arrays

## Key Concepts

### Chess Notation
Chess uses algebraic notation to identify squares:
- **Files (columns)**: Letters a-h (left to right)
- **Ranks (rows)**: Numbers 1-8 (bottom to top for white)

### Conversion Formulas

**Chess to Array:**
```python
file = ord(square[0].lower()) - ord('a')  # 'a'=0, 'b'=1, ..., 'h'=7
rank = int(square[1])                     # 1, 2, ..., 8
row = 8 - rank                            # rank 8→row 0, rank 1→row 7
col = file                                # direct mapping
```

**Array to Chess:**
```python
file_letter = chr(ord('a') + col)         # 0→'a', 1→'b', ..., 7→'h'
rank_number = 8 - row                     # row 0→rank 8, row 7→rank 1
square = f"{file_letter}{rank_number}"    # combine them
```

### Why This Mapping?
- Chess boards are displayed with rank 1 at bottom (white's side)
- Arrays typically start at index 0 for the "top"
- So we flip: chess rank 8 becomes array row 0

### Examples
| Chess Square | Array Position | Explanation |
|--------------|----------------|-------------|
| a1           | [7][0]        | Bottom-left corner |
| h1           | [7][7]        | Bottom-right corner |
| a8           | [0][0]        | Top-left corner |
| h8           | [0][7]        | Top-right corner |
| e4           | [4][4]        | Center-ish square |

## Running This Step
```bash
python chess_step_2.py
```

The program will:
1. Show coordinate conversion examples
2. Let you enter chess squares interactively
3. Display the corresponding array position and piece

## Next Step
Step 3 will implement basic piece movement using these coordinates.