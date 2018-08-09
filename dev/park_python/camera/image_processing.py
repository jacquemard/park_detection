##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Methods used to process images. It can be scaled using all     #
# of the CPUS                                                    #
##################################################################

import skimage
from skimage import io, transform, exposure, filters
from skimage.color.adapt_rgb import adapt_rgb, hsv_value
import warnings
from skimage import io
import argparse
from joblib import Parallel, delayed # parallelizing
import os

IMAGE_OUTPUT_SIZE = (270, 480)

'''
We are using a scharr filter to detect edges. 
The @adapt_rgb is a skimage annotation which adapts any grayscale filters to a per 
channel basis
The 'image' will be separated by channel (using the hsv color space here)
and the filter will be applied to each of them. The final image results of a concatenation
of these channels.
'''
@adapt_rgb(hsv_value)
def _scharr_hsv(image):
    return filters.scharr(image)

# Defining what to do when an image is received
def process_image(image_stream):
    # Converting to a skimage/opencv image (simply a [x, y, 3] numpy array)
    image = io.imread(image_stream)

    # Firstly, downsampling the image
    image = transform.resize(image, IMAGE_OUTPUT_SIZE, mode='reflect', anti_aliasing=True)

    # Secondly, detecting the edges
    image = _scharr_hsv(image)

    # return the processed image
    return image


IMAGE_EXT = ".jpg"
OUTPUT_IMAGE_EXT = ".bmp"
OUTPUT_IMAGE_SUFFIX = "processed"
def process_save_image(image_file):

    # Processing the image
    image = process_image(image_file)

    output_file = "{}_{}{}".format(image_file[:-len(IMAGE_EXT)], OUTPUT_IMAGE_SUFFIX, OUTPUT_IMAGE_EXT)

    # saving the image
    with warnings.catch_warnings(): # used to ignore loss of precision warning
        warnings.simplefilter("ignore")
        io.imsave(output_file, image)
        print(output_file)

def process_images(dataset_path):
    Parallel(n_jobs=4)(delayed(process_save_image)(os.path.join(root, f)) for root, _, files in os.walk(dataset_path) for f in files if f.endswith(IMAGE_EXT))


def get_processed_image_names(dataset_path):
    return [f[:-len(OUTPUT_IMAGE_SUFFIX) - len(OUTPUT_IMAGE_EXT)] for root, _, files in os.walk(dataset_path) for f in files if f.endswith("_{}{}".format(OUTPUT_IMAGE_SUFFIX, OUTPUT_IMAGE_EXT))]

parser = argparse.ArgumentParser("pklot")
parser.add_argument("-p", "--process_path", nargs=1, help="process all of the image of a folder", type=str)

if __name__ == '__main__':
    args = parser.parse_args()
    path = args.process_path[0]

    process_images(path)
    