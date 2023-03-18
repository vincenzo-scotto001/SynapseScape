from dataclasses import dataclass
from abc import ABC

@dataclass
class InteractableObject(ABC):
    pass

@dataclass
class Door(InteractableObject):
    is_open: bool

@dataclass
class LadderStairs(InteractableObject):
    destination_plane: int

@dataclass
class Chest(InteractableObject):
    is_open: bool
    content: str

@dataclass
class BankVault(InteractableObject):
    is_open: bool

@dataclass
class MineableRock(InteractableObject):
    resource_type: str
    available: bool

@dataclass
class Tree(InteractableObject):
    resource_type: str
    available: bool

@dataclass
class FishingSpot(InteractableObject):
    resource_type: str
    available: bool
