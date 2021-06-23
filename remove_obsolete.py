import os
from glob import glob
import cv2
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--upd", help="Directory to be updated",
                    type=str, default="")
    parser.add_argument("-r", "--ref", help="Reference directory",
                    type=str, default="")
    args = parser.parse_args()
    
    updDir = args.upd + '/'
    refDir = args.ref + '//'
    anns = glob(updDir + '*.txt')
    for ann in anns:
        basename = os.path.basename(ann)
        basename_without_ext = basename[: basename.rfind('.')]
        imgname_base = basename_without_ext + '.jpg'
        imgname = updDir + imgname_base
        annname_ref = refDir + basename
        if os.path.exists(annname_ref) is True and os.path.exists(imgname) is True:
            print('Already exist!:{0}', imgname)
            os.remove(imgname)
        #else:
        #    print('Not exist!:{0}', imgname)
    print('finished!')