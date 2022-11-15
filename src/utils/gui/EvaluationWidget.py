import cv2 as cv
import os
import numpy as np
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QMenu, QSizePolicy, QInputDialog, QMessageBox, QLabel
from matplotlib.figure import Figure
from PySide6 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from src.utils.Image import Image
from src.utils.gui.ImagePlot import ImagePlot
import json

#Vererbung ReferencePts und Evaluation?
# Beide setzen Pts -> SetPtWidget oder CompareImagesWidget

# Dont forget, You already Have Homography Matrix H !! 
# Hence calculate error:
#   Set Point on Destinaton Image
#   Set Point on Source Image
#   pt1 = point that has been set in Destinaton image
#   pt2 = H * Point that has been set in Source Image
#   Calculate distance (pt1, pt2) - as pt1 and pt2 should now have same coordinates --> in pixel
#   n mal -> RMSE --> in pixel
#   [[[pixel zu Meter umrechnen (Durch landmarken im destination img)]]] pixel-scale-factor


###### This means i need so save H!



class SetComparisonPointWidget(QWidget):
    def __init__(self):
        pass


class EvaluationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.source_image = ImagePlot(img=Image('Datasets/Dataset_1/Canon_550D/Images/c1/IMG_1241.JPG', 'source_image'))
        self.destination_image = ImagePlot(img=Image('Datasets/Dataset_1/Canon_550D/Images/c1/IMG_1241.JPG', 'destination_image'))
        self.btn_start_evaluation = QPushButton("Load Evaluation Data...")
        self.btn_start_evaluation.clicked.connect(self.btn_start_evaluation_handler)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addWidget(self.source_image)
        hbox.addWidget(self.destination_image)
        vbox.addWidget(self.btn_start_evaluation)
        self.setLayout(vbox)

    def btn_start_evaluation_handler(self):
        dir = self._ask_for_dir()
        self.load_data(dir)

    def load_data(self, dir):
        self.load_source_image(dir)
        self.load_destination_image(dir)
        self.load_output_image(dir)
        self.load_homography_matrix(dir)
        print(self.h)

    def load_source_image(self, dir):
        img = Image(dir + '/image_source_camera.jpg', 'souce_camera')
        self.source_image = img

    def load_destination_image(self, dir):
        img = Image(dir + '/image_destination_camera.jpg', 'destination_camera')
        self.destination_image = img

    def load_output_image(self, dir):
        img = Image(dir + '/image_output.jpg', 'image_output')
        self.output_image = img

    def load_homography_matrix(self, dir):
        h = json.load(dir + '/homograph_matrix.json')
        self.h = np.array(h)

    def _ask_for_dir(self):
        return QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", './')

