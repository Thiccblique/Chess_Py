# pieces.py - Individual piece movement logic

from typing import List, Tuple
from abc import ABC, abstractmethod

class ChessPiece(ABC):
    """Abstract base class for all chess pieces
    
    This class defines the common interface and helper methods that all chess pieces share.
    Each specific piece (pawn, rook, knight, etc.) inherits from this class and implements
    its own movement logic in the get_moves() method.
    """
    
    def __init__(self, is_white: bool):
        """Initialize a chess piece
        
        Args:
            is_white: True if this piece belongs to the white player, False for black
        """
        self.is_white = is_white
    
    @abstractmethod
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        """Get all possible moves for this piece at given position
        
        This is the main method that each piece type must implement.
        It should return a list of valid destination squares (row, col) that
        the piece can move to from its current position.
        
        Args:
            row: Current row position (0-7)
            col: Current column position (0-7) 
            board: The chess board object to check piece positions
            
        Returns:
            List of (row, col) tuples representing valid moves
        """
        pass
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if coordinates are within the 8x8 chess board bounds
        
        Chess boards are 8x8, so valid positions are 0-7 for both row and column.
        This prevents pieces from trying to move off the edge of the board.
        """
        return 0 <= row < 8 and 0 <= col < 8
    
    def _is_empty(self, row: int, col: int, board) -> bool:
        """Check if a square contains no piece
        
        Empty squares are represented by "." on the board.
        Pieces can move to empty squares freely (unless blocked by other rules).
        """
        return board.GetPiece(row, col) == "."
    
    def _is_enemy_piece(self, row: int, col: int, board) -> bool:
        """Check if target square contains an opponent's piece
        
        This determines if a piece can capture at the target square.
        White pieces are uppercase (P, R, N, B, Q, K) and black pieces are lowercase (p, r, n, b, q, k).
        A piece can capture any enemy piece but cannot capture its own pieces.
        
        Args:
            row: Target row to check
            col: Target column to check
            board: Chess board to check
            
        Returns:
            True if target contains an enemy piece that can be captured
        """
        target = board.GetPiece(row, col)
        # Empty squares don't contain enemy pieces
        if target == ".":
            return False
        # Check if the target piece belongs to the opposite color
        target_is_white = target.isupper()
        return self.is_white != target_is_white


class Pawn(ChessPiece):
    """Pawn piece movement logic
    
    Pawns have the most complex movement rules in chess:
    1. Move forward one square (cannot capture this way)
    2. Move forward two squares from starting position (cannot capture this way)
    3. Capture diagonally forward one square
    4. Cannot move backwards
    
    Note: En passant capture is not implemented in this basic version
    """
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        moves = []
        # White pawns move "up" the board (decreasing row numbers)
        # Black pawns move "down" the board (increasing row numbers)
        direction = -1 if self.is_white else 1
        # Starting positions: white pawns start on row 6, black pawns on row 1
        start_row = 6 if self.is_white else 1
        
        # === FORWARD MOVEMENT (no capture) ===
        # Pawns can only move forward, never backward or sideways
        new_row = row + direction
        if self._is_valid_position(new_row, col) and self._is_empty(new_row, col, board):
            moves.append((new_row, col))
            
            # === DOUBLE MOVE FROM STARTING POSITION ===
            # If pawn is on its starting square and the square two spaces ahead is also empty,
            # it can move two squares forward in one turn
            if row == start_row and self._is_empty(new_row + direction, col, board):
                moves.append((new_row + direction, col))
        
        # === DIAGONAL CAPTURES ===
        # Pawns capture by moving diagonally forward (unlike their normal movement)
        # They can only capture on diagonal squares, not move to empty diagonal squares
        for dc in [-1, 1]:  # Check both left and right diagonals
            new_col = col + dc
            if (self._is_valid_position(new_row, new_col) and 
                not self._is_empty(new_row, new_col, board) and 
                self._is_enemy_piece(new_row, new_col, board)):
                moves.append((new_row, new_col))
        
        return moves


class Rook(ChessPiece):
    """Rook piece movement logic
    
    Rooks move in straight lines along ranks (rows) and files (columns).
    They can move any number of squares horizontally or vertically,
    but cannot jump over other pieces.
    """
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        # Rook moves in four cardinal directions: up, down, left, right
        # (-1,0) = up one row, (1,0) = down one row
        # (0,-1) = left one column, (0,1) = right one column
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_sliding_moves(row, col, board, directions)
    
    def _get_sliding_moves(self, row: int, col: int, board, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Helper method for sliding piece movement
        
        Sliding pieces move in straight lines until blocked by another piece or board edge.
        They can capture enemy pieces but cannot jump over any piece.
        """
        moves = []
        
        # Check each direction the piece can slide
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Keep sliding until we hit something or go off the board
            while self._is_valid_position(new_row, new_col):
                if self._is_empty(new_row, new_col, board):
                    # Empty square - can move here and continue
                    moves.append((new_row, new_col))
                else:
                    # Found a piece - can we capture it?
                    if self._is_enemy_piece(new_row, new_col, board):
                        moves.append((new_row, new_col))
                    break  # Cannot slide past any piece
                
                new_row += dr
                new_col += dc
        
        return moves


class Knight(ChessPiece):
    """Knight piece movement logic
    
    Knights move in an L-shape: 2 squares in one direction and 1 square perpendicular.
    This is the only piece that can "jump over" other pieces.
    Knights have exactly 8 possible moves from any position (fewer near board edges).
    """
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        moves = []
        # All possible L-shaped moves for a knight
        # Format: (row_change, col_change)
        # (2,1) means: move 2 squares down and 1 square right
        # (2,-1) means: move 2 squares down and 1 square left
        # (-2,1) means: move 2 squares up and 1 square right
        # etc.
        knight_offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        # Check each possible L-shaped move
        for dr, dc in knight_offsets:
            new_row, new_col = row + dr, col + dc
            # Make sure the destination is on the board
            if self._is_valid_position(new_row, new_col):
                # Knights can move to empty squares or capture enemy pieces
                # (but not capture their own pieces)
                if (self._is_empty(new_row, new_col, board) or 
                    self._is_enemy_piece(new_row, new_col, board)):
                    moves.append((new_row, new_col))
        
        return moves


class Bishop(ChessPiece):
    """Bishop piece movement logic
    
    Bishops move diagonally any number of squares.
    They cannot jump over other pieces and are confined to squares of one color
    (each player starts with one light-square bishop and one dark-square bishop).
    """
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        # Bishop moves in four diagonal directions
        # (-1,-1) = up-left, (-1,1) = up-right
        # (1,-1) = down-left, (1,1) = down-right
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._get_sliding_moves(row, col, board, directions)
    
    def _get_sliding_moves(self, row: int, col: int, board, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Helper method for sliding piece movement along diagonals
        
        Bishops slide diagonally until blocked. They can capture enemy pieces
        but cannot jump over any piece.
        """
        moves = []
        
        # Check each diagonal direction
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Keep sliding diagonally until blocked or off-board
            while self._is_valid_position(new_row, new_col):
                if self._is_empty(new_row, new_col, board):
                    # Empty square - can move here and continue
                    moves.append((new_row, new_col))
                else:
                    # Found a piece - can we capture it?
                    if self._is_enemy_piece(new_row, new_col, board):
                        moves.append((new_row, new_col))
                    break  # Cannot slide past any piece
                
                new_row += dr
                new_col += dc
        
        return moves


class Queen(ChessPiece):
    """Queen piece movement logic
    
    The Queen is the most powerful piece, combining the movement of both
    Rook and Bishop. She can move any number of squares horizontally,
    vertically, or diagonally, but cannot jump over other pieces.
    """
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        # Queen combines rook movement (horizontal/vertical) and bishop movement (diagonal)
        # First 4 directions are rook-like: up, down, left, right
        # Last 4 directions are bishop-like: up-left, up-right, down-left, down-right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._get_sliding_moves(row, col, board, directions)
    
    def _get_sliding_moves(self, row: int, col: int, board, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Helper method for Queen's combined sliding movement
        
        Queens can slide in all 8 directions (like combining rook + bishop).
        They are blocked by any piece but can capture enemies.
        """
        moves = []
        
        # Check all 8 directions the queen can move
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Keep sliding until blocked or off-board
            while self._is_valid_position(new_row, new_col):
                if self._is_empty(new_row, new_col, board):
                    # Empty square - can move here and continue
                    moves.append((new_row, new_col))
                else:
                    # Found a piece - can we capture it?
                    if self._is_enemy_piece(new_row, new_col, board):
                        moves.append((new_row, new_col))
                    break  # Cannot slide past any piece
                
                new_row += dr
                new_col += dc
        
        return moves


class King(ChessPiece):
    """King piece movement logic
    
    The King is the most important piece but also the most restricted.
    He can move only one square in any direction (horizontal, vertical, or diagonal).
    The King cannot move into check (a square attacked by an enemy piece).
    
    Note: This basic implementation doesn't check for check/checkmate or castling.
    """
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        moves = []
        
        # Check all 8 adjacent squares (3x3 grid minus the center square)
        for dr in [-1, 0, 1]:  # Row offsets: up, same, down
            for dc in [-1, 0, 1]:  # Column offsets: left, same, right
                # Skip the center square (king's current position)
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                # Make sure the destination is on the board
                if self._is_valid_position(new_row, new_col):
                    # King can move to empty squares or capture enemy pieces
                    # (but cannot capture his own pieces)
                    if (self._is_empty(new_row, new_col, board) or 
                        self._is_enemy_piece(new_row, new_col, board)):
                        moves.append((new_row, new_col))
        
        return moves


class PieceFactory:
    """Factory for creating piece instances using the Factory design pattern
    
    This class centralizes the creation of chess piece objects based on the
    character representation used on the chess board. It eliminates the need
    for complex if/elif chains in the main game logic.
    
    Board representation:
    - Uppercase letters = White pieces (P, R, N, B, Q, K)
    - Lowercase letters = Black pieces (p, r, n, b, q, k)
    - '.' = Empty square
    """
    
    @staticmethod
    def create_piece(piece_char: str) -> ChessPiece:
        """Create a piece instance from its board character representation
        
        This method converts a single character from the chess board into
        the appropriate piece object with correct color.
        
        Args:
            piece_char: Single character representing the piece (e.g., 'P', 'p', 'R', 'r')
            
        Returns:
            ChessPiece: The appropriate piece object (Pawn, Rook, Knight, etc.)
            
        Raises:
            ValueError: If the piece character is not recognized
            
        Examples:
            create_piece('P') -> White Pawn
            create_piece('r') -> Black Rook
            create_piece('Q') -> White Queen
        """
        # Determine piece color: uppercase = white, lowercase = black
        is_white = piece_char.isupper()
        # Get piece type by converting to lowercase
        piece_type = piece_char.lower()
        
        # Map piece characters to their corresponding classes
        piece_map = {
            'p': Pawn,     # Pawn
            'r': Rook,     # Rook (castle)
            'n': Knight,   # Knight (horse)
            'b': Bishop,   # Bishop
            'q': Queen,    # Queen
            'k': King      # King
        }
        
        # Create and return the appropriate piece object
        if piece_type in piece_map:
            return piece_map[piece_type](is_white)
        else:
            raise ValueError(f"Unknown piece type: {piece_char}")