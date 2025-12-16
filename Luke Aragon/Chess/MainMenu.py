"""
MainMenu.py - Handles the main menu screen and game initialization  #NEW
This script contains:  #NEW
- Main menu screen display  #NEW
- Start game function   #NEW
- Menu button handling  #NEW
- Game state management (menu vs playing)  #NEW
"""

import pygame  #NEW
import sys  #NEW

class MainMenu:  #NEW
    def __init__(self, screen_width, screen_height):  #NEW
        """
        Initialize the main menu  #NEW
        
        Args:
            screen_width (int): Width of the game screen  #NEW
            screen_height (int): Height of the game screen  #NEW
        """
        self.screen_width = screen_width  #NEW
        self.screen_height = screen_height  #NEW
        self.font_large = pygame.font.Font(None, 72)  #NEW
        self.font_medium = pygame.font.Font(None, 48)  #NEW
        self.font_small = pygame.font.Font(None, 36)  #NEW
        
        # Menu state  #NEW
        self.showing_menu = True  #NEW
        self.game_started = False  #NEW
        
        # Colors  #NEW
        self.bg_color = (50, 50, 80)  #NEW
        self.button_color = (100, 150, 200)  #NEW
        self.button_hover_color = (120, 170, 220)  #NEW
        self.text_color = (255, 255, 255)  #NEW
        
        # Button rectangles  #NEW
        self.start_button = pygame.Rect(screen_width//2 - 100, screen_height//2 - 25, 200, 50)  #NEW
        self.quit_button = pygame.Rect(screen_width//2 - 100, screen_height//2 + 50, 200, 50)  #NEW
        
        # Mouse position for hover effects  #NEW
        self.mouse_pos = (0, 0)  #NEW
    
    def handle_event(self, event):  #NEW
        """
        Handle menu events (mouse clicks, hovers)  #NEW
        
        Args:
            event: Pygame event object  #NEW
            
        Returns:
            str: Action to take ('start', 'quit', 'none')  #NEW
        """
        if event.type == pygame.MOUSEMOTION:  #NEW
            self.mouse_pos = event.pos  #NEW
            
        elif event.type == pygame.MOUSEBUTTONDOWN:  #NEW
            if event.button == 1:  # Left click  #NEW
                if self.start_button.collidepoint(event.pos):  #NEW
                    self.showing_menu = False  #NEW
                    self.game_started = True  #NEW
                    return 'start'  #NEW
                elif self.quit_button.collidepoint(event.pos):  #NEW
                    return 'quit'  #NEW
        
        return 'none'  #NEW
    
    def draw(self, screen):  #NEW
        """
        Draw the main menu on the screen  #NEW
        
        Args:
            screen: Pygame screen surface to draw on  #NEW
        """
        if not self.showing_menu:  #NEW
            return  #NEW
            
        # Fill background  #NEW
        screen.fill(self.bg_color)  #NEW
        
        # Draw title  #NEW
        title_text = self.font_large.render("CHESS GAME", True, self.text_color)  #NEW
        title_rect = title_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 150))  #NEW
        screen.blit(title_text, title_rect)  #NEW
        
        # Draw subtitle  #NEW
        subtitle_text = self.font_small.render("Click Start to begin playing", True, self.text_color)  #NEW
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width//2, self.screen_height//2 - 100))  #NEW
        screen.blit(subtitle_text, subtitle_rect)  #NEW
        
        # Draw start button  #NEW
        start_color = self.button_hover_color if self.start_button.collidepoint(self.mouse_pos) else self.button_color  #NEW
        pygame.draw.rect(screen, start_color, self.start_button)  #NEW
        pygame.draw.rect(screen, self.text_color, self.start_button, 2)  #NEW
        
        start_text = self.font_medium.render("START", True, self.text_color)  #NEW
        start_text_rect = start_text.get_rect(center=self.start_button.center)  #NEW
        screen.blit(start_text, start_text_rect)  #NEW
        
        # Draw quit button  #NEW
        quit_color = self.button_hover_color if self.quit_button.collidepoint(self.mouse_pos) else self.button_color  #NEW
        pygame.draw.rect(screen, quit_color, self.quit_button)  #NEW
        pygame.draw.rect(screen, self.text_color, self.quit_button, 2)  #NEW
        
        quit_text = self.font_medium.render("QUIT", True, self.text_color)  #NEW
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)  #NEW
        screen.blit(quit_text, quit_text_rect)  #NEW
    
    def is_showing(self):  #NEW
        """
        Check if the menu is currently being shown  #NEW
        
        Returns:
            bool: True if menu is showing, False otherwise  #NEW
        """
        return self.showing_menu  #NEW
    
    def start_game(self):  #NEW
        """
        Start the game (called when start button is clicked)  #NEW
        This function transitions from menu to game state  #NEW
        """
        self.showing_menu = False  #NEW
        self.game_started = True  #NEW
        print("Game started! Transitioning from main menu to chess board...")  #NEW
    
    def show_menu(self):  #NEW
        """
        Show the menu again (useful for returning to menu from game)  #NEW
        """
        self.showing_menu = True  #NEW
        self.game_started = False  #NEW