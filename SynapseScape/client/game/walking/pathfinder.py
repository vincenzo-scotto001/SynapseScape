from collections import deque
from typing import List
from .coordmap import CoordMap
from ..collisionmap import CollisionMap
from ..worldpoint import WorldPoint


class Pathfinder:
    def __init__(self, collision_map: CollisionMap, start: WorldPoint, target: WorldPoint):
        self.collision_map = collision_map
        self.start = start
        self.target = target
        self.boundary = deque()
        self.predecessors = CoordMap()

    def find(self) -> List[WorldPoint]:
        self.boundary.append(self.start)
        self.predecessors[self.start] = None

        while self.boundary:
            node = self.boundary.popleft()

            if node == self.target:
                path = self._get_path(node)
                return path

            self._add_neighbours(node)

        return []

    def _add_neighbours(self, position: WorldPoint):
        if self.collision_map.w(position.x, position.y, position.plane):
            neighbor = position.dx(-1)
            if neighbor not in self.predecessors:
                self.predecessors.put_east(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.e(position.x, position.y, position.plane):
            neighbor = position.dx(1)
            if neighbor not in self.predecessors:
                self.predecessors.put_west(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.s(position.x, position.y, position.plane):
            neighbor = position.dy(-1)
            if neighbor not in self.predecessors:
                self.predecessors.put_north(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.n(position.x, position.y, position.plane):
            neighbor = position.dy(1)
            if neighbor not in self.predecessors:
                self.predecessors.put_south(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.sw(position.x, position.y, position.plane):
            neighbor = position.dx(-1).dy(-1)
            if neighbor not in self.predecessors:
                self.predecessors.put_northeast(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.se(position.x, position.y, position.plane):
            neighbor = position.dx(1).dy(-1)
            if neighbor not in self.predecessors:
                self.predecessors.put_northwest(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.nw(position.x, position.y, position.plane):
            neighbor = position.dx(-1).dy(1)
            if neighbor not in self.predecessors:
                self.predecessors.put_southeast(neighbor)
                self.boundary.append(neighbor)

        if self.collision_map.ne(position.x, position.y, position.plane):
            neighbor = position.dx(1).dy(1)
            if neighbor not in self.predecessors:
                self.predecessors.put_southwest(neighbor)
                self.boundary.append(neighbor)

    def _get_path(self, node: WorldPoint) -> List[WorldPoint]:
        path = []
        while node is not None:
            path.insert(0, node)
            node = self.predecessors[node]
        return path
