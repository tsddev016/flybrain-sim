"""Reward helpers for future training stages."""
from __future__ import annotations

def compute_step_reward(energy_delta, hunger_delta, thirst_delta, ate, drank, collided):
    r = 0.0
    if ate:
        r += 8.0
    if drank:
        r += 5.0
    r += energy_delta * 0.15
    r -= max(0.0, hunger_delta) * 0.05
    r -= max(0.0, thirst_delta) * 0.05
    if collided:
        r -= 0.5
    r -= 0.01
    return r
