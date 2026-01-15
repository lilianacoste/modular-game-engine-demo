# =========================================
# file: src/core/scene_manager.py
# =========================================
"""
SceneManager — controls global scene transitions.
Compatible with GameState, WindowManager, and scene_flow_act1 routing.
"""

import pygame


class SceneManager:
    """
    The SceneManager controls which Scene is currently active.
    Scenes must implement:
        - handle_event(event)
        - update(dt)
        - draw(screen, dt)
    """

    def __init__(self):
        self.stack = []  # active scene stack

    # ------------------------------------------------------------
    # Basic stack controls
    # ------------------------------------------------------------
    def set(self, scene):
        """
        Replace the current scene with a new one.
        """
        if scene:
            self.stack = [scene]
            self._record_scene(scene)

    def push(self, scene):
        """
        Push a new scene on top of the stack (pauses previous).
        """
        if scene:
            self.stack.append(scene)
            self._record_scene(scene)

    def pop(self):
        """
        Pop the top scene and return to the previous.
        """
        if self.stack:
            self.stack.pop()
            self._record_scene(self.current())

    def current(self):
        """
        Get the current active scene (top of stack).
        """
        return self.stack[-1] if self.stack else None

    # ------------------------------------------------------------
    # Transition helper (automatic routing)
    # ------------------------------------------------------------
    def transition(self, game_state, window_manager):
        """
        Automatically determine and load the next scene based on GameState.
        Uses scene_flow_act1.py for routing.
        """
        from src.scene_flow_act1 import next_scene_name
        from src.scene_registry import get_scene_by_name

        next_name = next_scene_name(game_state)
        if not next_name:
            print("⚠ No valid next scene found — transition aborted.")
            return

        next_cls = get_scene_by_name(next_name)
        if not next_cls:
            print(f"⚠ Scene '{next_name}' not found in registry.")
            return

        print(f"[SceneManager] Transitioning to → {next_name}")
        try:
            self.set(next_cls(self, window_manager))
        except Exception as e:
            print(f"❌ Failed to instantiate scene '{next_name}': {e}")

    # ------------------------------------------------------------
    # Main event + update + draw loop hooks
    # ------------------------------------------------------------
    def handle_event(self, event):
        """
        Pass event to the current scene.
        """
        if not self.stack:
            return
        top = self.stack[-1]
        if hasattr(top, "handle_event"):
            top.handle_event(event)

    def update(self, dt):
        """
        Update the current scene.
        """
        if not self.stack:
            return
        top = self.stack[-1]
        if hasattr(top, "update"):
            top.update(dt)

    def draw(self, screen, dt):
        """
        Draw the current scene.
        """
        if not self.stack:
            return
        top = self.stack[-1]
        if hasattr(top, "draw"):
            top.draw(screen, dt)

    def _record_scene(self, scene):
        if not scene:
            return
        try:
            from src.scene_registry import get_scene_name_by_class
            scene_name = get_scene_name_by_class(scene.__class__)
            if not scene_name:
                return
            window_manager = getattr(scene, "window_manager", None)
            if not window_manager:
                return
            game_state = getattr(window_manager, "game_state", None)
            if not game_state:
                return
            game_state.data["last_scene"] = scene_name
            game_state.save()
        except Exception:
            return
