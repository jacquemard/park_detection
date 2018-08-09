##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Used to create a trainval file for the darknet neural network  #
# library from a folder. Each images within it add a line to the #
# trainval file.                                                 #
##################################################################

import os
from pathlib import Path
import argparse

def create_trainval_file(input_path, ext, output_file):
     # creating the trainval text file
    trainval_file = open(output_file, "w")

    for root, _, files in os.walk(input_path):
        for f in files:
            if f.endswith(ext):
                path = Path(os.path.join(root, f))
                # Adding the image to trainvals
                trainval_file.write(str(path.resolve()) + "\n")
    trainval_file.close()

parser = argparse.ArgumentParser("darknet trainval file creator")
parser.add_argument("-i", "--input", nargs=1, help="the images path", type=str, required=True)
parser.add_argument("-o", "--output", nargs=1, help="the trainval output file", type=str, required=True)
parser.add_argument("-e", "--ext", nargs=1, help="the image file extensions", type=str, required=True)

if __name__ == '__main__':
    args = parser.parse_args()
    
    create_trainval_file(args.input[0], args.ext[0], args.output[0])

