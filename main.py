from __future__ import annotations

import sys

import pygame

from audio.audio_manager import AudioManager
from audio.sound_synth import ensure_ui_sounds
from config import FPS, SOUNDS_DIR, TITLE, WINDOW_HEIGHT, WINDOW_WIDTH
from core.resource_manager import ResourceManager
from core.scene_manager import SceneManager
from scenes.menu_scene import MenuScene


def main() -> None:
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    ensure_ui_sounds(SOUNDS_DIR)

    resources = ResourceManager()
    audio = AudioManager(resources)
    scene = SceneManager(MenuScene(resources, audio))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            scene.handle_event(event)

        scene.update(dt)
        scene.draw(screen)
        pygame.display.flip()

    audio.stop_all()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
