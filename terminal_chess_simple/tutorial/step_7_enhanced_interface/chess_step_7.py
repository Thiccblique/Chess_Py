
# Simple terminal chess (minimal rules)
# Designed for teaching - readable and easy to extend.
# Limitations: no castling, no en-passant, simple pawn promotion to Queen, no check/checkmate detection.

# GAME BOARD REPRESENTATION
# The chess board is a 2D list (8x8 grid)
# - Lowercase letters = Black pieces (r=rook, n=knight, b=bishop, q=queen, k=king, p=pawn)
# - Uppercase letters = White pieces (R=rook, N=knight, B=bishop, Q=queen, K=king, P=pawn)
# - "." = Empty square
# Row 0 = Rank 8 (top of board), Row 7 = Rank 1 (bottom of board)
board = [
    ["r","n","b","q","k","b","n","r"],  # Black back rank (rank 8)
    ["p","p","p","p","p","p","p","p"],  # Black pawns (rank 7)
    [".",".",".",".",".",".",".","."],  # Empty rank 6
    [".",".",".",".",".",".",".","."],  # Empty rank 5
    [".",".",".",".",".",".",".","."],  # Empty rank 4
    [".",".",".",".",".",".",".","."],  # Empty rank 3
    ["P","P","P","P","P","P","P","P"],  # White pawns (rank 2)
    ["R","N","B","Q","K","B","N","R"]   # White back rank (rank 1)
]

# DISPLAY FUNCTIONS
def print_board():
    """Display the chess board in a user-friendly format with coordinates"""
    print("\n    a b c d e f g h")  # Column labels (files)
    print("  +----------------+")
    for i,row in enumerate(board):
        rank = 8 - i  # Convert array index to chess rank (8,7,6...1)
        print(f"{rank} |", " ".join(row), "|")  # Row with rank number
    print("  +----------------+")

# COORDINATE CONVERSION FUNCTIONS
def coord_to_index(s):
    """Convert chess notation (like 'e4') to array indices (row, col)
    
    Chess uses files (a-h) for columns and ranks (1-8) for rows
    Our array uses 0-7 for both, with row 0 = rank 8
    """
    # s is like 'e2'
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

def path_clear(r1,c1,r2,c2):
    """Check if path between two squares is clear (for sliding pieces)
    
    Used by rooks, bishops, and queens to ensure no pieces block their path
    Calculates direction and checks each square along the way
    """
    dr = 1 if r2>r1 else -1 if r2<r1 else 0  # Row direction (-1, 0, or 1)
    dc = 1 if c2>c1 else -1 if c2<c1 else 0  # Column direction (-1, 0, or 1)
    r,c = r1+dr, c1+dc  # Start from first square after starting position
    while (r,c) != (r2,c2):  # Check each square until destination
        if board[r][c] != ".":
            return False  # Path blocked by piece
        r += dr; c += dc
    return True  # Path is clear

# MOVE GENERATION AND VALIDATION
def legal_moves_from(r,c):
    """Generate all legal moves for a piece at position (r,c)
    
    This is the core function that implements chess movement rules for each piece type.
    Returns a list of (row, col) tuples representing valid destination squares.
    """
    piece = board[r][c]
    if piece == ".": return []  # No piece at this position
    
    moves = []
    white = piece.isupper()  # Determine piece color
    p = piece.lower()        # Get piece type (normalized to lowercase)
    
    # PAWN MOVEMENT RULES
    if p == 'p':
        # Pawns move "forward" - up the board for white (-1 row), down for black (+1 row)
        step = -1 if white else 1
        
        # Forward movement (one square)
        if inside(r+step,c) and board[r+step][c] == ".":
            moves.append((r+step,c))
            
            # Double move from starting position
            start_row = 6 if white else 1  # White pawns start row 6, black pawns start row 1
            if r == start_row and board[r+2*step][c] == ".":
                moves.append((r+2*step,c))
        
        # Diagonal captures (pawns capture diagonally)
        for dc in (-1,1):  # Check both diagonal directions
            nr, nc = r+step, c+dc
            if inside(nr,nc) and board[nr][nc] != "." and is_enemy(piece, board[nr][nc]):
                moves.append((nr,nc))
        return moves
    
    # KNIGHT MOVEMENT RULES
    if p == 'n':
        # Knights move in an "L" shape: 2 squares in one direction, 1 in perpendicular
        knight_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for dr,dc in knight_moves:
            nr, nc = r+dr, c+dc
            if inside(nr,nc):  # Check if destination is on board
                target = board[nr][nc]
                # Knights can move to empty squares or capture enemy pieces
                if target=='.' or is_enemy(piece, target):
                    moves.append((nr,nc))
        return moves
    
    # SLIDING PIECE MOVEMENT (Rook, Bishop, Queen)
    if p == 'b' or p == 'r' or p == 'q':
        dirs = []  # Directions this piece can move
        
        # Bishops and Queens move diagonally
        if p in ('b','q'):
            dirs += [(-1,-1),(-1,1),(1,-1),(1,1)]  # All four diagonal directions
        
        # Rooks and Queens move horizontally/vertically  
        if p in ('r','q'):
            dirs += [(-1,0),(1,0),(0,-1),(0,1)]    # All four straight directions
        
        # For each direction, slide until hitting edge, piece, or enemy
        for dr,dc in dirs:
            nr, nc = r+dr, c+dc
            while inside(nr,nc):  # Keep moving in this direction
                if board[nr][nc] == ".":
                    moves.append((nr,nc))  # Empty square - can move here
                else:
                    if is_enemy(piece, board[nr][nc]):
                        moves.append((nr,nc))  # Enemy piece - can capture
                    break  # Stop sliding (hit any piece)
                nr += dr; nc += dc
        return moves
    
    # KING MOVEMENT RULES
    if p == 'k':
        # King moves one square in any direction (8 possible moves)
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr==0 and dc==0: continue  # Skip staying in same position
                nr, nc = r+dr, c+dc
                if inside(nr,nc):
                    target = board[nr][nc]
                    # King can move to empty squares or capture enemies
                    if target=='.' or is_enemy(piece, target):
                        moves.append((nr,nc))
        return moves
    
    return moves  # Unknown piece type

# HELPER FUNCTIONS
def inside(r,c):
    """Check if row,col coordinates are within the 8x8 board"""
    return 0 <= r < 8 and 0 <= c < 8

def is_white(piece):
    """Check if a piece belongs to white (uppercase = white, lowercase = black)"""
    return piece.isupper()

def is_enemy(piece, target):
    """Check if target square contains an enemy piece
    
    Two pieces are enemies if one is uppercase (white) and other is lowercase (black)
    Empty squares ('.') are not enemies
    """
    if target == ".": return False
    return piece.isupper() != target.isupper()

# PIECE SELECTION FUNCTIONS
def find_pieces_by_type(piece_letter, is_white_turn):
    """Find all pieces of a specific type for the current player
    
    Args:
        piece_letter: 'p', 'r', 'n', 'b', 'q', or 'k'
        is_white_turn: True for white's turn, False for black's turn
    
    Returns:
        List of (row, col) positions containing that piece type
    """
    pieces = []
    # Choose uppercase for white, lowercase for black
    target_piece = piece_letter.upper() if is_white_turn else piece_letter.lower()
    
    # Search entire board for matching pieces
    for r in range(8):
        for c in range(8):
            if board[r][c] == target_piece:
                pieces.append((r, c))
    return pieces

def show_piece_moves(piece_positions):
    """Display all pieces of selected type and their available moves
    
    This function helps players see their options when they select a piece type
    Each piece is numbered so the player can choose which one to move
    """
    print("\nAvailable pieces and their moves:")
    for i, (r, c) in enumerate(piece_positions):
        coord = index_to_coord(r, c)  # Convert to chess notation
        moves = legal_moves_from(r, c)  # Get all legal moves
        move_coords = [index_to_coord(mr, mc) for mr, mc in moves]  # Convert moves to notation
        piece_symbol = board[r][c]
        move_list = ', '.join(move_coords) if move_coords else 'No legal moves'
        print(f"{i+1}. {piece_symbol} at {coord}: {move_list}")

# INPUT PARSING FUNCTIONS
def parse_move(s):
    """Parse user input into start and end coordinates
    
    Accepts formats like:
    - "e2 e4" (space separated)
    - "e2e4" (concatenated)
    - "e2-e4" (dash separated)
    """
    s = s.strip().lower().replace('-', ' ').replace(',', ' ')  # Normalize input
    parts = s.split()
    
    if len(parts) == 1 and len(parts[0]) == 4:
        # Format like "e2e4"
        start = parts[0][:2]; end = parts[0][2:]
    elif len(parts) >= 2:
        # Format like "e2 e4"
        start, end = parts[0], parts[1]
    else:
        raise ValueError("Can't parse move. Use e2 e4 or e2e4")
    return start, end

# GAME STATE MANAGEMENT
def promote_if_needed(r,c):
    """Handle pawn promotion when a pawn reaches the opposite end
    
    Automatically promotes to Queen (simplest rule for teaching)
    White pawns promote when reaching row 0 (rank 8)
    Black pawns promote when reaching row 7 (rank 1)
    """
    piece = board[r][c]
    if piece.lower() == 'p':  # Check if piece is a pawn
        # Check if pawn reached promotion rank
        if (piece.isupper() and r == 0) or (piece.islower() and r == 7):
            # Promote to queen (keep same color)
            board[r][c] = 'Q' if piece.isupper() else 'q'
            print(f"Pawn promoted to {'Queen' if piece.isupper() else 'queen'}!")

# MAIN GAME LOOP
def main():
    """Main game loop - handles player turns and input processing"""
    turn_white = True  # White moves first in chess
    
    while True:
        # Display current board state
        print_board()
        
        # Prompt current player for input
        player = "White" if turn_white else "Black"
        try:
            raw = input(f"{player} move (piece letter like 'p', e2 e4, or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
            
        # Handle quit commands
        if raw.lower() in ('quit','exit','q'):
            print("Goodbye.")
            break
        
        # PIECE SELECTION BY LETTER (New Feature)
        # Check if input is a single piece letter (p, r, n, b, q, k)
        if len(raw) == 1 and raw.lower() in 'prnbqk':
            piece_letter = raw.lower()
            
            # Find all pieces of that type for current player
            pieces = find_pieces_by_type(piece_letter, turn_white)
            if not pieces:
                print(f"No {piece_letter} pieces available for {player}.")
                continue
            
            # Show player their options
            show_piece_moves(pieces)
            
            try:
                choice = input(f"Select piece number (1-{len(pieces)}) or enter move: ").strip()
                
                # Player selected a piece by number
                if choice.isdigit():
                    piece_num = int(choice) - 1
                    if 0 <= piece_num < len(pieces):
                        r1, c1 = pieces[piece_num]
                        moves = legal_moves_from(r1, c1)
                        
                        if not moves:
                            print("Selected piece has no legal moves.")
                            continue
                        
                        # Show selected piece and its moves
                        print(f"Selected {board[r1][c1]} at {index_to_coord(r1, c1)}")
                        move_coords = [index_to_coord(mr, mc) for mr, mc in moves]
                        print(f"Legal moves: {', '.join(move_coords)}")
                        
                        # Get destination from player
                        dest = input("Enter destination square: ").strip().lower()
                        try:
                            r2, c2 = coord_to_index(dest)
                            if (r2, c2) not in moves:
                                print("Illegal destination.")
                                continue
                                
                            # Execute the move
                            board[r2][c2] = board[r1][c1]  # Move piece to destination
                            board[r1][c1] = "."             # Clear starting square
                            promote_if_needed(r2, c2)       # Handle pawn promotion
                            turn_white = not turn_white      # Switch turns
                            
                        except Exception as e:
                            print("Invalid destination:", e)
                            continue
                    else:
                        print("Invalid piece number.")
                        continue
                else:
                    # Player entered a move instead of selecting by number
                    raw = choice
            except (EOFError, KeyboardInterrupt):
                continue
        
        # TRADITIONAL MOVE INPUT (e2 e4 format)
        if len(raw) > 1:  # Process move if not handled by piece selection
            try:
                # Parse the move input
                start_s, end_s = parse_move(raw)
                r1,c1 = coord_to_index(start_s)  # Convert start square to indices
                r2,c2 = coord_to_index(end_s)    # Convert end square to indices
            except Exception as e:
                print("Invalid input:", e)
                continue
                
            # Validate the move
            piece = board[r1][c1]
            if piece == ".":
                print("No piece at start square.")
                continue
                
            # Check if player is moving their own piece
            if piece.isupper() != turn_white:
                print("That's not your piece to move.")
                continue
                
            # Check if move is legal for this piece
            possible = legal_moves_from(r1,c1)
            if (r2,c2) not in possible:
                print("Illegal move for that piece (or blocked).")
                continue
                
            # Execute the move
            board[r2][c2] = board[r1][c1]  # Move piece to destination
            board[r1][c1] = "."             # Clear starting square
            promote_if_needed(r2,c2)        # Handle pawn promotion
            turn_white = not turn_white      # Switch turns

# PROGRAM ENTRY POINT
if __name__ == '__main__':
    """Start the chess game when script is run directly"""
    print("Welcome to Simple Terminal Chess!")
    print("Features:")
    print("- Type piece letters (p/r/n/b/q/k) to see available pieces")
    print("- Or use traditional notation like 'e2 e4'")
    print("- Type 'quit' to exit")
    print("\nLet's play!")
    main()
