import cv2
import numpy as np
import sys
from myIO import MyIO
from colorProcess import ColorProcess
from imageProcess import ImageProcess


class ColorManipulation:
    
# |----------------------------------------------------------------------------|
# linearStretchingInLUV
# |----------------------------------------------------------------------------|
    def myUI(self, w1, h1, w2, h2, name_input, name_output):
        '''
        given function performs the following tasks:
        1. read the image in BGR format
        2. convert w1, h1, w2, h2 window size in respective pixel format
        3. convert BGR image into Luv image
        4. find histogram of entire image on Luv domain,
           where L is in range of given window
        5. convert Luv image into BGR image
        6. write output image
        '''
        # 1. read the image in BGR format
        myIO = MyIO()
        bgrImg = myIO.readImage(name_input)
        
        # debug
        print("bgrImg =\n {}".format(bgrImg))
        # debug -ends
                
        # debug
        myIO.showImage(bgrImg, "BGR Image")
        # debug -ends

        # 2. convert w1, h1, w2, h2 window size in respective pixel format
        W1, H1, W2, H2 = myIO.windowsSizeMapping(inputImage = bgrImg,\
                                                 w1 = w1, h1=h1,\
                                                 w2 = w2, h2=h2)
        # debug
        print("W1 = {}, H1={}, W2={}, H2={}".format(W1, H1, W2, H2))
        # debug -ends


        # 3. convert BGR image into Luv image
        colorProcess=ColorProcess()
        LuvImg = colorProcess.bgrToLuv(bgrImg = bgrImg)
        # debug
        print("-----------------------------------------------------")
        print("\nLuvImg = \n{}".format(LuvImg))
        # debug -ends

        #4. find histogram of entire image on Luv domain,
        #   where L is in range of given window
        imageProcess = ImageProcess()
        HELuvImg = imageProcess.histogramEqualizationInLuv(LuvImg, W1, H1, W2, H2)
        
        # debug
        print("-----------------------------------------------------")
        print("HELuvImg = \n{}".format(HELuvImg))
        # debug -ends
        
        # 5. convert Luv image into BGR image
        HEBGRImage = colorProcess.LuvToBGR(LuvImage = HELuvImg)
        
        # debug
        myIO.showImage(HEBGRImage, "Histogram Equalized BGR Image")
        cv2.waitKey(0)
        # debug -ends

        # debug
        print("-----------------------------------------------------")
        print("HEBGRImage =\n {}".format(HEBGRImage))
        # debug -ends

        #6. write output image
        myIO.writeImage(outputImage = HEBGRImage, name_output = name_output)

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
    colorManipulation.myUI(w1, h1, w2, h2, name_input, name_output)