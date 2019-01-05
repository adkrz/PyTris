from Bricks.SquareBlock import SquareBlock
from Bricks.LineBlock import LineBlock
from Bricks.TBlock import TBlock
from Bricks.LBlock import LBlock
from Bricks.LBlock2 import LBlock2
from Bricks.SBlock import SBlock
from Bricks.SBlock2 import SBlock2
import random


class BlockFactory:
    @staticmethod
    def get_random_block(x,y):
        """ Creates randomly picked block at specified position """
        r = random.randrange(7)
        if r == 0:
            return SquareBlock(x, y)
        elif r == 1:
            return LineBlock(x, y)
        elif r == 2:
            return TBlock(x, y)
        elif r == 3:
            return LBlock(x, y)
        elif r == 4:
            return LBlock2(x, y)
        elif r == 5:
            return SBlock(x, y)
        elif r == 6:
            return SBlock2(x, y)
        else:
            raise RuntimeError("Wrong block number")