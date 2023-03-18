from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum

class Direction(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

@dataclass(frozen=True)
class WorldPoint:
    x: int
    y: int
    plane: int

    REGION_SIZE = 1 << 6
    CHUNK_SIZE = 1 << 4

    @staticmethod
    def from_region(region_id: int, region_x: int, region_y: int, plane: int) -> WorldPoint:
        return WorldPoint(((region_id >> 8) << 6) + region_x,
                          ((region_id & 0xFF) << 6) + region_y, plane)

    def dx(self, dx: int) -> WorldPoint:
        return WorldPoint(self.x + dx, self.y, self.plane)

    def dy(self, dy: int) -> WorldPoint:
        return WorldPoint(self.x, self.y + dy, self.plane)

    def dz(self, dz: int) -> WorldPoint:
        return WorldPoint(self.x, self.y, self.plane + dz)

    def get_region_id(self) -> int:
        return ((self.x >> 6) << 8) | (self.y >> 6)

    def get_region_x(self) -> int:
        return self.x & (WorldPoint.REGION_SIZE - 1)

    def get_region_y(self) -> int:
        return self.y & (WorldPoint.REGION_SIZE - 1)

    def distance_to(self, other: WorldPoint) -> int:
        return self.distance_to_2d(other) if self.plane == other.plane else int(1e9)

    def distance_to_2d(self, other: WorldPoint) -> int:
        return max(abs(self.x - other.x), abs(self.y - other.y))
