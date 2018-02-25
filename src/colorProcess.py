import cv2
import numpy as np

class colorProcess:

# |----------------------------------------------------------------------------|
# bgrToGray
# |----------------------------------------------------------------------------|
    def bgrToGray(self, inputImage, name_output, H1, H2, W1, W2):
        '''
        
        '''
        # The transformation should be based on the
        # historgram of the pixels in the W1,W2,H1,H2 range.
        # The following code goes over these pixels
        rows, cols, bands = inputImage.shape # bands == 3
        
        tmp = np.copy(inputImage)
        
        for i in range(H1, H2) :
            for j in range(W1, W2) :
                b, g, r = inputImage[i, j]
                gray = round(0.3*r + 0.6*g + 0.1*b + 0.5)
                tmp[i, j] = [gray, gray, gray]
        
        cv2.imshow('tmp', tmp)
        
        # end of example of going over window
        
        outputImage = np.zeros([rows, cols, bands], dtype=np.uint8)
        
        for i in range(0, rows) :
            for j in range(0, cols) :
                b, g, r = inputImage[i, j]
                outputImage[i,j] = [b, g, r]
        

        return outputImage
        
# |--------------------------------bgrToGray---------------------------------|


# |----------------------------------------------------------------------------|
# bgrToRGB
# |----------------------------------------------------------------------------|
    def bgrToRGB(self, bgrImage):
        '''
        given function converts BGRImage into RGBImage
        '''
        
        rows, cols, bands = bgrImage.shape # bands == 3
        
        rgbImage =  np.zeros([rows, cols, bands], dtype=np.uint8)

        for i in range(0, rows):
            for j in range(0, cols):
                b,g,r = bgrImage[i,j]
                rgbImage[i,j] = [r,g,b]
            #for j -ends
        #for i -ends
        
        return rgbImage
    
# |--------------------------------bgrToRGB------------------------------------|


    