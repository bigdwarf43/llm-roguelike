# Define a Tile class
class Tile:
    def __init__(self, blocked=True, block_sight=None):
        self.blocked = blocked
        self.isWall = False
        self.isInner = False
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

        self.isNPC = False

        self.name = "ground"