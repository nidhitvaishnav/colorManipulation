import cv2
import numpy as np
from numpy import dtype

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
# bgrToLuv
# |----------------------------------------------------------------------------|
    def bgrToLuv(self, bgrImg):
        '''
        converting BGR image into Luv format
        1. convert BGR to sRGB
        2. convert sRGB to non linear RGB
        3. convert non linear RGB to linear RGB
        4. convert linear RGB to XYZ
        5. convert XYZ to Luv
        '''
        sRGBImg = self.bgrTosRGB(bgrImage=bgrImg)
        
#         # debug
#         print("----------------------------------------------------")
#         print("sRGBImg = \n{}".format(sRGBImg))
#         # debug -ends
  
        nonLinearRGBImg = self.sRGBToNonLinearRGB(sRGBImage=sRGBImg)
        
#         # debug
#         print("----------------------------------------------------")
#         print("nonLinearRGBImg =\n {}".format(nonLinearRGBImg))
#         # debug -ends

                
        linearRGBImg = self.nonLinearRGBToLinearRGB(nonLinearRGBImg = \
                                                            nonLinearRGBImg)
        
#         # debug
#         print("----------------------------------------------------")
#         print("linearRGBImg =\n {}".format(linearRGBImg))
#         # debug -ends

        
#         # debug
#         myIO.showImage(linearRGBImg, "linearRGBImg")
#         cv2.waitKey(0)
#         # debug -ends
        
        XYZImg = self.linearRGBToXYZ(linearRGBImage = linearRGBImg)
        
#         # debug
#         print("----------------------------------------------------")
#         print("xyzImg =\n {}".format(XYZImg))
#         # debug -ends
        
        LuvImg, tlTable, du1v1table = self.XYZToLuv(XYZImg = XYZImg)
        
#         # debug
#         print("----------------------------------------------------")
#         print("tlTable = \n {}".format(tlTable))
#         print("du1v1 table = \n {}".format(du1v1table))
#         print("\n----------------------------------------------------")
#         print("LuvImg =\n {}".format(LuvImg))
#         # debug -ends
        return LuvImg
# |--------------------------------bgrToLuv---------------------------------|
    
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
        
        nonlinearRGBImg =  np.zeros([rows, cols, bands], dtype=float)

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = sRGBImage[i,j]
                nonlinearRGBImg[i,j] = [float(r)/255,float(g)/255,float(b)/255]
            #for j -ends
        #for i -ends
        
        return nonlinearRGBImg
        
# |--------------------------------sRGBToLinearRGB------------------------------|
    
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
        
        linearRGBImg =  np.zeros([rows, cols, bands], dtype=float)

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
        to find XYZ, we multiply linearRGB array with static array
        [[0.412453, 0.35758, 0.180423],
         [0.212671, 0.71516, 0.072169],
         [0.019334, 0.119193, 0.950227]]
        
        '''
        rows, cols, bands = linearRGBImage.shape # bands == 3
        
        XYZImage =  np.zeros([rows, cols, bands], dtype=float)
        multiplierMatrix = np.array([[0.412453, 0.35758, 0.180423],
                                     [0.212671, 0.71516, 0.072169],
                                     [0.019334, 0.119193, 0.950227]])

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = linearRGBImage[i,j]
                XYZImage[i,j] = np.matmul(multiplierMatrix, np.array([r,g,b]))
            #for j -ends
        #for i -ends
        
        return XYZImage 
        
# |--------------------------------linearRGBToXYZ------------------------------|
    
# |----------------------------------------------------------------------------|
# XYZToLuv
# |----------------------------------------------------------------------------|
    def XYZToLuv(self, XYZImg):
        '''
        To convert XYZ into Luv, we have
        Xw, Yw, Zw = 0.95, 1.0, 1.09
        
        uw = (4*Xw)/(Xw+15*Yw+3*Zw)
        vw = (9*Yw)/(Xw+15*Yw+3*Zw)
        
        Than we find values of t and L for each pixel,
        we find values of d, u'(u1) and v'(v1) for each pixel
        At the end we find u and v and store value of L in the Luv image 
        
        '''
        Xw, Yw, Zw = 0.95, 1.0, 1.09
        uw = (4*Xw)/(Xw+15*Yw+3*Zw)
        vw = (9*Yw)/(Xw+15*Yw+3*Zw)
        
#         # debug
#         print("uw = {}, vw = {}".format(uw, vw))
#         # debug -ends

        rows, cols, bands = XYZImg.shape # bands == 3

        tlTable = np.zeros([rows, cols, 2], dtype=float)
        du1v1table = np.zeros([rows, cols, bands], dtype=float)
        LuvImg = np.zeros([rows, cols, bands], dtype=float)
        
        for i in range(0,rows):
            for j in range(0, cols):
                x,y,z = XYZImg[i,j]
                t, l = self.findTL(y=y, yw=Yw)
                d, u1, v1 = self.finddu1v1(X=x, Y=y, Z=z) 
                # debug
                tlTable[i,j] = [t,l]
                du1v1table[i,j] = [d, u1, v1]
                # debug -ends
                LuvImg[i,j]= self.findLuv(l, u1, v1, uw, vw)
            #for j -ends
        #for i -ends
        return LuvImg, tlTable, du1v1table
# |--------------------------------XYZToLuv---------------------------------|

# |----------------------------------------------------------------------------|
# findTL
# |----------------------------------------------------------------------------|
    def findTL(self, y, yw):
        '''
        t=Y/Yw
        L = 116*(t)^(1/3)-16;    t>0.008856
          = 903.3t          ;    otherwise
        '''
        t=float(y)/float(yw)
        if t>0.008856:
            l=116*np.power(t,1/3)-16
        else:
            l=903.3*t
        #if -ends
        return t, l
# |--------------------------------findTL---------------------------------|
# |----------------------------------------------------------------------------|
# finddu1v1
# |----------------------------------------------------------------------------|
    def finddu1v1(self, X,Y,Z):
        '''
        d=X+15Y+3Z
        u'=4X/d;    v'=4Y/d
        '''
        d=X+15*Y+3*Z
        if d ==0:
            u1=0
            v1=0
        else:
            u1 = 4*X/d
            v1 = 9*Y/d    
        #if d -ends   
        return d,u1,v1
# |--------------------------------finddu1v1---------------------------------|
# |----------------------------------------------------------------------------|
# findLuv
# |----------------------------------------------------------------------------|
    def findLuv(self, l, u1, v1, uw, vw):
        '''
        
        '''
        u = 13*l*(u1-uw)
        v = 13*l*(v1-vw)
        return [l,u,v]
        
# |--------------------------------findLuv---------------------------------|
# |----------------------------------------------------------------------------|
# LuvToBGR
# |----------------------------------------------------------------------------|
    def LuvToBGR(self, LuvImage):
        '''
        Converting Luv format to BGR format
        1. Convert LuvImage into XYZ Image
        2. Convert XYZImage into linearsRGBImage
        3. Convert linearsRGBImage into nonLinearsRGB image
        4. convert sRGB image into RGB image
        5. convert RGB image to BGR image
        '''
        XYZImage = self.LuvToXYZ(LuvImage)
#         # debug
#         print("----------------------------------------------------")
#         print("XYZImage = {}".format(XYZImage))
#         # debug -ends
        
        linearsRGBImage = self.XYZToLinearRGB(XYZImage)
#         # debug
#         print("----------------------------------------------------")
#         print("linearsRGBImage =\n {}".format(linearsRGBImage))
#         # debug -ends

        nonLinearsRGBImage = self.linearsRGBToNonLinearRGB(linearRGBImage = linearsRGBImage)
#         # debug
#         print("----------------------------------------------------")
#         print("nonLinearsRGBImage =\n {}".format(nonLinearsRGBImage))
#         # debug -ends
        
        rgbImage = self.sRGBImageToRGBImage(sRGBImage=nonLinearsRGBImage)
#         # debug
#         print("----------------------------------------------------")
#         print("rgbImage =\n {}".format(rgbImage))
#         # debug -ends

        bgrImage = self.RGBToBGR(rgbImage)
#         # debug
#         print("----------------------------------------------------")
#         print("bgrImage =\n {}".format(bgrImage))
#         # debug -ends
        
        return bgrImage
        
# |--------------------------------LuvToBGR---------------------------------|
    
# |----------------------------------------------------------------------------|
# LuvToXYZ
# |----------------------------------------------------------------------------|
    def LuvToXYZ(self, LuvImage):
        '''
        To convert XYZ into Luv, we have
        Xw, Yw, Zw = 0.95, 1.0, 1.09
        
        uw = (4*Xw)/(Xw+15*Yw+3*Zw)
        vw = (9*Yw)/(Xw+15*Yw+3*Zw)
        
        1. find u1, v1 using l,u,v,uw,vw
        2. using L and Yw, find Y
        3. using u1, v1 and Y, find XYZ
        '''
        Xw, Yw, Zw = 0.95, 1.0, 1.09
        uw = (4*Xw)/(Xw+15*Yw+3*Zw)
        vw = (9*Yw)/(Xw+15*Yw+3*Zw)
        
#         # debug
#         print("uw = {}, vw = {}".format(uw, vw))
#         # debug -ends

        rows, cols, bands = LuvImage.shape # bands == 3
        XYZImg = np.zeros([rows, cols, bands], dtype=float)
        u1v1Table = np.zeros([rows, cols, 2], dtype=float)
        
        for i in range(0,rows):
            for j in range(0, cols):
                l,u,v = LuvImage[i,j]
                u1, v1 = self.findu1v1LuvToXYZ(l,u,v, uw, vw)
                
                # debug
                u1v1Table[i,j] = [u1,v1]
                # debug -ends
                
                Y = self.findY(l, Yw)
                XYZImg[i,j]= self.findXYZ(u1, v1, Y)
            #for j -ends
        #for i -ends
#         # debug
#         print("u1v1Table = {}".format(u1v1Table))
#         # debug -ends

        return XYZImg
        
# |--------------------------------LuvToXYZ---------------------------------|
# |----------------------------------------------------------------------------|
# findu1v1LuvToXYZ
# |----------------------------------------------------------------------------|
    def findu1v1LuvToXYZ(self, L, u, v, uw, vw):
        '''
        u1 = (u+13*uw*L)/13*L
        v1 = (v+13*vw*L)/13*L
        '''
        if L==0:
            u1=0
            v1=0
        else:
            u1 = (u+13*uw*L)/(13*L)
            v1 = (v+13*vw*L)/(13*L)
        #if L -ends
        return u1, v1
        
# |--------------------------------findu1v1LuvToXYZ---------------------------------|
# |----------------------------------------------------------------------------|
# findY
# |----------------------------------------------------------------------------|
    def findY(self, L, Yw):
        '''
        Y = Yw*((L+16)/116)^3;         if L>7.9996
          = L*Yw/903.3;                otherwise
        '''
        if L>7.9996:
            Y = np.power(((L+16)/116), 3)*Yw
        else:
            Y = L*Yw/903.3
        #if L -ends
        return Y
        
# |--------------------------------findY---------------------------------------|
# |----------------------------------------------------------------------------|
# findXYZ
# |----------------------------------------------------------------------------|
    def findXYZ(self, u1, v1, Y):
        '''
        X = Y*2.25u1/v1
        Z = Y*(3-0.75u1-5v1)/v1
        '''
        if v1 == 0:
            X=0
            Z=0
        else:
            X = Y*2.25*u1/v1
            Z = Y*(3-0.75*u1-5*v1)/v1
        #if v1 -ends
        return [X, Y, Z]
# |--------------------------------findXYZ-------------------------------------|

# |----------------------------------------------------------------------------|
# XYZToLinearRGB
# |----------------------------------------------------------------------------|
    def XYZToLinearRGB(self, XYZImage):
        '''
        to find linearsRGBImage, we multiply XYZImage with static array
        [[3.240479, -1.53715, -0.498535],
         [-0.969256, 1.875991, 0.041556],
         [0.055648, -0.204043, 1.057311]]
        
        '''
        rows, cols, bands = XYZImage.shape # bands == 3
        
        linearsRGBImage =  np.zeros([rows, cols, bands], dtype=float)
        multiplierMatrix = np.array([[3.240479, -1.53715, -0.498535],
                                     [-0.969256, 1.875991, 0.041556],
                                     [0.055648, -0.204043, 1.057311]])

        for i in range(0, rows):
            for j in range(0, cols):
                X,Y,Z = XYZImage[i,j]
                rgbList = np.matmul(multiplierMatrix, np.array([X,Y,Z]))
                for index, val in enumerate(rgbList):
                    if val<0:
                        rgbList[index]=0
                    #if val -ends
                    if val>1:
                        rgbList[index]=1
                    #if val -ends
                #for index, val -ends
                linearsRGBImage[i,j]=rgbList
            #for j -ends
        #for i -ends
        
        return linearsRGBImage 
        
# |--------------------------------XYZToLinearRGB------------------------------|

# |----------------------------------------------------------------------------|
# linearsRGBToNonLinearRGB
# |----------------------------------------------------------------------------|
    def linearsRGBToNonLinearRGB(self, linearRGBImage):
        '''
        converting Linear RGB into non Linear RGB by applying Gamma
        correction in following way:
        RGB = gamma(R',G',B')

        '''
        rows, cols, bands = linearRGBImage.shape # bands == 3
        
        nonLinearRGBImg =  np.zeros([rows, cols, bands], dtype=float)

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = linearRGBImage[i,j]
                nonLinearRGBImg[i,j] = self.gammaCorrection([r,g,b])
            #for j -ends
        #for i -ends
        
        return nonLinearRGBImg
        
        
# |--------------------------------linearsRGBToNonLinearRGB---------------------------------|
# |----------------------------------------------------------------------------|
# gammaCorrection
# |----------------------------------------------------------------------------|
    def gammaCorrection(self, invRGBList):
        '''
        I = 12.92D;                if D<0.00304
          = 1.055D^(1/2.4)-0.055;    otherwise
        '''
        rgbList = []
        for d in invRGBList:
            if d<0.00304:
                i=12.92*d
            else:
                i=np.power(d, 1/2.4)*1.055 - 0.055
            #if v -ends
            rgbList.append(i)
        #for v -ends
        return rgbList
# |--------------------------------gammaCorrection---------------------------------|
        
# |----------------------------------------------------------------------------|
# sRGBImageToRGBImage
# |----------------------------------------------------------------------------|
    def sRGBImageToRGBImage(self, sRGBImage):
        '''
        R = R'*255;  G = G'*255; B = B'*255;
        '''
        rows, cols, bands = sRGBImage.shape # bands == 3
        
        RGBImage =  np.zeros([rows, cols, bands], dtype=np.uint8)

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = sRGBImage[i,j]
                RGBImage[i,j] = [np.round(r*255), np.round(g*255), np.round(b*255)  ]
            #for j -ends
        #for i -ends
        
        return RGBImage
# |--------------------------------sRGBImageToRGBImage---------------------------------|
# |----------------------------------------------------------------------------|
# RGBToBGR
# |----------------------------------------------------------------------------|
    def RGBToBGR(self, rgbImage):
        '''
        
        '''
        rows, cols, bands = rgbImage.shape # bands == 3
        
        BGRImage =  np.zeros([rows, cols, bands], dtype=np.uint8)

        for i in range(0, rows):
            for j in range(0, cols):
                r,g,b = rgbImage[i,j]
                BGRImage[i,j] = [b,g,r]
            #for j -ends
        #for i -ends
        
        return BGRImage        
# |--------------------------------RGBToBGR---------------------------------|
    