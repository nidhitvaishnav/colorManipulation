import cv2
import numpy as np

class ColorProcess:

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
    def bgrTosRGB(self, bgrImage):
        '''
        given function converts BGRImage into RGBImage
        '''
        
        rows, cols, bands = bgrImage.shape # bands == 3
        
        sRGBImage =  np.zeros([rows, cols, bands], dtype=np.uint8)

        for i in range(0, rows):
            for j in range(0, cols):
                b,g,r = bgrImage[i,j]
                sRGBImage[i,j] = [r,g,b]
            #for j -ends
        #for i -ends
        
        return sRGBImage
    
# |--------------------------------bgrToRGB------------------------------------|

# |----------------------------------------------------------------------------|
# sRGBToLinearRGB
# |----------------------------------------------------------------------------|
    def sRGBToNonLinearRGB(self, sRGBImage):
        '''
        Given function converts sRGB Image into non Linear RGB image by
        R'=R/255; G'=G/255; B'=B/255
        '''
        rows, cols, bands = sRGBImage.shape # bands == 3
        
        nonlinearRGBImg =  np.zeros([rows, cols, bands], dtype=np.uint8)

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = sRGBImage[i,j]
                nonlinearRGBImg[i,j] = [float(r/255),float(g/255),float(b/255)]
            #for j -ends
        #for i -ends
        
        return nonlinearRGBImg
        
# |--------------------------------sRGBToLinearRGB---------------------------------|
    
# |----------------------------------------------------------------------------|
# nonLinearRGBToLinearRGB
# |----------------------------------------------------------------------------|
    def nonLinearRGBToLinearRGB(self, nonLinearRGBImg):
        '''
        converting nonLinear RGB into Linear RGB by applying inverse Gamma
        correction in following way:
        RGB = invgamma(R',G',B')
       
        '''
        rows, cols, bands = nonLinearRGBImg.shape # bands == 3
        
        linearRGBImg =  np.zeros([rows, cols, bands], dtype=np.uint8)

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = nonLinearRGBImg[i,j]
                linearRGBImg[i,j] = self.invGamma([r,g,b])
            #for j -ends
        #for i -ends
        
        return linearRGBImg 
        
# |--------------------------------nonLinearRGBToLinearRGB---------------------|

# |----------------------------------------------------------------------------|
# invGamma
# |----------------------------------------------------------------------------|
    def invGamma(self, rgbList):
        '''
        invgamma (D) = v/12.92;   if v<0.03928
                     = ((v+0.055)/1.055)^2.4;  otherwise
        '''
        invRGBList = []
        for v in rgbList:
            if v<0.03928:
                d=float(v)/12.92
            else:
                d=np.power(float(v+0.055)/1.055, 2.4)
            #if v -ends
            invRGBList.append(d)
        #for v -ends
        return invRGBList
                
# |--------------------------------invGamma------------------------------------|
    
# |----------------------------------------------------------------------------|
# linearRGBToXYZ
# |----------------------------------------------------------------------------|
    def linearRGBToXYZ(self, linearRGBImage):
        '''
        
        '''
        rows, cols, bands = linearRGBImage.shape # bands == 3
        
        xyzImage =  np.zeros([rows, cols, bands], dtype=np.uint8)
        multiplierMatrix = np.array([[0.412453, 0.35758, 0.180423],
                                     [0.212671, 0.71516, 0.072169],
                                     [0.019334, 0.119193, 0.950227]])

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = linearRGBImage[i,j]
                xyzImage[i,j] = np.matmul(multiplierMatrix, np.array([r,g,b]))
            #for j -ends
        #for i -ends
        
        return xyzImage 
        
# |--------------------------------linearRGBToXYZ---------------------------------|
    
    