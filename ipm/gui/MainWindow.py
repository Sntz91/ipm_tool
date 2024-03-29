from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMainWindow, QMessageBox, QFileDialog
from gui.CameraWidget import CameraWidget
from gui.ReferencePtsWidget import SetReferencePtsWindow
from gui.CalibrationWidget import CalibrationWidget
from gui.EvaluationWidget import EvaluationWidget
from utilities.Image import Image
import json
import numpy as np

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Show
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        #self.show()

    def init_ui(self):
        self._init_layout()
        self._init_buttons()
        self._init_widgets()
        self._populate_layout()

    def _init_widgets(self):
        self.source_camera = CameraWidget("souce_camera")
        self.destination_camera = CameraWidget("destination_camera")

    def _init_buttons(self):
        self.btn_set_reference_pts = QPushButton("Set Reference Points")
        self.btn_set_reference_pts.clicked.connect(self.btn_set_reference_pts_handler)
        self.btn_run_calibration = QPushButton("Calibrate Camera")
        self.btn_run_calibration.clicked.connect(self.btn_run_calibration_handler)
        self.btn_evaluate_ipm = QPushButton("Evaluate IPM")
        self.btn_evaluate_ipm.clicked.connect(self.btn_start_evaluation_handler)

    def btn_evaluate_ipm_handler(self):
        self.newwindow = EvaluationWidget()
        self.newwindow.show()
        # Load IPM Folder
        # Set Evaluation Points
        # Calculate Error (in realtime?)

    def _populate_layout(self):
        self.layout.addWidget(self.source_camera)
        self.layout.addWidget(self.destination_camera)
        self.layout.addWidget(self.btn_set_reference_pts)
        self.layout.addWidget(self.btn_run_calibration)
        self.layout.addWidget(self.btn_evaluate_ipm)

    def _init_layout(self):
        self.layout = QVBoxLayout()

    def btn_set_reference_pts_handler(self):
        try:
            if(not self._images_are_set()):
                raise Exception("Error, images are not set yet.")
            self.newwindow = SetReferencePtsWindow(self.source_camera.image, self.destination_camera.image)
            self.newwindow.show()
        except Exception as e:
            _show_error_box(str(e))

    def btn_run_calibration_handler(self):
        self.newwindow = CalibrationWidget()
        self.newwindow.show()

    def _images_are_set(self):
        return True if self.source_camera.image and self.destination_camera.image else False


    
    def btn_start_evaluation_handler(self):
        dir = self._ask_for_dir()
        self.load_data(dir)

    def load_data(self, dir):
        source_img = self.load_source_image(dir)
        destination_img = self.load_destination_image(dir)
        output_img = self.load_output_image(dir)
        h = self.load_homography_matrix(dir)
        self.newwindow = EvaluationWidget(source_img, destination_img, output_img, h)
        self.newwindow.show()

    def load_source_image(self, dir):
        img = Image(dir + '/image_source_camera.jpg', 'source_camera')
        return img

    def load_destination_image(self, dir):
        img = Image(dir + '/image_destination_camera.jpg', 'destination_camera')
        return img

    def load_output_image(self, dir):
        img = Image(dir + '/output_image.jpg', 'image_output')
        return img

    def load_homography_matrix(self, dir):
        f = open(dir + '/homography_matrix.json')
        h = json.load(f)
        f.close()
        return np.array(h)

    def _ask_for_dir(self):
        return QFileDialog.getExistingDirectory(self, "Select Directory", './')


def _show_error_box(text):
    dlg = QMessageBox()
    dlg.setText(text)
    dlg.setIcon(QMessageBox.Warning)
    dlg.exec_()