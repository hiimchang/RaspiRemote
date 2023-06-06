# coding=utf-8
import cv2
import sys

if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    fps = 10
    waitTime = 20

    width = int(cap.get(3))
    height = int(cap.get(4))

    print(width, height)

    if sys.argv.__len__() == 1:
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is None:
                break
            else:
                cv2.imshow("frames", frame)
                k = cv2.waitKey(waitTime) & 0xFF
                if k == 27:
                    break
        cap.release()
    elif sys.argv.__len__() == 2:
        angle = int(sys.argv[1])
        M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
        while cap.isOpened():
            ret, frame = cap.read()
            if frame is None:
                break
            else:
                rotate = cv2.warpAffine(frame, M, (width, height))
                cv2.imshow("frames", rotate)
                k = cv2.waitKey(waitTime) & 0xFF
                if k == 27:
                    break
        cap.release()
