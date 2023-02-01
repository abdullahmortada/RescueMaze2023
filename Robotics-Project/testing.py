import cv2
import numpy as np


#cap = cv2.VideoCapture(0)
cap = cv2.imread(r"y1.jpg")

def empty(a):
    pass

cv2.namedWindow("hsv")
cv2.resizeWindow("hsv",640,240)
cv2.createTrackbar("Hue Min","hsv",0,179,empty)
cv2.createTrackbar("Hue Max","hsv",179,179,empty)
cv2.createTrackbar("Sat Min","hsv",0,255,empty)
cv2.createTrackbar("Sat Max","hsv",255,255,empty)
cv2.createTrackbar("Value Min","hsv",0,255,empty)
cv2.createTrackbar("Value Max","hsv",255,255,empty)


while True:
    img = cap
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min= cv2.getTrackbarPos("Hue Min", "hsv")
    h_max= cv2.getTrackbarPos("Hue Max", "hsv")
    s_min= cv2.getTrackbarPos("Sat Min", "hsv")
    s_max= cv2.getTrackbarPos("Sat Max", "hsv")
    v_min= cv2.getTrackbarPos("Value Min", "hsv")
    v_max= cv2.getTrackbarPos("Value Max", "hsv")

    lower= np.array([h_min,s_min,v_min])
    upper= np.array([h_max,s_max,v_max])
    mask= cv2.inRange(imgHsv, lower, upper)
    result= cv2.bitwise_and(img,img, mask= mask)



    result = cv2.resize(result,(960,600))
   #cv2.imshow("HSV", imgHsv)
   #cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()