
import os
from glob import glob
#import cv2
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains input folder",
                    type=str, default="input")
    parser.add_argument("-o", "--output", help="Directory contains output folder",
                    type=str, default="output")
                    
    args = parser.parse_args()
    input = args.input + '/'
    output = args.output 
    if os.path.isdir(output) is False:
        os.mkdir(output)
    output += '/'
    
    exts = ['*.jpg', '*.png', '*.jpeg', '*.jfif']
    imgs = []
    for ext in exts:
        imgs += glob(input + ext)
    for img in imgs:
        basename = os.path.basename(img)
        annname = basename[: basename.rfind('.')] + '.txt'
        inputanname = input + '/' + annname
        if os.path.exists(inputanname) is False or (os.path.exists(inputanname) is True and os.stat(inputanname).st_size == 0):         
            outputannname = output + annname
            outputimagename = output + basename
            os.rename(img, outputimagename)
            if os.path.exists(inputanname) is True:
                print('Found empty file:', inputanname)
                os.rename(inputanname, outputannname)
            else:
                print('Annotation file does not exist: ', inputanname)
    print('Move files finished!')