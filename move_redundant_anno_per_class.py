import os
from glob import glob
import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory of input folder",
                    type=str, default="img")
    parser.add_argument("-c", "--class_file", help="Directory of class file",
                    type=str, default="obj.names")
    parser.add_argument("-o", "--output", help="Directory of output folder",
                    type=str, default="out")
    parser.add_argument("-n", "--number", help="Maximum number of bounding boxes per class in one image",
                    type=int, default=100)
    args = parser.parse_args()
    inpDir = args.input + '/'
    outDir = args.output + '/'
    
    if os.path.isdir(outDir) is False:
        os.mkdir(outDir)

    anns = glob(inpDir + '*.txt')
    
    count = dict()

    classFile = open(args.class_file, "rt")
    for line in classFile:
        if line[-1] != '\n':
            count[line[:-1]] = 0
    
    for ann in anns:
        basename = os.path.basename(ann)
        newann = outDir + basename
        name, _ = os.path.splitext(basename)
        img = inpDir + name + ".png"
        newimg = outDir + name + ".png"
        if os.path.exists(img) is True:
            
            for _class in count:
                count[_class] = 0

            data = np.loadtxt(ann).reshape(-1, 5)
            for line in data:
                count[line[0]] = count[line[0]] + 1

            for _class in count:
                if len(count[_class]) > args.number:
                    os.rename(ann, newann)
                    os.rename(img, newimg)
                    break     
     
            print(".", end="", flush=True)
            
    print("Completed!")
        