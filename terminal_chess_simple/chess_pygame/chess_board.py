# ChessBoard.py - Handles board state and game logic (like a GameManager in Unity)

from typing import List, Tuple, Optional
from enum import Enum

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
        piece = self.GetPiece(row, col)
        if piece == ".":
            return []
        
        piece_type = piece.lower()
        
        if piece_type == 'p':
            return self._GetPawnMoves(row, col, piece)
        elif piece_type == 'n':
            return self._GetKnightMoves(row, col, piece)
        elif piece_type == 'r':
            return self._GetRookMoves(row, col, piece)
        elif piece_type == 'b':
            return self._GetBishopMoves(row, col, piece)
        elif piece_type == 'q':
            return self._GetQueenMoves(row, col, piece)
        elif piece_type == 'k':
            return self._GetKingMoves(row, col, piece)
        
        return []
    
    def _GetPawnMoves(self, row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        """Calculate pawn movement"""
        moves = []
        is_white = self.IsWhitePiece(piece)
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        # Forward movement
        new_row = row + direction
        if self.IsValidPosition(new_row, col) and self.IsEmpty(new_row, col):
            moves.append((new_row, col))
            
            # Double move from starting position
            if row == start_row and self.IsEmpty(new_row + direction, col):
                moves.append((new_row + direction, col))
        
        # Diagonal captures
        for dc in [-1, 1]:
            new_col = col + dc
            if self.IsValidPosition(new_row, new_col):
                target = self.GetPiece(new_row, new_col)
                if not self.IsEmpty(new_row, new_col) and self.IsEnemyPiece(piece, target):
                    moves.append((new_row, new_col))
        
        return moves
    
    def _GetKnightMoves(self, row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        """Calculate knight movement"""
        moves = []
        knight_offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        
        for dr, dc in knight_offsets:
            new_row, new_col = row + dr, col + dc
            if self.IsValidPosition(new_row, new_col):
                target = self.GetPiece(new_row, new_col)
                if self.IsEmpty(new_row, new_col) or self.IsEnemyPiece(piece, target):
                    moves.append((new_row, new_col))
        
        return moves
    
    def _GetRookMoves(self, row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        """Calculate rook movement"""
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        return self._GetSlidingMoves(row, col, piece, directions)
    
    def _GetBishopMoves(self, row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        """Calculate bishop movement"""
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        return self._GetSlidingMoves(row, col, piece, directions)
    
    def _GetQueenMoves(self, row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        """Calculate queen movement (combines rook and bishop)"""
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]
        return self._GetSlidingMoves(row, col, piece, directions)
    
    def _GetKingMoves(self, row: int, col: int, piece: str) -> List[Tuple[int, int]]:
        """Calculate king movement"""
        moves = []
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                if self.IsValidPosition(new_row, new_col):
                    target = self.GetPiece(new_row, new_col)
                    if self.IsEmpty(new_row, new_col) or self.IsEnemyPiece(piece, target):
                        moves.append((new_row, new_col))
        
        return moves
    
    def _GetSlidingMoves(self, row: int, col: int, piece: str, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Calculate sliding piece movement (rook, bishop, queen)"""
        moves = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            while self.IsValidPosition(new_row, new_col):
                target = self.GetPiece(new_row, new_col)
                
                if self.IsEmpty(new_row, new_col):
                    moves.append((new_row, new_col))
                else:
                    if self.IsEnemyPiece(piece, target):
                        moves.append((new_row, new_col))
                    break  # Can't move past any piece
                
                new_row += dr
                new_col += dc
        
        return moves
    
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