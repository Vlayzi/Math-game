from __future__ import annotations

import pygame

from config import SOUNDS_DIR
from core.resource_manager import ResourceManager


class AudioManager:
    def __init__(self, resources: ResourceManager) -> None:
        self.resources = resources
        self.master_volume = 0.65

    def play_ui(self, name: str, volume: float = 1.0) -> None:
        sound = self.resources.sound(SOUNDS_DIR / name)
        sound.set_volume(self.master_volume * volume)
        sound.play()

    def set_master(self, value: float) -> None:
        self.master_volume = max(0.0, min(1.0, value))

    def stop_all(self) -> None:
        pygame.mixer.stop()
