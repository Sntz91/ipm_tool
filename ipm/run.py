import sys
from PySide6 import QtWidgets
from gui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())