"""
Window management system for a modular desktop-style application.

Coordinates stacked application windows, non-blocking overlays,
and centralized event routing. Extracted from a larger proprietary
project for portfolio demonstration purposes.
"""
# =========================================
# file: src/core/window_manager.py
# =========================================
"""
WindowManager — handles desktop apps, popups, and overlays.
Integrates tightly with VirtualDesktop and GameState.
"""

import pygame
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.game_state import GameState
    from src.scene_manager import SceneManager


class WindowManager:
    """
    Manages windows and overlays (desktop apps, task popups, etc.)
    Acts as a lightweight windowing layer for the Virtual Desktop.
    """

    def __init__(self, screen: pygame.Surface, state: Optional["GameState"] = None):
        self.screen = screen
        self.state = state
        self.stack: list = []       # active main windows (apps)
        self.overlays: list = []    # popups that draw above windows
        self.desktop = None         # set by VirtualDesktop
        self.game_state: Optional["GameState"] = None  # linked in run.py
        self.scene_manager: Optional["SceneManager"] = None  # linked in run.py
        self.header_font = pygame.font.SysFont("Arial", 16, bold=True)
        self.header_height = 26
        self.header_bg = (30, 60, 120)
        self.header_border = (15, 25, 60)
        self.header_text = (245, 245, 245)
        self.header_close_bg = (170, 60, 60)
        self.header_close_text = (255, 255, 255)

    # ------------------------------------------------------------
    # Window controls
    # ------------------------------------------------------------
    def open(self, app_cls, args=None):
        """Open a new app or popup window."""
        args = args or {}
        try:
            app = app_cls(self, **args)
        except Exception as e:
            print(f"❌ Failed to create app {app_cls.__name__}: {e}")
            return

        # Overlay windows (like TaskPopup)
        if getattr(app, "is_overlay", False):
            self.overlays.append(app)
        else:
            self.stack.append(app)

    def close(self, app=None):
        """Close an app or popup."""
        if app and app in self.overlays:
            self.overlays.remove(app)
        elif app and app in self.stack:
            self.stack.remove(app)
        elif self.stack:
            self.stack.pop()

    def close_all(self):
        """Close all apps and overlays."""
        self.stack.clear()
        self.overlays.clear()

    # ------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------
    def handle_event(self, event):
        """
        Send events to topmost overlay or window.
        """
        # overlays first (reverse order)
        for overlay in reversed(self.overlays):
            if hasattr(overlay, "handle_event"):
                result = overlay.handle_event(event)
                if result is True:
                    return  # overlay consumed event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hasattr(overlay, "rect") and overlay.rect.collidepoint(event.pos):
                        return

        # then top window
        if self.stack:
            top = self.stack[-1]
            if hasattr(top, "handle_event"):
                top.handle_event(event)

    # ------------------------------------------------------------
    # Update + draw loop integration
    # ------------------------------------------------------------
    def update(self, dt: float):
        """Update all windows and overlays."""
        if self.stack:
            top = self.stack[-1]
            if hasattr(top, "update"):
                top.update(dt)

        for overlay in self.overlays:
            if hasattr(overlay, "update"):
                overlay.update(dt)

    def draw(self, screen: pygame.Surface, dt: float):
        """Draw windows and overlays."""
        if self.stack:
            top = self.stack[-1]
            if hasattr(top, "draw"):
                top.draw(screen, dt)
            self._draw_window_header(top, screen)

        for overlay in self.overlays:
            if hasattr(overlay, "draw"):
                overlay.draw(screen, dt)

    def _draw_window_header(self, app, screen: pygame.Surface) -> None:
        if getattr(app, "is_overlay", False):
            return
        if getattr(app, "show_window_header", True) is False:
            return
        if hasattr(app, "rect"):
            return

        title = getattr(app, "window_title", app.__class__.__name__)
        rect = screen.get_rect()
        bar_rect = pygame.Rect(rect.x, rect.y, rect.width, self.header_height)
        pygame.draw.rect(screen, self.header_bg, bar_rect)
        pygame.draw.line(
            screen,
            self.header_border,
            (bar_rect.left, bar_rect.bottom - 1),
            (bar_rect.right, bar_rect.bottom - 1),
            2,
        )

        title_surf = self.header_font.render(title, True, self.header_text)
        screen.blit(title_surf, (bar_rect.x + 8, bar_rect.y + 4))

        close_rect = pygame.Rect(bar_rect.right - 26, bar_rect.y + 4, 18, 18)
        pygame.draw.rect(screen, self.header_close_bg, close_rect, border_radius=3)
        x_surf = self.header_font.render("X", True, self.header_close_text)
        screen.blit(
            x_surf,
            x_surf.get_rect(center=close_rect.center),
        )
