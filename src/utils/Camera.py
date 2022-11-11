from re import A
import numpy as np
import cv2 as cv
import glob
import os, json

class Camera():
    def __init__(self, calibration_dir, image_dir=None):
        self.calibration_images = sorted(glob.glob(calibration_dir + '/*.JPG'))
        if image_dir:
            self.undistorted_images = sorted(glob.glob(image_dir + '/*.JPG'))
        else:
            self.undistorted_images = []
        self.calibrated = False
        self.points = []
        self.images = []
        
        print('Camera has {0:d} calibration images and {1:d} images.'.format(
            len(self.calibration_images), len(self.undistorted_images)
        ))
        
    
    def calibrate(self):
        # termination criteria
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # preprare object points -> can also make it cm etc. if we know lenght of grid (x,y,z)
        objp = np.zeros((9*6, 3), np.float32)
        objp[:, :2] = np.mgrid[0:6, 0:9].T.reshape(-1, 2)
        
        # Arrays to store object points and image points from all the images
        objpoints = [] #3d point in real world space
        imgpoints = [] #2d points in image plane
        
        counter = 0
        
        for fname in self.calibration_images:
            print('Calibrate on image {0:d}/{1:d}'.format(counter+1, len(self.calibration_images)))
            counter += 1
            
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            ret, corners = cv.findChessboardCorners(gray, (6, 9), None)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        
        self.mtx = mtx
        self.dist = dist
        self.rvecs = rvecs
        self.tvecs = tvecs
        
        self.calibrated = True
        print('calibrated camera')

    
        return True

    def save_calibration(self, filename):
        d = {
            'mtx': self.mtx.tolist(),
            'dist': self.dist.tolist(),
            'rvecs': np.array(self.rvecs).tolist(),
            'tvecs': np.array(self.tvecs).tolist()
        }
        json.dump(d, open(filename, "w"))

    def load_calibration(self, filename):
        try:
            f = open(filename, 'r')
            data = json.load(f)
            self.mtx = np.array(data['mtx'])
            self.dist = np.array(data['dist'])
            self.rvecs = np.array(data['rvecs'])
            self.tvecs = np.array(data['tvecs'])
            self.calibrated = True
            print('calibrated camera')
        except FileNotFoundError:
            print('File not found!', filename)
            raise
        except Exception:
            print('Error reading file.', filename)
            raise
        
    def undistort_images(self, crop=False):
        if not self.calibrated: 
            print('Camera not calibrated, wont undistort images!')
            self.images = [cv.imread(img) for img in self.undistorted_images]
            return False
        counter = 0
        self.images = []
        
        for image in self.undistorted_images:
            print('Undistorted image {0:d}/{1:d}'.format(counter+1, len(self.undistorted_images)))
            counter+=1
            img = cv.imread(image)
            h, w = img.shape[:2]
            newcameramtx, roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))
            dst = cv.undistort(img, self.mtx, self.dist, None, newcameramtx)
            
            if crop:
                x, y, w, h = roi
                dst = dst[y:y+h, x:x+w]

            self.images.append(dst)
        print('undistorted images')
        return True
    
    def get_image(self, idx):
        assert idx < len(self.images)
        return self.images[idx]

    def get_undistorted_image(self, idx):
        assert idx < len(self.images)
        img = self.undistorted_images[idx]
        img = cv.imread(img)
        return img
    
    