"""Sons procedurais de insetos e eventos (sem arquivos externos)."""
from __future__ import annotations
import math
import random
from typing import Dict, Optional

import numpy as np

try:
    import pygame
    HAS_PYGAME = True
except ImportError:
    HAS_PYGAME = False


def _tone(freq: float, ms: int, vol: float = 0.2, wave: str = "sine"):
    if not HAS_PYGAME:
        return None
    rate = 22050
    n = int(rate * ms / 1000)
    t = np.linspace(0, ms / 1000.0, n, False)
    if wave == "sine":
        sig = np.sin(2 * np.pi * freq * t)
    elif wave == "buzz":
        sig = np.sign(np.sin(2 * np.pi * freq * t)) * 0.4 + np.sin(2 * np.pi * freq * 2 * t) * 0.3
    else:
        sig = np.sin(2 * np.pi * freq * t)
    env = np.linspace(1.0, 0.05, n)
    audio = np.int16(np.clip(sig * env * vol, -1, 1) * 32767)
    stereo = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))


def _chirp(start_f: float, end_f: float, ms: int, vol: float = 0.15):
    if not HAS_PYGAME:
        return None
    rate = 22050
    n = int(rate * ms / 1000)
    t = np.linspace(0, ms / 1000.0, n, False)
    freqs = np.linspace(start_f, end_f, n)
    phase = np.cumsum(2 * np.pi * freqs / rate)
    sig = np.sin(phase)
    env = np.concatenate([np.linspace(0, 1, n // 5), np.linspace(1, 0, n - n // 5)])
    audio = np.int16(np.clip(sig * env * vol, -1, 1) * 32767)
    stereo = np.column_stack((audio, audio))
    return pygame.sndarray.make_sound(np.ascontiguousarray(stereo))


class SoundManager:
    def __init__(self):
        self.enabled = False
        self.sounds: Dict[str, object] = {}
        if not HAS_PYGAME:
            return
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.sounds = {
                "eat": _tone(720, 90, 0.25),
                "drink": _tone(480, 110, 0.22),
                "fear": _tone(160, 140, 0.3, "buzz"),
                "mate": _chirp(400, 900, 180, 0.22),
                "sleep": _tone(220, 250, 0.12),
                "hatch": _chirp(500, 1200, 200, 0.2),
                "spider_hunt": _tone(120, 100, 0.28, "buzz"),
                "nest": _tone(300, 120, 0.15),
                "buzz": _tone(180, 80, 0.08, "buzz"),
                "chirp": _chirp(900, 1400, 60, 0.1),
            }
            self.enabled = True
        except Exception:
            self.enabled = False

    def play(self, name: str):
        if not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd is not None:
            try:
                snd.play()
            except Exception:
                pass

    def ambient_tick(self, frame: int):
        if not self.enabled:
            return
        if frame % 180 == 0 and random.random() < 0.4:
            self.play("chirp")
        if frame % 220 == 0 and random.random() < 0.3:
            self.play("buzz")
