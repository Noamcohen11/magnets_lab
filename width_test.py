import cv2
import numpy as np
import skimage.morphology
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


def get_width(img):

    # convert to
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # use thresholding
    thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )[1]

    # get distance transform
    distance = thresh.copy()
    distance = cv2.distanceTransform(
        distance, distanceType=cv2.DIST_L2, maskSize=5
    ).astype(np.float32)

    # get skeleton (medial axis)
    binary = thresh.copy()
    binary = binary.astype(np.float32) / 255
    skeleton = skimage.morphology.skeletonize(binary).astype(np.float32)
    cv2.imshow("blah", skeleton)
    cv2.waitKey(0)
    # apply skeleton to select center line of distance
    thickness = cv2.multiply(distance, skeleton)

    return thickness[skeleton != 0]


def main():
    # read input
    img = cv2.imread("3.57V.bmp")
    # img = image[1802:2048, 2304:2970]

    thickness = get_width(img)
    # get average thickness for non-zero pixels
    average = np.mean(thickness) * 2
    print(average)
    x = []
    y = []
    cnt = 0
    prev_t = 0
    for t in thickness:
        if t * 2 > 9:
            if prev_t != 0:
                cnt += 1
                x.append(cnt)
                y.append(t * 2)
            prev_t = t * 2

    plt.plot(x, y, "o", markersize=3, color="blue")
    plt.ylabel(r"domain thickness [Pixels]")
    plt.xlabel(r"x [Pixels]")
    plt.axhline(y=12 + 2.5, color="r", linestyle="--")
    plt.axhline(y=12 - 2.5, color="r", linestyle="--")

    # giving a title to my graph
    plt.title("Domain Thickness Vs Domain Position: 3.57V")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
