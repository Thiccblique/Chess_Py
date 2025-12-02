# Step 3: Basic Piece Movement
# Implement simple piece movement with basic validation

# Board setup
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
    """Display the chess board"""
    print("\n    a b c d e f g h")
    print("  +----------------+")
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank} |", " ".join(row), "|")
    print("  +----------------+")

def coord_to_index(s):
    """Convert chess notation to array indices"""
    file = ord(s[0].lower()) - ord('a')
    rank = int(s[1])
    row = 8 - rank
    col = file
    if 0 <= row < 8 and 0 <= col < 8:
        return row, col
    raise ValueError("Invalid coordinate")

# BASIC MOVEMENT FUNCTIONS
def is_empty(r, c):
    """Check if a square is empty"""
    return board[r][c] == '.'

def is_white_piece(piece):
    """Check if piece belongs to white (uppercase)"""
    return piece.isupper()

def can_move_pawn(from_r, from_c, to_r, to_c):
    """Basic pawn movement rules (forward only, no captures yet)"""
    piece = board[from_r][from_c]
    if piece.lower() != 'p':
        return False
    
    is_white = piece.isupper()
    
    # Pawns move \"forward\" - white up the board (decreasing row), black down (increasing row)
    if is_white:
        direction = -1  # White pawns move up (row decreases)
        start_row = 6   # White pawns start at row 6
    else:
        direction = 1   # Black pawns move down (row increases)
        start_row = 1   # Black pawns start at row 1
    
    # Must move in same column
    if from_c != to_c:
        return False
    
    # One square forward
    if to_r == from_r + direction:
        return is_empty(to_r, to_c)
    
    # Two squares forward from starting position
    if from_r == start_row and to_r == from_r + 2 * direction:
        return is_empty(to_r, to_c) and is_empty(from_r + direction, from_c)
    
    return False

def make_move(from_square, to_square):
    """Attempt to move a piece"""
    try:
        from_r, from_c = coord_to_index(from_square)
        to_r, to_c = coord_to_index(to_square)
    except ValueError as e:
        return False, f"Invalid coordinates: {e}"
    
    piece = board[from_r][from_c]
    if piece == '.':
        return False, "No piece at starting square"
    
    # For now, only implement pawn movement
    if piece.lower() == 'p':
        if can_move_pawn(from_r, from_c, to_r, to_c):
            # Make the move
            board[to_r][to_c] = piece
            board[from_r][from_c] = '.'
            return True, f"Moved {piece} from {from_square} to {to_square}"
        else:
            return False, "Invalid pawn move"
    else:
        return False, f"Movement for {piece} not implemented yet"

def main():
    """Simple chess game with basic pawn movement"""
    print("Welcome to Step 3: Basic Chess Movement!")
    print("Only pawn movement is implemented in this step.")
    print("Try moving pawns forward 1 or 2 squares.")
    print("Examples: e2 e3, e2 e4, d7 d5")
    
    while True:
        print_board()
        
        user_input = input("\\nEnter move (like 'e2 e4') or 'quit': ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thanks for playing!")
            break
        
        try:
            parts = user_input.split()
            if len(parts) != 2:
                print("Please enter move as 'from_square to_square' (e.g., e2 e4)")
                continue
            
            from_square, to_square = parts
            success, message = make_move(from_square, to_square)
            print(message)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()