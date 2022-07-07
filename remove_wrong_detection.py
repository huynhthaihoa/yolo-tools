import argparse
import os 
from glob import glob

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Path to the input folder",
                    type=str, default="input")
    parser.add_argument("-r", "--reference", help="Path to the reference folder",
                    type=str, default="refence")
    parser.add_argument("-o", "--output", help="Path to the output folder", 
                    type=str, default="output")
    
    args = parser.parse_args()
    
    rfnames = glob(os.path.join(args.reference, '*.jpg'))
    rbnames = [os.path.basename(fname) for fname in rfnames]
    
    fnames = glob(os.path.join(args.input, '*.jpg'))
    for fname in fnames:
        bname = os.path.basename(fname)
        if bname not in rbnames:
            print(bname)
            os.remove(fname)
            #os.rename(fname, os.path.join(args.output, bname))
    print("Finish!")
    
    