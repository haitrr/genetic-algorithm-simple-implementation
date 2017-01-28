from enum import Enum


class BlockType(Enum):
    Normal = 5
    Wall = 0
    Walker = 1
class Block:
    def __init__(self, position):
        self.position = position
        self.rectangle = None
        self.type = BlockType.Normal
        self.track = False

