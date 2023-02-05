import cv2 

def findLetters(cvIm):
    _, thresh = cv2.threshold(cvIm, 100, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > thresh.shape[1]*0.07 and h > thresh.shape[0]*0.07 and w < thresh.shape[1] and h < thresh.shape[0]:
            thresh = 255 - thresh
            return thresh[y:y+h, x:x+w]


if __name__ == "__main__":
    img = cv2.imread("/home/abdullah/Downloads/H2.jpg", cv2.IMREAD_GRAYSCALE)
    img = findLetters(img)
    cv2.imwrite("./im.png", img)
