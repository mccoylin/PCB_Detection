#!/usr/bin/python3
# -*- coding: utf-8 -*- 

# PCB DIP 零件缺件測試程式
#   發問者貼了兩張照片。引出神人講了照片要先做去背景，調整傾斜度和相同大小，二值化... 等等的方法。
#   還有程式碼及成功的範例圖片。
# ihttps://stackoverflow.com/questions/65684929/how-to-detect-defect-in-pcb-using-opencv-python

import cv2
import numpy as np

kernel = np.ones((7,7),np.uint8)

img1 = cv2.imread("orig.png")
img1 = cv2.resize(img1, (640, 480))
image1 = img1[10:-10,10:-10]

img2 = cv2.imread("defect.png")
img2 = cv2.resize(img2, (640, 480)) 
image2 = img2[10:-10,10:-10]


# Changing color space
g_o_img = cv2.cvtColor(image1, cv2.COLOR_BGR2LAB)   [...,0]
g_def_img = cv2.cvtColor(image2, cv2.COLOR_BGR2LAB)[...,0]

# Image subtraction
sub =cv2.subtract(g_o_img, g_def_img)

thresh = cv2.threshold(sub , 130, 255, cv2.THRESH_BINARY)[1]
# Morphological opening 
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)


# Detecting blobs
params = cv2.SimpleBlobDetector_Params()
params.filterByInertia = False
params.filterByConvexity = False
params.filterByCircularity = False

im=cv2.bitwise_not(opening)

detector = cv2.SimpleBlobDetector_create(params)

keypoints = detector.detect(im)

# Drawing circle around blobs
im_with_keypoints = cv2.drawKeypoints(img2, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Display image with circle around defect
cv2.imshow('image',im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
