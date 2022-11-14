from src.utils.Image import Image
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys

class InversePerspectiveMapping():
    def __init__(self):
        self.output_image = None
        self.output_directory = None
        self.source_image = None
        self.destination_image = None

    def set_source_img(self, filename):
        self.source_image = Image(filename, 'source_image')

    def set_destination_img(self, filename):
        self.destination_image = Image(filename, 'destination_image')

    def set_output_directory(self, dir):
        self.output_directory = dir

    def write_reference_pts(self):
        print('save reference pts')
        self.source_image.write_reference_pts(self.output_directory)
        self.destination_image.write_reference_pts(self.output_directory)

    def load_reference_pts(self, source_filename, destination_filename):
        self.source_image.load_reference_pts(source_filename)
        self.destination_image.load_reference_pts(destination_filename)

    def set_homography_reference_pts(self): #TODO GUI auslagern?
        print('set homography referene pts')
        reference_pts_source = []
        reference_pts_destination = []
        def on_press(event):
            sys.stdout.flush()
            if event.key == 'x':
                if event.inaxes == ax1:
                    ax1.plot(event.xdata, event.ydata, marker='x', markersize=12)
                    reference_pts_source.append((event.xdata, event.ydata))
                elif event.inaxes == ax2:
                    ax2.plot(event.xdata, event.ydata, marker='x', markersize=12)
                    reference_pts_destination.append((event.xdata, event.ydata))
                fig.canvas.draw()

        fig = plt.figure(figsize=(15, 10))
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        # Convert Colors for Matplotlib
        tmp_img1 = cv.cvtColor(self.source_image.img, cv.COLOR_BGR2RGB)
        tmp_img2 = cv.cvtColor(self.destination_image.img, cv.COLOR_BGR2RGB)
        ax1.imshow(tmp_img1)
        ax2.imshow(tmp_img2)
        cid = fig.canvas.mpl_connect('key_press_event', on_press)
        plt.show()
        self.source_image.reference_pts = reference_pts_source
        self.destination_image.reference_pts = reference_pts_destination

    def transform_img(self):
        print('transform image')
        h, status = cv.findHomography(
            np.array([self.source_image.reference_pts]),
            np.array([self.destination_image.reference_pts])
        )
        size = (self.destination_image.img.shape[1], self.destination_image.img.shape[0])
        self.output_image = Image(cv.warpPerspective(self.source_image.img, h, size), 'transformed')

    def save_images(self):
        self.source_image.save(self.output_directory)
        self.destination_image.save(self.output_directory)
        self.output_image.save(self.output_directory)

    def show_images(self):
        self.source_image.draw()
        self.destination_image.draw()
        self.output_image.draw()



    def __call__(self):
        self.set_homography_reference_pts()
        self.write_reference_pts()
        self.transform_img()
        self.save_images()
        self.show_images()
