"""
Corpo da mosca artificial: estado + sensores + cerebro + motor.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Optional

from simulator.world import World
from fly.sensors import Sensors, SensorReading
from fly.brain import FlyBrain, MotorCommand


@dataclass
class FlyState:
    x: float
    y: float
    heading: float
    energy: float = 100.0
    hunger: float = 10.0
    thirst: float = 10.0
    fear: float = 0.0
    alive: bool = True
    age: int = 0


class Fly:
    def __init__(
        self,
        x: float = 400.0,
        y: float = 300.0,
        heading: float = 0.0,
        seed: Optional[int] = None,
    ):
        self.state = FlyState(x=x, y=y, heading=heading)
        self.sensors = Sensors()
        self.brain = FlyBrain(seed=seed)
        self.last_command: Optional[MotorCommand] = None
        self.last_sensors: Optional[SensorReading] = None
        self.radius = 7.0
        self.max_speed = 2.8
        self.turn_rate = 1.0

        self.energy_drain_move = 0.035
        self.energy_drain_rest = 0.008
        self.hunger_rate = 0.045
        self.thirst_rate = 0.038

        self.eat_cooldown = 0
        self.drink_cooldown = 0

    def step(self, world: World) -> dict:
        if not self.state.alive:
            return {"alive": False}

        self.state.age += 1
        s = self.state

        reading = self.sensors.sense(
            world, s.x, s.y, s.heading, s.energy, s.hunger, s.thirst, s.fear
        )
        self.last_sensors = reading

        if reading.threat_strength > 0.15:
            s.fear = min(1.0, max(s.fear, reading.threat_strength * 1.1))
        reading.fear = s.fear

        cmd = self.brain.decide(reading, s.x, s.y, s.heading)
        self.last_command = cmd

        log = self._execute(cmd, world)
        self._metabolize(cmd)

        if s.energy <= 0:
            s.alive = False
            log["event"] = "morreu_exausta"

        return log

    def _execute(self, cmd: MotorCommand, world: World) -> dict:
        s = self.state
        log = {"action": cmd.action, "reason": cmd.reason, "reward": 0.0}

        if cmd.action == "rest":
            s.energy = min(100.0, s.energy + 0.4)
            return log

        s.heading = (s.heading + cmd.turn * self.turn_rate) % 360.0

        if cmd.forward > 0.01:
            rad = math.radians(s.heading)
            dx = math.cos(rad) * self.max_speed * cmd.forward
            dy = math.sin(rad) * self.max_speed * cmd.forward
            nx, ny = s.x + dx, s.y + dy
            nx, ny = world.resolve_collision(nx, ny, self.radius)
            s.x, s.y = nx, ny

        if self.eat_cooldown > 0:
            self.eat_cooldown -= 1
        if self.drink_cooldown > 0:
            self.drink_cooldown -= 1

        if cmd.action == "eat" and self.eat_cooldown <= 0:
            reward = self._try_eat(world)
            log["reward"] = reward
            if reward > 0:
                log["event"] = "comeu"
                self.eat_cooldown = 25
                self.brain.notify_outcome("ate", reward, s.x, s.y)
        elif cmd.action == "drink" and self.drink_cooldown <= 0:
            reward = self._try_drink(world)
            log["reward"] = reward
            if reward > 0:
                log["event"] = "bebeu"
                self.drink_cooldown = 30
                self.brain.notify_outcome("drank", reward, s.x, s.y)

        if self.last_sensors and self.last_sensors.food_strength > 1.0:
            self.brain.notify_outcome("food_detected", 0.0, s.x, s.y)
        if self.last_sensors and self.last_sensors.water_strength > 1.0:
            self.brain.notify_outcome("water_detected", 0.0, s.x, s.y)

        return log

    def _try_eat(self, world: World) -> float:
        for food in world.foods:
            if not food.active:
                continue
            dist = math.hypot(self.state.x - food.x, self.state.y - food.y)
            if dist < self.radius + food.radius + 4:
                gain = food.value
                self.state.hunger = max(0.0, self.state.hunger - gain * 1.8)
                self.state.energy = min(100.0, self.state.energy + gain * 0.9)
                food.active = False
                world.reset_food(food)
                return gain * 0.4
        return 0.0

    def _try_drink(self, world: World) -> float:
        for water in world.waters:
            if not water.active:
                continue
            dist = math.hypot(self.state.x - water.x, self.state.y - water.y)
            if dist < self.radius + water.radius + 4:
                gain = water.value
                self.state.thirst = max(0.0, self.state.thirst - gain * 1.6)
                self.state.energy = min(100.0, self.state.energy + gain * 0.25)
                return gain * 0.3
        return 0.0

    def _metabolize(self, cmd: MotorCommand):
        s = self.state
        if cmd.action == "rest" or cmd.forward < 0.05:
            s.energy -= self.energy_drain_rest
        else:
            s.energy -= self.energy_drain_move * (0.6 + 0.4 * cmd.forward)

        s.hunger = min(100.0, s.hunger + self.hunger_rate)
        s.thirst = min(100.0, s.thirst + self.thirst_rate)

        s.fear = max(0.0, s.fear * 0.96)

        if s.hunger > 85:
            s.energy -= 0.05
        if s.thirst > 85:
            s.energy -= 0.06
