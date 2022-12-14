##############################################################################
#                                   Imports                                  #
##############################################################################
import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt
import operator
import copy
from width_test import *

##############################################################################
#                                   constants                                #
##############################################################################
# Do you run a test or the full run:
FullRun = True
SingleImage = "/Users/noamcohen/Google Drive/My Drive/noam and yoav/part 2/2.8V 0.322A.bmp"

PATH = "/Users/noamcohen/Google Drive/My Drive/noam and yoav/part 2/"
NUM_OF_ROW_TILES = 11
# Pixel values:
BLACK = 255
WHITE = 0
LINK_IN_PIXELS_RATIO = 0.05
MIN_WALL_RATIO = 2


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


def __image_conversion(file_name: str):
    pass


def plot_volt_graph(volts, ratios, yerror=None, xerror=None):
    """Plots the graph"""
    # Plot the ratios per volt.
    plt.plot(volts, ratios, "o", markersize=3, color="blue")
    plt.errorbar(
        volts,
        ratios,
        yerr=yerror,
        xerr=xerror,
        fmt="o",
        color="black",
        ecolor="lightgray",
        elinewidth=3,
        capsize=0,
    )

    plt.xlabel(r"V $\propto$ H")
    # naming the y axis
    plt.ylabel(r"Pixel width $\propto$ width")
    # giving a title to my graph
    plt.title("Thickness VS H")
    plt.grid()
    plt.show()


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
        print(full_path)
        file_name = full_path.split("/").pop()
        volt = __volts_from_name(file_name)
        if volt > 0:
            volts.append(volt)
            img = cv2.imread(full_path)
            img = img[413:781, 1785:1967]
            if not FullRun:
                cv2.imshow("blaj", img)
                cv2.waitKey(0)
            thickness.append(np.mean(get_width(img)) * 4)

    plot_volt_graph(volts, thickness, yerror=2.5, xerror=0.1)


if __name__ == "__main__":
    main()
