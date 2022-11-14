from src.utils.Camera import CameraCalibration
from src.utils.InversePerspectiveMapping import InversePerspectiveMapping
from src.utils.Image import Image
import cv2 as cv
import sys
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QPushButton, QTabWidget, QGridLayout, QVBoxLayout, QMainWindow, QLineEdit, QGroupBox, QHBoxLayout, QCheckBox, QMenu, QSizePolicy
from PySide6.QtGui import QPixmap, QImage, qRgb, QColor, QPainter, QPen
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from src.utils.gui.CameraWidget import CameraWidget
from src.utils.gui.ReferencePtWidget import SetReferencePtsWindow
from src.utils.gui.CalibrationWidget import CalibrationWindow


class MainWindow(QMainWindow): # TODO Not main window but ipm
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Show
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def init_ui(self):
        #self.reference_pts_ui = SetReferencePtsWindow()
        self.layout = QVBoxLayout()
        self.source_camera = CameraWidget("Source Camera")
        self.destination_camera = CameraWidget("Destination Camera")
        self.btn_set_reference_pts = QPushButton("Set Reference Points")
        self.btn_set_reference_pts.clicked.connect(self.btn_set_reference_pts_handler)
        self.btn_run_calibration = QPushButton("Calibrate Camera")
        self.btn_run_calibration.clicked.connect(self.btn_run_calibration_handler)
        self.layout.addWidget(self.source_camera)
        self.layout.addWidget(self.destination_camera)
        self.layout.addWidget(self.btn_set_reference_pts)
        self.layout.addWidget(self.btn_run_calibration)

    def btn_set_reference_pts_handler(self):
        # The Problem noob... TODO 
        source_img = self.source_camera.image
        destination_img = self.destination_camera.image
        self.w = SetReferencePtsWindow(source_img, destination_img)
        self.w.show()

    def btn_run_calibration_handler(self):
        self.w = CalibrationWindow()
        self.w.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())