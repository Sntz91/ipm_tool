from utilities.Camera import CameraCalibration
from utilities.Image import Image
from PySide6 import QtWidgets, QtGui
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QCheckBox
from PySide6.QtGui import QPixmap, QImage
from PySide6 import QtCore
import numpy as np

HEADING_STYLE = "background-color: DarkRed; \
                color: white; \
                border-radius: 10px; \
                font: bold 14px; \
                min-width: 10em; \
                padding: 6px;"


class Header(QWidget):
    def __init__(self, text):
        super().__init__()
        self.label = QLabel(text)
        self.label.setStyleSheet(HEADING_STYLE)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        # Show
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        self.setLayout(vbox)



class CameraWidget(QWidget):
    def __init__(self, camera_name):
        super().__init__()
        self.camera_name = camera_name
        self.image = None
        self.init_ui()

    def init_ui(self):
        self.init_buttons()
        self.header = Header(self.camera_name)
        self.image_preview = _image_preview()
        self.configuration_preview = _status_preview('Camera Not Calibrated yet.', 'DarkRed')
        # Layout
        self.init_layout()
        self.left.addWidget(self.btn_load_image)
        self.left.addWidget(self.btn_load_configuration)
        self.left.addWidget(self.chk_crop)
        self.left.addWidget(self.configuration_preview)
        self.left.addStretch()
        self.right.addWidget(self.image_preview)
        self.right.addStretch()
        self.setLayout(self.main)

    def init_layout(self):
        self.main = QVBoxLayout()
        self.content = QHBoxLayout()
        self.left = QVBoxLayout()
        self.right = QVBoxLayout()
        self.main.addWidget(self.header)
        self.main.addLayout(self.content)
        self.content.addLayout(self.left)
        self.content.addLayout(self.right)


    def init_buttons(self):
        self.btn_load_configuration = QPushButton("Undistort Image with calibration file...")
        self.btn_load_configuration.clicked.connect(self.btn_load_configuration_handler)
        self.btn_load_configuration.setEnabled(False)
        self.btn_load_image = QPushButton("Load Image")
        self.btn_load_image.clicked.connect(self.btn_load_image_handler)
        self.chk_crop = QCheckBox("Crop")

    def btn_load_image_handler(self):
        filename = self._ask_for_filename('*.jpg')
        if filename:
            self._load_image(filename)
            self._update_preview_window()
            self.btn_load_configuration.setEnabled(True)

    def btn_load_configuration_handler(self):
        filename = self._ask_for_filename('*.json')
        mtx, dist = self._get_camera_calibration(filename)
        self.configuration_preview.update_text(f'camera calibrated. {filename.split("/")[-1]}', 'green')
        self._undistort_image(mtx, dist, crop=self.chk_crop.isChecked())
        print('undistorted')
        self._update_preview_window()
        self.btn_load_configuration.setEnabled(False)

    def _load_image(self, filename):
        self.image = Image(filename, self.camera_name)

    def _update_preview_window(self):
        self.image_preview.update(self.image.img) 
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
    def __init__(self, width=200): 
        super().__init__()
        self.width = width
        self.img = QPixmap('images/image-preview.png')
        self.img = self.img.scaledToWidth(self.width)

        self.helper_label = QLabel()
        self.helper_label.setPixmap(self.img)

        self.grid = QGridLayout()
        self.grid.addWidget(self.helper_label, 1, 1)
        self.setLayout(self.grid)

    def update(self, image):
        image = np.ascontiguousarray(image)
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        image = QtGui.QImage(image.data, width, height,
            bytesPerLine, QImage.Format.Format_RGB888)
        self.img = QtGui.QPixmap(image)

        #self.img = QPixmap(filename)
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
        vbox.addStretch()
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
