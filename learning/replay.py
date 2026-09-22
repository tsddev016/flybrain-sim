"""
Simple experience replay buffer (for Level 2+).
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Optional
import random


@dataclass
class Transition:
    sensors: dict
    action: str
    reward: float
    next_sensors: dict
    done: bool


class ReplayBuffer:
    def __init__(self, capacity: int = 10_000):
        self.buffer: Deque[Transition] = deque(maxlen=capacity)

    def push(self, transition: Transition):
        self.buffer.append(transition)

    def sample(self, batch_size: int) -> List[Transition]:
        return random.sample(list(self.buffer), min(batch_size, len(self.buffer)))

    def __len__(self) -> int:
        return len(self.buffer)
