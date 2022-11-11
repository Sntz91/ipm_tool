from src.utils.Camera import Camera
from src.utils.InversePerspectiveMapping import InversePerspectiveMapping
from src.utils.Image import Image
import cv2 as cv
import os
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QPushButton, QTabWidget, QGridLayout, QVBoxLayout, QMainWindow, QLineEdit, QGroupBox, QHBoxLayout, QCheckBox
from PySide6.QtGui import QPixmap, QImage, qRgb, QColor, QPainter, QPen
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class _image_preview(QWidget):
    def __init__(self, img='assets/image-preview.png'): 
        super().__init__()
        self.img = img

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.img)
        painter.drawPixmap(self.rect(), pixmap)


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


class CameraWidget(QWidget):
    def __init__(self, camera_name):
        super().__init__()
        self.camera_name = camera_name
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
        filename = QtWidgets.QFileDialog.getOpenFileName(self,
           self.tr("Open Image"), "", self.tr("Image Files (*.jpg)"))[0]
        if filename:
            self.image_preview.img = filename
            self.image_preview.update()

    def btn_load_configuration_handler(self):
        # TODO
        # Load Calibration of this camera..
        filename = QtWidgets.QFileDialog.getOpenFileName(self,
            self.tr("Open json"), "", self.tr("JSON Files (*.json)"))[0]
        print(filename)
        self.configuration_preview.update_text(f'camera calibrated. {filename.split("/")[-1]}', 'green')
    
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        reference_pts_source = []
        reference_pts_destination = []
        def on_press(event):
            sys.stdout.flush()
            if event.key == 'x':
                if event.inaxes == self.ax1:
                    self.ax1.plot(event.xdata, event.ydata, marker='x', markersize=12)
                    reference_pts_source.append((event.xdata, event.ydata))
                elif event.inaxes == self.ax2:
                    self.ax2.plot(event.xdata, event.ydata, marker='x', markersize=12)
                    reference_pts_destination.append((event.xdata, event.ydata))
                fig.canvas.draw()
        fig = Figure(figsize=(width, height), dpi=dpi)
        cid = fig.canvas.mpl_connect('key_press_event', on_press)
        self.ax1 = fig.add_subplot(121)
        self.ax2 = fig.add_subplot(122)
        super(MplCanvas, self).__init__(fig)

class SetReferencePtsWindow(QtWidgets.QMainWindow):
    def __init__(self):  
        super().__init__()
        self.resize(900, 400)
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        img = cv.imread('Dataset_1/Canon_550D/Images/c1/IMG_1241.JPG')
        sc.ax1.imshow(img)
        sc.ax2.imshow(img)
        self.setCentralWidget(sc)
        self.show()


class MainWindow(QMainWindow): # TODO Not main window but ipm
    def __init__(self):
        super().__init__()
        self.init_ui()
        # Show
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def init_ui(self):
        self.reference_pts_ui = SetReferencePtsWindow()
        self.layout = QVBoxLayout()
        self.source_camera = CameraWidget("Source Camera")
        self.destination_camera = CameraWidget("Destination Camera")
        self.btn_set_reference_pts = QPushButton("Set Reference Points")
        #self.btn_set_reference_pts.clicked.connect(self.btn_set_reference_pts_handler)
        self.btn_set_reference_pts.clicked.connect(self.reference_pts_ui.show)
        self.layout.addWidget(self.source_camera)
        self.layout.addWidget(self.destination_camera)
        self.layout.addWidget(self.btn_set_reference_pts)

    def btn_set_reference_pts_handler(self):
        #source_image = cv.imread('Dataset_1/Canon_550D/Images/c1/IMG_1241.JPG')
        #destination_image = cv.imread('Dataset_1/Canon_550D/Images/c1/IMG_1242.JPG')
        #output_dir = 'outputs'
        print('click')
        self.w = SetReferencePtsWindow()
        self.w.show
        #Filesnames

        #ipm = InversePerspectiveMapping(source_image, destination_image, output_dir)
        #ipm.set_homography_reference_pts()
        #print(ipm.source_image.reference_pts)
        #ipm.write_reference_pts()
        #ipm.transform_img()
        #ipm.save_images()
        #ipm.show_images()
        #ipm()
        #ipm.set_homography_reference_pts() # New Window tbh
        

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
        self.calibration_dir = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", './')
        self.calibrate_camera()
        self.close()

    def calibrate_camera(self):
        camera = Camera(calibration_dir=self.calibration_dir)
        camera.calibrate()
        camera.save_calibration(self.output_dir + '/' + self.filenameLineEdit.text() + '.json')

        #btn.setEnabled(False) !!!!

    #def load_calibration_file(self):
    #    self.calibration_file = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open Image"))
    #    self.close()

class MainWindow_(QMainWindow):
    def __init__(self):
        super().__init__()
        self.w = None  # No external window yet.
        # Buttons
        btn_calibrate_camera = QPushButton("Calibrate Camera")
        btn_calibrate_camera.clicked.connect(self.show_calibration_window)
        btn_set_reference_pts = QPushButton("Set Reference Points")

        # Preview images
        self.source_camera_img = QPixmap()
        self.source_camera_img = self.source_camera_img.scaledToWidth(250)
        self.source_camera_img_label = QtWidgets.QLabel()
        #self.source_camera_img_label.setPixmap(self.source_camera_img)

        self.destination_camera_img = QPixmap()
        self.destination_camera_img = self.source_camera_img.scaledToWidth(250)
        self.destination_camera_img_label = QtWidgets.QLabel()
        #self.destination_camera_img_label.setPixmap(self.destination_camera_img)

        # Layouts def
        main_layout = QVBoxLayout()
        camera_main_layout = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()
        # Layouts nesting
        camera_main_layout.addLayout(left)
        camera_main_layout.addLayout(right)
        main_layout.addWidget(btn_calibrate_camera)
        main_layout.addLayout(camera_main_layout)

        # TBD        
        main_layout.addWidget(btn_set_reference_pts)

        
        ### Left
        # Left Layouts
        cam1_groupbox = QGroupBox("Camera 1")
        left.addWidget(cam1_groupbox)
        fbox_cam1 = QFormLayout()
        cam1_groupbox.setLayout(fbox_cam1)

        # Left Buttons
        btn_load_cam1_calibration = QPushButton("Load Calibration File..")
        btn_load_cam1_calibration.clicked.connect(self.load_cam1_calibration) 
        btn_load_cam1_img = QPushButton("Load Image..")
        btn_load_cam1_img.clicked.connect(self.load_cam1_image)
        # Right Form
        fbox_cam1.addRow("Load Calibration File", btn_load_cam1_calibration)
        fbox_cam1.addRow("Load Image", btn_load_cam1_img)
        fbox_cam1.addRow("Undistort?", QCheckBox('undistort'))
        fbox_cam1.addRow("Crop?", QCheckBox('crop'))

        ### Right
        # Right Layouts
        cam2_groupbox = QGroupBox("Camera 2")
        left.addWidget(cam2_groupbox)
        fbox_cam2 = QFormLayout()
        cam2_groupbox.setLayout(fbox_cam2)

        # Right Buttons
        btn_load_cam2_calibration = QPushButton("Load Calibration File..")
        btn_load_cam2_calibration.clicked.connect(self.load_cam2_calibration) 
        btn_load_cam2_img = QPushButton("Load Image..")
        btn_load_cam2_img.clicked.connect(self.load_cam2_image)
        # Right Form
        self.cam2_crop_flg = QCheckBox('crop')
        self.cam2_undistort_flg = QCheckBox('undistort')
        fbox_cam2.addRow("Load Calibration File", btn_load_cam2_calibration)
        fbox_cam2.addRow("Load Image", btn_load_cam2_img)
        fbox_cam2.addRow("Undistort?", QCheckBox('undistort'))
        fbox_cam2.addRow("Crop?", QCheckBox('crop'))
        right.addWidget(self.source_camera_img_label)
        right.addWidget(self.destination_camera_img_label)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def load_cam1_image(self):
        cam_image = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open Image"))
        self.source_camera_img.load(str(cam_image[0]))
        self.source_camera_img = self.source_camera_img.scaledToWidth(200)
        # crop, undistort!  TODO
        
        self.source_camera_img_label.setPixmap(self.source_camera_img)

    def load_cam2_image(self):
        cam_image = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open Image"))
        self.destination_camera_img.load(str(cam_image[0]))
        self.destination_camera_img = self.destination_camera_img.scaledToWidth(200)
        # crop, undistort!  TODO
        self.destination_camera_img_label.setPixmap(self.destination_camera_img)

    def load_cam1_calibration(self):
        pass

    def load_cam2_calibration(self):
        pass
        



    def show_calibration_window(self, checked):
        if self.w is None:
            self.w = CalibrationWindow()
        self.w.show()



    def warning(self, text):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(text)
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.exec()

    @QtCore.Slot()
    def ipm(self):
        if not self.c1 or not self.c2:
            self.warning('no cameras defined yet.')
            return
        else:
            if not self.c1.calibrated and not self.c2.calibrated:
                print('cameras not calibrated yet.')
                return

        text, ok = QtWidgets.QInputDialog.getText(self, 'Inverse Perspective mapping', 'Choose Destination Folder: ')
        if ok and text:
            chosen_directory = text
        retval = self.check_and_mk_path(chosen_directory)
        if not retval:
            return

        # Get Images
        c1_img = self.c1.get_image(0)
        drone_img = self.c2.get_image(5)
        # rotate
        drone_img = cv.rotate(drone_img, cv.ROTATE_90_COUNTERCLOCKWISE)

        ipm = InversePerspectiveMapping(c1_img, drone_img, chosen_directory)
        ipm()

    def filedialog(self):
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self,
           self.tr("Open Image"), "", self.tr("Image Files (*.png *.jpg *bmp)"))
    
    def directorydialog(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")

    def check_and_mk_path(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
            return True
        else:
            self.warning('Directory already exists!')
            return False
            #raise Exception('Directory already exists!')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
    """
    ROOT = tk.Tk()
    ROOT.withdraw()
    FILE_DIR = simpledialog.askstring(title="Directory", prompt="Output Directory:")
    #print('Enter Output Directory: ')
    #FILE_DIR = input()
    FILE_DIR = os.path.join('outputs', FILE_DIR)
    check_and_mk_path(FILE_DIR)

    c1 = Camera(
        calibrate=False,
        calibration_file='canon_550d.json',
        image_dir='Dataset_1/Canon_550D/Images/c1',
        undistort=True,
        undistortion_crop=False
    )

    c2 = Camera(
        calibrate=False,
        calibration_file='dji_mini.json',
        image_dir='Dataset_1/DJI_Mini_2/Images',
        undistort=True,
        undistortion_crop=False
    )
    #TODO .calibrate() .undistort() .undistort_crop()
    #SET_POINTS = True

    c1_img = c1.get_image(0)
    drone_img = c2.get_image(5)

    # rotate
    drone_img = cv.rotate(drone_img, cv.ROTATE_90_COUNTERCLOCKWISE)

    ipm = InversePerspectiveMapping(c1_img, drone_img, FILE_DIR)
    ipm()
    """


