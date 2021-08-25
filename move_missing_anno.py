import os
from glob import glob
import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory of input folder",
                    type=str, default="img")
    parser.add_argument("-o", "--output", help="Directory of output folder",
                    type=str, default="out")
    
    args = parser.parse_args()
    inpDir = args.input + '/'
    outDir = args.output + '/'
    
    if os.path.isdir(outDir) is False:
        os.mkdir(outDir)

    anns = glob(inpDir + '*.txt')
    
    for ann in anns:
        basename = os.path.basename(ann)
        newann = outDir + basename
        name, _ = os.path.splitext(basename)
        img = inpDir + name + ".png"
        newimg = outDir + name + ".png"
        if os.path.exists(img) is True:
            count = len(np.loadtxt(ann).reshape(-1, 5))
            if count < 8:
                os.rename(ann, newann)
                os.rename(img, newimg)
            print(".", end="", flush=True)
            
    print("Completed!")
        