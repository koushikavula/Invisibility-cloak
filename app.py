
#live streaming webcam
# import cv2
# frameWidth = 640
# frameHeight = 480
# cap = cv2.cv2.VideoCapture(0)
# cap.set(3, frameWidth)
# cap.set(4, frameHeight)
# while True:
#     success, img = cap.read()
#     cv2.imshow("Result", img)
#     if cv2.waitKqey(1) & 0xFF == ord('q'):
#         break


#Import Libraries
import cv2
import time
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('video.avi',fourcc,20.0, (640,480))

##setting primary camera
cap = cv2.VideoCapture(0)

##webcam will start after 5 secs
time.sleep(5)
count = 0
background = 0

## Capture the background in range of 60
for i in range(60):
    ret,background = cap.read()
background = np.flip(background,axis=1)


## Reading frames from the webcam
while(cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)
    
    ## Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## Generat masks to detect red color
    # lower_red = np.array([0,120,50])
    # upper_red = np.array([10,255,255])
    # mask1 = cv2.inRange(hsv,lower_red,upper_red)

    # lower_red = np.array([170,120,70])
    # upper_red = np.array([180,255,255])
    # mask2 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([100, 40, 40])        
    upper_red = np.array([100, 255, 255]) 
    mask1 = cv2.inRange(hsv, lower_red, upper_red) 
    # setting the lower and upper range for mask2  
    lower_red = np.array([155, 40, 40]) 
    upper_red = np.array([180, 255, 255]) 
    mask2 = cv2.inRange(hsv, lower_red, upper_red) 

    mask1 = mask1+mask2

    ## Open and Dilate the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
 
 
    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)
 
 
    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask = mask1)
 
 
    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1,1,res2,1,0)
    out.write(finalOutput)
    cv2.imshow("Sarbari",finalOutput)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()