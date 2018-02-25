import cv2
import numpy as np

class ImageProcess:
    
# |----------------------------------------------------------------------------|
# linearScaling
# |----------------------------------------------------------------------------|
    def linearScaling(self, LuvImg, W1, H1, W2, H2):
        '''
        Linear scaling:
        X = [(x-a)*(B-A)/(b-a)] + A
        
        First we are finding the 
        '''
        rows, cols, bands = LuvImg.shape
        
        #providing maximum possible value as min value and 
        #minimum possible value as max value
        oldMinL = 100
        oldMaxL = 0
        
        #finding the actual oldMinL and oldMaxL in the given window
        for i in range(H1, H2):
            for j in range(W1, W2):
                l,u,v = LuvImg[i,j]
                if l<oldMinL:
                    oldMinL = l
                #if l<minL -ends
                if l>oldMaxL:
                    oldMaxL = l
                #if l>maxL -ends
            #for j -ends
        #for i -ends
        
        #new min is 0 and new max is 100
        newMinL = 0
        newMaxL = 100
        
        #creating the output image
        scaledLuvImg = np.zeros([rows, cols, bands], dtype=float)
        
        #performing linear scaling on L for each pixel based on the range 
        #provided in the window
        for i in range(rows):
            for j in range(cols):
                oldL, u, v = LuvImg[i,j]
                newL = ((oldL-oldMinL)*(newMaxL-newMinL)/(oldMaxL-oldMinL)) \
                                                                    + newMinL
                scaledLuvImg[i,j]=[newL,u,v]
            #for j -ends
        #for i -ends
        
        return scaledLuvImg                                                   

# |--------------------------------linearScaling-------------------------------|

# |----------------------------------------------------------------------------|
# histogramEqualization
# |----------------------------------------------------------------------------|
    def histogramEqualizationInLuv(self, LuvImg,  W1, H1, W2, H2):
        '''
        1. Given function reads Luv image and stores L in another array
        2. perfoms histogram equalization on L
        3. return HistogramEqualized Luv Image
        '''
        LArr = self.convertLuvImgToLArr(LuvImg)
        
        
                
        
# |--------------------------------histogramEqualization-----------------------|
    
# |----------------------------------------------------------------------------|
# convertLuvImgToLArr
# |----------------------------------------------------------------------------|
    def convertLuvImgToLArr(self, LuvImg):
        '''
        given function reads LuvImage values and returns the value of L in LArr
        of type Array
        '''
        #finding shape of image
        rows, cols, bands = LuvImg.shape
        
        #initializing LArr (2D array which contains only L) 
        LArr = np.zeros([rows, cols], dtype=float)
        
        #storing values in LArr
        for i in range(rows):
            for j in range(cols):
                l,u,v=LuvImg[i, j]
                LArr[i,j] = l
            #for j -ends
        #for i -ends
        return LArr
# |--------------------------------convertLuvImgToLArr-------------------------|
# |----------------------------------------------------------------------------|
# histogramEqualization
# |----------------------------------------------------------------------------|
    def histogramEqualization(self, LArr):
        '''
        1. finding frequency count for each unique values of L
        2. find hi
        3. find fi
        '''
        # finding frequency count for each value
        #getting unique values from LArr with their respective counts
        uniques, count = np.unique(LArr, return_counts=True)
        #finding total pixels n
        n = np.sum(count)
        print ("n = {}".format(n))

        #defining k        
        k= 101

        
        #finding hi
        hiArr = np.asarray((uniques, count)).T
        print("HiArr:\n{}".format(hiArr))
        
        #finding fi
        fiList = []
        fi = 0
        for freq in hiArr:
            fi = fi + freq[1]
            fiList.append([freq[0], fi])
        # for freq -ends
        fiArr = np.array(fiList)
        print("FiArr = \n{}".format(fiArr))
        
        #calculating histogram
        histVal = []
        for index, fi in enumerate(fiArr):
            if index ==0:
                tempNum = float(fi[1]*(k))/float(2*n)
            else:
                tempNum = float((fi[1]+fiArr[index-1][1])*(k))/float(2*n)
            # if index -ends
            floorPix = np.floor(tempNum)
            print("floorPix = {}".format(tempNum))
            if floorPix>=k:
                histVal.append([fi[0], floorPix-1])
            else:
                histVal.append([fi[0], floorPix])
            # if floorPix -ends
        # for index, fi -ends

        return histVal

        
# |--------------------------------histogramEqualization---------------------------------|
            