##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Used to delete regions of images from a dataset using a mask.  #
# Can be called from the command line                            #
##################################################################

import cv2 as cv
from skimage.restoration import inpaint
from skimage import io
import numpy as np
import os
import argparse

def dataset_inpaint(path, image_ext, mask_image_file):
    OUTPUT_IMAGE_SUFFIX = "_masked"
    
    mask = cv.imread(mask_image_file, 0)

    for root, _, files in os.walk(path) :
        for f in files:
            if f.endswith(image_ext):
                absolute_path = os.path.join(root, f)
                image = cv.imread(absolute_path)

                # processing file
                dst = cv.inpaint(image, mask, 3, cv.INPAINT_TELEA)

                output_file = "{}{}{}".format(absolute_path[:-len(image_ext)], OUTPUT_IMAGE_SUFFIX, image_ext)
                io.imsave(output_file, dst)


parser = argparse.ArgumentParser("dataset inpaint")
parser.add_argument("-p", "--path", nargs=1, help="the path to the image to mask", type=str, required=True)
parser.add_argument("-m", "--mask", nargs=1, help="the path to the mask image", type=str, required=True)
parser.add_argument("-e", "--ext", nargs=1, help="the extension of the images to mask", type=str, required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.path[0]
    mask = args.mask[0]
    ext = args.ext[0]

    dataset_inpaint(path, ext, mask)
