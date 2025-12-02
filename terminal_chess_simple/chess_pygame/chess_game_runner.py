# ChessGameRunner.py - Main entry point and game runner (like a main Unity scene)

import pygame
import sys

# Handle imports for both standalone and package execution
try:
    from .chess_board import ChessBoard
    from .chess_renderer import ChessRenderer, DisplaySettings
    from .input_manager import InputManager
    from .game_manager import GameManager
except ImportError:
    from chess_board import ChessBoard
    from chess_renderer import ChessRenderer, DisplaySettings
    from input_manager import InputManager
    from game_manager import GameManager

class ChessGameRunner:
    def __init__(self):
        self._InitializePygame()
        self._CreateGameObjects()
        self._InitializeGame()
    
    # ===== INITIALIZATION =====
    
    def _InitializePygame(self):
        """Initialize pygame and create window"""
        pygame.init()
        self.screen = pygame.display.set_mode((DisplaySettings.WINDOW_WIDTH, DisplaySettings.WINDOW_HEIGHT))
        pygame.display.set_caption("Pygame Chess - Clean Architecture")
        self.clock = pygame.time.Clock()
        print("Pygame initialized successfully")
    
    def _CreateGameObjects(self):
        """Create and wire up all game objects"""
        # Create core systems
        self.chess_board = ChessBoard()
        self.renderer = ChessRenderer(self.screen)
        self.input_manager = InputManager()
        
        # Create game manager with dependencies
        self.game_manager = GameManager(self.chess_board, self.renderer, self.input_manager)
        
        print("Game objects created and wired up")
    
    def _InitializeGame(self):
        """Set up initial game state"""
        print("Chess game initialized - ready to play!")
        print("Click pieces to select them, click highlighted squares to move!")
    
    # ===== MAIN GAME LOOP =====
    
    def Run(self):
        """Main game loop - handles timing and core loop"""
        print("Starting main game loop...")
        
        try:
            while self.game_manager.IsRunning():
                self._ProcessFrame()
                self._LimitFrameRate()
            
        except Exception as e:
            print(f"Error in main game loop: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self._Cleanup()
    
    def _ProcessFrame(self):
        """Process a single frame"""
        # Process input events
        self.input_manager.ProcessEvents()
        
        # Update game logic
        self.game_manager.Update()
        
        # Render the frame
        self.game_manager.Render()
    
    def _LimitFrameRate(self):
        """Maintain consistent frame rate"""
        self.clock.tick(60)  # 60 FPS
    
    def _Cleanup(self):
        """Clean up resources when game ends"""
        print("Cleaning up and closing...")
        pygame.quit()
        # Note: Not calling sys.exit() to allow calling script to continue

# ===== MAIN ENTRY POINT =====

def main():
    """Main entry point for the chess game"""
    print("=" * 50)
    print("PYGAME CHESS - CLEAN ARCHITECTURE VERSION")
    print("=" * 50)
    
    try:
        game_runner = ChessGameRunner()
        game_runner.Run()
        
    except Exception as e:
        print(f"Failed to start game: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()