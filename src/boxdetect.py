import cv2
import numpy as np
import time

# Load your image
def box_cropper(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Blur a little to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect edges
    edges = cv2.Canny(blur, 50, 150)

    x,y,w,h= 0 ,0,0,0
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # Now you have x, y, w, h!
        
        # Example: draw the rectangle
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cropped = img[y:y+h, x:x+w]
    cv2.waitKey(0)
    time.sleep(5)
    cv2.destroyAllWindows()

    return cropped