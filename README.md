# Modular Game Systems (Python)

This repository contains selected system code from a larger game project I’m actively developing.  
I’m sharing these files to show **how I structure applications, manage state, and handle complex flow**, not to release a full or playable game.

The complete project (story, assets, and full gameplay) is proprietary and intentionally not included.

---

## What This Is

At its core, this project is a **state-driven application** built in Python using Pygame.  
While the end product is a narrative game, most of the interesting work happens at the systems level — managing state, routing flow, coordinating UI layers, and keeping everything modular as complexity grows.

That’s the part this repository focuses on.

---

## Key Systems in This Repo

### Game State
The `GameState` module acts as the single source of truth for the application.

It handles things like:
- Persistent state stored as JSON
- Progression flags and feature gating
- Task tracking across different phases
- Backward compatibility for older saves as the project evolves

This file grew over time as the project expanded, which is why it includes migration logic and defensive checks.

---

### Scene Management
The `SceneManager` controls which scene is active and how transitions happen.

Scenes are treated as independent units and managed through a stack, which makes it easier to pause, replace, or resume parts of the experience without tightly coupling everything together.

Progression is also recorded here so state and navigation stay in sync.

---

### Scene Flow Routing
Rather than letting scenes decide what comes next, routing logic lives in a dedicated flow module.

For Act 1, scene progression is determined entirely by flags in `GameState`.  
This keeps narrative flow predictable and avoids scattering conditional logic across multiple files.

Conceptually, this behaves like a finite state controller.

---

### Scene Registry
Scenes are registered by name in a central registry.

This allows transitions to reference scenes symbolically instead of importing them directly, which keeps routing logic decoupled from implementations and makes the system easier to extend.

---

### Window and Overlay Management
The `WindowManager` handles layered UI behavior:
- Active windows or apps
- Non-blocking overlays like notifications
- Event routing from top to bottom
- Explicit draw ordering

This was designed to behave more like a desktop-style UI than a traditional single-screen game.

---

### Application Entry Point
The `run.py` file is intentionally minimal.

Its job is to:
- Initialize core systems
- Configure the display
- Wire managers together
- Hand control over to the scene system

All real behavior lives outside the entry point.

---

## Why This Repo Is Partial

The full project is still in development and includes original narrative content that I’m not releasing publicly.

This repository exists to demonstrate:
- How I think about architecture
- How I manage shared state
- How I structure flow and control logic
- How systems evolve as a project grows

Publishing a focused subset like this is a deliberate choice and mirrors how proprietary or internal projects are often shared in a portfolio context.

---

## What You Won’t Find Here

- No assets (art, audio, dialogue)
- No full gameplay loop
- No story scripts or puzzle logic
- No save files

This code is not meant to be run as a complete application.

---

## Tech Stack

- Python
- Pygame
- JSON-based persistence
- Modular, state-driven design

---

## License

All rights reserved.

This code is shared for portfolio and demonstration purposes only.  
It may not be used, copied, or redistributed without permission.

---

## Status

This is an **active project**.  
As systems evolve, this repository may be updated with additional representative components, but it will remain a curated subset rather than a full release.
