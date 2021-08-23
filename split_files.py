import os
from glob import glob
from shutil import copyfile
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Input folder",
                    type=str, default="input")
    parser.add_argument("-o", "--output", help="Output folder",
                    type=str, default="output")
    parser.add_argument("-n", "--number", help="Number of subfolder",
                    type=int, default=4)
    args = parser.parse_args()
    input = args.input + '/'
    #output = args.output + '/'
    imgs = glob(input + "*.png") + glob(input + "*.jpg")
    output = args.output
    if os.path.isdir(output) is False:
        os.mkdir(output)
    n = args.number
    sample_sizes = len(imgs) // n 
    seed = 0
    i = 0
    for img in imgs:
        dst = output + '/' + str(seed)
        if os.path.isdir(dst) is False:
            os.mkdir(dst)        
        dst += '/'
        basename = os.path.basename(img)
        dstname = dst + basename
        os.rename(img, dstname)
        print(".", end="", flush=True)
        i += 1
        if i == sample_sizes:
            i = 0
            seed += 1
    print('Divide finished!')
    