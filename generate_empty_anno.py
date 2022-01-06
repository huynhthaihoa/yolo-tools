from glob import glob
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory of input folder",
                    type=str, default="img")
    parser.add_argument("-o", "--output", help="Directory contains output folder",
                    type=str, default="")

    args = parser.parse_args()
    input = args.input + '/'
    
    output = args.output 
    
    if output == "":
        output = input
    else:
        if os.path.isdir(output) is False:
            os.mkdir(output)
        output += '/'
    
    exts = ['*.jpg', '*.png', '*.jpeg', '*.jfif']
    imgs = []
    for ext in exts:
        imgs += glob(input + ext)
    
    for img in imgs:
        basename = os.path.basename(img)
        annname = output + basename[: basename.rfind('.')] + '.txt'
        if os.path.exists(annname) is False:
            file = open(annname, "w+")
            file.close()
        print(".", end="", flush=True)
    
    print('Generate empty annotation files finished!')