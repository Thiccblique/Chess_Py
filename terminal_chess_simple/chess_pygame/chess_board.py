# ChessBoard.py - Handles board state and game logic (like a GameManager in Unity)

from typing import List, Tuple, Optional
from enum import Enum

# Handle imports for both standalone and package execution
try:
    from .pieces import PieceFactory
except ImportError:
    from pieces import PieceFactory

class PieceType(Enum):
    PAWN = 'p'
    ROOK = 'r'
    KNIGHT = 'n'
    BISHOP = 'b'
    QUEEN = 'q'
    KING = 'k'

class ChessBoard:
    def __init__(self):
        self.Reset()
    
    def Reset(self):
        """Initialize the board to starting position"""
        self.board = [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]
        ]
        self.current_turn_white = True
    
    # ===== BOARD QUERIES =====
    
    def GetPiece(self, row: int, col: int) -> str:
        """Get piece at position"""
        if self.IsValidPosition(row, col):
            return self.board[row][col]
        return "."
    
    def SetPiece(self, row: int, col: int, piece: str):
        """Set piece at position"""
        if self.IsValidPosition(row, col):
            self.board[row][col] = piece
    
    def IsValidPosition(self, row: int, col: int) -> bool:
        """Check if coordinates are within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def IsEmpty(self, row: int, col: int) -> bool:
        """Check if square is empty"""
        return self.GetPiece(row, col) == "."
    
    def IsWhitePiece(self, piece: str) -> bool:
        """Check if piece belongs to white player"""
        return piece.isupper() and piece != "."
    
    def IsBlackPiece(self, piece: str) -> bool:
        """Check if piece belongs to black player"""
        return piece.islower() and piece != "."
    
    def IsEnemyPiece(self, piece: str, target: str) -> bool:
        """Check if target is an enemy piece"""
        if target == ".":
            return False
        return piece.isupper() != target.isupper()
    
    def CanPlayerMovePiece(self, row: int, col: int) -> bool:
        """Check if current player can move this piece"""
        piece = self.GetPiece(row, col)
        if piece == ".":
            return False
        return self.IsWhitePiece(piece) == self.current_turn_white
    
    # ===== MOVE VALIDATION =====
    
    def GetLegalMoves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all legal moves for piece at position"""
        piece_char = self.GetPiece(row, col)
        if piece_char == ".":
            return []
        
        try:
            piece = PieceFactory.create_piece(piece_char)
            return piece.get_moves(row, col, self)
        except ValueError:
            return []
    

    
    # ===== GAME ACTIONS =====
    
    def TryMakeMove(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Attempt to make a move, returns success"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Validate basic conditions
        if not self.CanPlayerMovePiece(from_row, from_col):
            return False
        
        # Check if move is legal
        legal_moves = self.GetLegalMoves(from_row, from_col)
        if to_pos not in legal_moves:
            return False
        
        # Execute move
        piece = self.GetPiece(from_row, from_col)
        self.SetPiece(to_row, to_col, piece)
        self.SetPiece(from_row, from_col, ".")
        
        # Handle special cases
        promoted = self._HandlePawnPromotion(to_row, to_col)
        
        # Switch turns
        self.current_turn_white = not self.current_turn_white
        
        return True
    
    def _HandlePawnPromotion(self, row: int, col: int) -> bool:
        """Handle pawn promotion to queen"""
        piece = self.GetPiece(row, col)
        
        if piece.lower() == 'p':
            if (self.IsWhitePiece(piece) and row == 0) or (self.IsBlackPiece(piece) and row == 7):
                new_piece = 'Q' if self.IsWhitePiece(piece) else 'q'
                self.SetPiece(row, col, new_piece)
                return True
        
        return False
    
    # ===== GAME STATE =====
    
    def GetCurrentPlayer(self) -> str:
        """Get current player name"""
        return "White" if self.current_turn_white else "Black"
    
    def IsWhiteTurn(self) -> bool:
        """Check if it's white's turn"""
        return self.current_turn_white