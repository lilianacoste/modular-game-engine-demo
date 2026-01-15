"""
Window management system for a modular desktop-style application.

Coordinates stacked application windows, non-blocking overlays,
and centralized event routing. Extracted from a larger proprietary
project for portfolio demonstration purposes.
"""

import pygame

class WindowManager:
    def __init__(self, screen, state=None):
        self.screen = screen
        self.state = state   # GameState here
        self.stack = []      # active windows/apps
        self.overlays = []   # popups/notifications that don't block
        self.desktop = None  # Set by VirtualDesktop when it registers itself
        self.game_state = None  # Set in run.py after initialization

    def open(self, app_cls, args=None):
        args = args or {}
        app = app_cls(self, **args)
        # Check if it's a popup/overlay type
        if hasattr(app, 'is_overlay') and app.is_overlay:
            self.overlays.append(app)
        else:
            self.stack.append(app)

    def close(self, app=None):
        # Check overlays first
        if app and app in self.overlays:
            self.overlays.remove(app)
        elif app and app in self.stack:
            self.stack.remove(app)
        elif self.stack:
            self.stack.pop()

    def handle_event(self, event):
        # Let overlays handle events first (they're on top)
        for overlay in self.overlays[::-1]:  # Check top-to-bottom
            if hasattr(overlay, 'handle_event'):
                # Check if overlay wants to consume this event
                result = overlay.handle_event(event)
                # If it's a mouse click and hit the overlay, consume the event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(overlay, 'rect') and overlay.rect.collidepoint(event.pos):
                        return
                # If overlay returned True, it consumed the event
                if result is True:
                    return
        
        # Pass to main window if there is one
        if self.stack:
            self.stack[-1].handle_event(event)
        # If no main window but we got here, let desktop handle it
        elif hasattr(self, 'desktop'):
            self.desktop.handle_event(event)

    def draw(self, screen, dt):
        # Draw main window
        if self.stack:
            self.stack[-1].draw(screen, dt)
        
        # Draw overlays on top
        for overlay in self.overlays:
            overlay.draw(screen, dt)
