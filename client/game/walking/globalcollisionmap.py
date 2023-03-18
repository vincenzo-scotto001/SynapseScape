from ..collisionmap import CollisionMap
from typing import Optional
from bitarray import bitarray
from .bitset4d import BitSet4D
import numpy as np

class GlobalCollisionMap(CollisionMap):
    def __init__(self, data: bytes):
        """
        Constructs a GlobalCollisionMap from the given byte data.

        Args:
            data (bytes): The byte data to construct the GlobalCollisionMap from.
        """
        self.regions = [None] * 65536
        buffer = np.frombuffer(data, dtype=np.byte)
        while buffer.size > 0:
            region = buffer[0] << 8 | (buffer[1] & 0xff)
            self.regions[region] = BitSet4D.from_buffer(buffer[2:], 64, 64, 4, 2)
            buffer = buffer[4098:]

    def to_bytes(self) -> bytes:
        """
        Converts the GlobalCollisionMap to bytes.

        Returns:
            bytes: The GlobalCollisionMap represented as bytes.
        """
        region_count = sum(1 for region in self.regions if region is not None)
        buffer = bytearray(region_count * 4098)
        for i, region in enumerate(self.regions):
            if region is not None:
                buffer[i*4098:(i+1)*4098] = region.to_bytes(i)
        return bytes(buffer)

    def set(self, x: int, y: int, z: int, w: int, value: bool) -> None:
        """
        Sets the value at the specified coordinates.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
            z (int): The z coordinate.
            w (int): The w coordinate.
            value (bool): The value to set.
        """
        region = self.regions[x // 64 * 256 + y // 64]
        if region is not None:
            region.set(x % 64, y % 64, z, w, value)

    def get(self, x: int, y: int, z: int, w: int) -> bool:
        """
        Retrieves the value at the specified coordinates.

        Args:
            x (int): The x coordinate.
            y (int): The y coordinate.
            z (int): The z coordinate.
            w (int): The w coordinate.

        Returns:
            bool: The value at the specified coordinates.
        """
        region = self.regions[x // 64 * 256 + y // 64]
        if region is not None:
            return region.get(x % 64, y % 64, z, w)
        return False

    def create_region(self, region: int) -> None:
        """
        Creates a new region at the specified index.

        Args:
            region (int): The index of the region to create.
        """
        self.regions[region] = BitSet4D(64, 64, 4, 2)
        self.regions[region].set_all(True)

    def n(self, x: int, y: int, z: int) -> bool:
        return self.get(x, y, z, 0)
    
    def e(self, x: int, y: int, z: int) -> bool:
        return self.get(x, y, z, 1)