# InputManager.py - Handles input events (like an Input Manager in Unity)

import pygame
from typing import Tuple, Optional, Callable

class InputEvents:
    """Event type constants"""
    QUIT = "quit"
    ESCAPE = "escape"
    MOUSE_CLICK = "mouse_click"

class InputManager:
    def __init__(self):
        self.event_handlers = {}
        self._running = True
    
    # ===== EVENT REGISTRATION =====
    
    def RegisterHandler(self, event_type: str, callback: Callable):
        """Register a callback for specific event type"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(callback)
    
    def UnregisterHandler(self, event_type: str, callback: Callable):
        """Remove a callback for specific event type"""
        if event_type in self.event_handlers:
            if callback in self.event_handlers[event_type]:
                self.event_handlers[event_type].remove(callback)
    
    # ===== EVENT PROCESSING =====
    
    def ProcessEvents(self) -> bool:
        """Process all pygame events, returns False if should quit"""
        for event in pygame.event.get():
            self._HandleEvent(event)
        
        return self._running
    
    def _HandleEvent(self, event: pygame.event.Event):
        """Handle individual pygame event"""
        if event.type == pygame.QUIT:
            self._TriggerEvent(InputEvents.QUIT)
            self._running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._TriggerEvent(InputEvents.ESCAPE)
                self._running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self._TriggerEvent(InputEvents.MOUSE_CLICK, event.pos)
    
    def _TriggerEvent(self, event_type: str, data=None):
        """Trigger all registered callbacks for event type"""
        if event_type in self.event_handlers:
            for callback in self.event_handlers[event_type]:
                if data is not None:
                    callback(data)
                else:
                    callback()
    
    # ===== STATE QUERIES =====
    
    def ShouldQuit(self) -> bool:
        """Check if application should quit"""
        return not self._running
    
    def ForceQuit(self):
        """Force quit the application"""
        self._running = False