import cv2 as cv
import os
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QMenu, QSizePolicy, QInputDialog, QMessageBox
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from src.utils.gui.ImagePlot import ImagePlot
import json

# DOUBLE! Remove and import!
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# TODO Error handling ...
# TODO Hier aufraumen, dann save reference pts, images, etc.
# TODO ERROR if <4 pts
# TODO if infocus red border

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

        l1 = QHBoxLayout(self.main_widget)
        l12 = QVBoxLayout()
        l22 = QVBoxLayout()
        l1.addLayout(l12)
        l1.addLayout(l22)
        
        self.dc1 = ImagePlot(self.main_widget, width=5, height=4, dpi=100, img=self.source_img)
        self.dc2 = ImagePlot(self.main_widget, width=5, height=4, dpi=100, img=self.destination_img)
        #l.addWidget(sc)
        l12.addWidget(self.dc1)
        l12.addWidget(NavigationToolbar2QT(self.dc1, self))
        l22.addWidget(self.dc2)
        l22.addWidget(NavigationToolbar2QT(self.dc2, self))


        btn_run_ipm = QPushButton("Run IPM")
        btn_run_ipm.clicked.connect(self.btn_run_ipm_handler)
        btn_save_ipm = QPushButton("Save IPM")
        btn_save_ipm.clicked.connect(self.btn_save_ipm_handler)
        l12.addWidget(btn_run_ipm)
        l22.addWidget(btn_save_ipm)

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
        ok = self._run_ipm()
        if not ok:
            return 
        cv.imshow('img', self.output_img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def _run_ipm(self):
        if(not self._enough_reference_pts()):
            self._show_error_box("Not enough reference points! Need at least 4 for each image.")
            return False
        self.source_img.reference_pts = self.dc1.reference_pts
        self.destination_img.reference_pts = self.dc2.reference_pts
        output_img, h = self.transform_img(self.source_img, self.destination_img)
        self.output_img = cv.cvtColor(output_img, cv.COLOR_BGR2RGB)
        self.h = h
        return True

    def _enough_reference_pts(self):
        if len(self.dc1.reference_pts) < 4 or len(self.dc2.reference_pts) < 4:
            return False
        return True
            
    def _show_error_box(self, text):
        dlg = QMessageBox(self)
        dlg.setText(text)
        dlg.setIcon(QMessageBox.Warning)
        dlg.exec_()


    def btn_save_ipm_handler(self):
        ok = self._run_ipm()
        if not ok:
            return
        output_dir = self._ask_for_destination_folder()
        self._make_output_dir(output_dir)
        self._save_images(output_dir)
        self._save_reference_pts(output_dir)
        self._save_homography_matrix(output_dir)

    def _save_homography_matrix(self, dir):
        json.dump(self.h, open(dir + '/homography_matrix.json', "w"), cls=NpEncoder)

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
        output_image = cv.warpPerspective(source_img.img, h, size)
        return output_image, h
