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
        
        First find the minL and maxL, based use them as a and b in above formula
        Use A=0 and B=100 and apply linear scaling
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
        2. perform histogram equalization on LArr for given window
        3. Put histogram equalized value in the Histogram Equalized L Arr (HELArr)
        4. create Histogram Equalized LuvImage HELuvImage
        '''
        LArr = self.convertLuvImgToLArr(LuvImg)
        histValArr = self.histogramEqualization(LArr, W1, H1, W2, H2) 
#         # debug
#         print("histValArr =\n {}".format(histValArr))
#         # debug -ends

        HELarr = self.findHistogramEqualizedLarr(LArr, histValArr)
#         # debug
#         print("HELarr =\n {}".format(HELarr))
#         # debug -ends

        HELuvImage = self.createHELuvImage(LuvImage = LuvImg, HELArr = HELarr)
#         # debug
#         print("HELuvImage =\n {}".format(HELuvImage))
#         # debug -ends

        return HELuvImage
                
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
    def histogramEqualization(self, LArr, W1, H1, W2, H2):
        '''
        1. finding frequency count for each unique values of L
        2. find hi
        3. find fi
        4. find histValList by performing
        j = floor ((k*f(j-1)+f(j))/2*n)
        5. return histogram mapped array where column 0 is original 
           unique l value and column 1 is its equalized value
        '''
        # finding frequency count for each value
        #getting unique values from window LArr  with their respective counts
        
        uniques, count = np.unique(LArr[H1:H2, W1:W2], return_counts=True)
        #finding total pixels n
        n = np.sum(count)
#         # debug
#         print("n = {}".format(n))
#         # debug -ends

        #defining k        
        k= 101

        
        #finding hi
        hiArr = np.asarray((uniques, count)).T
#         # debug
#         print("hiArr = {}".format(hiArr))
#         # debug -ends

        #finding fi
        fiList = []
        fi = 0
        for freq in hiArr:
            fi = fi + freq[1]
            fiList.append([freq[0], fi])
        # for freq -ends
        fiArr = np.array(fiList)
#         # debug
#         print("fiArr = {}".format(fiArr))
#         # debug -ends

        
        #calculating histogram
        histValList = []
        for index, fi in enumerate(fiArr):
            if index ==0:
                tempNum = float(fi[1]*(k))/float(2*n)
            else:
                tempNum = float((fi[1]+fiArr[index-1][1])*(k))/float(2*n)
            # if index -ends
            floorPix = np.floor(tempNum)
            if floorPix>=k:
                histValList.append([fi[0], floorPix-1])
            else:
                histValList.append([fi[0], floorPix])
            # if floorPix -ends
        # for index, fi -ends

        return np.array(histValList)
        
# |--------------------------------histogramEqualization-----------------------|
# |----------------------------------------------------------------------------|
# findHistogramEqualizedLarr
# |----------------------------------------------------------------------------|
    def findHistogramEqualizedLarr(self, LArr, histValArr):
        '''
        Create HELarr (Histogram Equalized L array) by mapping values of LArr to
        its related value from histValArr
        '''
        rows, cols = LArr.shape
        HELArr = np.zeros([rows, cols], dtype=float)
        
        histCurrentValList = (histValArr[:,0]).tolist()
        
        #providing maximum possible value as min value and 
        #minimum possible value as max value
        minL = 100
        maxL = 0
        
        #finding the actual oldMinL and oldMaxL in the given window
        for l in (histCurrentValList):
            if l<minL:
                minL = l
            #if l<minL -ends
            if l>maxL:
                maxL=l 
            #if l>maxL -ends
            #for j -ends
        #for i -ends
        
        #if l<minL than map value to 0
        #if l>maxL than map value to 1
        #else map value to its nearest value in histogram equalized value
        for i in range(rows):
            for j in range(cols):
                l = LArr[i,j]
                if l<minL-1:
                    HELArr[i,j]=0
                elif l>maxL+1:
                    HELArr[i,j]=100
                else:
                    idx = self.findNearestVal(arr = histValArr[:,0], val=l)
                    HELArr[i,j] = histValArr[idx, 1]
                #if -ends
            #for j -ends
        #for i -ends
        return HELArr
# |--------------------------------findHistogramEqualizedLarr---------------------------------|

# |----------------------------------------------------------------------------|
# createHELImage
# |----------------------------------------------------------------------------|
    def createHELuvImage(self, LuvImage, HELArr):
        '''
        take Histogram Equalized L from HELArr, 
        take u and v from LuvImage and using this HEL, u and v, 
        create HELuvImage
        '''
        rows, cols, bands = LuvImage.shape
#         # debug
#         print("rows = {}, cols = {}, bands = {}".format(rows, cols, bands))
#         # debug -ends

        HELuvImage = np.zeros([rows, cols, bands], dtype = float)
        
        for i in range(rows):
            for j in range(cols):
                l,u,v = LuvImage[i,j]
                HEL = HELArr[i,j]
                HELuvImage[i,j] = [HEL, u, v]
            #for j -ends
        #for i -ends
        return HELuvImage
# |--------------------------------createHELImage---------------------------------|
    

# |----------------------------------------------------------------------------|
# findNearestVal
# |----------------------------------------------------------------------------|
    def findNearestVal(self, arr, val):
        '''
        given function finds nearest value val from 1D array arr
        '''
        idx = (np.abs(arr-val)).argmin()
        return idx
# |--------------------------------findNearestVal---------------------------------|

    