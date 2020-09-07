import numpy as np
import cv2


def pixelate_face(image, blocks=3):
    (h, w) = image.shape[:2]
    x_steps = np.linspace(0, w, blocks + 1, dtype="int")
    y_steps = np.linspace(0, h, blocks + 1, dtype="int")
    
    for i in range(1, len(y_steps)):
        for j in range(1, len(x_steps)):

            x_start = x_steps[j - 1]
            y_start = y_steps[i - 1]
            x_end = x_steps[j]
            y_end = y_steps[i]
            
            roi = image[y_start:y_end, x_start:x_end]
            (B, G, R) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(image, (x_start, y_start), (x_end, y_end),
                          (B, G, R), -1)

    return image
