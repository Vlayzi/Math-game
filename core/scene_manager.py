from __future__ import annotations


class SceneManager:
    def __init__(self, initial_scene) -> None:
        self.current_scene = initial_scene

    def handle_event(self, event) -> None:
        self.current_scene.handle_event(event)

    def update(self, dt: float) -> None:
        self.current_scene.update(dt)

    def draw(self, surface) -> None:
        self.current_scene.draw(surface)
