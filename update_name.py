import os
import argparse
from glob import glob

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory of original images",
                    type=str, default="input")
    args = parser.parse_args()
    input = args.input + '/'
    # prefix = args.prefix
    # exts = ['*.jpg', '*.png', '*.jpeg', '*.jfif']
    # imgs = []
    # for ext in exts:
        # imgs += glob(input + ext)
    
    imgs = glob(input + "*.png")
    for img in imgs:
        imgname = os.path.basename(img)
        imgname_update = imgname[imgname.find('_') + 1:]
        newimg = input + imgname_update
        annname = imgname[:imgname.rfind('.')]
        annname_update = annname[annname.find('_') + 1:]
        ann = input + annname + ".txt"
        newann = input + annname_update + ".txt"
        #newimg = input + "Cam" + prefix + '_' + basename
        #name = basename[:basename.rfind('.')]
        # ann = input + name + '.txt'
        # newann = input + ann[ann.find('_') + 1:] '.txt'
        # if os.path.exists(ann) is True:
            # newann = input + "Cam" + prefix + '_' + name + '.txt'
        os.rename(ann, newann)
        os.rename(img, newimg)
        print(".", end="", flush=True)
    print('Changing file names finished!')