"""
UI.py - Handles user interface elements and player turn indicators  #NEW
This script contains:  #NEW
- Current player turn display  #NEW
- Game status indicators  #NEW
- Player name/color display  #NEW
- Turn transition animations  #NEW
- UI helper functions for text rendering  #NEW
"""

import pygame  #NEW

class GameUI:  #NEW
    def __init__(self, screen_width, screen_height):
        """
        Initialize the game UI system
        
        Args:
            screen_width (int): Width of the game screen
            screen_height (int): Height of the game screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Initialize fonts for different UI elements
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Colors for UI elements
        self.white_color = (255, 255, 255)
        self.black_color = (0, 0, 0)
        self.highlight_color = (255, 215, 0)  # Gold color for current player
        self.bg_color = (240, 240, 240)
        
        # UI panel dimensions
        self.ui_panel_height = 60
        self.ui_panel_rect = pygame.Rect(0, 0, screen_width, self.ui_panel_height)
        
        # Turn indicator position
        self.turn_indicator_pos = (screen_width // 2, 30)
        
    def draw_turn_indicator(self, screen, current_turn):
        """
        Draw the current player turn indicator at the top of the screen
        
        Args:
            screen: Pygame screen surface to draw on
            current_turn (str): Current player's turn ("white" or "black")
        """
        # Draw UI panel background
        pygame.draw.rect(screen, self.bg_color, self.ui_panel_rect)
        pygame.draw.rect(screen, self.black_color, self.ui_panel_rect, 2)
        
        # Create turn text
        turn_text = f"Current Turn: {current_turn.capitalize()}"
        
        # Choose text color based on current player
        text_color = self.black_color if current_turn == "white" else self.white_color
        bg_color = self.white_color if current_turn == "white" else self.black_color
        
        # Render text with background highlight
        text_surface = self.font_medium.render(turn_text, True, text_color)
        text_rect = text_surface.get_rect(center=self.turn_indicator_pos)
        
        # Draw highlighted background for current player
        highlight_rect = text_rect.inflate(20, 10)
        pygame.draw.rect(screen, bg_color, highlight_rect)
        pygame.draw.rect(screen, self.highlight_color, highlight_rect, 3)
        
        # Draw the text
        screen.blit(text_surface, text_rect)
        
    def draw_player_info(self, screen, white_captures=0, black_captures=0):
        """
        Draw player information including captured pieces count
        
        Args:
            screen: Pygame screen surface to draw on
            white_captures (int): Number of pieces captured by white player
            black_captures (int): Number of pieces captured by black player
        """
        # White player info (left side)
        white_text = f"White Player - Captures: {white_captures}"
        white_surface = self.font_small.render(white_text, True, self.black_color)
        screen.blit(white_surface, (10, 10))
        
        # Black player info (right side)
        black_text = f"Black Player - Captures: {black_captures}"
        black_surface = self.font_small.render(black_text, True, self.black_color)
        black_rect = black_surface.get_rect()
        black_rect.topright = (self.screen_width - 10, 10)
        screen.blit(black_surface, black_rect)
    
    def draw_game_status(self, screen, status_message):
        """
        Draw game status messages (like "Check!", "Checkmate!", etc.)
        
        Args:
            screen: Pygame screen surface to draw on
            status_message (str): Status message to display
        """
        if not status_message:
            return
            
        # Create status text with larger font
        status_surface = self.font_large.render(status_message, True, (255, 0, 0))
        status_rect = status_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        
        # Draw background for status message
        bg_rect = status_rect.inflate(20, 10)
        pygame.draw.rect(screen, self.white_color, bg_rect)
        pygame.draw.rect(screen, (255, 0, 0), bg_rect, 3)
        
        # Draw the status text
        screen.blit(status_surface, status_rect)
    
    def draw_move_history(self, screen, move_history, max_moves=5):
        """
        Draw recent move history on the side of the screen
        
        Args:
            screen: Pygame screen surface to draw on
            move_history (list): List of recent moves
            max_moves (int): Maximum number of moves to display
        """
        if not move_history:
            return
            
        # Position for move history (right side of screen)
        x_pos = self.screen_width + 10  # This would be for a wider screen
        y_start = 100
        
        # For now, just print to console (you can modify this for side panel)
        # This is a placeholder for when you want to expand the screen width
        pass
    
    def get_ui_panel_height(self):
        """
        Get the height of the UI panel (used for board positioning)
        
        Returns:
            int: Height of the UI panel in pixels
        """
        return self.ui_panel_height
    
    def animate_turn_change(self, screen, old_turn, new_turn):
        """
        Create a brief animation when the turn changes
        
        Args:
            screen: Pygame screen surface to draw on
            old_turn (str): Previous player's turn
            new_turn (str): New player's turn
        """
        # This is a simple flash effect - you can expand this
        for i in range(3):
            # Flash the turn indicator
            self.draw_turn_indicator(screen, new_turn)
            pygame.display.flip()
            pygame.time.wait(100)
            
    def draw_selected_piece_info(self, screen, piece):
        """
        Draw information about the currently selected piece
        
        Args:
            screen: Pygame screen surface to draw on
            piece: The currently selected piece object
        """
        if not piece:
            return
            
        info_text = f"Selected: {piece.color.capitalize()} {piece.piece.capitalize()}"
        info_surface = self.font_small.render(info_text, True, self.highlight_color)
        info_rect = info_surface.get_rect(center=(self.screen_width // 2, self.ui_panel_height + 20))
        
        # Draw background
        bg_rect = info_rect.inflate(10, 5)
        pygame.draw.rect(screen, self.black_color, bg_rect)
        
        # Draw text
        screen.blit(info_surface, info_rect)