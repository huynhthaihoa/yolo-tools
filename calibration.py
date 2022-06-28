import cv2
import numpy as np
import os
import glob
import argparse

subpix_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input folder",
                    type=str, default="")
    parser.add_argument("-o", "--output", help="Path to the output calibration file",
                    type=str, default="calibration.txt")
    parser.add_argument("-c", "--checkerboard", help="Path to the checkboard shape (default is 6,9)", type=lambda s: [int(item) for item in s.split(',')], default = [6, 9])
    
    args = parser.parse_args()
    
    INPUT_DIR = args.input
    OUTPUT_FILE = args.output
    CHECKERBOARD = (args.checkerboard[0], args.checkerboard[1])
    
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    _img_shape = None
    objpoints = [] # 3d point in real world space
    imgpoints = []
    
    images = glob.glob(INPUT_DIR + '\*.jpg')
for fname in images:
    print(fname)
    img = cv2.imread(fname)
    if _img_shape == None:
        _img_shape = img.shape[:2]
    else:
        assert _img_shape == img.shape[:2], "All images must share the same size."
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("OK!")
        objpoints.append(objp)
        cv2.cornerSubPix(gray, corners, (3,3), (-1,-1), subpix_criteria)
        imgpoints.append(corners)
    else:
        print("NG!")
    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)] # rotation vector
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)] # translation vector
    rms, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        gray.shape[::-1],
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6)
    )
    
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape[::-1]))
    print("K=np.asarray(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")
    print("rvecs={}\n".format(rvecs))
    print("tvecs={}\n".format(tvecs))
    file = open(OUTPUT_FILE, "w+")
    file.write("Found " + str(N_OK) + " valid images for calibration\n")
    file.write("DIM=" + str(_img_shape[::-1]) + "\n")
    file.write("K=np.array(" + str(K.tolist()) + ")\n")
    file.write("D=np.array(" + str(D.tolist()) + ")\n")
    file.write("rvecs={}\n".format(rvecs))
    file.write("tvecs={}\n".format(tvecs))
    file.close()

