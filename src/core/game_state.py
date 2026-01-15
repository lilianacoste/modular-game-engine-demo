# =========================================
# file: src/core/game_state.py
# =========================================
"""
GameState: manages player progress, flags, trust, tasks, and persistence.
Integrated with JSON save system in /save/state.json.
"""

import json
import os


class GameState:
    def __init__(self, save_file: str = "save/state.json"):
        self.save_file = save_file
        self.data = self._load_or_init()
        self._ensure_flags()  # ensure new flags exist in older saves
        self._ensure_resonance_data()
        self._ensure_scene_tracking()

    # ------------------------------------------------------------
    # Load or create new state
    # ------------------------------------------------------------
    def _load_or_init(self):
        """Load state from file, or create a new one if missing."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠ Failed to load save: {e}")

        # Default player name (fallback safe for sandbox/headless)
        try:
            player_name = os.getlogin()
        except Exception:
            player_name = "Student"

        # Default new-game structure
        data = {
            "player_name": player_name,
            "act": 1,
            "trust": 0.5,
            "act3_trust": 0.0,
            "betrayal_count": 0,
            "resonance": 0,
            "resonance_flags_seen": [],
            "last_scene": None,
            "settings": {"flash_effects": True},
            "flags": {
                # Minimal seed; _ensure_flags() will fill the rest.
                "pink_channel_synced": False
            },
            "tasks": [
                {"text": "Join Dr. Timothy's Zoom", "done": False},
                {"text": "Launch Lottie AI", "done": False},
                {"text": "Join Dr. Beatrice's Zoom", "done": False},
                {"text": "Complete Lottie Assignment 2", "done": False},
                {"text": "Log off Desktop", "done": False},
            ],
        }

        self._save_data(data)
        return data

    def load(self):
        """Compatibility wrapper so older scenes can call gs.load()."""
        self.data = self._load_or_init()
        self._ensure_flags()
        self._ensure_resonance_data()
        self._ensure_scene_tracking()

    # ------------------------------------------------------------
    # Ensure flags exist in old saves
    # ------------------------------------------------------------
    def _ensure_flags(self):
        """Backfill any newly-added flags so older saves don't break."""
        flags = self.data.setdefault("flags", {})

        # Core scene/app flags used throughout Acts 1–2 (and some later hooks)
        defaults = {
            # Lottie mission flow (Act 1)
            "lottie_home_waiting": False,
            "lottie_admin_assigned": False,
            "lottie_home_sequence_complete": False,
            "lottie_home_denied": False,
            "pink_channel_synced": flags.get("pink_channel_synced", False),

            # Lottie post-mission (Act 1)
            "lottie_post_qna_complete": False,
            "lottie_post_mission_greeted": False,
            "lottie_creepy_event_done": False,

            # Zooms (Act 1)
            "timothy_zoom_complete": False,
            "beatrice_zoom_complete": False,

            # Assignments (Act 1)
            "lottie_assignment1_complete": False,
            "lottie_assignment2_complete": False,

            # Desktop UX bits
            "desktop_intro_shown": False,
            "portal_reminder_shown": False,

            # Misc discoveries / easter eggs
            "terminal_388_found": False,
            "hallway_freechat_typed": False,
            "stain_discovered": False,
            "stain_lottie_chat_done": False,

            # --- NEW FLAGS FOR ACT 1 FLOW ---
            "bluebird_complete": False,
            "dorm_after_bluebird_complete": False,
            "bluebird_signal_detected": False,
            "act1_fast_forward": False,

            # Hallway stealth sequence
            "hallway_game_complete": False,   # main
            "hallway_completed": False,       # legacy compatibility

            # Control room
            "control_room_complete": False,

            # Admin desktop / narrative progression
            "admin_intro_shown": False,
            "admin_lottie_autostarted": False,
            "dorm_brainmap_cache_received": False,
            "neuroscan_unlocked": False,
            "memory_core_downloaded": False,

            # Lab / night mission hook
            "lab_signal_relay_complete": flags.get("lab_signal_relay_complete", False),

            # Lux console channels
            "lux_channel2_shown": False,
            "lux_channel3_shown": False,
            "lux_channel2_unlocked": False,
            "lux_channel3_unlocked": False,

            # Hangman lock / Neuroscan
            "hangman_lock_solved": False,

            # --- Act 2 flags ---
            "talked_to_lottie_prezoom": False,
            "dr_anand_zoom_complete": False,
            "anand_suspicious": False,
            "anand_assignment_complete": False,
            "lottie_override_anand_question": False,

            "dr_rachel_zoom_complete": False,
            "rachel_assignment_complete": False,
            "rachel_suspicious": False,

            # Act 2 logoff + night mission
            "act2_logoff_complete": False,
            "lottie_lab_intro_complete": False,
            "act2_night_mission_complete": False,
            "act2_complete": False,

            # Post-lab, Lottie update & dreams
            "lottie_update2_complete": False,
            "charlotte_dream_complete": False,

            # --- Act 3 flags ---
            # Lottie intro variants
            "act3_lottie_intro_seen": False,
            "act3_lottie_intro_locked": False,
            "act3_lottie_intro_lowtrust_seen": False,
            "desktop_act3_intro_shown": False,

            # Zoom 3 completions
            "timothy_zoom3_complete": False,
            "beatrice_zoom3_complete": False,
            "timothy_assignment_complete": False,

            # Suspicion flags for all four profs (used in logoff router)
            "timothy_suspicious": False,
            "beatrice_suspicious": False,
            # anand_suspicious / rachel_suspicious already defined above

            # Logoff and betrayal
            "act3_safe_logoff": False,
            "act3_betrayal": False,
            "act3_logoff_complete": False,
            "act3_normal_logoff": False,
            "force_interrogation": False,
            "lottie_instruction_started" : False,
            "lottie_instruction_complete" : False,
            "act3_metaforest_started": False,
            "act3_metaforest_complete": False,
            "act3_channel3_flow_pending": False,
            "act3_channel3_exit_ready": False,

            # One-time bonuses / bookkeeping
            "act2_trust_bonus_granted": False,

            # --- Act 4 stable route flags ---
            "act4_route": "unknown",
            "act4_route_stable": False,
            "act4_route_corrupted": False,
            "act4_corrupted_reason": "",
            "act4_lottie_stable_confirmed": False,
            "act4_timothy_zoom4_complete": False,
            "act4_beatrice_zoom4_complete": False,
            "act4_optional_assignment_complete": False,
            "act4_checkin_complete": False,
            "act4_complete": False,
            "act4_end_unlocked": False,
        }

        changed = False
        for k, v in defaults.items():
            if k not in flags:
                flags[k] = v
                changed = True

        # Backfill hallway completion only if the glitch event already happened.
        if flags.get("hallway_glitch"):
            if not flags.get("hallway_game_complete"):
                flags["hallway_game_complete"] = True
                flags["hallway_completed"] = True
                changed = True

        # ------------------------------------------------------------------
        # Fast-forward Act 1 chain up to Control Room if the player is already
        # past the desktop/logoff checkpoints (for saves resuming mid-stream).
        # ------------------------------------------------------------------
        if (
            self.data.get("act", 1) == 1
            and flags.get("act1_fast_forward")
            and flags.get("desktop_unlocked")
            and flags.get("logoff_scene_complete")
        ):
            # Core progression beats before Control Room
            for k in [
                "application_complete",
                "desktop_unlocked",
                "timothy_zoom_complete",
                "lottie_assignment1_complete",
                "beatrice_zoom_complete",
                "lottie_assignment2_complete",
                "bluebird_complete",
                "dorm_after_bluebird_complete",
                "hallway_game_complete",
                "hallway_completed",
                "control_room_complete",
            ]:
                if not flags.get(k):
                    flags[k] = True
                    changed = True
        # Ensure Act 3 tasks exist when entering Act 3+
        tasks_changed = self._ensure_act3_tasks() or self._ensure_act4_tasks()

        if changed or tasks_changed:
            self.save()

    def _ensure_resonance_data(self):
        """Backfill resonance keys for older saves."""
        changed = False
        if "resonance" not in self.data:
            self.data["resonance"] = 0
            changed = True
        if "resonance_flags_seen" not in self.data:
            self.data["resonance_flags_seen"] = []
            changed = True
        if changed:
            self.save()

    def _ensure_scene_tracking(self):
        """Backfill scene tracking key for older saves."""
        if "last_scene" not in self.data:
            self.data["last_scene"] = None
            self.save()

    def _ensure_act3_tasks(self):
        """
        Keep Act 3 tasks separate from earlier acts.
        When act >= 3, replace the task list with Act 3 objectives and
        mark completion based on flags.
        """
        act = self.data.get("act", 1)
        if act < 3:
            return False

        tasks = []
        def add(text, done):
            tasks.append({"text": text, "done": bool(done)})

        add("Join Dr. Timothy's Zoom 3", self.get_flag("timothy_zoom3_complete"))
        add("Complete Timothy's Assignment", self.get_flag("timothy_assignment_complete"))
        add("Join Dr. Beatrice's Zoom 3", self.get_flag("beatrice_zoom3_complete"))
        add("Log Off Act 3", self.get_flag("act3_logoff_complete"))

        changed = tasks != self.data.get("tasks")
        if changed:
            self.data["tasks"] = tasks
        return changed

    def _ensure_act4_tasks(self):
        """
        When act >= 4, sync the task list to the stable route beats.
        Older saves that reach Act 4 should see the new objectives.
        """
        act = self.data.get("act", 1)
        if act < 4:
            return False

        tasks = []
        def add(text, done):
            tasks.append({"text": text, "done": bool(done)})

        add("Check on Lottie (Act 4 start)", self.get_flag("act4_lottie_stable_confirmed"))
        add("Join Dr. Timothy's Zoom 4", self.get_flag("act4_timothy_zoom4_complete"))
        add("Join Dr. Beatrice's Zoom 4", self.get_flag("act4_beatrice_zoom4_complete"))
        add("Complete optional assignment", self.get_flag("act4_optional_assignment_complete"))
        add("Finish Act 4 day", self.get_flag("act4_complete"))

        changed = tasks != self.data.get("tasks")
        if changed:
            self.data["tasks"] = tasks
        return changed

    # ------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------
    def save(self):
        self._save_data(self.data)

    def _save_data(self, data):
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
        with open(self.save_file, "w") as f:
            json.dump(data, f, indent=2)

    def clear_flag(self, key: str):
        """Reset a flag to False."""
        if key in self.data.get("flags", {}):
            self.data["flags"][key] = False
            self.save()

    def reset(self):
        """Reset to a clean new-game state."""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        self.data = self._load_or_init()
        self._ensure_flags()

    # ------------------------------------------------------------
    # Flags (binary game progression markers)
    # ------------------------------------------------------------
    def get_flag(self, key: str, default=False):
        return self.data.get("flags", {}).get(key, default)

    def set_flag(self, key: str, value=True, resonance_points=None):
        """
        Set a narrative / progression flag.
        Use this for things like:
            self.state.set_flag("rachel_suspicious", True)
        """
        if not self._is_json_safe(value):
            raise TypeError(
                f"[GameState] set_flag rejected non-JSON value: "
                f"{type(value).__name__} = {value}"
            )
        self.data.setdefault("flags", {})[key] = value
        self.save()
        self.auto_sync_tasks()
        if value and resonance_points is not None:
            self.award_resonance_for_flag(key, resonance_points)

    def _is_json_safe(self, value):
        """Return True if value is JSON-serializable."""
        if isinstance(value, (str, int, float, bool)) or value is None:
            return True
        if isinstance(value, list):
            return all(self._is_json_safe(i) for i in value)
        if isinstance(value, dict):
            return all(
                isinstance(k, str) and self._is_json_safe(v)
                for k, v in value.items()
            )
        return False

    def auto_sync_tasks(self):
        """
        Automatically keep Act 2 task list synced with key flags.
        This will just silently do nothing if a matching task text
        isn't present in the current task list.
        """
        mapping = [
            ("dr_anand_zoom_complete", "Join Dr. Anand’s Zoom"),
            ("anand_assignment_complete", "Complete Anand's Assignment"),
            ("dr_rachel_zoom_complete", "Join Dr. Rachel’s Zoom"),
            ("rachel_assignment_complete", "Complete Rachel’s Assignment"),
            ("act2_logoff_complete", "Log Off"),
            ("lottie_lab_intro_complete", "Prepare for Night Mission"),
            ("timothy_zoom3_complete", "Join Dr. Timothy's Zoom 3"),
            ("timothy_assignment_complete", "Complete Timothy's Assignment"),
            ("beatrice_zoom3_complete", "Join Dr. Beatrice's Zoom 3"),
            ("act3_logoff_complete", "Log Off Act 3"),
        ]

        for flag, task_text in mapping:
            if self.get_flag(flag):
                self.complete_task(task_text)

    # ------------------------------------------------------------
    # Resonance (global counter)
    # ------------------------------------------------------------
    def get_resonance(self):
        return int(self.data.get("resonance", 0))

    def set_resonance(self, value: int):
        self.data["resonance"] = int(value)
        self.save()

    def add_resonance(self, delta: int):
        self.data["resonance"] = self.get_resonance() + int(delta)
        self.save()

    def award_resonance_for_flag(self, flag_key: str, points: int = 1):
        """
        Award resonance once when a specific flag is complete.
        Safe to call multiple times; it only applies the first time.
        """
        if not self.get_flag(flag_key):
            return False
        seen = self.data.setdefault("resonance_flags_seen", [])
        if flag_key in seen:
            return False
        self.data["resonance"] = self.get_resonance() + int(points)
        seen.append(flag_key)
        self.save()
        return True

    def sync_resonance_from_flags(self, flag_points: dict):
        """
        Backfill resonance based on a mapping of {flag_key: points}.
        Useful for migrating older saves.
        """
        changed = False
        for flag_key, points in flag_points.items():
            if self.award_resonance_for_flag(flag_key, points):
                changed = True
        return changed

    # ------------------------------------------------------------
    # Player + Trust
    # ------------------------------------------------------------
    def player_name(self):
        return self.data.get("player_name", "Student")

    def change_trust(self, delta: float):
        """
        Modify global trust (0.0–1.0), clamped.

        Use this DIRECTLY from scenes, e.g.:
            self.state.change_trust(-0.5)
            self.state.change_trust(+0.2)

        Act 3 has an additional act3_trust track; this function
        updates the global trust bar that UI scenes read.
        """
        trust = float(self.data.get("trust", 0.5))
        trust = max(0.0, min(1.0, trust + float(delta)))
        self.data["trust"] = trust
        self.save()

    def get_trust(self):
        return float(self.data.get("trust", 0.5))

    # Legacy alias used by some Act 4 scenes
    def trust(self):
        return self.get_trust()

    # ------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------
    def get_setting(self, key: str, default=None):
        settings = self.data.setdefault("settings", {})
        return settings.get(key, default)

    def set_setting(self, key: str, value):
        settings = self.data.setdefault("settings", {})
        settings[key] = value
        self.save()

    # --- Act 3 Special Trust System ---
    def get_betrayal_state(self):
        return self.get_flag("act3_betrayal", False)

    def set_betrayal(self, betrayed: bool):
        """
        Mark whether the player betrayed Lottie in Act 3.
        This also adjusts both global trust and act3_trust.
        """
        self.set_flag("act3_betrayal", betrayed)

        act3_trust = float(self.data.get("act3_trust", 0.5))
        if betrayed:
            self.change_trust(-0.5)
            act3_trust = max(0.0, act3_trust - 0.5)
        else:
            self.change_trust(+0.3)
            act3_trust = min(1.0, act3_trust + 0.3)

        self.data["act3_trust"] = act3_trust
        self.save()

    def get_act3_trust(self):
        return float(self.data.get("act3_trust", 0.5))

    # ------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------
    def tasks(self):
        return self.data.get("tasks", [])

    def add_task(self, text: str):
        """Add a new task if not already present."""
        tasks = self.data.setdefault("tasks", [])
        if not any(t["text"] == text for t in tasks):
            tasks.append({"text": text, "done": False})
            self.save()
        # NOTE: UI popups should be triggered by desktop scenes, not here.

    def complete_task(self, text: str):
        """Mark a task as complete (if present)."""
        changed = False
        for t in self.data.get("tasks", []):
            if t["text"] == text and not t.get("done", False):
                t["done"] = True
                changed = True
        if changed:
            self.save()
        # NOTE: UI popups should be triggered externally if desired.

    def active_task(self):
        """Return the first incomplete task text, or None."""
        for t in self.data.get("tasks", []):
            if not t.get("done", False):
                return t["text"]
        return None

    def all_tasks_complete(self):
        """
        Return True if all key Act 1 flags are marked complete (for logoff trigger).
        This is kept for backward compatibility with Act 1 flow.
        """
        f = self.data.get("flags", {})
        return (
            f.get("timothy_zoom_complete")
            and f.get("lottie_assignment1_complete")
            and f.get("beatrice_zoom_complete")
            and f.get("lottie_assignment2_complete")
        )


# Optional CLI utilities for debugging saves quickly
if __name__ == "__main__":
    gs = GameState()
    print("[GameState] Flags:")
    for k in sorted(gs.data.get("flags", {}).keys()):
        print(f"  {k}: {gs.get_flag(k)}")

