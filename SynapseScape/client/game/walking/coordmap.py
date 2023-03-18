from typing import Dict, Optional
from dataclasses import dataclass, field
from ..worldpoint import WorldPoint

@dataclass
class CoordMap:
    """
    A mapping of WorldPoints to custom coordinates in various directions.

    Attributes:
        regions (Dict[int, Optional[bytearray]]): A dictionary of region indices to the corresponding bytearrays of direction codes.
        custom (Dict[WorldPoint, WorldPoint]): A dictionary of WorldPoints to custom coordinates.
        NONE (int): A constant representing no direction.
        CUSTOM (int): A constant representing a custom direction.
        N (int): A constant representing the north direction.
        NE (int): A constant representing the north-east direction.
        E (int): A constant representing the east direction.
        SE (int): A constant representing the south-east direction.
        S (int): A constant representing the south direction.
        SW (int): A constant representing the south-west direction.
        W (int): A constant representing the west direction.
        NW (int): A constant representing the north-west direction.

    Methods:
        contains_key(self, key: WorldPoint) -> bool:
            Checks if the given WorldPoint is contained in the CoordMap.
        get(self, key: WorldPoint) -> Optional[WorldPoint]:
            Retrieves the custom coordinate corresponding to the given WorldPoint.
        put(self, key: WorldPoint, value: WorldPoint, code: int = 1) -> None:
            Associates a custom coordinate with the given WorldPoint and direction code.
        index(self, world_point: WorldPoint) -> int:
            Computes the index corresponding to the given WorldPoint.
        region(self, world_point: WorldPoint) -> Optional[bytearray]:
            Retrieves the bytearray corresponding to the region containing the given WorldPoint.

    """

    NONE: int = 0
    CUSTOM: int = 1
    N: int = 2
    NE: int = 3
    E: int = 4
    SE: int = 5
    S: int = 6
    SW: int = 7
    W: int = 8
    NW: int = 9

    regions: Dict[int, Optional[bytearray]] = field(default_factory=dict)
    custom: Dict[WorldPoint, WorldPoint] = field(default_factory=dict)

    def contains_key(self, key: WorldPoint) -> bool:
        """
        Checks if the given WorldPoint is contained in the CoordMap.

        Args:
            key (WorldPoint): The WorldPoint to check.

        Returns:
            bool: True if the WorldPoint is contained in the CoordMap, False otherwise.
        """
        region = self.region(key)
        return region is not None and region[self.index(key)] != 0

    def get(self, key: WorldPoint) -> Optional[WorldPoint]:
        """
        Retrieves the custom coordinate corresponding to the given WorldPoint.

        Args:
            key (WorldPoint): The WorldPoint to retrieve the custom coordinate for.

        Returns:
            Optional[WorldPoint]: The custom coordinate corresponding to the WorldPoint, or None if not found.
        """
        region = self.region(key)
        if region is not None:
            code = region[self.index(key)]
            if code == 1:
                return self.custom.get(key)
            elif code == 2:
                return key.dy(1)
            elif code == 3:
                return key.dx(1).dy(1)
            elif code == 4:
                return key.dx(1)
            elif code == 5:
                return key.dx(1).dy(-1)
            elif code == 6:
                return key.dy(-1)
            elif code == 7:
                return key.dx(-1).dy(-1)
            elif code == 8:
                return key.dx(-1)
            elif code == 9:
                return key.dx(-1).dy(1)
        return key

    def put(self, key: WorldPoint, value: WorldPoint, code: int = 1) -> None:
        """
        Associates a custom coordinate with the given WorldPoint and direction code.

        Args:
            key (WorldPoint): The WorldPoint to associate with a custom coordinate.
            value (WorldPoint): The custom coordinate to associate with the WorldPoint.
            code (int): The direction code to associate with the WorldPoint. Defaults to 1.
        """
        region = self.region(key)
        if region is not None:
            region[self.index(key)] = code
            if code == 1:
                self.custom[key] = value

    def index(self, world_point: WorldPoint) -> int:
        """
        Computes the index corresponding to the given WorldPoint.

        Args:
            world_point (WorldPoint): The WorldPoint to compute the index for.

        Returns:
            int: The index corresponding to the WorldPoint.
        """
        return world_point.getX() % 64 + world_point.getY() % 64 * 64 + world_point.getPlane() % 64 * 64 * 64

    def region(self, world_point: WorldPoint) -> Optional[bytearray]:
        """
        Retrieves the bytearray corresponding to the region containing the given WorldPoint.

        Args:
            world_point (WorldPoint): The WorldPoint to retrieve the bytearray for.

        Returns:
            Optional[bytearray]: The bytearray corresponding to the region containing the WorldPoint, or None if not found.
        """
        region_index = world_point.getX() // 64 * 256 + world_point.getY() // 64
        region = self.regions.get(region_index)
        if region is None:
            region = bytearray(16384)
            self.regions[region_index] = region
        return region
