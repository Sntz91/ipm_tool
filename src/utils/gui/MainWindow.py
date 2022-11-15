from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMainWindow, QMessageBox
from src.utils.gui.CameraWidget import CameraWidget
from src.utils.gui.ReferencePtsWidget import SetReferencePtsWindow
from src.utils.gui.CalibrationWidget import CalibrationWidget
from src.utils.gui.EvaluationWidget import EvaluationWidget

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
        self.btn_evaluate_ipm.clicked.connect(self.btn_evaluate_ipm_handler)

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

def _show_error_box(text):
    dlg = QMessageBox()
    dlg.setText(text)
    dlg.setIcon(QMessageBox.Warning)
    dlg.exec_()