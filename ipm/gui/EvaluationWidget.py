import numpy as np
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QMenu, QSizePolicy, QInputDialog, QMessageBox, QLabel
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from gui.ImagePlot import ImagePlot

class SetComparisonPointWidget(QWidget):
    def __init__(self):
        pass


class EvaluationWidget(QWidget):
    def __init__(self, source_image, destination_image, output_image, h):
        super().__init__()
        self.source_image = ImagePlot(img=source_image)
        self.destination_image = ImagePlot(img=destination_image)
        self.output_image = output_image
        self.h = h
        self.btn_start_evaluation = QPushButton("Start Evaluation")
        self.btn_start_evaluation.clicked.connect(self.btn_start_evaluation_handler)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        l12 = QVBoxLayout()
        l22 = QVBoxLayout()

        vbox.addLayout(hbox)
        hbox.addLayout(l12)
        hbox.addLayout(l22)
        
        #l.addWidget(sc)
        l12.addWidget(self.source_image)
        l12.addWidget(NavigationToolbar2QT(self.source_image, self))
        l22.addWidget(self.destination_image)
        l22.addWidget(NavigationToolbar2QT(self.destination_image, self))

        self.loss_container = QLabel("0")

        #hbox.addWidget(self.source_image)
        #hbox.addWidget(self.destination_image)
        l12.addWidget(self.btn_start_evaluation)
        l22.addWidget(self.loss_container)
        self.setLayout(vbox)

    def btn_start_evaluation_handler(self):
        # add z for homogeneous coordinate
        transformed_source_pts = \
            [self.h.dot(np.array(pt + (1.0,))) for pt in self.source_image.reference_pts]
        transformed_source_pts = \
            [pt / pt[2] for pt in transformed_source_pts]

        self.destination_image.reference_pts_transformed = transformed_source_pts
        self.destination_image.axes.set_prop_cycle(None)
        for pt in self.destination_image.reference_pts_transformed:
            self.destination_image.axes.plot(pt[0], pt[1], marker='+', markersize=12)
            self.destination_image.draw()

        # TODO PIXEL TO CM

        # calc loss
        losses = []
        for pt1, pt2 in zip(self.destination_image.reference_pts, self.destination_image.reference_pts_transformed):
            tmp_loss = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
            losses.append(tmp_loss)
        print(losses)
        print(np.sum(losses))
        self.loss_container.setText("Loss: {:.2f}".format(np.sum(losses)))
        



        
