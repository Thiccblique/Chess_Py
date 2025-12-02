# pieces.py - Individual piece movement logic

from typing import List, Tuple
from abc import ABC, abstractmethod

class ChessPiece(ABC):
    """Abstract base class for all chess pieces"""
    
    def __init__(self, is_white: bool):
        self.is_white = is_white
    
    @abstractmethod
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        """Get all possible moves for this piece at given position"""
        pass
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if coordinates are within board bounds"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def _is_empty(self, row: int, col: int, board) -> bool:
        """Check if square is empty"""
        return board.GetPiece(row, col) == "."
    
    def _is_enemy_piece(self, row: int, col: int, board) -> bool:
        """Check if target square contains an enemy piece"""
        target = board.GetPiece(row, col)
        if target == ".":
            return False
        target_is_white = target.isupper()
        return self.is_white != target_is_white


class Pawn(ChessPiece):
    """Pawn piece movement logic"""
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        moves = []
        direction = -1 if self.is_white else 1
        start_row = 6 if self.is_white else 1
        
        # Forward movement
        new_row = row + direction
        if self._is_valid_position(new_row, col) and self._is_empty(new_row, col, board):
            moves.append((new_row, col))
            
            # Double move from starting position
            if row == start_row and self._is_empty(new_row + direction, col, board):
                moves.append((new_row + direction, col))
        
        # Diagonal captures
        for dc in [-1, 1]:
            new_col = col + dc
            if (self._is_valid_position(new_row, new_col) and 
                not self._is_empty(new_row, new_col, board) and 
                self._is_enemy_piece(new_row, new_col, board)):
                moves.append((new_row, new_col))
        
        return moves


class Rook(ChessPiece):
    """Rook piece movement logic"""
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return self._get_sliding_moves(row, col, board, directions)
    
    def _get_sliding_moves(self, row: int, col: int, board, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        moves = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            while self._is_valid_position(new_row, new_col):
                if self._is_empty(new_row, new_col, board):
                    moves.append((new_row, new_col))
                else:
                    if self._is_enemy_piece(new_row, new_col, board):
                        moves.append((new_row, new_col))
                    break  # Can't move past any piece
                
                new_row += dr
                new_col += dc
        
        return moves


class Knight(ChessPiece):
    """Knight piece movement logic"""
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        moves = []
        knight_offsets = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        
        for dr, dc in knight_offsets:
            new_row, new_col = row + dr, col + dc
            if self._is_valid_position(new_row, new_col):
                if (self._is_empty(new_row, new_col, board) or 
                    self._is_enemy_piece(new_row, new_col, board)):
                    moves.append((new_row, new_col))
        
        return moves


class Bishop(ChessPiece):
    """Bishop piece movement logic"""
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._get_sliding_moves(row, col, board, directions)
    
    def _get_sliding_moves(self, row: int, col: int, board, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        moves = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            while self._is_valid_position(new_row, new_col):
                if self._is_empty(new_row, new_col, board):
                    moves.append((new_row, new_col))
                else:
                    if self._is_enemy_piece(new_row, new_col, board):
                        moves.append((new_row, new_col))
                    break  # Can't move past any piece
                
                new_row += dr
                new_col += dc
        
        return moves


class Queen(ChessPiece):
    """Queen piece movement logic"""
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        return self._get_sliding_moves(row, col, board, directions)
    
    def _get_sliding_moves(self, row: int, col: int, board, directions: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        moves = []
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            while self._is_valid_position(new_row, new_col):
                if self._is_empty(new_row, new_col, board):
                    moves.append((new_row, new_col))
                else:
                    if self._is_enemy_piece(new_row, new_col, board):
                        moves.append((new_row, new_col))
                    break  # Can't move past any piece
                
                new_row += dr
                new_col += dc
        
        return moves


class King(ChessPiece):
    """King piece movement logic"""
    
    def get_moves(self, row: int, col: int, board) -> List[Tuple[int, int]]:
        moves = []
        
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                if self._is_valid_position(new_row, new_col):
                    if (self._is_empty(new_row, new_col, board) or 
                        self._is_enemy_piece(new_row, new_col, board)):
                        moves.append((new_row, new_col))
        
        return moves


class PieceFactory:
    """Factory for creating piece instances"""
    
    @staticmethod
    def create_piece(piece_char: str) -> ChessPiece:
        """Create a piece instance from board character"""
        is_white = piece_char.isupper()
        piece_type = piece_char.lower()
        
        piece_map = {
            'p': Pawn,
            'r': Rook,
            'n': Knight,
            'b': Bishop,
            'q': Queen,
            'k': King
        }
        
        if piece_type in piece_map:
            return piece_map[piece_type](is_white)
        else:
            raise ValueError(f"Unknown piece type: {piece_char}")