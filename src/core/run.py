# placeholder for run.pyimport pygame
import pygame
from src.scene_manager import SceneManager
from src.window_manager import WindowManager
from src.game_state import GameState
from src.scenes.main_menu import MainMenuScene
from src.scenes.warning_screen import WarningScreenScene

def main():
    pygame.init()
    info = pygame.display.Info()
    screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN | pygame.SCALED)
    clock = pygame.time.Clock()

    game_state = GameState()
    scene_manager = SceneManager()
    window_manager = WindowManager(screen, state=game_state)
    window_manager.game_state = game_state
    window_manager.scene_manager = scene_manager

    # Start at Warning Screen before Main Menu
    start_scene = WarningScreenScene(scene_manager, window_manager)
    scene_manager.set(start_scene)

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_manager.handle_event(event)

        scene_manager.update(dt)
        scene_manager.draw(screen, dt)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()



if __name__ == "__main__":
    main()
