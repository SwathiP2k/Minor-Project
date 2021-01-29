# image processing code
from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
import imutils
import os
from PIL import Image, ImageDraw,ImageFont
from PIL import Image, ImageTk
root = Tk()

# code to upload an image
root.filename = filedialog.askopenfilename(initialdir="/", title="Select A file",
                                           filetypes=(("png files", ".png"),
                                                      ("jpeg files", "jpeg"),
                                                      ("all files", "*.*")))
my_label = Label(root, text=root.filename).pack()

# code to find side of ear
ori_image = cv2.imread(root.filename)
image1 = cv2.imread(r"E:\Project\left eardrum.png")

image1 = cv2.resize(image1, (500, 500))
image2 = cv2.resize(ori_image, (500, 500))

sift = cv2.xfeatures2d.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(image1, None)
kp_2, desc_2 = sift.detectAndCompute(image2, None)

index_params = dict(algorithm=0, trees=5)
search_params = dict()

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(desc_1, desc_2, k=2)
good_points = []
for m, n in matches:
    if m.distance < 0.9 * n.distance:
        good_points.append(m)
key_points_consider = 0
if len(kp_1) >= len(kp_2):
    key_points_consider = len(kp_1)
else:
    key_points_consider = len(kp_2)

percentage = len(good_points) / key_points_consider * 100
if percentage > 20:
    side = "LEFT EAR"
else:
    side = "RIGHT EAR"
print(side)

# For eye image
# image1 = cv2.imread("E:/Project/right eye1.png")
# # image2 = cv2.imread("E:/Project/left cotton_wool_spot.png")
#
# # made same sized images inorder to compare two images
#
# image1 = cv2.resize(image1, (500, 500))
# image2 = cv2.resize(ori_image, (500, 500))
#
# # check if some similarities are present
#
# sift = cv2.xfeatures2d.SIFT_create()
# kp_1, desc_1 = sift.detectAndCompute(image1, None)
# kp_2, desc_2 = sift.detectAndCompute(image2, None)
#
# index_params = dict(algorithm=0, trees=5)
# search_params = dict()
#
# # Flann algorithm is used to compare two images
# flann = cv2.FlannBasedMatcher(index_params, search_params)
#
# matches = flann.knnMatch(desc_1, desc_2, k=2)
# good_points = []
# for m, n in matches:
#     if m.distance < 0.9 * n.distance:
#         good_points.append(m)
#
# key_points_consider = 0
# if len(kp_1) >= len(kp_2):
#     key_points_consider = len(kp_1)
# else:
#     key_points_consider = len(kp_2)
#
# percentage = len(good_points) / key_points_consider * 100
#
# if percentage < 26:
#     side = "RIGHT EYE"
# else:
#     side = "LEFT EYE"
# print(side)

# code to sharpen an image
kernel_sharpening = np.array([-1, -1, -1
                              - 1, 9, -1
                              - 1, -1, -1])

sharpened_img = cv2.filter2D(ori_image, -1, kernel_sharpening)

# code to rotate image
img = cv2.imwrite("r.png", sharpened_img)
image = cv2.imread("r.png")

for angle in np.arange(0, 720, 5):
    rotated_img = imutils.rotate_bound(image, angle)
    cv2.imshow("Press s if you want go ahead with this rotated image otherwise press any key", rotated_img)

    img = cv2.imwrite("r.png", rotated_img)
    image = cv2.imread("r.png")
    k = cv2.waitKey(0)
    if k == ord('s'):
        cv2.destroyAllWindows()

        # code to write text on image
        image = Image.open("r.png")
        font1 = ImageFont.truetype("arial.ttf", 25)
        draw = ImageDraw.Draw(image)
        points1 = 000, 000
        points2 = 00, 30
        points3 = 00, 60
        print("enter the name of patient")
        name = input()

        print("enter the age of patient")
        age = input()

        draw.text(points1, name, "white", font=font1)
        draw.text(points2, age, "white", font=font1)
        draw.text(points3, side, "white", font=font1)
        break

# displaying processed image
cv2.imshow("Original Image", ori_image)
cv2.imshow("Sharpened Image", sharpened_img)
cv2.imshow("Rotated Image", rotated_img)
image.show()
image.save(r"E:/Project/saved_img.png")
cv2.waitKey(0)
cv2.destroyAllWindows()
root.mainloop()