"""
Update YOLO annotation files according to update .names file, assuming that the new .names file includes a subset of class from 
the old .names file but with different order.
For example:

old .names file has:
person
face
fire
smoke

new .names file has:
face
person

Therefore, all bounding boxes with old id = 0 (person) will be changed into new id = 1 (person) 
corresponds to new .names file, old id = 1 -> new id = 0, whereas every bounding boxes with old id = 2 or old id = 3 will be 
suppressed

Created on February 17th 2022

@author: Thai-Hoa Huynh
"""
import os
from glob import glob
import numpy as np
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--ann", help="Directory of old annotation files",
                    type=str, default="ann")
    parser.add_argument("-u", "--update", help="Directory of new annotation files",
                    type=str, default="update")
    parser.add_argument("-o", "--old", help="Old .names file path",
                    type=str, default="old.names")
    parser.add_argument("-n", "--new", help="New .names file path",
                    type=str, default="new.names")
    
    args = parser.parse_args()
    #anns = args.ann
    updates = args.update
    if os.path.isdir(updates) is False:
        os.mkdir(updates)
    updates += '/'
    
    oldClassFile = open(args.old, "rt")
    oldClasses = list()
            
    with open(args.old, "rt") as f:
        for line in f:
            if line[-1] == '\n':
                oldClasses.append(line[:-1])
                
            #print(line[:-1] + ":" + str(len(line[:-1])))
            else:
                oldClasses.append(line)
    
    for line in oldClasses:
        print(line)
    
    updateIndices = dict()
    with open(args.new, "rt") as f: 
        newIdx = 0
        for line in f:
            if line[-1] == '\n':
                line = line[:-1]
            if line in oldClasses:
                oldIdx = oldClasses.index(line)
                print("{0} {1}\n".format(oldIdx, newIdx))
                updateIndices[oldIdx] = newIdx
                newIdx += 1
    
    oldAnns = glob(args.ann + "/*.txt")
    for oldAnn in oldAnns:
        data = np.loadtxt(oldAnn).reshape(-1, 5)
        n_bboxes = len(data)

        annName = os.path.basename(oldAnn)
        newAnn = updates + annName
        
        newAnnFile = open(newAnn, "wt")
        for i in range(n_bboxes):
            data_conv = data[i]
            oldIdx = int(data_conv[0])
            if oldIdx not in updateIndices:
                continue
            for j in range(5):
                if(j == 0):
                    newAnnFile.write(str(updateIndices[oldIdx]))
                else:
                    newAnnFile.write(str(data_conv[j]))
                if(j < 4):
                    newAnnFile.write(' ')
                else:
                    newAnnFile.write('\n')                
        newAnnFile.close()
        
        print(".", end="", flush=True)
            
    print('\nUpdating YOLO annotation finished!')


            
    