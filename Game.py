from PyQt5.QtCore import QBasicTimer, pyqtSignal, QObject
from Board import Board


class Game(QObject):
    # must be static
    boardUpdated = pyqtSignal()
    statusUpdated = pyqtSignal(str)
    scoreUpdated = pyqtSignal(int)
    levelUpdated = pyqtSignal(int)

    pointsForSingleBlock = 1
    pointsForRowCleared = 5
    pointsForLevelUp = 20  # after gaining n points ** level, level increases
    baseSpeed = 320  # update interval for lvl 1
    speedDecrement = 20  # decrement of timer for each level
    highSpeed = 50  # timer interval when space is pressed

    def __init__(self, board: Board):
        super().__init__()
        self._timer = QBasicTimer()
        self._board = board
        self._speed = self.baseSpeed
        self._speedBackup = self._speed
        self._highSpeedMode = False
        self._score = 0
        self._level = 1
        self._status = ""
        self._game_over = False
        self.new_game()

    def start(self):
        if not self._game_over:
            self._timer.start(self._speed, self)

    def stop(self):
        self._timer.stop()

    def _change_speed(self, speed):
        self._speed = speed
        if self._timer.isActive():
            self.start()

    def _add_points(self,added):
        """ Updates score and speed. Number of added points is level dependent """
        added = added * self._level
        self._score = self._score + added
        self.scoreUpdated.emit(self._score)
        self.unset_high_speed()
        if self._score > self._number_of_points_to_change_level() and self._speed - self.speedDecrement > 0:
            self._level = self._level + 1
            self.levelUpdated.emit(self._level)
            self._change_speed(self._speed - self.speedDecrement)

    def _number_of_points_to_change_level(self):
        return self.pointsForLevelUp ** self._level

    def _change_status_message(self, msg):
        self._status = msg
        self.statusUpdated.emit(msg)

    def timerEvent(self, event):
        if event.timerId() == self._timer.timerId():
            if self._board.can_move_current_block(0, 1):
                self._board.current_block.move_down()
            else:
                self._board.permanently_insert_current_block()
                self._add_points(self.pointsForSingleBlock)
                rows_removed = self._board.remove_full_rows()
                self._add_points(self.pointsForRowCleared * rows_removed)
                if not self._board.try_insert_random_block():
                    self._change_status_message("Game over!")
                    self._game_over = True
                    self.stop()
            self.boardUpdated.emit()

    def get_status(self) -> str:
        return self._status

    def get_score(self) -> int:
        return self._score

    def get_level(self) -> int:
        return self._level

    def set_high_speed(self):
        if not self._highSpeedMode:
            self._highSpeedMode = True
            self._speedBackup = self._speed
            self._change_speed(self.highSpeed)

    def unset_high_speed(self):
        if self._highSpeedMode:
            self._change_speed(self._speedBackup)
            self._highSpeedMode = False

    def toggle_pause(self):
        if not self._game_over:
            if self._timer.isActive():
                self._change_status_message("Paused")
                self.stop()
            else:
                self.start()
                self._change_status_message("")

    def new_game(self):
        self.stop()
        self._speed = self.baseSpeed
        self._speedBackup = self._speed
        self._highSpeedMode = False
        self._score = 0
        self._level = 1
        self._game_over = False;
        self.scoreUpdated.emit(self._score)
        self.levelUpdated.emit(self._level)
        self._change_status_message("")
        self._board.remove_all()
        self._board.try_insert_random_block()
        self.boardUpdated.emit()
