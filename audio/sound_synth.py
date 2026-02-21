from __future__ import annotations

import math
import struct
import wave
from pathlib import Path


SAMPLE_RATE = 44100


def _write_wave(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(path.as_posix(), "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for sample in samples:
            clipped = max(-1.0, min(1.0, sample))
            frames.extend(struct.pack("<h", int(clipped * 32767)))
        wav_file.writeframes(bytes(frames))


def _envelope(i: int, total: int, attack: float = 0.08, decay: float = 0.2) -> float:
    t = i / max(total, 1)
    if t < attack:
        return t / attack
    tail = 1 - t
    return max(0.0, min(1.0, tail / decay))


def _tone(freq: float, seconds: float, volume: float = 0.6, wobble: float = 0.0) -> list[float]:
    total = int(seconds * SAMPLE_RATE)
    samples: list[float] = []
    for i in range(total):
        t = i / SAMPLE_RATE
        f = freq + math.sin(t * 17) * wobble
        sample = math.sin(2 * math.pi * f * t) * _envelope(i, total) * volume
        samples.append(sample)
    return samples


def _mix(*tracks: list[float]) -> list[float]:
    max_len = max(len(t) for t in tracks)
    out = [0.0] * max_len
    for track in tracks:
        for i, val in enumerate(track):
            out[i] += val
    return [v / len(tracks) for v in out]


def ensure_ui_sounds(sound_dir: Path) -> None:
    sounds = {
        "hover.wav": _mix(_tone(760, 0.12, 0.35, 9), _tone(1020, 0.12, 0.18, 4)),
        "click.wav": _mix(_tone(440, 0.08, 0.5), _tone(660, 0.18, 0.3, 20)),
        "error.wav": _mix(_tone(220, 0.25, 0.35), _tone(180, 0.25, 0.25)),
        "menu_open.wav": _mix(_tone(440, 0.18, 0.35), _tone(660, 0.2, 0.35), _tone(880, 0.22, 0.25)),
        "whoosh.wav": _mix(_tone(540, 0.28, 0.22, 60), _tone(720, 0.28, 0.2, 90)),
    }
    for name, data in sounds.items():
        path = sound_dir / name
        if not path.exists():
            _write_wave(path, data)
