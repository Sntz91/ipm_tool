import sys
from PySide6 import QtWidgets
from src.utils.gui.MainWindow import MainWindow

# TODO1: Error Handling
# TODO2: Evaluation
# TODO3: Refactor

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())