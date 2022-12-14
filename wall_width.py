"""
@file sobel_demo.py
@brief Sample code using Sobel and/or Scharr OpenCV functions to make a simple Edge Detector
"""
import sys
import cv2 as cv
import glob
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
#                                   constants                                #
##############################################################################
# Do you run a test or the full run:
FullRun = True
SingleImage = "/Users/noamcohen/Google Drive/My Drive/noam and yoav/crops of a domain/2.7V 0.311A.bmp"

PATH = (
    "/Users/noamcohen/Google Drive/My Drive/noam and yoav/crops of a domain/"
)
NUM_OF_ROW_TILES = 11

addr = {
    2.7: [[170, 197, 54, 70], [258, 273, 82, 94]],
    2.8: [[178, 198, 71, 82], [259, 278, 94, 108]],
    2.9: [[162, 183, 87, 108], [247, 264, 115, 127]],
    3.1: [[106, 127, 72, 90], [118, 203, 98, 112]],
    3.2: [[156, 169, 0, 56], [249, 264, 61, 73]],
    3.3: [[90, 103, 99, 110], [167, 184, 119, 129]],
    3.4: [[116, 133, 71, 86], [212, 222, 88, 100]],
    3.5: [[107, 122, 77, 91], [184, 211, 92, 104]],
    3.7: [[113, 130, 84, 96], [193, 206, 93, 108]],
    3.8: [[128, 140, 88, 103], [194, 212, 97, 114]],
}


##############################################################################
#                                  Functions                                 #
##############################################################################
def __volts_from_name(file_name: str):
    ### Needs to be programmed per user. ###
    """Takes bolt parameter from file name."""
    volt = file_name.split("V")[0]
    if "R" in volt:
        volt = volt.split()[1]
    return float(volt)


def plot_wall_graph(volts, thickness, yerror=None, xerror=None):
    """Plots the graph"""
    # Plot the ratios per volt.
    plt.plot(volts, thickness, "o", markersize=3, color="blue")
    # plt.errorbar(volts, ratios, yerr=yerror, xerr=xerror, color='b',
    #            linestyle='')
    plt.xlabel(r"V $\propto$ H")
    # naming the y axis
    plt.ylabel(r"Wall Thickness")
    # giving a title to my graph
    plt.title("Wall Thickness vs B")
    plt.grid()
    plt.show()


def wall_width(src):

    window_name = "Sobel Demo - Simple Edge Detector"
    scale = 1
    delta = 0
    ddepth = cv.CV_16S

    # cv.imshow(window_name, src)
    # cv.waitKey(0)
    # Check if image is loaded fine
    if src is None:
        print("Error opening image: " + argv[0])
        return -1

    src = cv.GaussianBlur(src, (3, 3), 0)

    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    grad_x = cv.Sobel(
        gray,
        ddepth,
        1,
        0,
        ksize=3,
        scale=scale,
        delta=delta,
        borderType=cv.BORDER_DEFAULT,
    )
    # Gradient-Y
    # grad_y = cv.Scharr(gray,ddepth,0,1)
    grad_y = cv.Sobel(
        gray,
        ddepth,
        0,
        1,
        ksize=3,
        scale=scale,
        delta=delta,
        borderType=cv.BORDER_DEFAULT,
    )

    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    grad = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    print(np.mean(grad, axis=0))
    if not FullRun:
        cv.imshow("blaj", grad)
        cv.waitKey(0)
    print()
    return sum(g > 40 for g in np.mean(grad, axis=0))
    return 0


def main():
    """Find the ratio of magnetization for each volt."""
    volts = []
    volts_error = []
    thickness = []

    if FullRun:
        paths = glob.glob(PATH + "*.bmp")
    else:
        paths = [SingleImage]
    for full_path in paths:
        file_name = full_path.split("/").pop()
        volt = __volts_from_name(file_name)
        if volt in addr:
            print(full_path)
            volts.append(volt)
            img = cv.imread(full_path)
            img_addr = addr[volt][0]
            img = img[img_addr[0] : img_addr[1], img_addr[2] : img_addr[3]]
            # img = img[img_addr[0] : img_addr[1], 0:-1]
            if not FullRun:
                cv.imshow("blaj", img)
                cv.waitKey(0)
            thickness.append(wall_width(img))

    if FullRun:
        plot_wall_graph(volts, thickness)
    else:
        print("thickness:", thickness)


if __name__ == "__main__":
    main()
