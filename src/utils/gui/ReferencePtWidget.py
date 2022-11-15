from src.utils.Camera import CameraCalibration
from src.utils.InversePerspectiveMapping import InversePerspectiveMapping
from src.utils.Image import Image
import cv2 as cv
import sys, os
import numpy as np
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QFormLayout, QPushButton, QTabWidget, QGridLayout, QVBoxLayout, QMainWindow, QLineEdit, QGroupBox, QHBoxLayout, QCheckBox, QMenu, QSizePolicy, QInputDialog
from PySide6.QtGui import QPixmap, QImage, qRgb, QColor, QPainter, QPen
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from src.utils.gui.CameraWidget import CameraWidget


# TODO Hier aufraumen, dann save reference pts, images, etc.

class MyMPLCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, img=''):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure(img)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding,
                                            QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def compute_initial_figure(self, img):
        pass


class MyStaticMplCanvas(MyMPLCanvas):
    def compute_initial_figure(self, img):
        #img = cv.imread(img)
        self.axes.imshow(img.img)

class MyDynamicMplCanvas(MyMPLCanvas):
    def __init__(self, *args, **kwargs):
        MyMPLCanvas.__init__(self, *args, **kwargs)
        self.reference_pts = []
        self.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.setFocus()
        cid = self.mpl_connect('key_press_event', self.on_press)

    def compute_initial_figure(self, img):
        #img = cv.imread(img)
        self.axes.imshow(img.img)

    def on_press(self, event):
        # extra: number for the pts 
        if event.key == 'x':
            self.axes.plot(event.xdata, event.ydata, marker='x', markersize=12)
            self.reference_pts.append((event.xdata, event.ydata))
            self.axes.text(event.xdata, event.ydata, len(self.reference_pts))
        self.draw()


class SetReferencePtsWindow(QMainWindow):
    def __init__(self, source_img, destination_img):  
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.source_img = source_img
        self.destination_img = destination_img

        self.reference_pts_source = []
        self.reference_pts_destination = []

        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QWidget(self)

        l = QVBoxLayout(self.main_widget)
        self.dc1 = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100, img=self.source_img)
        self.dc2 = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100, img=self.destination_img)
        #l.addWidget(sc)
        l.addWidget(self.dc1)
        l.addWidget(NavigationToolbar2QT(self.dc1, self))
        l.addWidget(self.dc2)
        l.addWidget(NavigationToolbar2QT(self.dc2, self))


        btn_run_ipm = QPushButton("Run IPM")
        btn_run_ipm.clicked.connect(self.btn_run_ipm_handler)
        btn_save_ipm = QPushButton("Save IPM")
        btn_save_ipm.clicked.connect(self.btn_save_ipm_handler)
        l.addWidget(btn_run_ipm)
        l.addWidget(btn_save_ipm)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("Set reference pts!", 2000) 


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About", "test")

    def btn_run_ipm_handler(self):
        self.source_img.reference_pts = self.dc1.reference_pts
        self.destination_img.reference_pts = self.dc2.reference_pts
        output_img = self.transform_img(self.source_img, self.destination_img)
        self.output_img = cv.cvtColor(output_img, cv.COLOR_BGR2RGB)
        cv.imshow('img', self.output_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def btn_save_ipm_handler(self):
        output_dir = self._ask_for_destination_folder()
        self._make_output_dir(output_dir)
        self._save_images(output_dir)
        self._save_reference_pts(output_dir)

    def _ask_for_destination_folder(self):
        dir, ok = QInputDialog().getText(self, "Output directory", "Enter output directory:") #TBD
        if ok:
            dir = './outputs/' + dir
            return dir

    def _make_output_dir(self, dir):
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        else:
            # handle it
            pass

    def _save_images(self, dir):
        self.source_img.save(dir)
        self.destination_img.save(dir)
        cv.imwrite(dir+'/output_image.jpg', self.output_img)

    def _save_reference_pts(self, dir):
        self.source_img.write_reference_pts(dir)
        self.destination_img.write_reference_pts(dir)



    def transform_img(self, source_img, destination_img):
        h, status = cv.findHomography(
            np.array([source_img.reference_pts]),
            np.array([destination_img.reference_pts])
        )
        size = (destination_img.img.shape[1], destination_img.img.shape[0])
        # FAIL TODO I need now Imagename to load for image
        output_image = cv.warpPerspective(source_img.img, h, size)
        return output_image
