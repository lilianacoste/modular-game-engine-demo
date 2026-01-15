"""
Game state management for a modular, state-driven application.

This file contains a representative implementation extracted from a larger
proprietary project and is provided for portfolio demonstration purposes.
"""

import json
import os

class GameState:
    def __init__(self, save_file="save/state.json"):
        self.save_file = save_file
        if os.path.exists(save_file):
            with open(save_file, "r") as f:
                self.data = json.load(f)
        else:
            # Try to get OS login name
            try:
                player_name = os.getlogin()
            except Exception:
                player_name = "Student"

            # Initial state
            self.data = {
                "player_name": player_name,
                "act": 1,
                "trust": 0.5,
                "flags": {},
                "tasks": [
                    {"text": "Join Dr. Timothy's Zoom", "done": False},
                    {"text": "Launch Lottie AI", "done": False},
                    {"text": "Join Dr. Beatrice's Zoom", "done": False},
                    {"text": "Complete Lottie Assignment 2", "done": False},
                    {"text": "Log off Desktop", "done": False}
                ]
            }
            self.save()

    # ---------- persistence ----------
    def save(self):
        os.makedirs(os.path.dirname(self.save_file), exist_ok=True)
        with open(self.save_file, "w") as f:
            json.dump(self.data, f, indent=2)

    # ---------- player name ----------
    def player_name(self):
        return self.data.get("player_name", "Student")

    # ---------- flags ----------
    def get_flag(self, key, default=False):
        return self.data["flags"].get(key, default)

    def set_flag(self, key, value=True):
        self.data["flags"][key] = value
        self.save()

    # ---------- trust ----------
    def change_trust(self, delta):
        self.data["trust"] = max(0, min(1, self.data.get("trust", 0.5) + delta))
        self.save()

    def trust(self):
        return self.data.get("trust", 0.5)

    # ---------- tasks ----------
    def tasks(self):
        return self.data["tasks"]

    def add_task(self, text):
        if not any(t["text"] == text for t in self.data["tasks"]):
            self.data["tasks"].append({"text": text, "done": False})
            self.save()

    def complete_task(self, text):
        for t in self.data["tasks"]:
            if t["text"] == text:
                t["done"] = True
        self.save()

    def active_task(self):
        for t in self.data["tasks"]:
            if not t["done"]:
                return t["text"]
        return None
    
    def all_tasks_complete(self):
        """Check if all critical tasks are done (used to trigger Log Off)."""
        return (
            self.get_flag("timothy_zoom_complete") and
            self.get_flag("lottie_assignment1_complete") and
            self.get_flag("beatrice_zoom_complete") and
            self.get_flag("lottie_assignment2_complete")
        )
