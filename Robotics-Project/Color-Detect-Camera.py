
import cv2

def detect_colors_live():
    # Define the color boundaries for each color in the HSV color space
    boundaries = {
        'red': ([170, 120, 70], [180, 255, 255]),
        'blue': ([100, 150, 0], [140, 255, 255]),
        'yellow': ([20, 100, 100], [30, 255, 255]),
        'black': ([0, 0, 0], [180, 255, 30])
    }
    # Create an empty list to store the detected colors
    detected_colors = []
    # Open the camera
    cap = cv2.VideoCapture(0)
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()
        # Convert the frame to the HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Iterate over the color boundaries
        for color, (lower, upper) in boundaries.items():
            # Create a mask for the current color
            mask = cv2.inRange(hsv, lower, upper)
            # Use the mask to find the color in the frame
            if cv2.countNonZero(mask) > 0:
                detected_colors.append(color)
                cv2.putText(frame, color, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # Display the frame with the detected color
        cv2.imshow("Color Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Release the camera and close the display window
    cap.release()
    cv2.destroyAllWindows()
    return detected_colors

# Example usage
colors = detect_colors_live()
print(colors)
