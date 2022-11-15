from src.utils.Camera import CameraCalibration
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QPushButton, QVBoxLayout, QLineEdit 

class CalibrationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Calibration")
        self.calibration_dir = None
        self.output_dir = None
        self.output_filename = None

        self._init_ui()
        self.setLayout(self.main_layout)

    def _init_ui(self):
        self._init_buttons()
        self._init_widgets()
        self._init_layout()
        self._populate_layout()

    def _init_buttons(self):
        self.btn_load_output_dir = QPushButton("Set Output Directory")
        self.btn_load_output_dir.clicked.connect(self.btn_load_output_dir_handler)
        self.btn_load_calibration_dir = QPushButton("Load Calibration Directory")
        self.btn_load_calibration_dir.clicked.connect(self.btn_load_calibration_dir_handler)

    def _init_widgets(self):
        self.heading_form = QLabel("Output Directory & Filename:")
        self.filenameLineEdit = QLineEdit()
        self.heading_vbox = QLabel("Determine calibration directory, including the calibration images:")
        self.form_row_filename = (QLabel("Filename"), self.filenameLineEdit)
        self.form_row_directory = (QLabel("Directory"), self.btn_load_output_dir)

    def _populate_layout(self):
        self.form_layout.addWidget(self.heading_form)
        self.form_layout.addRow(self.form_row_filename[0], self.form_row_filename[1])
        self.form_layout.addRow(self.form_row_directory[0], self.form_row_directory[1])

        self.v_layout.addWidget(self.heading_vbox)
        self.v_layout.addWidget(self.btn_load_calibration_dir)

    def _init_layout(self):
        self.main_layout = QVBoxLayout()
        self.form_layout = QFormLayout()
        self.v_layout = QVBoxLayout()
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addLayout(self.v_layout)

    def btn_load_calibration_dir_handler(self):
        if not self.output_dir or not self.filenameLineEdit.text():
            return
        calibration_dir = self._ask_for_calibration_dir()
        self.camera_calibration = CameraCalibration(calibration_dir)
        self.camera_calibration.calibrate()
        self.camera_calibration.save_calibration(self.output_dir + '/' + self.filenameLineEdit.text() + '.json')
        self.close()

    def btn_load_output_dir_handler(self):
        self._ask_for_output_dir()

    def _ask_for_output_dir(self):
        self.output_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

    def _ask_for_calibration_dir(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", './')

    def calibrate_camera(self):
        self.camera_calibration.calibrate(self.calibration_dir)
        self.camera_calibration.save_calibration('test')
