import os
from glob import glob
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", help="Directory of referencing folder",
                    type=str, default="img")
    parser.add_argument("-d", "--dst", help="Directory of referenced folder",
                    type=str, default="img")
    parser.add_argument("-l", "--log", help="Log file",
                    type=str, default="log.txt")                
    args = parser.parse_args()
    srcDir = args.src + '/'
    dstDir = args.dst + '/'
    imgs = glob(srcDir + "*.png") + glob(srcDir + "*.jpg")
    log = open(args.log, "wt")
    for img in imgs:
        name = os.path.basename(img)
        filename, _ = os.path.splitext(name)
        dstImg = dstDir + filename + '.jpg'
        if os.path.exists(dstImg) is False:
            print(name + "\n")
            log.write(name + "\n")
    log.close()
    print("Finish!")
            
    