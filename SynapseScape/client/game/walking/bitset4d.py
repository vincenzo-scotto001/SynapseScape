from dataclasses import dataclass
from bitarray import bitarray
from typing import Any, Union

@dataclass
class BitSet4D:
    """
    A 4-dimensional bit set, implemented using bitarray.

    Attributes:
        sizeX (int): The size of the first dimension.
        sizeY (int): The size of the second dimension.
        sizeZ (int): The size of the third dimension.
        sizeW (int): The size of the fourth dimension.
        bits (Optional[bitarray]): The bitarray to be used to store the bits.

    Methods:
        __post_init__(self): Initializes the bits attribute if not already set.
        from_buffer(cls, buffer: bytearray, sizeX: int, sizeY: int, sizeZ: int, sizeW: int) -> BitSet4D:
            Creates a new BitSet4D instance from a bytearray.
        write(self, buffer: bytearray) -> None:
            Writes the bits of the BitSet4D instance to a bytearray.
        index(self, x: int, y: int, z: int, w: int) -> int:
            Computes the 1D index corresponding to the 4D coordinates.
        get(self, x: int, y: int, z: int, w: int) -> bool:
            Gets the boolean value at the specified 4-dimensional coordinates.
        set(self, x: int, y: int, z: int, w: int, value: bool) -> None:
            Sets the boolean value at the specified 4-dimensional coordinates.
        set_all(self, value: bool) -> None:
            Sets all bits to the specified value.
    """
    sizeX: int
    sizeY: int
    sizeZ: int
    sizeW: int
    bits: bitarray = None

    def __post_init__(self):
        """
        Initializes the bits attribute if not already set.
        """
        if self.bits is None:
            self.bits = bitarray(self.sizeX * self.sizeY * self.sizeZ * self.sizeW)
            self.bits.setall(False)

    @classmethod
    def from_buffer(cls, buffer: bytearray, sizeX: int, sizeY: int, sizeZ: int, sizeW: int) -> 'BitSet4D':
        """
        Creates a new BitSet4D instance from a bytearray.

        Args:
            buffer (bytearray): The bytearray to create the BitSet4D from.
            sizeX (int): The size of the first dimension.
            sizeY (int): The size of the second dimension.
            sizeZ (int): The size of the third dimension.
            sizeW (int): The size of the fourth dimension.

        Returns:
            BitSet4D: A new BitSet4D instance.

        Raises:
            ValueError: If the size of the buffer does not match the specified dimensions.
        """
        bits = bitarray()
        bits.frombytes(buffer)
        bits = bits[:sizeX * sizeY * sizeZ * sizeW]
        return cls(sizeX=sizeX, sizeY=sizeY, sizeZ=sizeZ, sizeW=sizeW, bits=bits)

    def write(self, buffer: bytearray) -> None:
        """
        Writes the bit values to a bytearray.

        Args:
            buffer (bytearray): The bytearray to write the bit values to.
        """
        buffer.extend(self.bits.tobytes())

    def get(self, x: int, y: int, z: int, w: int) -> bool:
        """
        Gets the boolean value at the specified 4-dimensional coordinates.

        Args:
            x (int): The first dimension coordinate.
            y (int): The second dimension coordinate.
            z (int): The third dimension coordinate.
            w (int): The fourth dimension coordinate.

        Returns:
            bool: The boolean value at the specified coordinates.
        """
        return self.bits[self.index(x, y, z, w)]

    def set(self, x: int, y: int, z: int, flag: int, value: bool) -> None:
        """
        Sets the boolean value at the specified 4-dimensional coordinates.

        Args:
            x (int): The first dimension coordinate.
            y (int): The second dimension coordinate.
            z (int): The third dimension coordinate.
            flag (int): The fourth dimension coordinate.
            value (bool): The boolean value to set at the specified coordinates.
        """
        self.bits[self.index(x, y, z, flag)] = value

    def set_all(self, value: bool) -> None:
        """
        Sets all boolean values in the BitSet4D to the specified value.

        Args:
            value (bool): The boolean value to set for all elements.
        """
        self.bits.setall(value)

    def index(self, x: int, y: int, z: int, w: int) -> int:
        """
        Computes the 1D index corresponding to the 4D coordinates.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
            z (int): The z-coordinate.
            w (int): The w-coordinate.

        Returns:
            int: The computed 1D index.

        Raises:
            IndexError: If any of the coordinates are out of bounds.
        """
        if (x < 0 or y < 0 or z < 0 or w < 0 or x >= self.sizeX or y >= self.sizeY
                or z >= self.sizeZ or w >= self.sizeW):
            raise IndexError(f"({x}, {y}, {z}, {w})")
        index = z
        index = index * self.sizeY + y
        index = index * self.sizeX + x
        index = index * self.sizeW + w
        return index
