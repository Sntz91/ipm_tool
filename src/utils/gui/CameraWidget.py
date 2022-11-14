from src.utils.Camera import CameraCalibration
from src.utils.Image import Image
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QPushButton, QTabWidget, QGridLayout, QVBoxLayout, QMainWindow, QLineEdit, QGroupBox, QHBoxLayout, QCheckBox, QMenu, QSizePolicy
from PySide6.QtGui import QPixmap, QImage, qRgb, QColor, QPainter, QPen

# TODO undistort etc.

class CameraWidget(QWidget):
    def __init__(self, camera_name):
        super().__init__()
        self.camera_name = camera_name
        self.image = None
        self.init_ui()

    def init_ui(self):
        self.init_buttons()
        self.image_preview = _image_preview()
        self.configuration_preview = _status_preview('Camera Not Calibrated yet.', 'red')
        # Layout
        self.init_layout()
        label_camera_name = QLabel(self.camera_name)
        self.left.addWidget(label_camera_name)
        self.left.addWidget(self.btn_load_configuration)
        self.left.addWidget(self.btn_load_image)
        self.left.addWidget(self.chk_undistort)
        self.left.addWidget(self.chk_crop)
        self.left.addWidget(self.configuration_preview)
        #self.left.addStretch()
        self.right.addWidget(self.image_preview)
        self.setLayout(self.main)

    def init_layout(self):
        self.main = QVBoxLayout()
        self.content = QHBoxLayout()
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()
        self.main.addLayout(self.content)
        self.content.addLayout(self.left)
        self.content.addLayout(self.right)


    def init_buttons(self):
        self.btn_load_configuration = QPushButton("Load configuration")
        self.btn_load_configuration.clicked.connect(self.btn_load_configuration_handler)
        self.btn_load_image = QPushButton("Load Image")
        self.btn_load_image.clicked.connect(self.btn_load_image_handler)
        self.chk_undistort = QCheckBox("Undistort")
        self.chk_crop = QCheckBox("Crop")

    def btn_load_image_handler(self):
        filename = self._ask_for_filename('*.jpg')
        if filename:
            self._load_image(filename)
            self._update_preview_window()

    def btn_load_configuration_handler(self):
        filename = self._ask_for_filename('*.json')
        mtx, dist = self._get_camera_calibration(filename)
        self.configuration_preview.update_text(f'camera calibrated. {filename.split("/")[-1]}', 'green')
        self._undistort_image(mtx, dist, crop=True)
        print('undistorted')
        self._update_preview_window()

    def _load_image(self, filename):
        self.image = Image(filename, self.camera_name)

    def _update_preview_window(self):
        self.image_preview.update(self.image.filename)
        print('updated')

    def _ask_for_filename(self, datatype='*'):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self,
            self.tr("Open File"),
            "",
            self.tr(f"Files ({datatype})")
        )[0]
        print(filename)
        return filename

    def _get_camera_calibration(self, filename):
        assert '.json' == filename[-5:]
        camera = CameraCalibration()
        camera.load_calibration(filename)
        return camera.calibration_matrix.mtx, camera.calibration_matrix.dist

    def _undistort_image(self, mtx, dist, crop=False):
        assert self.image
        self.image.undistort(mtx, dist, crop)

        

class _image_preview(QWidget):
    def __init__(self, width=320): 
        super().__init__()
        self.width = width
        self.img = QPixmap('assets/image-preview.png')
        self.img = self.img.scaledToWidth(self.width)

        self.helper_label = QLabel()
        self.helper_label.setPixmap(self.img)

        self.grid = QGridLayout()
        self.grid.addWidget(self.helper_label, 1, 1)
        self.setLayout(self.grid)

    def update(self, filename):
        self.img = QPixmap(filename)
        self.img = self.img.scaledToWidth(self.width)
        self.helper_label.setPixmap(self.img)
        self.setLayout(self.grid)


class _status_preview(QWidget):
    def __init__(self, text, color):
        super().__init__()
        self.init_ui(text, color)
        # Show
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        self.setLayout(vbox)

    def init_ui(self, text, color):
        self.color = color
        self.label = QLabel(text)
        self._set_label(text, color)

    def update_text(self, text, color):
        self._set_label(text, color)

    def _set_label(self, text, color):
        self.label.setText(text)
        self.label.setStyleSheet(f"color: {color};")
