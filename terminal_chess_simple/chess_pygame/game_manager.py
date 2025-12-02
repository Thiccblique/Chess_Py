# GameManager.py - Main game logic controller (like a GameManager in Unity)

from typing import Tuple, Set, Optional

# Handle imports for both standalone and package execution
try:
    from .chess_board import ChessBoard
    from .chess_renderer import ChessRenderer
    from .input_manager import InputManager, InputEvents
except ImportError:
    from chess_board import ChessBoard
    from chess_renderer import ChessRenderer
    from input_manager import InputManager, InputEvents

class GameState:
    """Game state constants"""
    PLAYING = "playing"
    GAME_OVER = "game_over"
    PAUSED = "paused"

class GameManager:
    def __init__(self, chess_board: ChessBoard, renderer: ChessRenderer, input_manager: InputManager):
        self.chess_board = chess_board
        self.renderer = renderer
        self.input_manager = input_manager
        
        # Game state
        self.game_state = GameState.PLAYING
        self.selected_piece_pos: Optional[Tuple[int, int]] = None
        self.highlighted_moves: Set[Tuple[int, int]] = set()
        
        # Register input handlers
        self._RegisterInputHandlers()
    
    # ===== INITIALIZATION =====
    
    def _RegisterInputHandlers(self):
        """Set up input event handlers"""
        self.input_manager.RegisterHandler(InputEvents.QUIT, self._OnQuit)
        self.input_manager.RegisterHandler(InputEvents.ESCAPE, self._OnEscape)
        self.input_manager.RegisterHandler(InputEvents.MOUSE_CLICK, self._OnMouseClick)
    
    # ===== GAME LOOP METHODS =====
    
    def Update(self):
        """Main game update - called every frame"""
        if self.game_state == GameState.PLAYING:
            self._UpdateGameplay()
    
    def _UpdateGameplay(self):
        """Update gameplay logic"""
        # Game logic updates would go here
        # For chess, most logic is event-driven, so this can be minimal
        pass
    
    def Render(self):
        """Render the current game state"""
        self.renderer.DrawBackground()
        
        if self.game_state == GameState.PLAYING:
            self._RenderGameplay()
        
        self.renderer.RefreshDisplay()
    
    def _RenderGameplay(self):
        """Render gameplay elements"""
        current_player = self.chess_board.GetCurrentPlayer()
        
        self.renderer.DrawBoard(self.selected_piece_pos or (-1, -1), self.highlighted_moves)
        self.renderer.DrawPieces(self.chess_board)
        self.renderer.DrawUI(current_player)
    
    # ===== INPUT HANDLERS =====
    
    def _OnQuit(self):
        """Handle quit event"""
        print("Quit requested")
        self.game_state = GameState.GAME_OVER
    
    def _OnEscape(self):
        """Handle escape key"""
        print("Escape pressed - quitting game")
        self.game_state = GameState.GAME_OVER
    
    def _OnMouseClick(self, mouse_pos: Tuple[int, int]):
        """Handle mouse click"""
        if self.game_state != GameState.PLAYING:
            return
        
        # Convert screen coordinates to board position
        board_pos = self.renderer.ScreenToBoard(mouse_pos[0], mouse_pos[1])
        if not self.renderer.IsValidBoardPosition(board_pos[0], board_pos[1]):
            return
        
        self._HandleBoardClick(board_pos)
    
    def _HandleBoardClick(self, board_pos: Tuple[int, int]):
        """Handle click on board square"""
        row, col = board_pos
        
        # If no piece is selected, try to select one
        if self.selected_piece_pos is None:
            self._TrySelectPiece(row, col)
        else:
            # A piece is already selected
            self._TryMoveOrReselect(row, col)
    
    def _TrySelectPiece(self, row: int, col: int):
        """Try to select a piece at the given position"""
        if self.chess_board.CanPlayerMovePiece(row, col):
            self.selected_piece_pos = (row, col)
            self.highlighted_moves = set(self.chess_board.GetLegalMoves(row, col))
            print(f"Selected piece at {chr(ord('a')+col)}{8-row}")
        else:
            self._ClearSelection()
    
    def _TryMoveOrReselect(self, row: int, col: int):
        """Try to move selected piece or select a different piece"""
        # Check if clicking on a valid move
        if (row, col) in self.highlighted_moves:
            self._ExecuteMove(row, col)
        # Check if clicking on another piece of the same color
        elif self.chess_board.CanPlayerMovePiece(row, col):
            self._TrySelectPiece(row, col)  # Reselect different piece
        else:
            # Invalid move or empty square - clear selection
            self._ClearSelection()
    
    def _ExecuteMove(self, to_row: int, to_col: int):
        """Execute the move from selected piece to target position"""
        if self.selected_piece_pos is None:
            return
        
        from_row, from_col = self.selected_piece_pos
        
        # Attempt the move
        move_successful = self.chess_board.TryMakeMove(self.selected_piece_pos, (to_row, to_col))
        
        if move_successful:
            # Move notation for feedback
            from_notation = f"{chr(ord('a')+from_col)}{8-from_row}"
            to_notation = f"{chr(ord('a')+to_col)}{8-to_row}"
            current_player = "White" if not self.chess_board.IsWhiteTurn() else "Black"  # Player who just moved
            print(f"{current_player} moved: {from_notation} -> {to_notation}")
            
            # Check for pawn promotion (would have been handled in chess_board)
            piece = self.chess_board.GetPiece(to_row, to_col)
            if piece.lower() == 'q' and ((piece.isupper() and to_row == 0) or (piece.islower() and to_row == 7)):
                print("Pawn promoted to Queen!")
        
        self._ClearSelection()
    
    def _ClearSelection(self):
        """Clear current selection and highlights"""
        self.selected_piece_pos = None
        self.highlighted_moves.clear()
    
    # ===== GAME STATE QUERIES =====
    
    def IsRunning(self) -> bool:
        """Check if game should continue running"""
        return self.game_state != GameState.GAME_OVER and not self.input_manager.ShouldQuit()
    
    def GetCurrentPlayer(self) -> str:
        """Get current player name"""
        return self.chess_board.GetCurrentPlayer()
    
    # ===== GAME CONTROLS =====
    
    def ResetGame(self):
        """Reset the game to initial state"""
        self.chess_board.Reset()
        self._ClearSelection()
        self.game_state = GameState.PLAYING
        print("Game reset!")
    
    def PauseGame(self):
        """Pause the game"""
        self.game_state = GameState.PAUSED
    
    def ResumeGame(self):
        """Resume the game"""
        self.game_state = GameState.PLAYING