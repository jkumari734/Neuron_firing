#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np
import pandas as pd


# for i in range(1, 501):
#     if i > 0 and i < 10:
#         s = 'Image'+str(i)+'.jpg'
#     elif i > 9 and i < 100:
#         s = 'Image'+str(i)+'.jpg'
#     else:
#         s = 'Image'+str(i)+'.jpg'
    

#     img = cv2.imread(s)
#     img_binary = cv2.imread(s,0)
    
#     img_binary = cv2.medianBlur(img_binary, 3)
   
#     kernel = np.ones((3,3), np.uint8) 

#     img_dilation = cv2.dilate(img_binary, kernel, iterations=1) 
#     ret, a = cv2.threshold(img_dilation,140,255,cv2.THRESH_BINARY)   ## VERY IMPORTANT
#     ret, b = cv2.threshold(a,150,255,cv2.THRESH_BINARY_INV)
#     img_final = cv2.dilate(a, kernel, iterations=4) 

#     cv2.imshow('White background', a) 
# #     cv2.imshow('Black background ', b) 
#     cv2.imshow('No line', img_binary) 
    

#     cv2.waitKey(200) 


# In[ ]:


img = cv2.imread('Image1.jpg',0)
ret,thresh = cv2.threshold(img,140,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:5]

for i in range(len(cnts)):
    print(cv2.contourArea(cnts[i]),"cnt")

centroids = {}
for c in contours:
    M = cv2.moments(c)
       # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    centroids[(cX,cY)] = cv2.contourArea(c)
    
print(centroids)


# In[10]:


counter = 0
centroids = {}
visited = {}

for i in range(1, 501):
    if i > 0 and i < 10:
        s = 'Image'+str(i)+'.jpg'
    elif i > 9 and i < 100:
        s = 'Image'+str(i)+'.jpg'
    else:
        s = 'Image'+str(i)+'.jpg'
        
    img = cv2.imread(s,0)
    ret,thresh = cv2.threshold(img,140,255,0)
#     ret, b = cv2.threshold(thresh,200,255,cv2.THRESH_BINARY_INV)
    contours,hierarchy = cv2.findContours(thresh, 1, 2)
    cnts = sorted(contours, key = cv2.contourArea, reverse = True)
    
    temp = {}
    
    for j in range(len(cnts)):
        M = cv2.moments(cnts[j])
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        if cv2.contourArea(cnts[j]) > 5:
            temp[(cX,cY)] = cv2.contourArea(cnts[j])
                
    for c in contours:
        if cv2.contourArea(c) > 10:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            if (cX,cY) in centroids.keys():
                
                if temp[(cX, cY)] >= centroids[(cX,cY)]:
                    centroids[(cX,cY)] = temp[(cX, cY)]
                    visited[(cX,cY)] = False
                    
                elif temp[(cX, cY)] <= 0.3 * centroids[(cX,cY)]:
                    centroids[(cX,cY)] = temp[(cX, cY)]
                    visited[(cX,cY)] = False
                    
                else:
                    if temp[(cX, cY)] < centroids[(cX,cY)] and visited[(cX,cY)]==False:
                        counter += 1
                        visited[(cX,cY)] = True
                        if i == 20 or i==30 or i==40 or i==50 or i==60:
                            x,y,w,h = cv2.boundingRect(c)
                            cv2.rectangle(img,(x-10,y-10),(x+w+20,y+h+20),(128,128,0),2)
                            cv2.imshow(str(i), img) 
                            cv2.waitKey(0) 

            else:
                centroids[(cX, cY)] = cv2.contourArea(c)
                visited[(cX,cY)] = False


# In[ ]:


print(counter)


# In[ ]:


import cv2
from matplotlib import pyplot as plt

hist = cv2.calcHist([img], [0], None, [256], [0, 256])
plt.plot(hist, color='blue')
plt.xlim([0, 256])

