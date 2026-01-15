# =========================================
# file: src/core/scene_registry.py
"""
Global scene registry for resolving scenes by string key.

Provides a centralized mapping between scene identifiers and their
implementations, enabling state-driven routing and decoupled scene loading.
Extracted from a larger proprietary project for portfolio demonstration.
"""

# =========================================

# -------------------------
# ACT 1 SCENES
# -------------------------
from src.scenes.act1.application_scene import ApplicationScene
from src.scenes.act1.virtual_desktop import VirtualDesktop
from src.scenes.act1.dormscene import DormScene
from src.scenes.act1.logoff_scene import LogOffScene
from src.scenes.act1.bluebird_terminal import BluebirdTerminalScene
from src.scenes.act1.bluebird_chat import BlueBirdChat
from src.scenes.act1.dorm_after_bluebird import DormAfterBluebirdScene
from src.scenes.act1.hallway.game import HallwayScene
from src.scenes.act1.control_room import ControlRoomScene
from src.scenes.act1.act1_closing_scene import Act1ClosingScene
from src.scenes.act1.go_bed_scene import GoBedScene

# -------------------------
# ACT 2 DESKTOP + APPS
# -------------------------
from src.scenes.act2.act2_desktop import VirtualDesktopAct2
from src.apps.zoom_anand import ZoomAnand
from src.apps.zoom_rachel import ZoomRachel
from src.scenes.act2.lottie_assignment_anand import LottieAnandAssignment
from src.scenes.act2.lottie_assignment_rachel import LottieRachelAssignment
from src.scenes.act2.lottie_lab_intro import LottieLabIntroScene

# -------------------------
# LAB NIGHT MISSION
# -------------------------
from src.scenes.lab.lab_signal_relay import LabSignalRelayScene

# -------------------------
# ACT 2 NIGHT SCENES
# -------------------------
from src.scenes.act2.dorm_night2 import DormNight2Scene
from src.scenes.act2.update_lottie2 import UpdateLottie2Scene

# Dream sequence
from src.scenes.act2.dream_sequence_charlotte import DreamSequenceCharlotte

# -------------------------
# SHARED APPS
# -------------------------
from src.apps.zoom_timothy import ZoomTimothy
from src.apps.zoom_beatrice import ZoomBeatrice
from src.apps.log_viewer import LogViewer
from src.apps.lottie import LottieApp

#ACT 3
from src.scenes.act3.act3_desktop import Act3DesktopScene
from src.scenes.act3.act3_logoff_router import Act3_LogOffRouterScene
from src.scenes.act3.zoom_timothy_act3 import ZoomTimothy3
from src.scenes.act3.lottie_assignment_timothy import TimothySecurityAssignment
from src.scenes.act3.zoom_beatrice_act3 import ZoomBeatriceAct3
from src.scenes.act3.dormscene3 import DormScene3
from src.scenes.act3.lottie_instruction_scene import LottieInstructionScene
from src.scenes.act3.metaforest_scene import MetaForestScene


# =========================================
# SCENE REGISTRY
# =========================================
SCENES = {

    # ===== ACT 1 =====
    "act1/application": ApplicationScene,
    "act1/desktop": VirtualDesktop,
    "act1/logoff": LogOffScene,
    "act1/dorm": DormScene,
    "act1/bluebird_terminal": BluebirdTerminalScene,
    "act1/bluebird_chat": BlueBirdChat,
    "act1/dorm_after_bluebird": DormAfterBluebirdScene,
    "act1/hallway_game": HallwayScene,
    "act1/control_room": ControlRoomScene,
    "act1/closing": Act1ClosingScene,
    "act1/go_to_bed": GoBedScene,

    # ===== ACT 2 =====
    "act2/desktop": VirtualDesktopAct2,
    "act2/zoom_anand": ZoomAnand,
    "act2/anand_assignment": LottieAnandAssignment,
    "act2/zoom_rachel": ZoomRachel,
    "act2/rachel_assignment": LottieRachelAssignment,
    "act2/lab_intro": LottieLabIntroScene,

    # ===== LAB NIGHT MISSION =====
    "lab/signal_relay": LabSignalRelayScene,

    # ===== ACT 2 NIGHT EVENTS =====
    "act2/dorm_night2": DormNight2Scene,
    "act2/update_lottie2": UpdateLottie2Scene,
    "act2/dream_charlotte": DreamSequenceCharlotte,
    # ===== ACT 3 =====
    "act3/desktop": Act3DesktopScene,
    "act3/logoff_router": Act3_LogOffRouterScene,
    "act3/zoom_timothy3": ZoomTimothy3,
    "act3/timothy_assignment": TimothySecurityAssignment,
    "act3/zoom_beatrice3": ZoomBeatriceAct3,
    "act3/dorm": DormScene3,
    "act3/lottie_instruction": LottieInstructionScene,
    "act3/metaforest": MetaForestScene,
    # ===== SHARED APPS =====
    "log_viewer": LogViewer,
    "zoom_timothy": ZoomTimothy,
    "zoom_beatrice": ZoomBeatrice,
    "lottie": LottieApp,
    
    #FOREST MINI GAME
}


def get_scene_by_name(name: str):
    """Return the scene class from string identifier."""
    return SCENES.get(name)


_SCENE_CLASS_TO_NAME = {v: k for k, v in SCENES.items()}


def get_scene_name_by_class(scene_class):
    """Return the scene name for a class, or None if not registered."""
    return _SCENE_CLASS_TO_NAME.get(scene_class)
