import os
from glob import glob
import argparse
import numpy as np
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

def unconvert_simple(imgSize, bbSize, bbRatio):
    return int((bbRatio*imgSize) - (bbSize * imgSize) / 2.0)


def update_ROI(width, height, size, xmin, xmax, ymin, ymax):
    '''
    Convert from original detection size to standard size:
    @width [in]: width of the original image
    @height [in]: height of the original image
    @size [in]: standard size
    @xmin [in]: left border of the original detected region
    @xmax [in]: right border of the original detected region
    @ymin [in]: top border of the original detected region
    @ymax [in]: bottom border of the original detected region 
    return in order: xmin_new, xmax_new, ymin_new, ymax_new, size_new
    '''
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
    log.write("Original: {0} {1} - {2} {3}. Size: {4}\n".format(xmin, xmax, ymin, ymax, size))
    return (int(xmin), int(xmax), int(ymin), int(ymax), int(size))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--img", help="Directory of original images",
                    type=str, default="img")
    parser.add_argument("-o", "--old", help="Directory of old cropped images & annotation files",
                    type=str, default="ann")
    parser.add_argument("-n", "--new", help="Directory of updated cropped images & annotation files",
                    type=str, default="ann_2")
    parser.add_argument("-s", "--size", help="Cropped image size",
                    type=int, default=608)
    #parser.add_argument("-a", "--anchor", help="Index of anchor box", type=int, default=3)
    parser.add_argument("-x", "--anchorX", help="Index of anchor box X", type=int, default=-1)
    parser.add_argument("-y",  "--anchorY", help="Index of anchor box Y", type=int, default=-1)
    log = open("log_relocate.txt", "wt")
    args = parser.parse_args()
    size = args.size
    imgDir = args.img + '/'
    oldDir = args.old + '/'
    newDir = args.new 
    idX = args.anchorX
    idY = args.anchorY
    if os.path.isdir(newDir) is False:
        os.mkdir(newDir)
    newDir += '/'
    anns = glob(oldDir + '*.txt')
    data = dict()
    for ann in anns:
        oldAnnFile = open(ann, "rt")
        
        basename = os.path.basename(ann)
        basename = basename[: basename.rfind('.')]
        #print(basename)
        log.write(ann + "\n")
        if basename == 'classes':
            continue

        targetName = newDir + basename
        
        '''
        The new annotation file & cropped image for recognition
        '''
        updateAnnFile = open(targetName + ".txt", "wt")
        updateImgName = targetName + ".png"
        try:
            idx = int(basename[basename.rfind('_') + 1: ])
            basename = basename[: basename.rfind('_')]
        except:
            pass  
        detAnnName = imgDir + basename + ".txt"
        if os.path.isfile(detAnnName) is True and os.stat(detAnnName).st_size > 0:
            if detAnnName not in data:
                data[detAnnName] = np.loadtxt(detAnnName).reshape(-1, 5)
            imgname = imgDir + basename + '.png'
            if os.path.isfile(imgname) is True:
                log.write(imgname + "\n")
                img = Image.open(imgname)
                W, H = img.size
                (xR_min_origin, xR_max_origin, yR_min_origin, yR_max_origin) = unconvert(W, H, float(data[detAnnName][idx][1]), float(data[detAnnName][idx][2]), float(data[detAnnName][idx][3]), float(data[detAnnName][idx][4]))
                log.write("Range origin: {0} {1} - {2} {3}\n".format(xR_min_origin, xR_max_origin, yR_min_origin, yR_max_origin))
                (xR_min_old, xR_max_old, yR_min_old, yR_max_old, size_old) = update_ROI(W, H, size, xR_min_origin, xR_max_origin, yR_min_origin, yR_max_origin)
                annData = np.loadtxt(ann).reshape(-1, 5)#oldAnnFile.readlines()
                if idY != -1:
                    anchorY = annData[idY]
                if idX != -1:
                    anchorX = annData[idX]#[11]#annData[11]
                difX = 0
                offsetX_anno = 0
                if idX != -1:
                    difX = 1 - (anchorX[1] - (anchorX[3] / 2.0))
                    offsetX_anno = size - int(size_old * (anchorX[1] - (anchorX[3] / 2.0)))
                difY = 0 
                offsetY_anno = 0
                if idY != -1:
                    difY = 1 - (anchorY[2] - (anchorY[4] / 2.0))
                    offsetY_anno = size - int(size_old * (anchorY[2] - (anchorY[4] / 2.0)))

                log.write("anchorX: {0} {1} {2}\n".format(anchorX[1], anchorX[3], difX))
                log.write("anchorY: {0} {1} {2}\n".format(anchorY[2], anchorY[4], difY))       
                offsetX = int(size_old * difX)# - 1
                offsetY = int(size_old * difY)# + 1
                log.write("offsetX: {0}\n".format(offsetX))
                log.write("offsetY: {0}\n".format(offsetY))
                for i in range(4):
                    data_conv = annData[i]
                    for j in range(5):
                        if j == 0:
                            updateAnnFile.write(str(int(data_conv[j])))
                        elif j == 1:
                            x_new = (size_old * data_conv[j] + offsetX_anno) / size
                            updateAnnFile.write(str(x_new))
                        elif j == 2:
                            y_new = (size_old * data_conv[j] + offsetY_anno) / size
                            updateAnnFile.write(str(y_new))
                        else:
                            w_new = (data_conv[j] * size_old) / size
                            updateAnnFile.write(str(w_new))
                        if j < 4:
                            updateAnnFile.write(' ')
                        else:
                            updateAnnFile.write('\n')   

                xR_max_new = xR_max_old - offsetX
                xR_min_new = xR_max_new - size
                yR_max_new = yR_max_old - offsetY
                yR_min_new = yR_max_new - size
                cropArea = (xR_min_new, yR_min_new, xR_max_new, yR_max_new)
                cropImg = img.crop(cropArea)
                cropImg.save(updateImgName)
                print(".", end="", flush=True)
                log.write("Range old: {0} {1} - {2} {3}\n".format(xR_min_old, xR_max_old, yR_min_old, yR_max_old))
                log.write("Range new: {0} {1} - {2} {3}\n".format(xR_min_new, xR_max_new, yR_min_new, yR_max_new))
    print('Relocating cropped region finished!')
    log.close()