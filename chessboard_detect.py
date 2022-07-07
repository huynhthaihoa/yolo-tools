import cv2
import numpy as np
import os
from glob import glob
import argparse
import json
# import pickle

checkboard_corner_flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
subpix_criteria = cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1

def getTimeStamp(index, fps):
    '''
    get time stamp of the frame:
    @index [in]: frame index,
    @fps [in]: camera frame per second
    '''
    millisecond = int(index * (1000 / fps))
    second, millisecond = divmod(millisecond, 1000)
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    return "{0:02d}h{1:02d}m{2:02d}s{3:03d}ms".format(hour, minute, second, millisecond)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input video/folder",
                    type=str, default="inp")
    parser.add_argument("-c", "--checkerboard", help="Checkboard shape (default is 7,10)", type=lambda s: [int(item) for item in s.split(',')], default = [7, 10])
    parser.add_argument("-w", "--win_size", help="Square size (default is 11)", type=int, default=11)
    parser.add_argument("-o", "--output", help="Path to the output folder", type=str, default="out")
    parser.add_argument("-e", "--error", help="Path to the error folder", type=str, default="err")
    parser.add_argument("-r", "--record_file", help="Path to save corner detection file", type=str, default="detections.pickle")
    args = parser.parse_args()
    
    INPUT = args.input
    CHECKERBOARD = (args.checkerboard[0], args.checkerboard[1])
    OUTPUT_DIR = args.output
    ERR_DIR = args.error
    SQUARE_SIZE = args.win_size
    
    objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    print(objp.shape)
    _img_shape = None
    # objpoints = [] # 3d point in real world space
    imgpoints = list()
    #stamps = []
    if os.path.isdir(OUTPUT_DIR) is False:
        os.mkdir(OUTPUT_DIR)
    if os.path.isdir(ERR_DIR) is False:
        os.mkdir(ERR_DIR)
    
    images = list() # original images
    grays = list() # grayscale images
    names = list() # image base names
    fnames = list() # image file names
    imgpoints = list()
    stamps = list()
    
    if os.path.isdir(INPUT) is True:
        fnames = glob(INPUT + "\*.jpg")
        for fname in fnames:
            name = os.path.basename(fname)
            image = cv2.imread(fname)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            names.append(name)
            images.append(image)
            grays.append(gray)
    else:
        source = cv2.VideoCapture(INPUT)
        fps = source.get(cv2.CAP_PROP_FPS)
        basename = os.path.basename(INPUT).split('.')[0]
        INPUT_DIR = INPUT[:INPUT.rfind('.')]
        if os.path.isdir(INPUT_DIR) is False:
            os.mkdir(INPUT_DIR)
        i = 0
        while True:
            ret, image = source.read()
            if not ret:
                break
            suffix = getTimeStamp(i, fps)
            name = basename + "_" + suffix + ".jpg"
            i += 1
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            names.append(name)
            images.append(image)
            grays.append(gray)
            fname = os.path.join(INPUT_DIR, name)
            cv2.imwrite(fname, image)
            fnames.append(fname)
    
    data = dict() # for saving detection result
    
    for idx, gray in enumerate(grays):
        print(names[idx])
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, checkboard_corner_flags)
        if ret is True:
            print("OK!")
            corners = cv2.cornerSubPix(gray, corners, (SQUARE_SIZE, SQUARE_SIZE), (-1, -1), subpix_criteria)
            out = cv2.drawChessboardCorners(images[idx], CHECKERBOARD, corners, ret)
            cv2.imwrite(os.path.join(OUTPUT_DIR, names[idx]), out)
            # objpoints.append(objp)
            imgpoints.append(corners.squeeze())
            stamps.append(fnames[idx])
        else:
            print("NG!")
            os.rename(fnames[idx], os.path.join(ERR_DIR, name)) 
    
    # data = dict()
    # for stamp, objpoint, imgpoint in zip(stamps, objpoints, imgpoints):
    #     data[stamp] = {
    #         "object_points": objpoint.tolist(), 
    #         "image_points": imgpoint.tolist()
    #         }
    with open(args.record_file, "w") as f:
        json.dump(
            {
               'detections': {
                   stamp: {
                       "object_points": objp.tolist(), 
                       "image_points": imgpoint.tolist()
                  }  
                  for stamp, imgpoint in zip(stamps, imgpoints)
               }
            }, f, indent=2
        )
        # for stamp, objpoint, imgpoint in zip(stamps, objpoints, imgpoints):
        #     json.dump({
        #      stamp:
        #      {
        #          'image_points': imgpoint.tolist(),
        #          'object_points': objpoint.tolist()
        #     }}, f)
        #     f.write('\n')
        
        # for record in data:
        #     json.dump(record, f, indent=2)
        # json.dump({
        #     stamp:
        #     {
        #         'image_points': imgpoint.tolist(),
        #         'object_points': objpoint.tolist()
        #     }   
        #     for stamp, imgpoint, objpoint in zip(stamps, objpoints, imgpoints)
        # }, f, indent=2)
        #f.write('\n')
        #json.dump(data, f)
    print("Finish!")




