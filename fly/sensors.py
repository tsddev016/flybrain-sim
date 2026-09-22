"""
Sensores limitados inspirados na percepcao de insetos.
A mosca NAO recebe coordenadas absolutas dos objetos.
Recebe sinais relativos, ruidosos e restritos ao campo de visao.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Optional

from simulator.world import World, WorldObject


@dataclass
class SensorReading:
    food_distance: float = 999.0
    food_angle: float = 0.0
    food_strength: float = 0.0
    water_distance: float = 999.0
    water_angle: float = 0.0
    water_strength: float = 0.0
    obstacle_distance: float = 999.0
    obstacle_angle: float = 0.0
    wall_ahead: float = 999.0
    wall_left: float = 999.0
    wall_right: float = 999.0
    wall_far_left: float = 999.0
    wall_far_right: float = 999.0
    threat_distance: float = 999.0
    threat_angle: float = 0.0
    threat_strength: float = 0.0
    light_level: float = 0.5
    energy: float = 100.0
    hunger: float = 0.0
    thirst: float = 0.0
    fear: float = 0.0
    visual_left: float = 0.0
    visual_center: float = 0.0
    visual_right: float = 0.0


class Sensors:
    def __init__(self, max_smell_range: float = 200.0, fov_deg: float = 130.0, threat_range: float = 160.0):
        self.max_smell_range = max_smell_range
        self.fov_deg = fov_deg
        self.threat_range = threat_range

    def sense(self, world: World, x: float, y: float, heading_deg: float, energy: float, hunger: float, thirst: float, fear: float) -> SensorReading:
        reading = SensorReading(energy=energy, hunger=hunger, thirst=thirst, fear=fear, light_level=world.light_intensity_at(x, y))
        self._update_attraction(reading, world.foods, x, y, heading_deg, "food")
        self._update_attraction(reading, world.waters, x, y, heading_deg, "water")
        self._update_obstacle(reading, world.obstacles, x, y, heading_deg)
        self._update_walls(reading, world, x, y, heading_deg)
        self._update_threat(reading, world, x, y, heading_deg)
        self._update_visual_sectors(reading, world, x, y, heading_deg)
        return reading

    def _relative_angle(self, dx: float, dy: float, heading_deg: float) -> float:
        abs_angle = math.degrees(math.atan2(dy, dx))
        rel = abs_angle - heading_deg
        while rel > 180:
            rel -= 360
        while rel < -180:
            rel += 360
        return rel

    def _update_attraction(self, reading: SensorReading, objects: List[WorldObject], x: float, y: float, heading: float, kind: str):
        best_strength = 0.0
        best_dist = 999.0
        best_angle = 0.0
        for obj in objects:
            if not obj.active:
                continue
            dx, dy = obj.x - x, obj.y - y
            dist = math.hypot(dx, dy)
            if dist > self.max_smell_range or dist < 1e-3:
                continue
            strength = obj.value * (1.0 / (1.0 + (dist / 45.0) ** 2))
            angle = self._relative_angle(dx, dy, heading)
            if abs(angle) > self.fov_deg / 2:
                strength *= 0.30
            if strength > best_strength:
                best_strength = strength
                best_dist = dist
                best_angle = angle
        if kind == "food":
            reading.food_distance = best_dist
            reading.food_angle = best_angle
            reading.food_strength = best_strength
        else:
            reading.water_distance = best_dist
            reading.water_angle = best_angle
            reading.water_strength = best_strength

    def _update_obstacle(self, reading: SensorReading, obstacles: List[WorldObject], x: float, y: float, heading: float):
        best_dist = 999.0
        best_angle = 0.0
        for obs in obstacles:
            if not obs.active:
                continue
            dx, dy = obs.x - x, obs.y - y
            dist = math.hypot(dx, dy) - obs.radius
            if dist < 0:
                dist = 0.0
            if dist > 110:
                continue
            angle = self._relative_angle(dx, dy, heading)
            if abs(angle) < 100 and dist < best_dist:
                best_dist = dist
                best_angle = angle
        reading.obstacle_distance = best_dist
        reading.obstacle_angle = best_angle

    def _update_walls(self, reading: SensorReading, world: World, x: float, y: float, heading: float):
        max_d = 140.0
        reading.wall_ahead = self._raycast(world, x, y, heading, max_d)
        reading.wall_left = self._raycast(world, x, y, heading - 35, max_d)
        reading.wall_right = self._raycast(world, x, y, heading + 35, max_d)
        reading.wall_far_left = self._raycast(world, x, y, heading - 70, max_d)
        reading.wall_far_right = self._raycast(world, x, y, heading + 70, max_d)

    def _raycast(self, world: World, x: float, y: float, heading_deg: float, max_dist: float) -> float:
        rad = math.radians(heading_deg)
        dx, dy = math.cos(rad), math.sin(rad)
        min_t = max_dist
        for w in world.walls:
            t = self._ray_segment_intersect(x, y, dx, dy, w.x1, w.y1, w.x2, w.y2)
            if t is not None and 0 < t < min_t:
                min_t = t
        return min_t

    @staticmethod
    def _ray_segment_intersect(ox, oy, dx, dy, x1, y1, x2, y2) -> Optional[float]:
        sx, sy = x2 - x1, y2 - y1
        denom = dx * sy - dy * sx
        if abs(denom) < 1e-8:
            return None
        t = ((x1 - ox) * sy - (y1 - oy) * sx) / denom
        u = ((x1 - ox) * dy - (y1 - oy) * dx) / denom
        if t >= 0 and 0 <= u <= 1:
            return t
        return None

    def _update_threat(self, reading: SensorReading, world: World, x: float, y: float, heading: float):
        best_dist = 999.0
        best_angle = 0.0
        best_str = 0.0
        for sp in world.spiders:
            dist = sp.distance_to(x, y)
            if dist > self.threat_range:
                continue
            dx, dy = sp.x - x, sp.y - y
            angle = self._relative_angle(dx, dy, heading)
            strength = 1.0 - (dist / self.threat_range)
            if abs(angle) > self.fov_deg / 2:
                strength *= 0.55
            if strength > best_str:
                best_str = strength
                best_dist = dist
                best_angle = angle
        reading.threat_distance = best_dist
        reading.threat_angle = best_angle
        reading.threat_strength = best_str

    def _update_visual_sectors(self, reading: SensorReading, world: World, x: float, y: float, heading: float):
        left = center = right = 0.0
        half = self.fov_deg / 2
        sector = self.fov_deg / 3
        for obj in world.foods + world.waters + world.obstacles:
            if not obj.active:
                continue
            dx, dy = obj.x - x, obj.y - y
            dist = math.hypot(dx, dy)
            if dist > 160 or dist < 1:
                continue
            angle = self._relative_angle(dx, dy, heading)
            if abs(angle) > half:
                continue
            strength = 1.0 / (1.0 + dist / 50.0)
            if angle < -sector / 2:
                left += strength
            elif angle > sector / 2:
                right += strength
            else:
                center += strength
        reading.visual_left = left
        reading.visual_center = center
        reading.visual_right = right
