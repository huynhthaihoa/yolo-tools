"""
Fisheye distortion based on Scaramuzza Ocamcalib toolbox:
@credit: https://github.com/carlosferrazza/Python-Calibration
"""

import cv2
import numpy as np
import argparse
import pickle
import os
from glob import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input folder",
                    type=str, default="")
    parser.add_argument("-c", "--calibration", help="Path to the output calibration file",
                    type=str, default="calibration.dat")
    parser.add_argument("-o", "--output", help="Path to the output folder",
                    type=str, default="")
    parser.add_argument("-b", "--balance", help="Balance value",
                    type=float, default=0.0)
    
    args = parser.parse_args()
    
    INPUT_DIR = args.input
    
    with open(args.calibration, "rb") as f:
        data = pickle.load(f)
        dim, ret, K, D, rvecs, tvecs = data
        print(dim)
        print(K)
        print(D)
        #newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, dim, 1)
        # undistort
        #mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, dim, 5)
        #x, y, w, h = roi
        newcameramtx = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim, np.eye(3), balance=args.balance)
        mapx, mapy = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), newcameramtx, dim, cv2.CV_16SC2)
        print(mapx)
        print(mapy)
        
    OUTPUT_DIR = args.output
    if os.path.isdir(OUTPUT_DIR) is False:
        os.mkdir(OUTPUT_DIR)
    OUTPUT_DIR += '/'
    
    fnames = glob(INPUT_DIR + '\*.jpg')
    for fname in fnames:
        print(fname)
        basename = os.path.basename(fname)
        img = cv2.imread(fname)
        
        #undistort
        #dst = cv2.fisheye.undistortImage(img, mtx, dist, None, newcameramtx)
        dst = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        #dst = dst[y:y + h, x:x + w] 
        cv2.imwrite(OUTPUT_DIR + basename, dst)
    
    