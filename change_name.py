import os
import argparse
from glob import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains folder",
                    type=str, default="input")
    parser.add_argument("-p", "--prefix", help="Prefix",
                    type=str, default="")
    
    args = parser.parse_args()
    input = args.input + '/'
    prefix = args.prefix
    exts = ['*.jpg', '*.png', '*.jpeg', '*.jfif']
    imgs = []
    for ext in exts:
        imgs += glob(input + ext)
    
    for img in imgs:
        basename = os.path.basename(img)
        newimg = input + "Cam" + prefix + '_' + basename
        name = basename[:basename.rfind('.')]
        ann = input + name + '.txt'
        if os.path.exists(ann) is True:
            newann = input + "Cam" + prefix + '_' + name + '.txt'
            os.rename(ann, newann)
        os.rename(img, newimg)
        print(".", end="", flush=True)
    print('Changing file names finished!')