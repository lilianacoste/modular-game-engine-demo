 =========================================
# file: src/core/scene_flow_act1.py
# =========================================
"""
Automatic routing logic for Act 1.
Determines which scene to load next based on GameState flags.
Integrates full end-of-Act-1 chain (GoBedScene → Act2DesktopScene).
"""

from src.scene_registry import get_scene_by_name


def next_scene_name(game_state):
    """
    Determine the next scene based on current GameState flags.
    Returns a string key (scene name) registered in scene_registry.py.
    """
    f = game_state.data.get("flags", {})
    act = game_state.data.get("act", 1)

    if act != 1:
        return None  # Only handles Act 1 progression

    # --- Act 1 Start ---
    if not f.get("application_complete"):
        return "act1/application"

    # --- Desktop Hub unlocked after application ---
    if not f.get("desktop_unlocked"):
        game_state.set_flag("desktop_unlocked", True)
        return "act1/desktop"

    # --- Faculty Zooms & Assignments ---
    if not f.get("timothy_zoom_complete"):
        return "zoom_timothy"

    if not f.get("lottie_assignment1_complete"):
        return "lottie"

    if not f.get("beatrice_zoom_complete"):
        return "zoom_beatrice"

    if not f.get("lottie_assignment2_complete"):
        return "lottie"

    # --- Log Off transition ---
    if not f.get("logoff_scene_complete"):
        return "act1/logoff"

    # --- Dorm / Bluebird Sequence ---
    if not f.get("bluebird_signal_detected"):
        return "act1/dorm"

    if not f.get("bluebird_complete"):
        return "act1/bluebird_chat"

    if not f.get("dorm_after_bluebird_complete"):
        return "act1/dorm_after_bluebird"
    # # --- Hallway Puzzle + Control Room ---
    if not f.get("hallway_game_complete"):
      return "act1/hallway_game"

    if not f.get("control_room_complete"):
       return "act1/control_room"

    # # --- Closing Scenes ---
    # # Laptop → triggers Lottie update
    if not f.get("lottie_update_started"):
        return "act1/closing"

    # # Bed → Go to Bed → Fade-out sequence
    if not f.get("act1_complete"):
        return "act1/go_to_bed"

    # --- Act 2 Start ---
    game_state.data["act"] = 2
    game_state.save()
    return "act2/act2_desktop"


# =========================================
# Helper for SceneManager
# =========================================
def transition(scene_manager, window_manager):
    """
    Convenience helper for any scene to move forward in Act 1.
    """
    next_name = next_scene_name(window_manager.game_state)
    if not next_name:
        print("⚠ No valid next scene found for Act 1.")
        return

    scene_class = get_scene_by_name(next_name)
    if not scene_class:
        print(f"⚠ Scene '{next_name}' not found in registry.")
        return

    # If the next scene is an app-style Zoom/Lottie, open via WindowManager with game_state.
    app_names = {"zoom_timothy", "zoom_beatrice", "lottie"}
    if next_name in app_names and window_manager:
        window_manager.open(scene_class, args={"game_state": window_manager.game_state})
        return

    # Instantiate and set new scene
    if window_manager:
        scene_manager.set(scene_class(scene_manager, window_manager))
    else:
        scene_manager.set(scene_class(scene_manager))

# Flexible variant that supports App-style constructors
def flex_transition(scene_manager, window_manager):
    next_name = next_scene_name(window_manager.game_state)
    if not next_name:
        print("[SceneFlow] No valid next scene found for Act 1.")
        return

    scene_class = get_scene_by_name(next_name)
    if not scene_class:
        print(f"[SceneFlow] Scene '{next_name}' not found in registry.")
        return

    try:
        # Only correct signature for all Act 1 scenes
        instance = scene_class(scene_manager, window_manager)
        scene_manager.set(instance)
    except Exception as e:
        print(f"[SceneFlow] Failed to instantiate '{next_name}': {e}")
