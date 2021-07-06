"""
Generate label dataset using YOLO annotation files
Created on March 4th 2021

@author: Thai-Hoa Huynh
"""

import os
from glob import glob
#import cv2
import numpy as np
import argparse
from PIL import Image

def unconvert(width, height, x, y, w, h):
    '''
    Convert the normalized positions into integer positions:
    @width [in]:
    @height [in]:
    @x [in]:
    @y [in]:
    @xmin [out]:
    @xmax [out]:
    @ymin [out]:
    @ymax [out]:
    '''
    xmax = int((x*width) + (w * width)/2.0)
    xmin = int((x*width) - (w * width)/2.0)
    ymax = int((y*height) + (h * height)/2.0)
    ymin = int((y*height) - (h * height)/2.0)
    return (xmin, xmax, ymin, ymax)
    #else:  

# def update(width, height, size, x, y, w, h):
#     (xmin, xmax, ymin, ymax) =  unconvert(width, height, x, y, w, h)
#     if size < xmax - xmin:
#         size = xmax - xmin
#     if size < ymax - ymin:
#         size = ymax - ymin
#     r_width = size + xmin - xmax
#     r_height = size + ymin - ymax
#     r_width_left = (size + xmin - xmax) / 3
#     r_height_top = (size + ymin - ymax) / 3
   
#     #if xmin - r_width_left >= 0:
#     xmin -= r_width_left
#     if xmin < 0:
#         xmin = 0
#     xmax = xmin + size
#     if xmax > width:
#         xmax = width
#         xmin = xmax - size
#     ymin -= r_height_top
#     if ymin < 0:
#         ymin = 0
#     ymax = ymin + size
#     if ymax > height:
#         ymax = height
#         ymin = ymax - size
#     return (xmin, xmax, ymin, ymax)
    
def update_ROI(width, height, size, xmin, xmax, ymin, ymax):
    if size < xmax - xmin:
        size = xmax - xmin
    if size < ymax - ymin:
        size = ymax - ymin
    # r_width = size + xmin - xmax
    # r_height = size + ymin - ymax
    r_width_left = (size + xmin - xmax) / 3
    r_height_top = (size + ymin - ymax) / 3
   
    #if xmin - r_width_left >= 0:
    xmin -= r_width_left
    if xmin < 0:
        xmin = 0
    xmax = xmin + size
    if xmax > width:
        xmax = width
        xmin = xmax - size
    ymin -= r_height_top
    if ymin < 0:
        ymin = 0
    ymax = ymin + size
    if ymax > height:
        ymax = height
        ymin = ymax - size
    return (int(xmin), int(xmax), int(ymin), int(ymax))

def convert(size, x_min, x_max, y_min, y_max, digit=6):
    '''
    Convert object size into bounding box:
    @size [in]
    @box [in]
    @digit
    '''
    dw = 1./(size)
    dh = 1./(size)
    x = (x_min + x_max)/2.0 - 1
    y = (y_min + y_max)/2.0 - 1
    w = x_max - x_min
    h = y_max - y_min
    x = round(x * dw, digit)
    w = round(w * dw, digit)
    y = round(y * dh, digit)
    h = round(h * dh, digit)
    return (x, y, w, h)

# def update_annotation(width, height, size, x, y, w, h):
    # (xmin_old, xmax_old, ymin_old, ymax_old) =  unconvert(width, height, x, y, w, h)
    # W_old = xmax_old - xmin_old
    # H_old = ymax_old - ymin_old
    # (xmin_new, xmax_new, ymin_new, ymax_new) =  update(width, height, size, x, y, w, h)
    # W_new = xmax_new - xmin_new
    # H_new = ymax_new - ymin_new
    # dif_x = (xmin_old - xmin_new)
    # dif_y = (ymin_old - ymin_new)
    # x_new = ((x * W_old) + dif_x) / W_new
    # y_new = ((y * H_old) + dif_y) / H_new 
    # w_new = (w * W_old) / W_new 
    # h_new = (h * H_old) / H_new
    # return (x_new, y_new, w_new, h_new)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of original images",
                    type=str, default="D:\img_detection")                               
    parser.add_argument("-a", "--ann", help="Directory of original OCR annotation files (.txt)",
                    type=str, default="D:\img_LPR")
    parser.add_argument("-s", "--size", help="Cropped image size",
                    type=int, default=608)
    parser.add_argument("-u", "--update_ann", help="Directory of updated OCR annotation files (.txt)",
                    type=str, default="D:\img_LPR_update")
    args = parser.parse_args()
    size = args.size
    dSize = 1. / size
    annDir = args.ann + '/'
    imgDir = args.img + '/'
    data = dict()
    newannDir = args.update_ann
    if os.path.isdir(newannDir) is False:
        os.mkdir(newannDir)
    newannDir += '/'
    anns = glob(annDir + '/*.txt')
    exts = ['.jpg', '.png', '.jpeg', '.jfif']
    log = open("log_update_annotations.txt", "wt")
    for ann in anns:

        inputAnnFile = open(ann, "rt")
        basename = os.path.basename(ann)
        basename = basename[: basename.rfind('.')]
        #print(basename)
        if basename == 'classes':
            continue
        targetName = newannDir + basename
        updateAnnFile = open(targetName + ".txt", "wt")
        cropImgName = targetName + ".png"
        idx = 0
        id_stop = basename.find('-')
        if(id_stop != -1):
            basename = basename[: id_stop]
        # try:
        #     #idx = int(basename[basename.rfind('_') + 1: basename.rfind('.')])
        #     basename = basename[: basename.find('-')]
        # except:
        #     pass
        
        detAnnName = imgDir + basename + ".txt"
        if os.path.isfile(detAnnName) is True and os.stat(detAnnName).st_size > 0:
            if detAnnName not in data:
                data[detAnnName] = np.loadtxt(detAnnName).reshape(-1, 5)
            #print("Data: {0} {1} {2} {3}\n".format(float(data[detAnnName][idx][1]), float(data[detAnnName][idx][2]), float(data[detAnnName][idx][3]), float(data[detAnnName][idx][4])))

            for ext in exts:
                imgname = imgDir + basename + ext
                if os.path.isfile(imgname) is True:
                    img = Image.open(imgname)
                    width, height = img.size
                    # (xmin, xmax, ymin, ymax) = update(width, height, size, float(data[detAnnName][idx][1]), float(data[detAnnName][idx][2]), float(data[detAnnName][idx][3]), float(data[detAnnName][idx][4]))                
                    # cropArea = (xmin, ymin, xmax, ymax)
                    # cropImg = img.crop(cropArea)
                    #print(ids[i])
                    
                    (xR_min_old, xR_max_old, yR_min_old, yR_max_old) = unconvert(width, height, float(data[detAnnName][idx][1]), float(data[detAnnName][idx][2]), float(data[detAnnName][idx][3]), float(data[detAnnName][idx][4]))
                    #print("Old: {0} {1} {2} {3}\n".format(xR_min_old, xR_max_old, yR_min_old, yR_max_old))
                    wR_old = xR_max_old - xR_min_old
                    hR_old = yR_max_old - yR_min_old
                    (xR_min_new, xR_max_new, yR_min_new, yR_max_new) = update_ROI(width, height, size, xR_min_old, xR_max_old, yR_min_old, yR_max_old)
                    cropArea = (xR_min_new, yR_min_new, xR_max_new, yR_max_new)
                    cropImg = img.crop(cropArea)
                    cropImg.save(cropImgName)
                    dif_xR = xR_min_old - xR_min_new
                    dif_yR = yR_min_old - yR_min_new
                    #print("Difference: {0} {1}\n".format(dif_xR, dif_yR))
                    #wR_new = xR_max_new - xR_min_new
                    #hR_new = yR_max_new - yR_min_new
                    for line in inputAnnFile:
                        elems = line.split(' ')
                        try:
                            x_center_old = float(elems[1])
                            y_center_old = float(elems[2])
                            width_old = float(elems[3])
                            height_old = float(elems[4])
                            x_center_new = (x_center_old * wR_old + dif_xR) * dSize
                            y_center_new = (y_center_old * hR_old + dif_yR) * dSize
                            width_new = (width_old * wR_old) * dSize
                            height_new = (height_old * hR_old) * dSize
                            updateAnnFile.write("{0} {1} {2} {3} {4}\n".format(int(elems[0]), x_center_new, y_center_new, width_new, height_new))
                            # (x_min_old, x_max_old, y_min_old, y_max_old) = unconvert(wR_old, hR_old, float(elems[1]), float(elems[2]), float(elems[3]), float(elems[4]))
                            # #print("Recognition: {0} {1} {2} {3}\n".format(x_min_old + dif_xR, x_max_old + dif_xR, y_min_old + dif_xR, y_max_old + dif_xR))
                            # # x_min_new = x_min_old + dif_xR
                            # # y_min_new = y_min_old + dif_yR
                            # # x_max_new = x_max_old + dif_xR
                            # # y_max_new = y_max_old + dif_yR
                            # #print("Anno: {0} {1} {2} {3}\n".format(x_min_new, y_min_new, x_max_new, y_max_new))
                            # (x, y, w, h) = convert(size, x_min_old + dif_xR, x_max_old + dif_xR, y_min_old + dif_xR, y_max_old + dif_xR)
                            # #print("*", end="", flush=True)
                            # #x_new = ((x_min_new + x_max_new) >> 1) / float(size)
                            # #y_new = ((y_min_new + y_max_new) >> 1) / float(size)
                            # #w_new = (x_max_new - x_min_new) / float(size)
                            # #h_new = (y_max_new - y_min_new) / float(size)
                            # updateAnnFile.write("{0} {1} {2} {3} {4}\n".format(int(elems[0]), x, y, w, h))
                            print(".", end="", flush=True)

                        except:
                            log.write(ann + '\n')
                            continue
                    inputAnnFile.close()
                    updateAnnFile.close()
                    break
    
    print('Updating YOLO annotation finished!')