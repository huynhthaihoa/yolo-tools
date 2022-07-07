import cv2
import numpy as np
import os
import glob
import argparse
import json
import pickle

calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_FIX_SKEW#+cv2.fisheye.CALIB_CHECK_COND
checkboard_corner_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
subpix_criteria = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1
termination_criteria = cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input folder",
                    type=str, default="")
    parser.add_argument("-c", "--checkerboard", help="Path to the checkboard shape (default is 7,10)", type=lambda s: [int(item) for item in s.split(',')], default = [7, 10])
    parser.add_argument("-v", "--validation", help="Path to the output validation folder", type=str, default="val")
    parser.add_argument("-e", "--error", help="Path to the error folder", type=str, default="err")
    parser.add_argument("-o", "--output", help="Path to the output calibration file (json/dat)",
                    type=str, default="calibration.json")
    
    args = parser.parse_args()
    
    INPUT_DIR = args.input
    OUTPUT_FILE = args.output
    VAL_DIR = args.validation
    ERR_DIR = args.error
    CHECKERBOARD = (args.checkerboard[0], args.checkerboard[1])
    
    if os.path.isdir(VAL_DIR) is False:
        os.mkdir(VAL_DIR)
    if os.path.isdir(ERR_DIR) is False:
        os.mkdir(ERR_DIR)
    
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    _img_shape = None
    objpoints = [] # 3d point in real world space
    imgpoints = []
    
    fnames = glob.glob(INPUT_DIR + '\*.jpg')
    for fname in fnames:
        print(fname)
        name = os.path.basename(fname)
        img = cv2.imread(fname)
        if _img_shape == None:
            _img_shape = img.shape[:2][::-1]
        else:
            assert _img_shape == img.shape[:2][::-1], "All images must share the same size."
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, checkboard_corner_flags)
        # If found, add object points, image points (after refining them)
        if ret == True:
            print("OK!")
            objpoints.append(objp)
            #Refine the corner locations
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), subpix_criteria)
            imgpoints.append(corners)
            val = cv2.drawChessboardCorners(img, CHECKERBOARD, corners, ret)
            cv2.imwrite(os.path.join(VAL_DIR, name), val)
        else:
            print("NG!")
            os.rename(fname, os.path.join(ERR_DIR, name))
    N_OK = len(objpoints)
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)] # rotation vector
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for i in range(N_OK)] # translation vector
    rms, K, D, rvecs, tvecs = cv2.fisheye.calibrate(
        objpoints,
        imgpoints,
        _img_shape,
        K,
        D,
        rvecs,
        tvecs,
        calibration_flags,
        termination_criteria
    )
    
    print("Found " + str(N_OK) + " valid images for calibration")
    print("DIM=" + str(_img_shape))
    print("K=np.asarray(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")
    print("rvecs={}\n".format(rvecs))
    print("tvecs={}\n".format(tvecs))
    ext = OUTPUT_FILE.split('.')[-1]
    if ext == 'dat':
        with open(OUTPUT_FILE, "wb") as f:
            data = [_img_shape, rms, K, D, rvecs, tvecs]
            pickle.dump(data, f)
    elif ext == 'json':
        with open(OUTPUT_FILE, "w") as f:
            data = {
                'dim': _img_shape,
                'rms': rms,
                'K': K.tolist(),
                'D': D.tolist(),
                'rvecs': rvecs,
                'tvecs': tvecs
        }
            json.dump(data, f)
    # file = open(OUTPUT_FILE, "w+")
    # file.write("Found " + str(N_OK) + " valid images for calibration\n")
    # file.write("DIM=" + str(_img_shape[::-1]) + "\n")
    # file.write("K=np.array(" + str(K.tolist()) + ")\n")
    # file.write("D=np.array(" + str(D.tolist()) + ")\n")
    # file.write("rvecs={}\n".format(rvecs))
    # file.write("tvecs={}\n".format(tvecs))
    # file.close()

