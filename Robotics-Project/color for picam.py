

import numpy as np
import cv2

def detect_colors(image_path):
    # Load the image
    img = cv2.imread(image_path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Define the color boundaries for each color in the RGB color space
    boundaries = {
        'red': ([1, 84, 90], [9, 255, 255]),
        'green': ([43, 60, 50], [64, 255, 255]),
        'yellow': ([25, 60, 99], [35, 255, 255]),
        #'black': ([0, 0, 0], [179, 255, 35])
    }
    
    # Create an empty list to store the detected colors
    detected_colors = []
    # Iterate over the color boundaries
    for color, (lower, upper) in boundaries.items():
        lower = np.array(lower)
        upper = np.array(upper)
        # create a mask for the current color
        mask = cv2.inRange(imgHSV, lower, upper)
        # Use the mask to find the color in the image
        if cv2.countNonZero(mask) > 0:
            detected_colors.append(color)
    
    return detected_colors

# Example usage
def main():
    for i in range(7):
        image_path = f'/home/pi/Desktop/pig{i}.jpg'
        colors = detect_colors(image_path)
        print(colors)

if __name__ == "__main__":
    main()

