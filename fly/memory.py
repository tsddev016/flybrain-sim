"""
Simple short-term + associative memory inspired by insect mushroom bodies.
Not a full neural simulation – a practical, inspectable memory module.
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, List, Optional, Tuple
import time


@dataclass
class MemoryEvent:
    timestamp: float
    kind: str                       # "food_found", "obstacle", "ate", "drank", "wander"
    x: float
    y: float
    strength: float = 1.0
    extra: dict = field(default_factory=dict)


class Memory:
    def __init__(self, short_term_size: int = 40, max_landmarks: int = 12):
        self.short_term: Deque[MemoryEvent] = deque(maxlen=short_term_size)
        self.landmarks: Dict[str, List[Tuple[float, float, float]]] = {
            "food": [],
            "water": [],
        }
        self.max_landmarks = max_landmarks
        self.last_goal: Optional[str] = None
        self.last_decision: str = "explore"
        self.total_rewards: float = 0.0
        self.steps_alive: int = 0

    def add(self, kind: str, x: float, y: float, strength: float = 1.0, **extra):
        evt = MemoryEvent(
            timestamp=time.time(),
            kind=kind,
            x=x,
            y=y,
            strength=strength,
            extra=extra,
        )
        self.short_term.append(evt)

        if kind in ("food_found", "ate") and strength > 0.3:
            self._add_landmark("food", x, y, strength)
        elif kind in ("water_found", "drank") and strength > 0.3:
            self._add_landmark("water", x, y, strength)

    def _add_landmark(self, category: str, x: float, y: float, strength: float):
        lst = self.landmarks[category]
        for i, (lx, ly, s) in enumerate(lst):
            if (lx - x) ** 2 + (ly - y) ** 2 < 40 ** 2:
                lst[i] = (lx, ly, min(2.0, s + 0.3))
                return
        lst.append((x, y, strength))
        if len(lst) > self.max_landmarks:
            lst.sort(key=lambda t: t[2])
            self.landmarks[category] = lst[-self.max_landmarks :]

    def nearest_landmark(
        self, category: str, x: float, y: float
    ) -> Optional[Tuple[float, float, float]]:
        best = None
        best_d2 = float("inf")
        for lx, ly, s in self.landmarks.get(category, []):
            d2 = (lx - x) ** 2 + (ly - y) ** 2
            if d2 < best_d2:
                best_d2 = d2
                best = (lx, ly, s)
        return best

    def recent_events(self, n: int = 8) -> List[MemoryEvent]:
        return list(self.short_term)[-n:]

    def summary(self) -> dict:
        return {
            "short_term_count": len(self.short_term),
            "food_landmarks": len(self.landmarks["food"]),
            "water_landmarks": len(self.landmarks["water"]),
            "last_decision": self.last_decision,
            "total_rewards": round(self.total_rewards, 2),
            "steps": self.steps_alive,
        }
