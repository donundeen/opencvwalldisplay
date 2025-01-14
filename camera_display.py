import cv2
from picamera2 import Picamera2, Preview

def apply_trippy_effect(frame):
    # Invert the colors
    inverted_frame = cv2.bitwise_not(frame)
    
    # Apply Gaussian blur
    trippy_frame = cv2.GaussianBlur(inverted_frame, (15, 15), 0)
    
    return trippy_frame

def main():
    # Initialize the camera
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration())
    picam2.start()

    while True:
        # Capture frame-by-frame
        frame = picam2.capture_array()
        
        # Apply the trippy effect
        frame = apply_trippy_effect(frame)

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