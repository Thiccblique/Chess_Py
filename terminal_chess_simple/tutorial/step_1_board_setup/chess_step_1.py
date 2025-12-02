# Step 1: Basic Board Setup
# Learn how to represent and display a chess board

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

# DISPLAY FUNCTION
def print_board():
    """Display the chess board in a user-friendly format with coordinates"""
    print("\n    a b c d e f g h")  # Column labels (files)
    print("  +----------------+")
    for i, row in enumerate(board):
        rank = 8 - i  # Convert array index to chess rank (8,7,6...1)
        print(f"{rank} |", " ".join(row), "|")  # Row with rank number
    print("  +----------------+")

def main():
    """Simple demonstration of the board display"""
    print("Welcome to Step 1: Basic Chess Board!")
    print("This shows how we represent and display a chess board.")
    
    print_board()
    
    print("\nKey Concepts:")
    print("- Board is stored as a 2D list (list of lists)")
    print("- Each piece is represented by a letter")
    print("- Uppercase = White pieces, Lowercase = Black pieces")
    print("- '.' represents empty squares")
    print("- Array indices [0-7] map to chess ranks [8-1]")

if __name__ == '__main__':
    main()