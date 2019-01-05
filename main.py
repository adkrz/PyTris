from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow
import sys

if __name__ == "__main__":

    app = QApplication([])
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())

    print("ok")
