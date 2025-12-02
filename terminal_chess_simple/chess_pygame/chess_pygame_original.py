# Pygame Chess - Graphical version of the terminal chess game
# Same game logic, beautiful graphical interface

import pygame
import sys
from typing import List, Tuple, Optional, Set

# Initialize Pygame
pygame.init()

# CONSTANTS
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BOARD_SIZE = 480
BOARD_OFFSET_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_OFFSET_Y = 50
SQUARE_SIZE = BOARD_SIZE // 8

# COLORS
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_MOVE = (50, 205, 50)      # Lime green for available moves
HIGHLIGHT_SELECT = (255, 255, 0)     # Yellow for selected piece
PIECE_WHITE = (255, 255, 255)        # Pure white for white pieces
PIECE_BLACK = (0, 0, 0)              # Pure black for black pieces
BG_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# GAME BOARD (same as terminal version)
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

class ChessGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pygame Chess")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.piece_font = pygame.font.Font(None, 48)
        
        # Game state
        self.turn_white = True
        self.selected_piece = None  # (row, col) of selected piece
        self.highlighted_moves = set()  # Set of (row, col) for valid moves
        self.running = True
        
    def screen_to_board(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Convert screen coordinates to board position"""
        board_x = x - BOARD_OFFSET_X
        board_y = y - BOARD_OFFSET_Y
        
        if 0 <= board_x < BOARD_SIZE and 0 <= board_y < BOARD_SIZE:
            col = board_x // SQUARE_SIZE
            row = board_y // SQUARE_SIZE
            return (row, col)
        return None
    
    def board_to_screen(self, row: int, col: int) -> Tuple[int, int]:
        """Convert board position to screen coordinates"""
        x = BOARD_OFFSET_X + col * SQUARE_SIZE
        y = BOARD_OFFSET_Y + row * SQUARE_SIZE
        return (x, y)
    
    def draw_board(self):
        """Draw the chess board with squares"""
        for row in range(8):
            for col in range(8):
                # Determine square color
                color = WHITE if (row + col) % 2 == 0 else BLACK
                
                # Highlight selected square
                if self.selected_piece == (row, col):
                    color = HIGHLIGHT_SELECT
                # Highlight available moves
                elif (row, col) in self.highlighted_moves:
                    color = HIGHLIGHT_MOVE
                
                x, y = self.board_to_screen(row, col)
                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw border
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)
    
    def draw_pieces(self):
        """Draw chess pieces on the board"""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != '.':
                    x, y = self.board_to_screen(row, col)
                    
                    # Choose color and outline based on piece
                    if piece.isupper():  # White pieces
                        piece_color = PIECE_WHITE
                        outline_color = PIECE_BLACK
                    else:  # Black pieces
                        piece_color = PIECE_BLACK
                        outline_color = PIECE_WHITE
                    
                    # Draw outline (slightly offset in multiple directions)
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            outline_surface = self.piece_font.render(piece, True, outline_color)
                            outline_rect = outline_surface.get_rect()
                            outline_rect.center = (x + SQUARE_SIZE // 2 + dx, y + SQUARE_SIZE // 2 + dy)
                            self.screen.blit(outline_surface, outline_rect)
                    
                    # Draw main piece on top
                    piece_surface = self.piece_font.render(piece, True, piece_color)
                    piece_rect = piece_surface.get_rect()
                    piece_rect.center = (x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2)
                    self.screen.blit(piece_surface, piece_rect)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Current player
        player = "White" if self.turn_white else "Black"
        player_text = self.font.render(f"Current Player: {player}", True, TEXT_COLOR)
        self.screen.blit(player_text, (10, 10))
        
        # Instructions
        instructions = [
            "Click a piece to select it",
            "Click a highlighted square to move",
            "ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font.render(instruction, True, TEXT_COLOR)
            self.screen.blit(text, (10, WINDOW_HEIGHT - 80 + i * 25))
        
        # File and rank labels
        files = "abcdefgh"
        ranks = "87654321"
        
        # File labels (bottom)
        for col in range(8):
            x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = BOARD_OFFSET_Y + BOARD_SIZE + 10
            text = self.font.render(files[col], True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # Rank labels (left side)
        for row in range(8):
            x = BOARD_OFFSET_X - 20
            y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2
            text = self.font.render(ranks[row], True, TEXT_COLOR)
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
    
    # ===== GAME LOGIC (Same as terminal version) =====
    
    def inside(self, r: int, c: int) -> bool:
        """Check if coordinates are within board"""
        return 0 <= r < 8 and 0 <= c < 8
    
    def is_enemy(self, piece: str, target: str) -> bool:
        """Check if target is an enemy piece"""
        if target == ".":
            return False
        return piece.isupper() != target.isupper()
    
    def legal_moves_from(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Generate all legal moves for piece at (r,c) - same logic as terminal version"""
        piece = board[r][c]
        if piece == ".":
            return []
        
        moves = []
        white = piece.isupper()
        p = piece.lower()
        
        # PAWN MOVEMENT
        if p == 'p':
            step = -1 if white else 1
            
            # Forward movement
            if self.inside(r+step, c) and board[r+step][c] == ".":
                moves.append((r+step, c))
                
                # Double move from start
                start_row = 6 if white else 1
                if r == start_row and board[r+2*step][c] == ".":
                    moves.append((r+2*step, c))
            
            # Captures
            for dc in (-1, 1):
                nr, nc = r+step, c+dc
                if self.inside(nr, nc) and board[nr][nc] != "." and self.is_enemy(piece, board[nr][nc]):
                    moves.append((nr, nc))
        
        # KNIGHT MOVEMENT
        elif p == 'n':
            knight_moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
            for dr, dc in knight_moves:
                nr, nc = r+dr, c+dc
                if self.inside(nr, nc):
                    target = board[nr][nc]
                    if target == '.' or self.is_enemy(piece, target):
                        moves.append((nr, nc))
        
        # SLIDING PIECES (Rook, Bishop, Queen)
        elif p in 'brq':
            dirs = []
            if p in 'bq':  # Bishop/Queen diagonals
                dirs += [(-1,-1),(-1,1),(1,-1),(1,1)]
            if p in 'rq':  # Rook/Queen straight lines
                dirs += [(-1,0),(1,0),(0,-1),(0,1)]
            
            for dr, dc in dirs:
                nr, nc = r+dr, c+dc
                while self.inside(nr, nc):
                    if board[nr][nc] == ".":
                        moves.append((nr, nc))
                    else:
                        if self.is_enemy(piece, board[nr][nc]):
                            moves.append((nr, nc))
                        break
                    nr += dr
                    nc += dc
        
        # KING MOVEMENT
        elif p == 'k':
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r+dr, c+dc
                    if self.inside(nr, nc):
                        target = board[nr][nc]
                        if target == '.' or self.is_enemy(piece, target):
                            moves.append((nr, nc))
        
        return moves
    
    def promote_if_needed(self, r: int, c: int):
        """Handle pawn promotion"""
        piece = board[r][c]
        if piece.lower() == 'p':
            if (piece.isupper() and r == 0) or (piece.islower() and r == 7):
                board[r][c] = 'Q' if piece.isupper() else 'q'
                return True
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Attempt to make a move"""
        r1, c1 = from_pos
        r2, c2 = to_pos
        
        piece = board[r1][c1]
        if piece == '.':
            return False
        
        # Check if it's the right player's turn
        if piece.isupper() != self.turn_white:
            return False
        
        # Check if move is legal
        legal_moves = self.legal_moves_from(r1, c1)
        if (r2, c2) not in legal_moves:
            return False
        
        # Make the move
        board[r2][c2] = piece
        board[r1][c1] = '.'
        
        # Handle promotion
        if self.promote_if_needed(r2, c2):
            print(f"Pawn promoted to Queen!")
        
        # Switch turns
        self.turn_white = not self.turn_white
        self.selected_piece = None
        self.highlighted_moves.clear()
        
        return True
    
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse click on board"""
        board_pos = self.screen_to_board(pos[0], pos[1])
        if board_pos is None:
            return
        
        row, col = board_pos
        
        # If no piece selected, try to select one
        if self.selected_piece is None:
            piece = board[row][col]
            if piece != '.' and piece.isupper() == self.turn_white:
                self.selected_piece = (row, col)
                self.highlighted_moves = set(self.legal_moves_from(row, col))
        
        # If piece is selected, try to move
        else:
            if (row, col) in self.highlighted_moves:
                # Valid move
                self.make_move(self.selected_piece, (row, col))
            elif board[row][col] != '.' and board[row][col].isupper() == self.turn_white:
                # Select different piece
                self.selected_piece = (row, col)
                self.highlighted_moves = set(self.legal_moves_from(row, col))
            else:
                # Invalid move, deselect
                self.selected_piece = None
                self.highlighted_moves.clear()
    
    def run(self):
        """Main game loop"""
        print("Game loop starting...")
        try:
            while self.running:
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Quit event received")
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("Escape key pressed")
                            self.running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left click
                            self.handle_click(event.pos)
                
                # Draw everything
                self.screen.fill(BG_COLOR)
                self.draw_board()
                self.draw_pieces()
                self.draw_ui()
                
                pygame.display.flip()
                self.clock.tick(60)
                
        except Exception as e:
            print(f"Error in game loop: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("Closing pygame...")
            pygame.quit()
            # Don't call sys.exit() to allow the program to continue

def main():
    """Start the Pygame chess game"""
    print("Starting Pygame Chess...")
    print("Click pieces to select them, click highlighted squares to move!")
    
    try:
        game = ChessGame()
        game.run()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()