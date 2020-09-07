from filters import blur_face as bf
from filters import pixelate_face as pf

import numpy as np
import argparse
import cv2

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-i", "--image", required=True,
                        help="path to input image")

arg_parser.add_argument("-m", "--method", type=str, default="simple",
                        choices=["simple", "pixelated"],
                        help="choose method for anonymizing")
arg_parser.add_argument("-b", "--blocks", type=int, default=20,
                        help="# of blocks for the pixelated blurring method")
arg_parser.add_argument("-c", "--confidence", type=float, default=0.5,
                        help="minimum probability to filter weak detections")
args = vars(arg_parser.parse_args())

prototxt_path = 'face_detection_model/deploy.prototxt'
weights_path = 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel'
face_net = cv2.dnn.readNet(prototxt_path, weights_path)

image = cv2.imread(args["image"])
original_img = image.copy()
(h, w) = image.shape[:2]

blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                             (104.0, 177.0, 123.0))

face_net.setInput(blob)
detections = face_net.forward()

for i in range(0, detections.shape[2]):

    confidence = detections[0, 0, i, 2]

    if confidence > args["confidence"]:
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (x_start, y_start, x_end, y_end) = box.astype("int")

        face = image[y_start:y_end, x_start:x_end]
    else:
        continue

    if args["method"] == "simple":
        face = bf.blur_face(face, factor=3.0)
    else:
        face = pf.pixelate_face(face,
                                blocks=args["blocks"])
    image[y_start:y_end, x_start:x_end] = face

anonymize_face = np.hstack([original_img, image])

# cv2.imwrite('result.jpg', anonymize_face)
cv2.imshow("Output", anonymize_face)
cv2.waitKey(0)
cv2.destroyAllWindows()
