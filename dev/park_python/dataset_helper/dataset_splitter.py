##################################################################
#        MESURE DU TAUX D'OCCUPATION DE PARKINGS A L'AIDE        #
#                       DE CAMERAS VIDEOS                        #
# -------------------------------------------------------------- #
#              Rémi Jacquemard - TB 2018 - HEIG-VD               #
#                   remi.jacquemard@heig-vd.ch                   #
#               https://github.com/remij1/TB_2018                #
#                           July 2018                            #
# -------------------------------------------------------------- #
# Usefull to split a dataset to 3 folders: test, train and dev   #
# Each rate can be set, and it can be called from the command    #
# line.                                                          #
##################################################################

import glob
import os
import re
import random
from shutil import copyfile
import argparse


TEST_RATE = 0.1
DEV_RATE = 0.1

def split_dataset(dataset_path, output_path, exts, test_rate=TEST_RATE, dev_rate=DEV_RATE):
    TRAIN_PATH = output_path + "/train"
    TEST_PATH = output_path + "/test"
    DEV_PATH = output_path + "/dev"

    # finding files
    all_files = []
    for root, _, files in os.walk(dataset_path):
        for f in files:
            if f.endswith(exts[0]):
                # finding all of the related files
                name = f[:-len(exts[0])]
                related_files = []
                for ext in exts:
                    related_files.append(os.path.join(root, name + ext))
                all_files.append(related_files)

    #shuffling files
    random.shuffle(all_files)

    nb_test = test_rate * len(all_files)
    nb_dev = dev_rate * len(all_files)


    for files in all_files:
        path = TRAIN_PATH # train dataset
        if nb_test >= 0: # test dataset
            path = TEST_PATH
            nb_test -= 1
        elif nb_dev >= 0: # dev dataset
            path = DEV_PATH
            nb_dev -= 1
        os.makedirs(path, exist_ok=True)

        for f in files:
            copyfile(f, path + "/" + os.path.basename(f))



parser = argparse.ArgumentParser("dataset_splitter")
parser.add_argument("-i", "--input", nargs=1, help="the path to the dataset to split", type=str, required=True)
parser.add_argument("-o", "--output", nargs=1, help="the output path", type=str, required=True)
parser.add_argument("-e", "--exts", nargs='+', help="the extensions of data files. Ex.: if image.jpg and image.xml have to be related, ext: .jpg .xml", type=str, required=True)
parser.add_argument("-t", "--test_rate", nargs=1, help="the proportion of test data", type=float)
parser.add_argument("-d", "--dev_rate", nargs=1, help="the proportion of dev data", type=float)


if __name__ == '__main__':
    args = parser.parse_args()
    dataset_path = args.input[0]
    output_path = args.output[0]
    exts = args.exts
    
    test_rate = TEST_RATE
    if args.test_rate != None:
        test_rate = args.test_rate[0]

    dev_rate = DEV_RATE
    if args.dev_rate != None:
        dev_rate = args.dev_rate[0]

    split_dataset(dataset_path, output_path, exts, test_rate, dev_rate)
    