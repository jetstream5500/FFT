import numpy as np
import cv2

if __name__ == '__main__':
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)

    for i in range(1000):
        A = np.random.randn(10,10)
        cv2.imshow("img", A)
        cv2.waitKey(1)  # it's needed, but no problem, it won't pause/wait
