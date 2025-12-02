# Step 2: Coordinate System
# Learn how to convert between chess notation and array indices

# Board setup (same as Step 1)
board = [
    ["r","n","b","q","k","b","n","r"],
    ["p","p","p","p","p","p","p","p"],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    [".",".",".",".",".",".",".","."],
    ["P","P","P","P","P","P","P","P"],
    ["R","N","B","Q","K","B","N","R"]
]

def print_board():
    """Display the chess board in a user-friendly format with coordinates"""
    print("\n    a b c d e f g h")
    print("  +----------------+")
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank} |", " ".join(row), "|")
    print("  +----------------+")

# COORDINATE CONVERSION FUNCTIONS
def coord_to_index(s):
    """Convert chess notation (like 'e4') to array indices (row, col)
    
    Chess uses files (a-h) for columns and ranks (1-8) for rows
    Our array uses 0-7 for both, with row 0 = rank 8
    """
    # s is like 'e4'
    file = ord(s[0].lower()) - ord('a')  # Convert 'a'-'h' to 0-7
    rank = int(s[1])  # Get rank number 1-8
    row = 8 - rank   # Convert rank to array row (rank 8 = row 0)
    col = file       # File directly maps to column
    if 0 <= row < 8 and 0 <= col < 8:
        return row, col
    raise ValueError("Invalid coordinate")

def index_to_coord(r, c):
    """Convert array indices (row, col) back to chess notation like 'e4'"""
    file_letter = chr(ord('a') + c)  # Convert 0-7 to 'a'-'h'
    rank_number = 8 - r              # Convert row back to rank
    return f"{file_letter}{rank_number}"

def get_piece_at(square):
    """Get the piece at a chess square (like 'e4')"""
    try:
        row, col = coord_to_index(square)
        return board[row][col]
    except ValueError:
        return None

def main():
    """Interactive demonstration of coordinate conversion"""
    print("Welcome to Step 2: Chess Coordinate System!")
    print("Learn how to convert between chess notation and array indices.")
    
    print_board()
    
    print("\nCoordinate Conversion Examples:")
    
    # Show some examples
    examples = ['e4', 'a1', 'h8', 'd5']
    for square in examples:
        row, col = coord_to_index(square)
        piece = get_piece_at(square)
        back_to_square = index_to_coord(row, col)
        print(f"Square {square} → Array[{row}][{col}] → Piece: '{piece}' → Back to: {back_to_square}")
    
    print("\nTry it yourself!")
    while True:
        try:
            user_input = input("\nEnter a square (like e4) or 'quit' to exit: ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
                
            # Convert and display
            row, col = coord_to_index(user_input)
            piece = board[row][col]
            print(f"Square {user_input}:")
            print(f"  → Array position: [{row}][{col}]")
            print(f"  → Piece at that square: '{piece}'")
            if piece != '.':
                color = "White" if piece.isupper() else "Black"
                piece_name = {
                    'p': 'Pawn', 'r': 'Rook', 'n': 'Knight', 
                    'b': 'Bishop', 'q': 'Queen', 'k': 'King'
                }[piece.lower()]
                print(f"  → That's a {color} {piece_name}")
                
        except ValueError as e:
            print(f"Invalid square: {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()