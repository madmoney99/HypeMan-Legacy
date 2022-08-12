import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt

def adjust_gamma(image, gamma=1.0):

   invGamma = 1.0 / gamma
   table = np.array([((i / 255.0) ** invGamma) * 255
      for i in np.arange(0, 256)]).astype("uint8")

   return cv2.LUT(image, table)

gamma = 0.8                                   # change the value here to get different result

if len(sys.argv)>= 2:
    print('Argument Number 2: ', str(sys.argv[1])) 

    if str(sys.argv[1]) == 'bomb':
        src2 = cv2.imread('Images/FA-18D_Dropping_Bombs.png', cv2.IMREAD_COLOR)  
    elif str(sys.argv[1]) == 'strafe':    
        src2 = cv2.imread('Images/FA-18D_Strafing.png', cv2.IMREAD_COLOR)
  

try:
    src1 = cv2.imread('boardRange.png',cv2.IMREAD_COLOR)
except:
    print('exception thrown while opening image')                 

if src1 is None:
    print('image is none.')             
    print('Error opening image.')
    sys.exit(0)


img2_resized = cv2.resize(src2, (src1.shape[1], src1.shape[0]))
# add or blend the images
img = cv2.addWeighted(src1, 0.7, img2_resized, 0.3, 0.0)

cv2.imwrite('finalRange.jpg',img)



##plt.show()