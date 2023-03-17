from dataclasses import dataclass, field
from typing import List, Union, Tuple, Dict
from interactibles import InteractibleObject

@dataclass
class Tile:
    """
    Represents a tile in the game world.
    
    Attributes:
        x (int): The x coordinate of the tile.
        y (int): The y coordinate of the tile.
        items (List[str]): A list of items on the tile.
        enemies (List[str]): A list of enemies on the tile.
        interactible_object (Union[InteractibleObject, None]): The interactible object on the tile.
        player (bool): Whether the player is on the tile.
        movement_flags (Tuple[bool, bool, bool, bool]): A tuple of flags indicating whether the tile is accessible in the four cardinal directions.
        """
    _x: int
    _y: int
    items: List[Item] = field(default_factory=list)
    enemies: List[Enemy] = field(default_factory=list)
    interactible_object: Optional[InteractibleObject] = None
    player: bool = False
    movement_flags: Tuple[bool, bool, bool, bool] = field(default_factory=lambda: (False, False, False, False))

    def __post_init__(self):
        object.__setattr__(self, "movement_flags", tuple(self.movement_flags))

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
    def inaccessible(self):
        """
        Checks if the tile is inaccessible.
        
        Returns:
            bool: True if the tile is inaccessible, False otherwise.
        """
        return all(self.movement_flags)

    @staticmethod
    def new_tile_with_item(tile: 'Tile', item: str) -> 'Tile':
        """
        Creates a new tile with the given item added to the tile.

        Args:
            tile (Tile): The tile to add the item to.
            item (str): The item to add to the tile.

        Returns:
            Tile: A new tile with the item added to it.
        """
        return Tile(
            x=tile.x,
            y=tile.y,
            items=tile.items + [item],
            enemies=tile.enemies,
            interactible_object=tile.interactible_object,
            player=tile.player,
            movement_flags=tile.movement_flags
        )

    @staticmethod
    def new_tile_with_enemy(tile: 'Tile', enemy: str) -> 'Tile':
        """
        Creates a new tile instance with the specified enemy added.

        Args:
            tile (Tile): The original tile.
            enemy (str): The enemy to add to the new tile.

        Returns:
            Tile: A new tile instance with the added enemy.
        """
        return Tile(
            x=tile.x,
            y=tile.y,
            items=tile.items,
            enemies=tile.enemies + [enemy],
            interactible_object=tile.interactible_object,
            player=tile.player,
            movement_flags=tile.movement_flags
        )

    @staticmethod
    def new_tile_with_interactible_object(tile: 'Tile', interactible_object: str) -> 'Tile':
        """
        Creates a new tile instance with the specified interactible object added.

        Args:
            tile (Tile): The original tile.
            interactible_object (str): The interactible object to add to the new tile.

        Returns:
            Tile: A new tile instance with the added interactible object.
        """
        return Tile(
            x=tile.x,
            y=tile.y,
            items=tile.items,
            enemies=tile.enemies,
            interactible_object=interactible_object,
            player=tile.player,
            movement_flags=tile.movement_flags
        )

    @staticmethod
    def new_tile_with_player(tile: 'Tile', player: bool) -> 'Tile':
        """
        Creates a new tile instance with the specified player presence.

        Args:
            tile (Tile): The original tile.
            player (bool): The player presence flag to set in the new tile.

        Returns:
            Tile: A new tile instance with the updated player presence.
        """
        return Tile(
            x=tile.x,
            y=tile.y,
            items=tile.items,
            enemies=tile.enemies,
            interactible_object=tile.interactible_object,
            player=player,
            movement_flags=tile.movement_flags
        )

@dataclass
class Map:
    width: int = 10
    height: int = 7
    tiles: List[List[Tile]] = None
    connections: Dict[str, 'Map'] = None

    def __post_init__(self):
        if self.tiles is None:
            self.tiles = OldSchoolRunescapeEnv.create_game_map(self.width, self.height)
        if self.connections is None:
            self.connections = {}