from PIL import Image
import pytesseract as pt 
import cv2
import numpy as np

def filterImg(img):
    #greyscale the image
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #erode noise
    kernel = np.ones((4,4),np.uint8)
    grey = cv2.erode(grey, kernel, iterations = 1)
    #threshold to get uniform background and text
    grey = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return grey

for i in range(1,11):
    img = cv2.imread(f"S ({i}).jpg")
    filtered = filterImg(img)
    cv2.imshow("im", filtered)
    cv2.waitKey(0)
    filtered = Image.fromarray(filtered)
    old = Image.open(f"S ({i}).jpg")
    print('old: ' , pt.image_to_string(old))
    print('new: ', pt.image_to_string(filtered))