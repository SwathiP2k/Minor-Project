import cv2
import numpy as np


left_original = cv2.imread("E:\Project\images\left eardrum.png")
image_to_compare = cv2.imread("E:\Project\images\left eardrum1.png")

# 1)check if two images are equal

#image1 = left_original.shape
#image2 = left_duplicate.shape

if left_original.shape == image_to_compare.shape:
    print("The images have same size and channels")
    difference = cv2.subtract(left_original, image_to_compare)
    b, g, r = cv2.split(difference)
    
    #print(cv2.countNonZero(b))
    if (cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and 
    cv2.countNonZero(r) == 0):
        print("The images are completely equal")
    else:
        print("The images are not equal")
   
# 2) check if some similarities are present

sift = cv2.xfeatures2d.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(left_original, None)
kp_2, desc_2 = sift.detectAndCompute(image_to_compare, None)


index_params = dict(algorithm=0, trees=5)
search_params = dict()

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(desc_1, desc_2, k=2)
print(len(matches))


cv2.imshow("Original left", left_original)
cv2.imshow("Duplicate left", image_to_compare)
cv2.waitKey(0)
cv2.destroyAllWindows()

