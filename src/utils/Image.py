import cv2 as cv
import json
from datetime import datetime
import os

class Image():
    def __init__(self, img, img_name):
        img = cv.imread(img)
        self.img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.filename = img
        self.name = img_name
        self.reference_pts = []
        
    def draw(self):
        for pt in self.reference_pts:
            cv.circle(self.img, (int(pt[0]), int(pt[1])), 2, (0, 0, 255), 2)
        img = cv.cvtColor(self.img, cv.COLOR_RGB2BGR)
        cv.imshow('img', img)
        cv.waitKey(0)

    def _draw_reference_pts(self):
        for pt in self.reference_pts:
            cv.circle(self.img, (int(pt[0]), int(pt[1])), 2, (255, 0, 0), 2)
        

    def save(self, dir):
        filename = os.path.join(dir, 'image_'+self.name+'.jpg')
        self._draw_reference_pts()
        img = cv.cvtColor(self.img, cv.COLOR_RGB2BGR)
        cv.imwrite(filename, img)

    def undistort(self, camera_matrix, dist_coeffs, crop=False):
        h, w = self.img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(
            camera_matrix, dist_coeffs, (w,h), 1, (w,h)
        )
        dst = cv.undistort(self.img, camera_matrix, dist_coeffs, None, newcameramtx)
        
        if crop:
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
         
        self.img = dst


    def write_reference_pts(self, dir):
        filename = os.path.join(dir, 'reference_pts_'+self.name+'.json')
        with open(filename, 'w') as file:
            json.dump(self.reference_pts, file)

    def load_reference_pts(self, filename):
        try:
            with open(filename, 'r') as file:
                self.reference_pts = json.load(file)
        except:
            print("error")
            raise
        