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

class CalibrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Calibration")
        self.calibration_dir = None
        self.output_dir = None
        self.output_filename = None
        # Text
        heading_form = QLabel('Form Heading')
        main_text = QLabel("Let's Calibrate the camera.")
        self.filenameLineEdit = QLineEdit()
        heading_vbox = QLabel("Start")

        # Button
        btn_load_output_dir = QPushButton("Set Output Directory")
        btn_load_calibration_dir = QPushButton("Load Calibration Directory")
        btn_load_output_dir.clicked.connect(self.load_output_dir)
        btn_load_calibration_dir.clicked.connect(self.load_calibration_dir)

        # Main 
        main_layout = QVBoxLayout()
        # FBOX
        form_layout = QFormLayout()
        form_layout.addWidget(heading_form)
        form_layout.addRow(QLabel("Filename"), self.filenameLineEdit)
        form_layout.addRow(QLabel("Directory"), btn_load_output_dir)
        # VBOX
        v_layout = QVBoxLayout()
        v_layout.addWidget(heading_vbox)
        v_layout.addWidget(main_text)
        v_layout.addWidget(btn_load_calibration_dir)

        main_layout.addLayout(form_layout) 
        main_layout.addLayout(v_layout)
        self.setLayout(main_layout)

    def load_output_dir(self):
        self.output_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

    def load_calibration_dir(self):
        if not self.output_dir or not self.filenameLineEdit.text():
            return
        calibration_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", './')
        self.camera_calibration = CameraCalibration(calibration_dir)
        self.camera_calibration.calibrate()
        self.camera_calibration.save_calibration(self.output_dir + '/' + self.filenameLineEdit.text() + '.json')
        self.close()

    def calibrate_camera(self):
        self.camera_calibration.calibrate(self.calibration_dir)
        self.camera_calibration.save_calibration('test')
