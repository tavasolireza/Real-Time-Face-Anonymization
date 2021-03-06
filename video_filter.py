from filters import blur_face as bf
from filters import pixelate_face as pf

import numpy as np
import argparse
import cv2
from imutils.video import VideoStream
import imutils
import time

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-m", "--method", type=str, default="blur",
                        choices=["blur", "pixelated"],
                        help="choose method for anonymizing")
arg_parser.add_argument("-b", "--blocks", type=int, default=20,
                        help="# of blocks for the pixelated blurring method")
arg_parser.add_argument("-c", "--confidence", type=float, default=0.5,
                        help="minimum probability to filter weak detections")
args = vars(arg_parser.parse_args())

prototxt_path = 'face_detection_model/deploy.prototxt'
weights_path = 'face_detection_model/res10_300x300_ssd_iter_140000.caffemodel'
face_net = cv2.dnn.readNet(prototxt_path, weights_path)

video_stream = VideoStream(src=0).start()
time.sleep(2.0)

while True:

    frame = video_stream.read()
    frame = imutils.resize(frame, width=400)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))

    face_net.setInput(blob)
    detections = face_net.forward()
    for i in range(0, detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        if confidence > args["confidence"]:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x_start, y_start, x_end, y_end) = box.astype("int")

            face = frame[y_start:y_end, x_start:x_end]

            if args["method"] == "blur":
                face = bf.blur_face(face, factor=3.0)
            else:
                face = pf.pixelate_face(face,
                                        blocks=args["blocks"])
            frame[y_start:y_end, x_start:x_end] = face
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    cv2.destroyAllWindows()
    video_stream.stop()
