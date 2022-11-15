from PySide6 import QtCore
from PySide6.QtWidgets import QSizePolicy
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class BaseMatplotCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100, img=''):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure(img)
        FigureCanvasQTAgg.__init__(self, fig)
        self.setParent(parent)
        FigureCanvasQTAgg.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def compute_initial_figure(self, img):
        pass

class ImagePlot(BaseMatplotCanvas):
    def __init__(self, *args, **kwargs):
        BaseMatplotCanvas.__init__(self, *args, **kwargs)
        self.reference_pts = []
        self.setFocusPolicy( QtCore.Qt.ClickFocus )
        self.setFocus()
        cid = self.mpl_connect('key_press_event', self.on_press)

    def compute_initial_figure(self, img):
        #img = cv.imread(img)
        self.axes.imshow(img.img)

    def on_press(self, event):
        if event.key == 'x':
            self.axes.plot(event.xdata, event.ydata, marker='x', markersize=12)
            self.reference_pts.append((event.xdata, event.ydata))
            self.axes.text(event.xdata, event.ydata, len(self.reference_pts))
        if event.key == 'r':
            self.axes.lines[-1].remove()
            del_el = self.reference_pts.pop()
        self.draw()