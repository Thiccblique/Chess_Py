# ChessRenderer.py - Handles all drawing and visual elements (like a UI Manager in Unity)

import pygame
from typing import Tuple, Set

# Handle imports for both standalone and package execution
try:
    from .chess_board import ChessBoard
except ImportError:
    from chess_board import ChessBoard

class GameColors:
    """Color constants organized in a class"""
    WHITE_SQUARE = (240, 217, 181)
    BLACK_SQUARE = (181, 136, 99)
    HIGHLIGHT_MOVE = (50, 205, 50)      # Green for available moves
    HIGHLIGHT_SELECT = (255, 255, 0)     # Yellow for selected piece
    PIECE_WHITE = (255, 255, 255)        # White pieces
    PIECE_BLACK = (0, 0, 0)              # Black pieces
    BACKGROUND = (50, 50, 50)
    TEXT = (255, 255, 255)

class DisplaySettings:
    """Display constants organized in a class"""
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 600
    BOARD_SIZE = 480
    BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
    BOARD_OFFSET_Y = 50
    SQUARE_SIZE = BOARD_SIZE // 8

class ChessRenderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.piece_font = pygame.font.Font(None, 48)
    
    # ===== COORDINATE CONVERSION =====
    
    def ScreenToBoard(self, screen_x: int, screen_y: int) -> Tuple[int, int]:
        """Convert screen coordinates to board position"""
        board_x = screen_x - DisplaySettings.BOARD_OFFSET_X
        board_y = screen_y - DisplaySettings.BOARD_OFFSET_Y
        
        if 0 <= board_x < DisplaySettings.BOARD_SIZE and 0 <= board_y < DisplaySettings.BOARD_SIZE:
            col = board_x // DisplaySettings.SQUARE_SIZE
            row = board_y // DisplaySettings.SQUARE_SIZE
            return (row, col)
        return (-1, -1)  # Invalid position
    
    def BoardToScreen(self, row: int, col: int) -> Tuple[int, int]:
        """Convert board position to screen coordinates"""
        x = DisplaySettings.BOARD_OFFSET_X + col * DisplaySettings.SQUARE_SIZE
        y = DisplaySettings.BOARD_OFFSET_Y + row * DisplaySettings.SQUARE_SIZE
        return (x, y)
    
    def IsValidBoardPosition(self, row: int, col: int) -> bool:
        """Check if board position is valid"""
        return row != -1 and col != -1
    
    # ===== DRAWING METHODS =====
    
    def DrawBackground(self):
        """Clear screen with background color"""
        self.screen.fill(GameColors.BACKGROUND)
    
    def DrawBoard(self, selected_pos: Tuple[int, int], highlighted_moves: Set[Tuple[int, int]]):
        """Draw the chess board with highlights"""
        for row in range(8):
            for col in range(8):
                # Determine base square color
                is_light_square = (row + col) % 2 == 0
                color = GameColors.WHITE_SQUARE if is_light_square else GameColors.BLACK_SQUARE
                
                # Apply highlights
                if (row, col) == selected_pos:
                    color = GameColors.HIGHLIGHT_SELECT
                elif (row, col) in highlighted_moves:
                    color = GameColors.HIGHLIGHT_MOVE
                
                # Draw square
                x, y = self.BoardToScreen(row, col)
                square_rect = (x, y, DisplaySettings.SQUARE_SIZE, DisplaySettings.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, square_rect)
                
                # Draw border
                pygame.draw.rect(self.screen, (0, 0, 0), square_rect, 1)
    
    def DrawPieces(self, chess_board: ChessBoard):
        """Draw all chess pieces on the board"""
        for row in range(8):
            for col in range(8):
                piece = chess_board.GetPiece(row, col)
                if piece != '.':
                    self._DrawSinglePiece(row, col, piece)
    
    def _DrawSinglePiece(self, row: int, col: int, piece: str):
        """Draw a single chess piece with outline"""
        x, y = self.BoardToScreen(row, col)
        
        # Determine colors
        if piece.isupper():  # White pieces
            piece_color = GameColors.PIECE_WHITE
            outline_color = GameColors.PIECE_BLACK
        else:  # Black pieces
            piece_color = GameColors.PIECE_BLACK
            outline_color = GameColors.PIECE_WHITE
        
        # Draw outline (multiple offsets for thick outline)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                outline_surface = self.piece_font.render(piece, True, outline_color)
                outline_rect = outline_surface.get_rect()
                center_x = x + DisplaySettings.SQUARE_SIZE // 2 + dx
                center_y = y + DisplaySettings.SQUARE_SIZE // 2 + dy
                outline_rect.center = (center_x, center_y)
                self.screen.blit(outline_surface, outline_rect)
        
        # Draw main piece
        piece_surface = self.piece_font.render(piece, True, piece_color)
        piece_rect = piece_surface.get_rect()
        piece_rect.center = (x + DisplaySettings.SQUARE_SIZE // 2, y + DisplaySettings.SQUARE_SIZE // 2)
        self.screen.blit(piece_surface, piece_rect)
    
    def DrawUI(self, current_player: str):
        """Draw user interface elements"""
        self._DrawCurrentPlayer(current_player)
        self._DrawInstructions()
        self._DrawBoardLabels()
    
    def _DrawCurrentPlayer(self, current_player: str):
        """Draw current player indicator"""
        player_text = f"Current Player: {current_player}"
        text_surface = self.font.render(player_text, True, GameColors.TEXT)
        self.screen.blit(text_surface, (10, 10))
    
    def _DrawInstructions(self):
        """Draw game instructions"""
        instructions = [
            "Click a piece to select it",
            "Click a highlighted square to move",
            "ESC to quit"
        ]
        
        base_y = DisplaySettings.WINDOW_HEIGHT - 80
        for i, instruction in enumerate(instructions):
            text_surface = self.font.render(instruction, True, GameColors.TEXT)
            self.screen.blit(text_surface, (10, base_y + i * 25))
    
    def _DrawBoardLabels(self):
        """Draw file and rank labels around the board"""
        files = "abcdefgh"
        ranks = "87654321"
        
        # File labels (bottom of board)
        for col in range(8):
            x = DisplaySettings.BOARD_OFFSET_X + col * DisplaySettings.SQUARE_SIZE + DisplaySettings.SQUARE_SIZE // 2
            y = DisplaySettings.BOARD_OFFSET_Y + DisplaySettings.BOARD_SIZE + 10
            text_surface = self.font.render(files[col], True, GameColors.TEXT)
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
        
        # Rank labels (left side of board)
        for row in range(8):
            x = DisplaySettings.BOARD_OFFSET_X - 20
            y = DisplaySettings.BOARD_OFFSET_Y + row * DisplaySettings.SQUARE_SIZE + DisplaySettings.SQUARE_SIZE // 2
            text_surface = self.font.render(ranks[row], True, GameColors.TEXT)
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
    
    def RefreshDisplay(self):
        """Update the display"""
        pygame.display.flip()