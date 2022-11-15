import sys
from PySide6 import QtWidgets
from src.utils.gui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())