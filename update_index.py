from glob import glob
import numpy as np

anns = glob("F:/KRISO/Yolo_mark/x64/Release/data/crop4alphabets/anchorX10Y4_2/*.txt")
for ann in anns:
    annfile = open(ann, "rt")
    data = annfile.readlines()
    #print(data)
    annfile.close()
    annfile = open(ann, "wt")
    for i in range(14):
        # if i == 11:
        #     annfile.write(data[12])
        # elif i == 12:
        #     annfile.write(data[11]) 
        # else:
        annfile.write(data[i]) 
        if i == 8:
            annfile.write(data[14])
        #line = data[i]
        # for j in range(5):
        #     if(j == 0):
        #         annfile.write(str(data[i][j]))
        #     if(j < 4):
        #         annfile.write(' ')
        #     else:
        #         annfile.write('\n') 
        # annfile.write(data[i])
        # #annfile.write('\n')
        # if i == 11:
        #     # for j in range(5):
        #     #     if(j == 0):
        #     #         annfile.write(str(data[14][j]))
        #     #     if(j < 4):
        #     #         annfile.write(' ')
        #     #     else:
        #     #         annfile.write('\n') 
        #     # for j in range(5):
        #     #     if(j == 0):
        #     #         annfile.write(str(data[13][j]))
        #     #     if(j < 4):
        #     #         annfile.write(' ')
        #     #     else:
        #     #         annfile.write('\n') 
        #     annfile.write(data[14])
        #     #annfile.write('\n')
        #     #annfile.write(data[13])
        #     #annfile.write('\n')
        # elif i == 6:
        #     annfile.write(data[14])
    annfile.close()
    print(".", end="", flush=True)
print('\nUpdating label indices finished!')
