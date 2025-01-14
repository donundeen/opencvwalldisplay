import cv2
import numpy as np
from picamera2 import Picamera2, Preview

# Initialize a variable to hold the previous frame for the change detection
previous_frame = None

def apply_trippy_effect(frame):
    # Invert the colors
    inverted_frame = cv2.bitwise_not(frame)
    
    # Apply Gaussian blur
    trippy_frame = cv2.GaussianBlur(inverted_frame, (15, 15), 0)
    
    return trippy_frame

def show_significant_changes(frame, threshold=30):
    global previous_frame
    
    if previous_frame is None:
        previous_frame = frame.copy()
        return frame  # Return the current frame if there's no previous frame

    # Calculate the absolute difference between the current frame and the previous frame
    diff = cv2.absdiff(frame, previous_frame)
    
    # Convert the difference to grayscale
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Apply a binary threshold to highlight significant changes
    _, thresh = cv2.threshold(gray_diff, threshold, 255, cv2.THRESH_BINARY)

    # Create an output frame that shows only the significant changes
    output_frame = cv2.bitwise_and(frame, frame, mask=thresh)

    # Update the previous frame
    previous_frame = frame.copy()
    
    return output_frame

def main():
    # Initialize the camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration())
    picam2.start()

    # Create a full-screen window
    cv2.namedWindow('Camera Input', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('Camera Input', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()
        
        # Apply the trippy effect
        frame = apply_trippy_effect(frame)
        
        # Show only significant changes
        frame = show_significant_changes(frame)

        # Display the resulting frame
        cv2.imshow('Camera Input', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, stop the camera
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()