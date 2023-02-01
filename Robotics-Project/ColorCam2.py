import cv2
import numpy as np

def detect_colors_live():
    # Define the color boundaries for each color in the BGR color space
    boundaries = {
        'red': ([170, 120, 70], [180, 255, 255]),
        'blue': ([100, 150, 0], [140, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'black': ([0, 0, 0], [180, 255, 30])
    }
    # Create an empty list to store the detected colors
    detected_colors = []
    # Open the camera
    print("bruhca,syc")
    cap = cv2.VideoCapture(0)
    print("bruh")
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        # Iterate over the color boundaries
        for color, (lower, upper) in boundaries.items():
            print("bruh1")
            # Use numpy to find the color in the frame
            mask = np.zeros(frame.shape[:2], dtype='uint8')
            mask[((frame[:,:,0] >= lower[0]) & (frame[:,:,0] <= upper[0]))
            & ((frame[:,:,1] >= lower[1]) & (frame[:,:,1] <= upper[1]))
            & ((frame[:,:,2] >= lower[2]) & (frame[:,:,2] <= upper[2]))] = 255
            if np.count_nonzero(mask) > 0:
                detected_colors.append(color)
                cv2.putText(frame, color, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print("bruh2")
        # Display the frame with the detected color
        cv2.imshow("Color Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the camera and close the display window
    cap.release()
    cv2.destroyAllWindows()
    print("bruh")
    return detected_colors


# Example usage
colors = detect_colors_live()
print(colors)
