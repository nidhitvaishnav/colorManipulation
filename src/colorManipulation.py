import cv2
import numpy as np
import sys
from myIO import MyIO
from colorProcess import ColorProcess


class ColorManipulation:
    
# |----------------------------------------------------------------------------|
# linearStretchingInLUV
# |----------------------------------------------------------------------------|
    def linearStretchingInLUV(self, w1, h1, w2, h2, name_input, name_output):
        '''
        
        '''
        myIO = MyIO()
        bgrImg = myIO.readImage(name_input)
        
        # debug
        print("bgrImg =\n {}".format(bgrImg))
        # debug -ends

        
#         # debug
#         myIO.showImage(bgrImg, "BGR Image")
#         # debug -ends

        colorProcess=ColorProcess()
        LuvImg = colorProcess.bgrToLuv(bgrImg = bgrImg)
        # debug
        print("\nLuvImg = \n{}".format(LuvImg))
        # debug -ends



        

        
# |--------------------------------linearStretchingInLUV---------------------------------|
    






if __name__ == '__main__':
    if(len(sys.argv) != 7) :
        print(sys.argv[0], ": takes 6 arguments. Not ", len(sys.argv)-1)
        print("Expecting arguments: w1 h1 w2 h2 ImageIn ImageOut.")
        print("Example:", sys.argv[0], " 0.2 0.1 0.8 0.5 fruits.jpg out.png")
        sys.exit()

    w1 = float(sys.argv[1])
    h1 = float(sys.argv[2])
    w2 = float(sys.argv[3])
    h2 = float(sys.argv[4])
    name_input = sys.argv[5]
    name_output = sys.argv[6]
    
    if(w1<0 or h1<0 or w2<=w1 or h2<=h1 or w2>1 or h2>1) :
        print(" arguments must satisfy 0 <= w1 < w2 <= 1, 0 <= h1 < h2 <= 1")
        sys.exit()

    # debug
    print("w1 = {}, h1={}, w2={}, h2={}".format(w1, w2, h1, h2))
    # debug -ends

    colorManipulation = ColorManipulation()
    colorManipulation.linearStretchingInLUV(w1, h1, w2, h2, name_input, name_output)