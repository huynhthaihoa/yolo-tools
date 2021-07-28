"""
Generate label dataset using YOLO annotation files
Created on March 4th 2021

@author: Thai-Hoa Huynh
"""

import os
from glob import glob
#import cv2
#import numpy as np
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
    
def update(width, height, size, x, y, w, h):
    (xmin, xmax, ymin, ymax) =  unconvert(width, height, x, y, w, h)
    if size < xmax - xmin:
        size = xmax - xmin
    if size < ymax - ymin:
        size = ymax - ymin
    r_width = size + xmin - xmax
    r_height = size + ymin - ymax
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
    return (xmin, xmax, ymin, ymax)
    #else:  

# def update_yolo(width, height, size, x, y, w, h):
#     (xmin_old, xmax_old, ymin_old, ymax_old) =  unconvert(width, height, x, y, w, h)
#     W_old = xmax_old - xmin_old
#     H_old = ymax_old - ymin_old
#     (xmin_new, xmax_new, ymin_new, ymax_new) =  update(width, height, size, x, y, w, h)
#     W_new = xmax_new - xmin_new
#     H_new = ymax_new - ymin_new
#     dif_x = (xmin_old - xmin_new)
#     dif_y = (ymin_old - ymin_new)
#     x_new = ((x * W_old) + dif_x) / W_new
#     y_new = ((y * H_old) + dif_y) / H_new 
#     w_new = (w * W_old) / W_new 
#     h_new = (h * H_old) / H_new
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix", help="Camera prefix", type=str, default="")
    parser.add_argument("-i", "--img", help="Directory of input images",
                    type=str, default="img")
    parser.add_argument("-a", "--ann", help="Directory of original YOLO annotation files (.txt)",
                    type=str, default="")
    parser.add_argument("-s", "--size", help="Cropped image size",
                    type=int, default=608)
    parser.add_argument("-c", "--class_file", help="Class name file (.txt)",
                    type=str, default="obj.names")
    parser.add_argument("-l", "--output", help="Output directory to contain dataset",
                    type=str, default="Labels/")
                 
    args = parser.parse_args()
    size = args.size
    imgDir = args.img
    prefix = args.prefix
    if args.ann == "":
        annDir = args.img + '/'
    else:
        annDir = args.ann + '/'
    out = args.output
    if os.path.isdir(out) is False:
        os.mkdir(out)
    out += '/'
    classFile = open(args.class_file, "rt")
    classes = []
    for line in classFile:
        if line[-1] == '\n':
            classes.append(line[:-1])
        else:
            classes.append(line)
    exts = ['/*.jpg', '/*.png', '/*.jpeg', '/*.jfif']
    imgs = []
    for ext in exts:
        imgs += glob(imgDir + ext)
    ids = [os.path.basename(x) for x in imgs]
    log = open("log_generate.txt", "wt")
    for i, imgpath in enumerate(imgs):
        basename = ids[i][: ids[i].rfind('.')]
        #print(imgpath)
        annpath = annDir + basename + '.txt'
        #annpath = annDir + ids[i][: ids[i].rfind('.')] + '.txt'
        #annpath = annDir + ids[i].split('.')[0] + '.txt'
        #print(annpath)
        if os.path.isfile(annpath) is True:
            
            #img = cv2.imread(imgpath)
            img = Image.open(imgpath)
            #height, width, _ = img.shape
            width, height = img.size
            inFile = open(annpath, "rt")
            for j, line in enumerate(inFile):
                elems = line.split(' ')
                try:
                    className = classes[int(elems[0])]
                except:
                    className = 'outlier'
                classDir = out + className
                if os.path.isdir(classDir) is False:
                    os.mkdir(classDir)
                classDir += '/'
                try:
                    (xmin, xmax, ymin, ymax) = update(width, height, size, float(elems[1]), float(elems[2]), float(elems[3]), float(elems[4]))                  
                except:
                    log.write(annpath + '\n')
                    continue
                #cropImg = img[ymin : ymax, xmin : xmax]
                cropArea = (xmin, ymin, xmax, ymax)#(left, upper, right, lower)
                try:
                    print(".", end="", flush=True)
                    cropImg = img.crop(cropArea)
                    #print(ids[i])
                    if prefix != "":
                        cropImg.save(classDir + prefix + '_' + basename + '_' + str(j) + '.png')
                    else:
                    #    prefix += '_'
                        cropImg.save(classDir + basename + '_' + str(j) + '.png')
                    #cv2.imwrite(classDir + ids[i].split('.')[0] + '_' + str(j) + '.jpg', cropImg)
                except:
                    log.write(imgpath + '\n')
                    pass
            inFile.close()
    log.close()
    print('Generating dataset from YOLO annotation finished!')