import cv2

from picamera import PiCamera
from time import sleep
import numpy as np
import runModel


def picture(x):
    path = '/home/pi/Desktop/'
    # start picamera
    camera = PiCamera()
    #camera.start_preview()
    
    #start logitech
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    
    # wait to focus cams
    sleep(3)
    # take pic from picam
    pipath = f'{path}pi{x}.jpg'
    camera.capture(pipath)
    #camera.stop_preview()   
    
    # take pic from logitech
    _, img = cap.read()
    logpath = f'{path}log{x}.jpg'
    cv2.imwrite(logpath, img)
    cap.release() 
    
    return pipath, logpath


def main():
    pipath, path = picture(1)
    pimg = cv2.imread(pipath, cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    piPred = runModel.runModel(pimg)
    pred = runModel.runModel(img)
    print(piPred, pred)
    

if __name__ == "__main__":
    main()
