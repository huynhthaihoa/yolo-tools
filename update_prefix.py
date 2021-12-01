import os
import argparse
from glob import glob

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Directory of original images",
                    type=str, default="input")
    parser.add_argument("-o", "--output", help="Directory of output image",
                    type=str, default="")
    parser.add_argument("-d", "--date", help="Date prefix",
                    type=str, default="input")  
    parser.add_argument("-p", "--position", help="Position prefix",
                    type=str, default="input")                    
    args = parser.parse_args()
    input = args.input + '/'
    
    output = args.output
    if(args.output == ""):
        output = input
    else:
        output += '/'
    
    date_prefix = args.date
    pos_prefix = args.position
    
    imgs = glob(input + "*.png")
    for img in imgs:
        imgname = os.path.basename(img)
        basename = imgname[:imgname.find('.')]
        annname = basename + '.txt'
        ann = input + annname
        imgname_keep = imgname[imgname.rfind('-') + 1:]
        annname_keep = annname[annname.rfind('-') + 1:]
        img_new = output + date_prefix + '-' + pos_prefix + '-' + imgname_keep
        ann_new = output + date_prefix + '-' + pos_prefix + '-' + annname_keep
        os.rename(img, img_new)
        os.rename(ann, ann_new)
        print(".", end="", flush=True)
    print('Changing file names finished!')