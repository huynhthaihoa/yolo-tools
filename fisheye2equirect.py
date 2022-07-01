import cv2
import argparse
from glob import glob
from math import pi, sin, cos
import numpy as np
import os

def findFisheye(Xe, Ye, R, Cfx, Cfy, He, We):
    """Find the corresponding fisheye output point corresponding to an input cartesian point
    
    Args:
        Xe: X-coordinate (column position) of the input cartesian point 
        Ye: Y-coordinate (row position) of the input cartesian point
        R: fisheye output radius
        Cfx: X-coordinate (column position) of the fisheye principal point
        Cfy: Y-coordinate (row position) of the fisheye principal point
        He: input cartesian image height (number of rows)
        We: input cartesian image width (number of columns)
        
    Returns:
        Xf: X-coordinate (column position) of the fisheye output point
        Yf: Y-coordinate (row position) of the fisheye output point
    """
    
    #Polar coordinates for the fisheye image
    r = Ye / He * R
    theta = Xe / We * 2.0 * pi
    
    #Cartesian coordinates for the fisheye image
    Xf = int(Cfx + r * sin(theta))
    Yf = int(Cfy + r * cos(theta))
    
    return (Xf, Yf)

def convert(imagePath):
    """Convert fisheye image into equirectangular image

    Args:
        imagePath: path to the fisheye image

    Returns:
        image: equirectangular image
    """    
    image = cv2.imread(imagePath)
    
    
    Hf, Wf = image.shape[:2] #get fisheye image size
    Cfy = Hf / 2.0 #Y-coordinate (row position) of the fisheye principal point
    Cfx = Wf / 2.0 #X-coordinate (column position) of the fisheye principal point
    R = Hf / 2.0 #fisheye output radius (not correct => need to re-calculate)
    print(Hf)
    print(Wf)
    
    #determine equirectangular image size
    He = int(R) #equirectangular image height (number of rows)
    We = int(2 * pi * R) #equirectangular image width (number of columns) (maybe not correct)
    
    equirectangularImage = np.zeros((He, We, 3), dtype=image.dtype)
    print(He)
    print(We)
    for Ye in range(He): #image height (number of rows) -> row position (Y-coordinate)
        for Xe in range(We): #image with (number of columns) -> column position (X-coordinate)
            (Xf, Yf) = findFisheye(Xe, Ye, R, Cfx, Cfy, He, We)
            equirectangularImage[Ye, Xe, :] = image[Yf, Xf, :]
    return equirectangularImage

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the input file/folder (JPG images)",
                    type=str, default="")
    parser.add_argument("-o", "--output", help="Path to the output file/folder (JPG images)",
                    type=str, default="")
    args = parser.parse_args()
    input = args.input
    output = args.output
    if os.path.isdir(input) is True:
        """input is folder"""
        if os.path.isdir(output) is False:
            os.mkdir(output)
        fnames = glob(input + '/*.jpg')
        for fname in fnames:
            print(fname)
            basename = os.path.basename(fname)
            image = convert(fname)
            cv2.imwrite(os.path.join(output, basename), image)
    else:
        image = convert(input)
        cv2.imwrite(output, image)
    print("Finished!")
    