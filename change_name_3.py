import os
import argparse
from glob import glob

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory of original images",
                    type=str, default="input")
    parser.add_argument("-o", "--output", help="Directory of updated images",
                    type=str, default="output")
    
    args = parser.parse_args()
    input = args.input + '/'
    output = args.output
    if os.path.isdir(output) is False:
        os.mkdir(output)
    output += '/'
    
    anns = glob(input + "*.txt")
    for ann in anns:
        basename = os.path.basename(ann)
        basename_keep = basename[:basename.rfind('-') + 1]
        #ext = basename[basename.rfind('.'):]
        suffix = basename[basename.rfind('-') + 1: basename.rfind('.')]
        suffix_new = int(suffix) + 1
        #basename_new = basename_keep + str(suffix_new) + ".txt"
        #img_new = output + basename_new
        #os.rename(img, img_new)
        #name = basename[:basename.rfind('.')]
        #ann = input + name + '.txt'
        #if os.path.exists(ann) is True:
        ann_new = output + basename_keep + str(suffix_new) + ".txt"
        os.rename(ann, ann_new)
            # newann = input + "Cam" + prefix + '_' + name + '.txt'
            # os.rename(ann, newann)
        # os.rename(img, newimg)
        print(".", end="", flush=True)
    print('Changing file names finished!')