from Bricks.BlockFactory import BlockFactory
from Bricks import Brick


class Board:
    current_block = ...  # type: Brick.Brick
    Width = 10
    Height = 20
    NewBlockX = Width / 2 - 1
    NewBlockY = 0

    def __init__(self):
        # self.data = [[0] * self.Width] * self.Height # bad! references to same list!
        self.data = [[0] * self.Width for _ in range(self.Height)]
        self.current_block = None
        # self.try_insert_random_block()

    def try_insert_random_block(self):
        self.current_block = BlockFactory.get_random_block(self.NewBlockX, self.NewBlockY)
        for pt in self.current_block.get_coords():
            if pt[0] >= 0 and pt[1] >= 0:  # blocks may be created at negative pos
                if self.data[pt[1]][pt[0]] != 0:
                    return False
        print("Inserted ", self.current_block.get_name())
        return True

    def can_move_current_block(self, x_offset, y_offset):
        coords = self.current_block.peek_coords(x_offset, y_offset)
        return all(0 <= x < self.Width and 0 <= y < self.Height for x, y in coords) \
            and all(self.data[j][i] == 0 for i, j in coords)

    def can_rotate_current_block(self, direction):
        """ Direction: 1 right 2 left"""
        coords = self.current_block.peek_rotated_coords(direction)
        return all(0 <= x < self.Width and 0 <= y < self.Height for x, y in coords) \
               and all(self.data[j][i] == 0 for i, j in coords)

    def permanently_insert_current_block(self):
        for pt in self.current_block.get_coords():
            self.data[pt[1]][pt[0]] = 1

    def remove_full_rows(self) -> int:
        """ Returns number of rows removed (0 if any) """
        rows_removed = 0
        for row in range(0,self.Height):
            if all(self.data[row][col] for col in range(0, self.Width)):
                rows_removed = rows_removed + 1
                for row1 in range(row,0,-1): # y axis goes down
                    self._copy_row(row1 - 1, row1)
                self._clear_row(0)
        return rows_removed

    def remove_all(self):
        for row in range (0, self.Height):
            for col in range(0, self.Width):
                self.data[row][col] = 0

    def _copy_row(self, src_row_index, target_row_index):
        for i in range(0,self.Width):
            self.data[target_row_index][i] = self.data[src_row_index][i]

    def _clear_row(self, row_index):
        for i in range(0,self.Width):
            self.data[row_index][i] = 0