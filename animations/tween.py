from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


def ease_out_back(t: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def ease_in_out_sine(t: float) -> float:
    import math

    return -(math.cos(math.pi * t) - 1) / 2


@dataclass
class Tween:
    duration: float
    start: float
    end: float
    easing: Callable[[float], float]
    elapsed: float = 0.0
    done: bool = False

    def update(self, dt: float) -> float:
        if self.done:
            return self.end
        self.elapsed += dt
        t = min(self.elapsed / self.duration, 1.0)
        value = self.start + (self.end - self.start) * self.easing(t)
        if t >= 1:
            self.done = True
        return value
