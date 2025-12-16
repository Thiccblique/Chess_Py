"""
Animations.py - Handles animations and visual polish for the chess game  #NEW
This script contains:  #NEW
- Piece movement animations  #NEW
- Board highlight animations  #NEW
- Capture animations  #NEW
- Turn transition effects  #NEW
- Visual feedback for user interactions  #NEW
"""

import pygame  #NEW
import math  #NEW

class GameAnimations:  #NEW
    def __init__(self, screen_width, screen_height):
        """
        Initialize the animation system
        
        Args:
            screen_width (int): Width of the game screen
            screen_height (int): Height of the game screen
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.animations_playing = []
        
        # Animation settings
        self.animation_speed = 0.3  # Speed of piece movements
        self.highlight_pulse_speed = 0.1
        self.capture_animation_duration = 500  # milliseconds
        
    def animate_piece_move(self, piece, start_pos, end_pos, target_file, target_rank, duration=300):
        """
        Create smooth movement animation for a piece
        
        Args:
            piece: The piece object to animate
            start_pos (tuple): Starting position (x, y) in pixels
            end_pos (tuple): Ending position (x, y) in pixels
            target_file (int): Target file position (1-8)
            target_rank (int): Target rank position (1-8)
            duration (int): Animation duration in milliseconds
        """
        # Clear any existing animations for this piece to prevent conflicts
        self.stop_piece_animations(piece)
        
        animation = {
            'type': 'move',
            'piece': piece,
            'start_pos': start_pos,
            'end_pos': end_pos,
            'target_file': target_file,
            'target_rank': target_rank,
            'start_time': pygame.time.get_ticks(),
            'duration': duration,
            'active': True
        }
        self.animations_playing.append(animation)
        return animation
    
    def animate_capture(self, captured_piece, duration=300):
        """
        Create capture animation (piece fading out)
        
        Args:
            captured_piece: The piece being captured
            duration (int): Animation duration in milliseconds
        """
        animation = {
            'type': 'capture',
            'piece': captured_piece,
            'start_time': pygame.time.get_ticks(),
            'duration': duration,
            'start_alpha': 255,
            'active': True
        }
        self.animations_playing.append(animation)
        return animation
    
    def animate_selection_pulse(self, piece_rect):
        """
        Create pulsing highlight animation for selected piece
        
        Args:
            piece_rect: Rectangle of the selected piece
        """
        animation = {
            'type': 'selection_pulse',
            'rect': piece_rect,
            'start_time': pygame.time.get_ticks(),
            'active': True
        }
        self.animations_playing.append(animation)
        return animation
    
    def animate_valid_move_highlight(self, move_positions):
        """
        Animate highlighting of valid move positions
        
        Args:
            move_positions (list): List of (x, y) positions for valid moves
        """
        for pos in move_positions:
            animation = {
                'type': 'move_highlight',
                'position': pos,
                'start_time': pygame.time.get_ticks(),
                'active': True
            }
            self.animations_playing.append(animation)
    
    def update_animations(self, screen):
        """
        Update and draw all active animations
        
        Args:
            screen: Pygame screen surface to draw on
        """
        current_time = pygame.time.get_ticks()
        animations_to_remove = []
        
        for animation in self.animations_playing:
            if not animation['active']:
                animations_to_remove.append(animation)
                continue
                
            if animation['type'] == 'move':
                self._update_move_animation(animation, current_time, screen)
            elif animation['type'] == 'capture':
                self._update_capture_animation(animation, current_time, screen)
            elif animation['type'] == 'selection_pulse':
                self._update_selection_pulse(animation, current_time, screen)
            elif animation['type'] == 'move_highlight':
                self._update_move_highlight(animation, current_time, screen)
        
        # Remove completed animations
        for animation in animations_to_remove:
            self.animations_playing.remove(animation)
    
    def _update_move_animation(self, animation, current_time, screen):
        """
        Update piece movement animation
        """
        elapsed = current_time - animation['start_time']
        progress = min(elapsed / animation['duration'], 1.0)
        
        if progress >= 1.0:
            animation['active'] = False
            # Move piece to final position when animation completes
            piece = animation['piece']
            piece.set_position(animation['target_file'], animation['target_rank'])
            return
        
        # Use smooth easing for all moves
        eased_progress = self._ease_in_out_cubic(progress)
        
        start_x, start_y = animation['start_pos']
        end_x, end_y = animation['end_pos']
        
        # Calculate smooth interpolated position
        current_x = start_x + (end_x - start_x) * eased_progress
        current_y = start_y + (end_y - start_y) * eased_progress
        
        # Draw piece at interpolated position
        piece = animation['piece']
        screen.blit(piece.image, (int(current_x), int(current_y)))
    
    def _update_capture_animation(self, animation, current_time, screen):
        """
        Update piece capture animation (fade out)
        """
        elapsed = current_time - animation['start_time']
        progress = min(elapsed / animation['duration'], 1.0)
        
        if progress >= 1.0:
            animation['active'] = False
            return
        
        # Calculate fading alpha
        alpha = int(animation['start_alpha'] * (1.0 - progress))
        
        # Draw fading piece (this would need to be implemented in the Piece class)
        piece = animation['piece']
        if hasattr(piece, 'draw_with_alpha'):
            piece.draw_with_alpha(screen, alpha)
    
    def _update_selection_pulse(self, animation, current_time, screen):
        """
        Update selection pulse animation
        """
        elapsed = current_time - animation['start_time']
        pulse_cycle = (elapsed / 1000.0) * self.highlight_pulse_speed * 2 * math.pi
        
        # Create pulsing effect
        pulse_intensity = (math.sin(pulse_cycle) + 1) / 2  # Normalize to 0-1
        alpha = int(50 + pulse_intensity * 100)  # Pulse between 50-150 alpha
        
        # Draw pulsing highlight
        rect = animation['rect']
        highlight_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        highlight_surface.fill((255, 255, 0, alpha))  # Yellow with varying alpha
        screen.blit(highlight_surface, rect.topleft)
    
    def _update_move_highlight(self, animation, current_time, screen):
        """
        Update valid move position highlights
        """
        elapsed = current_time - animation['start_time']
        pulse_cycle = (elapsed / 1000.0) * self.highlight_pulse_speed * 2 * math.pi
        
        # Create pulsing effect for valid moves
        pulse_intensity = (math.sin(pulse_cycle) + 1) / 2
        alpha = int(30 + pulse_intensity * 60)  # Pulse between 30-90 alpha
        
        # Draw pulsing highlight on board square
        pos_x, pos_y = animation['position']
        square_size = 90  # Updated to match new board size
        board_start_y = 80  # Updated to match new board position
        rect = pygame.Rect(pos_x * square_size, pos_y * square_size + board_start_y, square_size, square_size)
        
        highlight_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        highlight_surface.fill((0, 255, 0, alpha))  # Green with varying alpha
        screen.blit(highlight_surface, rect.topleft)
    
    def _ease_in_out_cubic(self, t):
        """
        Smoother cubic easing function for animations
        
        Args:
            t (float): Time parameter (0.0 to 1.0)
            
        Returns:
            float: Eased value
        """
        # Clamp t to [0, 1] to prevent overshoot
        t = max(0.0, min(1.0, t))
        
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - math.pow(-2 * t + 2, 3) / 2
    
    def _ease_in_out_quad(self, t):
        """
        Quadratic easing function for smoother movement
        
        Args:
            t (float): Time parameter (0.0 to 1.0)
            
        Returns:
            float: Eased value
        """
        # Clamp t to [0, 1] to prevent overshoot
        t = max(0.0, min(1.0, t))
        
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - math.pow(-2 * t + 2, 2) / 2
    
    def stop_all_animations(self):
        """
        Stop and clear all running animations
        """
        self.animations_playing.clear()
    
    def stop_selection_animations(self):
        """
        Stop only selection-related animations, keep movement animations
        """
        animations_to_remove = []
        for animation in self.animations_playing:
            if animation.get('type') in ['selection_pulse', 'move_highlight']:
                animations_to_remove.append(animation)
        
        for animation in animations_to_remove:
            self.animations_playing.remove(animation)
    
    def stop_piece_animations(self, piece):
        """
        Stop all animations for a specific piece
        
        Args:
            piece: The piece whose animations should be stopped
        """
        animations_to_remove = []
        for animation in self.animations_playing:
            if animation.get('piece') == piece:
                animations_to_remove.append(animation)
        
        for animation in animations_to_remove:
            self.animations_playing.remove(animation)
    
    def is_animating(self):
        """
        Check if any animations are currently playing
        
        Returns:
            bool: True if animations are playing, False otherwise
        """
        return len(self.animations_playing) > 0
    
    def is_piece_animating(self, piece):
        """
        Check if a specific piece is currently being animated
        
        Args:
            piece: The piece to check
            
        Returns:
            bool: True if the piece is being animated, False otherwise
        """
        for animation in self.animations_playing:
            if animation.get('piece') == piece and animation.get('type') == 'move':
                return True
        return False
    
    def create_button_hover_effect(self, button_rect, is_hovered):
        """
        Create hover effect for buttons
        
        Args:
            button_rect: Rectangle of the button
            is_hovered (bool): Whether the button is being hovered
            
        Returns:
            tuple: (color, scale_factor) for drawing the button
        """
        if is_hovered:
            # Slightly larger and brighter when hovered
            scale_factor = 1.05
            color_modifier = 20  # Make color brighter
            return color_modifier, scale_factor
        else:
            return 0, 1.0
    
    def animate_board_flip(self, duration=1000):
        """
        Create board flip animation (for changing perspectives)
        
        Args:
            duration (int): Duration of the flip animation in milliseconds
        """
        animation = {
            'type': 'board_flip',
            'start_time': pygame.time.get_ticks(),
            'duration': duration,
            'active': True
        }
        self.animations_playing.append(animation)
        return animation
    
    def animate_turn_change(self, screen, old_turn, new_turn):
        """
        Create a brief animation when the turn changes
        
        Args:
            screen: Pygame screen surface to draw on
            old_turn (str): Previous player's turn
            new_turn (str): New player's turn
        """
        # This is a simple implementation - just a brief visual feedback
        # You can expand this with more complex animations later
        print(f"Turn animation: {old_turn} -> {new_turn}")
        return True  # Simple placeholder for now