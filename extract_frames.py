import cv2
import argparse
import os 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Path to the input video",
                    type=str, default="input.mp4")
    parser.add_argument("-o", "--output", help="Path to the output folder",
                    type=str, default="output")
    args = parser.parse_args()
    
    inputPath = args.input
    source = cv2.VideoCapture(inputPath)
    name = os.path.basename(inputPath).split('.')[0]
    out = args.output
    if os.path.isdir(out) is False:
        os.mkdir(out)
    out += '/'
    i = 0
    while cv2.waitKey(1) < 0:
        ret, frame = source.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        framename = out + name + '_' + str(i) + '.jpg'
        cv2.imwrite(framename, frame)
        print(".", end="", flush=True)
        i += 1
    print('Extract video finished!')