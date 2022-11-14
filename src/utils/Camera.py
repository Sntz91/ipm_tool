from re import A
import numpy as np
import cv2 as cv
import glob
import os, json
from collections import namedtuple

CalibrationMatrix = namedtuple('CalibrationMatrix', ['ret', 'mtx', 'dist', 'rvecs', 'tvecs'])

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class CameraCalibration():
    def __init__(self, calibration_dir=None):
        self.calibration_dir = calibration_dir
        self.calibrated = False
        self.calibration_matrix = None

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

        calibration_img_names = sorted(glob.glob(self.calibration_dir + '/*.JPG'))
            
        for fname in calibration_img_names:
            print('Calibrate on image {0:d}/{1:d}'.format(counter+1, len(calibration_img_names))) 
            counter += 1
                
            img = cv.imread(fname)
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

            ret, corners = cv.findChessboardCorners(gray, (6, 9), None)
            if ret == True:
                objpoints.append(objp)
                corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners)

        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        self.calibration_matrix = CalibrationMatrix(ret, mtx, dist, rvecs, tvecs) #BS TODO
        self.calibrated = True

    def save_calibration(self, filename):
        #try:
        json.dump(self.calibration_matrix._asdict(), open(filename, "w"), cls=NpEncoder)

    def load_calibration(self, filename):
        file = open(filename, 'r')
        data = json.load(file)
        print(data)
        self.calibration_matrix = CalibrationMatrix(data['ret'], np.array(data['mtx']), np.array(data['dist']), data['rvecs'], data['tvecs'])