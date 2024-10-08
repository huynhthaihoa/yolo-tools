
import os
from glob import glob
from distutils.util import strtobool
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory contains input folder",
                    type=str, default="input")
    parser.add_argument("-o", "--output", help="Directory contains output folder",
                    type=str, default="output")
    parser.add_argument("-r", "--remove", help="Remove empty annotation file ? (default is true)",
                    type=lambda x: bool(strtobool(x)), default="True")
                    
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
        if os.path.exists(inputanname) is False or os.stat(inputanname).st_size == 0:         
            outputimagename = output + basename
            os.rename(img, outputimagename)
            if os.path.exists(inputanname) is True:
                print('Found empty file:', inputanname)
                if args.remove == True:
                    os.remove(inputanname)
                else:
                    outputannname = output + annname
                    os.rename(inputanname, outputannname)
            else:
                print('Annotation file does not exist: ', inputanname)
        else:
            print(".", end="", flush=True)
    print('Move files finished!')