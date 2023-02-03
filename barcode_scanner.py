#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
from pyzbar.pyzbar import decode


# In[4]:


def decoder(image):
    gray_img = cv2.cvtColor(image,1)
    barcode = decode(gray_img)
    gray = cv2.cvtColor(gray_img, cv2.COLOR_BGR2GRAY)
    # compute the Scharr gradient magnitude representation of the images
    # in both the x and y direction using OpenCV 2.4
    ddepth = cv2.CV_32F 
    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    for obj in barcode:
        points = obj.polygon
        rect_pts = obj.rect
        pts = np.array([obj.polygon], np.int32)
        cv2.polylines(image, [pts], True, (0, 255, 0), 3)

        barcodeData = obj.data.decode("utf-8")
        string = str(barcodeData)
        
        cv2.putText(frame, str(string), (rect_pts[0],rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(72,255,85), 2)
        print("Barcode: "+barcodeData)

cap = cv2.VideoCapture(0)
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break;
    decoder(frame)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(1)
    if code == ord('q'):
        break


# In[ ]:




