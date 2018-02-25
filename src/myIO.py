import sys
import cv2

class MyIO:

# |----------------------------------------------------------------------------|
# readImage
# |----------------------------------------------------------------------------|
    def readImage(self, name_input):
        '''
        given function reads the image
        '''
        inputImage = cv2.imread(name_input, cv2.IMREAD_COLOR)
        if(inputImage is None) :
            print(sys.argv[0], ": Failed to read image from: ", name_input)
            sys.exit()
        return inputImage
# |--------------------------------readImage-----------------------------------|
        
# |----------------------------------------------------------------------------|
# showImage
# |----------------------------------------------------------------------------|
    def showImage(self, inputImage, imageText):
        '''
        given function displays the image
        '''
        cv2.imshow("image: "+imageText, inputImage)
# |--------------------------------showImage-----------------------------------|
# |----------------------------------------------------------------------------|
# writeImage
# |----------------------------------------------------------------------------|
    def writeImage(self, outputImage, name_output):
        '''
        given function writes the image on the location described by name_output
        '''
        cv2.imwrite(name_output, outputImage);
# |--------------------------------writeImage---------------------------------|
    
            
# |----------------------------------------------------------------------------|
# windowsSizeConversion
# |----------------------------------------------------------------------------|
    def windowsSizeMapping(self, inputImage, w1, h1, w2, h2):
        '''
        
        '''
        rows, cols, bands = inputImage.shape # bands == 3
        W1 = round(w1*(cols-1))
        H1 = round(h1*(rows-1))
        W2 = round(w2*(cols-1))
        H2 = round(h2*(rows-1))

        return W1, H1, W2, H2
# |--------------------------------windowsSizeConversion---------------------------------|


