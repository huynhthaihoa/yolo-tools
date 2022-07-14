"""
Fisheye distortion based on Scaramuzza Ocamcalib toolbox:
@credit: https://github.com/carlosferrazza/Python-Calibration
"""

import cv2
import numpy as np
import argparse
import json
import os
from glob import glob
import pickle

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input folder",
                    type=str, default="")
    parser.add_argument("-c", "--calibration", help="Path to the calibration file (json/dat)",
                    type=str, default="calibration.json")
    parser.add_argument("-o", "--output", help="Path to the output folder",
                    type=str, default="")
    # parser.add_argument("-b", "--balance", help="Balance value",
    #                 type=float, default=0.0)
    
    args = parser.parse_args()
    
    INPUT_DIR = args.input
    
    calibration = args.calibration
    ext = calibration.split('.')[-1]
    if ext == 'dat':
        with open(args.calibration, "rb") as f:
            data = pickle.load(f)
        # data = json.load(f)
            dim, ret, K, D, rvecs, tvecs = data
    elif ext == 'json':
        with open(args.calibration, "r") as f:
            data = json.load(f)
            dim = data['dim']
            ret = data['rms']
            K = np.array(data['K'])
            D = np.array(data['D'])
            rvecs = data['rvecs']
            tvecs = data['tvecs']
        #dim, ret, K, D = data
    print(dim)
    print(K)
    print(D)
        #newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx, dist, dim, 1)
        # undistort
        #mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, dim, 5)
        #x, y, w, h = roi
        # newcameramtx = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(K, D, dim, np.eye(3), balance=args.balance)
        # mapx, mapy = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), newcameramtx, dim, cv2.CV_16SC2)
        # print(mapx)
        # print(mapy)
        
    OUTPUT_DIR = args.output
    if os.path.isdir(OUTPUT_DIR) is False:
        os.mkdir(OUTPUT_DIR)
    OUTPUT_DIR += '/'
    
    fnames = glob(INPUT_DIR + '\*.jpg')
    for fname in fnames:
        print(fname)
        basename = os.path.basename(fname)
        img = cv2.imread(fname)
        # img_dim = (640, 480)
        img_dim = img.shape[:2][::-1]
        
        scaled_K = K * img_dim[0] / float(dim[0])
        scaled_K[2][2] = 1.0
        
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(scaled_K, D, img_dim, 1) #K
        
        mapx, mapy = cv2.fisheye.initUndistortRectifyMap(
            scaled_K, D, np.eye(3), newcameramtx, img_dim, cv2.CV_16SC2
        )
        dst = cv2.remap(img, mapx, mapy, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

        # dst = cv2.fisheye.undistortImage(img, scaled_K, D, None, newcameramtx) #K

        cv2.imwrite(OUTPUT_DIR + basename, dst)
    
    