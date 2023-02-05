import cv2 

def findLetters(cvIm):
    _, thresh = cv2.threshold(cvIm, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 50 and h > 50 and w < thresh.shape[1] and h < thresh.shape[0]:
            cv2.rectangle(thresh, (x, y), (x+w, y+h), (0,255,0), 3)
            cv2.imshow("lel", thresh)
            cv2.waitKey(0)
            return thresh[y:y+h, x:x+w]



img = cv2.imread("/home/abdullah/Downloads/U.jpg", cv2.IMREAD_GRAYSCALE)
img = findLetters(img)
cv2.imwrite("./im.png", img)
