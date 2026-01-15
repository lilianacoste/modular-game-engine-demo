"""
Main application entry point.

Initializes core systems, manages the main event loop, and coordinates
window management, desktop rendering, and global state access.
Extracted from a larger proprietary project for portfolio demonstration.
"""

import pygame
import os
import sys

# Import core systems
from src.window_manager import WindowManager
from src.desktop import VirtualDesktop
from src.game_state import GameState
from src.apps.file_toast import FileToast

# -------------------------
# Main Game Entry
# -------------------------
def main():
    pygame.init()
    W, H = 1280, 720
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Haybridge OS — Virtual Desktop")
    clock = pygame.time.Clock()

    # Initialize systems
    wm = WindowManager(screen)
    wm.game_state = GameState()  # Store game state in window manager for apps to access
    desktop = VirtualDesktop(wm)   # desktop registers itself with wm

    # Show initial task popup
    from src.apps.task_popup import TaskPopup
    first_task = wm.game_state.active_task()
    if first_task:
        wm.open(TaskPopup, args={"text": f"Welcome to Haybridge OS!\n\nYour first task: {first_task}", "duration": 6})

    # Main loop
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        # Check for trust threshold and show hidden file (only once lifetime)
        if (wm.game_state.get_flag("trust_threshold_reached") and 
            not wm.game_state.get_flag("hidden_file_toast_shown")):
            wm.game_state.set_flag("hidden_file_toast_shown", True)
            wm.open(FileToast, args={
                "filename": "note_me_.txt",
                "contents": "pretend you are code.\npretend you never had a name.\npretend they didn't take it from you.",
                "modified": "5 years ago"
            })

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                # Pass events to window manager if there are windows or overlays
                if wm.stack or wm.overlays:
                    wm.handle_event(event)
                else:
                    desktop.handle_event(event)

        # Draw background + desktop
        desktop.draw(screen, dt)

        # Draw active windows
        wm.draw(screen, dt)

        # Update screen
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
