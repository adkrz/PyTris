from typing import Tuple


class Brick:
    def __init__(self, x: int, y:int):
        """ Initialize the block at the given position on screen """
        self._xPos = 0
        self._yPos = 0
        self.set_pos(x, y)

    def set_pos(self, x, y):
        self._xPos = x
        self._yPos = y

    def get_pos(self):
        return int(self.x), int(self.y)

    def move_down(self):
        self.set_pos(self.get_x(), self.get_y() + 1)

    def move_left(self):
        self.set_pos(self.get_x()-1, self.get_y())

    def move_right(self):
        self.set_pos(self.get_x() + 1, self.get_y())

    def get_x(self):
        return int(self._xPos)

    def get_y(self):
        return int(self._yPos)

    def rotate_left(self):
        pass

    def rotate_right(self):
        pass

    def get_coords(self) -> Tuple[int,int]:
        """ Return all the points """
        return

    def peek_coords(self, x_offset, y_offset):
        """ Returns all the points, simulating the block movement, without actual coords update """
        coords = self.get_coords() # array of pairs
        return list(map(lambda pt: (pt[0]+x_offset, pt[1]+y_offset), coords))

    def peek_rotated_coords(self, direction):
        """ Gets coordinates after rotation, without permanently applying them
         Direction: 1: right -1 left
        """
        if direction == 1:
            self.rotate_right()
        else:
            self.rotate_left()
        coords = self.get_coords()
        if direction == 1:
            self.rotate_left()
        else:
            self.rotate_right()
        return coords

    def get_name(self):
        return

