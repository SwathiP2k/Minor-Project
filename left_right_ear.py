from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

root = Tk()

root.filename = filedialog.askopenfilename(initialdir="/", title="Select A file",
                                           filetypes=(("png files", ".png"),
                                                      ("jpeg files", "jpeg"),
                                                      ("all files", "*.*")))
my_label = Label(root, text=root.filename).pack()
upload_img = ImageTk.PhotoImage(Image.open(root.filename))
upload_img_label = Label(image=upload_img).pack()

root.mainloop()

# image1 is a reference image
image1 = cv2.imread("E:/Project/left eardrum.png")
image2 = cv2.imread(root.filename)

# made same sized images inorder to compare two images

image1 = cv2.resize(image1, (500, 500))
image2 = cv2.resize(image2, (500, 500))

# check if some similarities are present

sift = cv2.xfeatures2d.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(image1, None)
kp_2, desc_2 = sift.detectAndCompute(image2, None)

index_params = dict(algorithm=0, trees=5)
search_params = dict()

# Flann algorithm is used to compare two images
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

if percentage > 25:
    print("LEFT EAR")
else:
    print("RIGHT EAR")

result = cv2.drawMatches(image1, kp_1, image2, kp_2, good_points, None)

# cv2.imshow("result", cv2.resize(result, None, fx=0.7, fy=0.7))
# cv2.imshow("Original left", image1)
# cv2.imshow("Test image", image2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

