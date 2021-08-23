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
    return (int(xmin), int(xmax), int(ymin), int(ymax), int(size))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--old", help="Directory of old cropped images & annotation files",
                    type=str, default="ann")
    parser.add_argument("-n", "--new", help="Directory of updated cropped images & annotation files",
                    type=str, default="ann_2")
    parser.add_argument("-s", "--size", help="Cropped image size",
                    type=int, default=608)
    #parser.add_argument("-h", "--is_horizontal", help="Is horizontal layout", type=bool, default=True)
    #parser.add_argument("-a", "--anchor", help="Index of anchor box", type=int, default=3)

    args = parser.parse_args()
    size = args.size
    oldDir = args.old + '/'
    newDir = args.new 
    anns = glob(oldDir + '*.txt')
    if os.path.isdir(newDir) is False:
        os.mkdir(newDir)
    newDir += '/'
    for ann in anns:
        oldAnnFile = open(ann, "rt")        
        basename = os.path.basename(ann)
        basename = basename[: basename.rfind('.')]
        if basename == 'classes':
            continue
        imgname = oldDir + basename + ".png"
        targetName = newDir + basename
        updateAnnFile = open(targetName + ".txt", "wt")
        updateImgName = targetName + ".png"
        if os.path.isfile(imgname) is True:
            img = Image.open(imgname)
            width, height = img.size
            annData = np.loadtxt(ann).reshape(-1, 5)
            nObjects = len(annData)
            xMax = 0
            yMax = 0
            for i in range(nObjects):
                data = annData[i]
                _, xmax, _, ymax = unconvert(width, height, float(data[1]), float(data[2]), float(data[3]), float(data[4]))
                if xmax > xMax:
                    xMax = xmax
                if ymax > yMax:
                    yMax = ymax
            print(xMax, yMax)

            offsetX_anno = size - xMax - 5
            offsetY_anno = size - yMax - 5
            #offsetX = width - xMax + 5
            
            for i in range(nObjects):
                data = annData[i]
                for j in range(5):
                    if j == 0:
                            #data_new.append(int(data_conv[j]))
                        updateAnnFile.write(str(int(data[j])) + " ")
                    elif j == 1:
                        x_new = (width * data[j] + offsetX_anno) / size
                        # if x_new >= 1:
                        #     break
                        # data_new.append(x_new)
                        updateAnnFile.write(str(x_new) + " ")
                    elif j == 2:
                        y_new = (height * data[j] + offsetY_anno) / size
                        updateAnnFile.write(str(y_new) + " ")
                    elif j == 3:
                        w_new = (width * data[j]) / size
                        updateAnnFile.write(str(w_new) + " ")
                    else:
                        h_new = (height * data[j]) / size
                        updateAnnFile.write(str(h_new) + "\n")
            xMax_R = xMax + 5
            xMin_R = xMax_R - size
            yMax_R = yMax + 5
            yMin_R = yMax_R - size
            cropArea = (xMin_R, yMin_R, xMax_R, yMax_R)
            cropImg = img.crop(cropArea)
            cropImg.save(updateImgName)
            #print(".", end="", flush=True)
    print('Relocating cropped region finished!')
