from enum import Enum


class BlockType(Enum):
    Normal = 5
    Food = 10
    Wall = 0
    Snake = 1
class Block:
    def __init__(self, position):
        self.position = position
        self.type = BlockType.Normal
        self.owners = []

