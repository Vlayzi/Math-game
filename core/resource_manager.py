from __future__ import annotations

from pathlib import Path

import pygame


class ResourceManager:
    def __init__(self) -> None:
        self._images: dict[Path, pygame.Surface] = {}
        self._fonts: dict[tuple[Path | None, int], pygame.font.Font] = {}
        self._sounds: dict[Path, pygame.mixer.Sound] = {}

    def image(self, path: Path) -> pygame.Surface:
        if path not in self._images:
            self._images[path] = pygame.image.load(path.as_posix()).convert_alpha()
        return self._images[path]

    def font(self, size: int, path: Path | None = None) -> pygame.font.Font:
        key = (path, size)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(path.as_posix() if path else None, size)
        return self._fonts[key]

    def sound(self, path: Path) -> pygame.mixer.Sound:
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path.as_posix())
        return self._sounds[path]
