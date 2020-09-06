import numpy as np
import cv2
def blur_face(image, factor=3.0):

	(h, w) = image.shape[:2]
	kernel_w = int(w / factor)
	kernel_h = int(h / factor)

	if kernel_w % 2 == 0:
		kernel_w -= 1

	if kernel_h % 2 == 0:
		kernel_h -= 1

	return cv2.GaussianBlur(image, (kernel_w, kernel_h), 0)